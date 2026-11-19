from django.conf import settings
from .base import AIProvider
from .ollama_provider import OllamaProvider
from .gemini_provider import GeminiProvider
from .fake_provider import FakeProvider


def get_ai_provider() -> AIProvider:
    """
    Factory function to get the configured AI provider.

    Returns:
        Configured AIProvider instance based on settings.

    Raises:
        ValueError: If provider is not configured or unknown.
    """
    provider_name = settings.AI_PROVIDER.lower()

    if provider_name == "fake":
        return FakeProvider()
    elif provider_name == "ollama":
        return OllamaProvider(
            base_url=settings.OLLAMA_BASE_URL,
            chat_model=settings.OLLAMA_CHAT_MODEL,
            embedding_model=settings.OLLAMA_EMBEDDING_MODEL,
        )
    elif provider_name == "gemini":
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY must be set to use Gemini provider")
        return GeminiProvider(api_key=settings.GEMINI_API_KEY)
    else:
        raise ValueError(f"Unknown AI provider: {provider_name}")
