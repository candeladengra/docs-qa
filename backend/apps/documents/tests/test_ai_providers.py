import pytest
from apps.documents.ai_providers.base import AIProvider


class FakeAIProvider(AIProvider):
    """Fake AI provider for testing without real LLM calls."""

    def generate_embeddings(self, texts):
        return [[0.1] * 768 for _ in texts]

    def generate_answer(self, question, context_chunks):
        doc_names = [chunk["document_name"] for chunk in context_chunks]
        return f"Answer based on {len(context_chunks)} chunks from {', '.join(set(doc_names))}"

    def is_available(self):
        return True


class TestFakeAIProvider:
    """Test the fake AI provider used in tests."""

    def test_generate_embeddings(self):
        provider = FakeAIProvider()
        texts = ["Hello world", "Test document"]
        embeddings = provider.generate_embeddings(texts)

        assert len(embeddings) == 2
        assert len(embeddings[0]) == 768
        assert all(isinstance(val, float) for val in embeddings[0])

    def test_generate_answer(self):
        provider = FakeAIProvider()
        context = [
            {"content": "Test content", "document_name": "test.pdf", "page_number": 1}
        ]
        answer = provider.generate_answer("What is this?", context)

        assert isinstance(answer, str)
        assert "1 chunks" in answer
        assert "test.pdf" in answer

    def test_is_available(self):
        provider = FakeAIProvider()
        assert provider.is_available() is True


class TestProviderInterface:
    """Test that providers implement the required interface."""

    def test_provider_has_required_methods(self):
        provider = FakeAIProvider()

        assert hasattr(provider, "generate_embeddings")
        assert hasattr(provider, "generate_answer")
        assert hasattr(provider, "is_available")
        assert callable(provider.generate_embeddings)
        assert callable(provider.generate_answer)
        assert callable(provider.is_available)
