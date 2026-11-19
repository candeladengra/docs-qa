from typing import List, Dict, Any
from .base import AIProvider


class FakeProvider(AIProvider):
    """
    Fake AI provider for testing and development without real LLM calls.
    Returns mock embeddings and answers based on the input.
    """

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate fake embeddings (768-dimensional vectors)."""
        import hashlib

        embeddings = []
        for text in texts:
            hash_val = int(hashlib.md5(text.encode()).hexdigest(), 16)
            # Generate deterministic "fake" embedding from hash
            embedding = [
                ((hash_val >> i) % 1000) / 1000.0 for i in range(768)
            ]
            embeddings.append(embedding)
        return embeddings

    def generate_answer(
        self, question: str, context_chunks: List[Dict[str, Any]]
    ) -> str:
        """Generate a fake answer based on context chunks."""
        if not context_chunks:
            return "I don't have enough information to answer this question."

        doc_names = set(chunk["document_name"] for chunk in context_chunks)
        pages = [chunk["page_number"] for chunk in context_chunks]

        answer_parts = [
            f"Based on the provided documents ({', '.join(doc_names)}), "
        ]

        # Add some content from the chunks
        if context_chunks:
            first_chunk = context_chunks[0]
            content_preview = first_chunk["content"][:150]
            answer_parts.append(
                f"the information indicates: {content_preview}... "
            )

        answer_parts.append(
            f"[Doc: {context_chunks[0]['document_name']}, "
            f"Page: {context_chunks[0]['page_number']}]"
        )

        if len(context_chunks) > 1:
            answer_parts.append(
                f" Additional relevant information was found on "
                f"pages {', '.join(map(str, pages[1:]))}."
            )

        return "".join(answer_parts)

    def is_available(self) -> bool:
        """Fake provider is always available."""
        return True
