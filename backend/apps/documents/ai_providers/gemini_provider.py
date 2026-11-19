import google.generativeai as genai
from typing import List, Dict, Any
from .base import AIProvider


class GeminiProvider(AIProvider):
    """Google Gemini AI provider."""

    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Gemini API key is required")

        genai.configure(api_key=api_key)
        self.chat_model = genai.GenerativeModel("gemini-pro")
        self.embedding_model = "models/embedding-001"

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using Gemini."""
        embeddings = []

        for text in texts:
            try:
                result = genai.embed_content(
                    model=self.embedding_model,
                    content=text,
                    task_type="retrieval_document",
                )
                embeddings.append(result["embedding"])
            except Exception as e:
                raise RuntimeError(f"Failed to generate embedding: {str(e)}")

        return embeddings

    def generate_answer(
        self, question: str, context_chunks: List[Dict[str, Any]]
    ) -> str:
        """Generate an answer using Gemini."""
        context_text = self._format_context(context_chunks)

        prompt = f"""You are a helpful assistant that answers questions \
based on the provided document context.

Context from documents:
{context_text}

Question: {question}

Instructions:
- Answer the question based ONLY on the provided context
- Include citations in your answer using the format [Doc: filename, Page: X]
- If the context doesn't contain enough information to answer, say so
- Be concise and accurate

Answer:"""

        try:
            response = self.chat_model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Failed to generate answer: {str(e)}")

    def is_available(self) -> bool:
        """Check if Gemini is available."""
        try:
            genai.list_models()
            return True
        except Exception:
            return False

    def _format_context(self, chunks: List[Dict[str, Any]]) -> str:
        """Format context chunks for the prompt."""
        formatted = []
        for i, chunk in enumerate(chunks, 1):
            doc_name = chunk.get("document_name", "Unknown")
            page = chunk.get("page_number", "?")
            content = chunk.get("content", "")
            formatted.append(f"[{i}] Document: {doc_name}, Page: {page}\n{content}")
        return "\n\n".join(formatted)
