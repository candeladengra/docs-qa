from abc import ABC, abstractmethod
from typing import List, Dict, Any


class AIProvider(ABC):
    """Abstract base class for AI providers."""

    @abstractmethod
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors (each vector is a list of floats)
        """
        pass

    @abstractmethod
    def generate_answer(
        self, question: str, context_chunks: List[Dict[str, Any]]
    ) -> str:
        """
        Generate an answer to a question based on context chunks.

        Args:
            question: The user's question
            context_chunks: List of relevant chunks with 'content' and metadata

        Returns:
            The generated answer text with citations
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available and configured correctly."""
        pass
