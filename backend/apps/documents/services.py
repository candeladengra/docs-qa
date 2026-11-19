import re
from typing import List, Dict, Any
from PyPDF2 import PdfReader
from django.conf import settings
from .models import Document, Chunk
from .ai_providers import get_ai_provider


class PDFProcessingService:
    """Service for processing PDF documents."""

    def __init__(self):
        self.chunk_size = settings.CHUNK_SIZE
        self.chunk_overlap = settings.CHUNK_OVERLAP

    def extract_text_from_pdf(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Extract text from PDF file, page by page.

        Args:
            file_path: Path to the PDF file

        Returns:
            List of dicts with 'page_number' and 'text' keys
        """
        reader = PdfReader(file_path)
        pages = []

        for page_num, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            if text.strip():
                pages.append({"page_number": page_num, "text": text})

        return pages

    def chunk_text(self, text: str, page_number: int) -> List[Dict[str, Any]]:
        """
        Split text into overlapping chunks.

        Args:
            text: Text to chunk
            page_number: Page number for reference

        Returns:
            List of chunks with metadata
        """
        text = self._clean_text(text)

        if len(text) <= self.chunk_size:
            return [
                {
                    "content": text,
                    "page_number": page_number,
                }
            ]

        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size

            if end < len(text):
                end = self._find_sentence_boundary(text, end)

            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append(
                    {
                        "content": chunk_text,
                        "page_number": page_number,
                    }
                )

            start = end - self.chunk_overlap
            if start >= len(text):
                break

        return chunks

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        text = re.sub(r"\s+", " ", text)
        text = text.strip()
        return text

    def _find_sentence_boundary(self, text: str, position: int) -> int:
        """Find the nearest sentence boundary after the position."""
        sentence_endings = ".!?"
        search_range = 100

        for i in range(position, min(position + search_range, len(text))):
            if text[i] in sentence_endings:
                return i + 1

        return position

    def process_document(self, document_id: int):
        """
        Process a document: extract text, chunk, generate embeddings, and store.

        This is the main task function that will be called by the worker.
        """
        try:
            document = Document.objects.get(id=document_id)

            pages = self.extract_text_from_pdf(document.file.path)
            document.page_count = len(pages)
            document.save()

            all_chunks = []
            chunk_index = 0

            for page in pages:
                page_chunks = self.chunk_text(page["text"], page["page_number"])

                for chunk_data in page_chunks:
                    all_chunks.append(
                        {
                            "document_id": document.id,
                            "content": chunk_data["content"],
                            "page_number": chunk_data["page_number"],
                            "chunk_index": chunk_index,
                        }
                    )
                    chunk_index += 1

            if not all_chunks:
                raise ValueError("No text could be extracted from the PDF")

            provider = get_ai_provider()
            texts = [chunk["content"] for chunk in all_chunks]
            embeddings = provider.generate_embeddings(texts)

            chunk_objects = []
            for chunk_data, embedding in zip(all_chunks, embeddings):
                chunk_objects.append(
                    Chunk(
                        document_id=chunk_data["document_id"],
                        content=chunk_data["content"],
                        page_number=chunk_data["page_number"],
                        chunk_index=chunk_data["chunk_index"],
                        embedding=embedding,
                    )
                )

            Chunk.objects.bulk_create(chunk_objects)

            document.status = "ready"
            document.save()

        except Exception as e:
            document.status = "failed"
            document.error_message = str(e)
            document.save()
            raise


class QueryService:
    """Service for querying documents using RAG."""

    def __init__(self):
        self.top_k = settings.TOP_K_RESULTS

    def query(self, question: str) -> Dict[str, Any]:
        """
        Answer a question using RAG over all documents.

        Args:
            question: User's question

        Returns:
            Dict with 'answer' and 'sources' (list of relevant chunks)
        """
        provider = get_ai_provider()

        question_embedding = provider.generate_embeddings([question])[0]

        similar_chunks = self._find_similar_chunks(question_embedding)

        if not similar_chunks:
            return {
                "answer": "I couldn't find any relevant information in the uploaded documents.",
                "sources": [],
            }

        context_chunks = [
            {
                "content": chunk.content,
                "document_name": chunk.document.title,
                "page_number": chunk.page_number,
                "document_id": chunk.document.id,
            }
            for chunk in similar_chunks
        ]

        answer = provider.generate_answer(question, context_chunks)

        return {"answer": answer, "sources": context_chunks}

    def _find_similar_chunks(self, embedding: List[float]) -> List[Chunk]:
        """Find the most similar chunks using pgvector."""
        from pgvector.django import CosineDistance

        chunks = (
            Chunk.objects.filter(document__status="ready")
            .annotate(distance=CosineDistance("embedding", embedding))
            .order_by("distance")[: self.top_k]
        )

        return list(chunks)
