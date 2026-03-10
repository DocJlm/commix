"""
Claude provider for commix.
"""
import os
from typing import Dict, Any

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

from .base import BaseProvider


class ClaudeProvider(BaseProvider):
    """Anthropic Claude provider."""

    @property
    def name(self) -> str:
        return "claude"

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get("api_key") or os.getenv("ANTHROPIC_API_KEY")
        self.model = config.get("model", "claude-3-haiku-20240307")

        if HAS_ANTHROPIC and self.api_key:
            self.client = anthropic.Anthropic(
                api_key=self.api_key,
            )
        else:
            self.client = None

    def is_available(self) -> bool:
        """Check if Claude is configured."""
        return HAS_ANTHROPIC and self.api_key is not None

    def generate(self, prompt: str) -> str:
        """Generate text using Claude."""
        if not self.is_available():
            raise RuntimeError("Claude is not configured. Set ANTHROPIC_API_KEY.")

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=300,
                temperature=0.3,
                system="You are a helpful assistant that generates clear, concise git commit messages.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text.strip()
        except Exception as e:
            raise RuntimeError(f"Claude API error: {e}")
