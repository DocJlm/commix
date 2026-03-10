"""
OpenAI provider for commix.
"""
import os
from typing import Dict, Any

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

from .base import BaseProvider


class OpenAIProvider(BaseProvider):
    """OpenAI GPT provider."""

    @property
    def name(self) -> str:
        return "openai"

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key") or os.getenv("OPENAI_API_KEY")
        self.model = config.get("model", "gpt-4o-mini")
        self.base_url = config.get("base_url")

        if HAS_OPENAI and self.api_key:
            self.client = openai.OpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
            )
        else:
            self.client = None

    def is_available(self) -> bool:
        """Check if OpenAI is configured."""
        return HAS_OPENAI and self.api_key is not None

    def generate(self, prompt: str) -> str:
        """Generate text using OpenAI."""
        if not self.is_available():
            raise RuntimeError("OpenAI is not configured. Set OPENAI_API_KEY.")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that generates clear, concise git commit messages."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=300,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {e}")
