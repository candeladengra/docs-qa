import requests
from typing import List, Dict, Any
from .base import AIProvider


class OllamaProvider(AIProvider):
    """Ollama AI provider for local embeddings and chat."""

    def __init__(self, base_url: str, chat_model: str, embedding_model: str):
        self.base_url = base_url.rstrip("/")
        self.chat_model = chat_model
        self.embedding_model = embedding_model

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using Ollama."""
        embeddings = []

        for text in texts:
            try:
                response = requests.post(
                    f"{self.base_url}/api/embeddings",
                    json={"model": self.embedding_model, "prompt": text},
                    timeout=30,
                )
                response.raise_for_status()
                embedding = response.json().get("embedding", [])
                embeddings.append(embedding)
            except Exception as e:
                raise RuntimeError(f"Failed to generate embedding: {str(e)}")

        return embeddings

    def generate_answer(
        self, question: str, context_chunks: List[Dict[str, Any]]
    ) -> str:
        """Generate an answer using Ollama chat model."""
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
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={"model": self.chat_model, "prompt": prompt, "stream": False},
                timeout=60,
            )
            response.raise_for_status()
            return response.json().get("response", "")
        except Exception as e:
            raise RuntimeError(f"Failed to generate answer: {str(e)}")

    def is_available(self) -> bool:
        """Check if Ollama is available."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False

    def _format_context(self, chunks: List[Dict[str, Any]]) -> str:
        """Format context chunks for the prompt."""
        formatted = []
        for i, chunk in enumerate(chunks, 1):
            doc_name = chunk.get("document_name", "Unknown")
            page = chunk.get("page_number", "?")
            content = chunk.get("content", "")
            formatted.append(
                f"[{i}] Document: {doc_name}, Page: {page}\n{content}"
            )
        return "\n\n".join(formatted)
