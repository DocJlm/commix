"""
AI providers for commix.
"""
from .base import BaseProvider
from .openai import OpenAIProvider
from .claude import ClaudeProvider
from .ollama import OllamaProvider

__all__ = [
    "BaseProvider",
    "OpenAIProvider",
    "ClaudeProvider",
    "OllamaProvider",
]

PROVIDER_MAP = {
    "openai": OpenAIProvider,
    "claude": ClaudeProvider,
    "ollama": OllamaProvider,
}

def get_provider(name: str, config: dict) -> BaseProvider:
    """Get provider instance by name."""
    provider_class = PROVIDER_MAP.get(name)
    if not provider_class:
        raise ValueError(f"Unknown provider: {name}")
    return provider_class(config)
