"""
Ollama local provider for commix.
"""
import os
import json
from typing import Dict, Any
import urllib.request
import urllib.error

from .base import BaseProvider


class OllamaProvider(BaseProvider):
    """Ollama local model provider."""

    @property
    def name(self) -> str:
        return "ollama"

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_url = config.get("base_url", "http://localhost:11434")
        self.model = config.get("model", "llama3.2")

    def is_available(self) -> bool:
        """Check if Ollama is running."""
        try:
            req = urllib.request.Request(
                f"{self.base_url}/api/tags",
                method="GET",
            )
            with urllib.request.urlopen(req, timeout=2) as response:
                return response.status == 200
        except Exception:
            return False

    def generate(self, prompt: str) -> str:
        """Generate text using Ollama."""
        if not self.is_available():
            raise RuntimeError(
                "Ollama is not available. Make sure Ollama is running at "
                f"{self.base_url}"
            )

        try:
            data = json.dumps({
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "system": "You are a helpful assistant that generates clear, concise git commit messages.",
            }).encode("utf-8")

            req = urllib.request.Request(
                f"{self.base_url}/api/generate",
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST",
            )

            with urllib.request.urlopen(req, timeout=120) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result.get("response", "").strip()
        except Exception as e:
            raise RuntimeError(f"Ollama API error: {e}")

    def list_models(self) -> list:
        """List available models."""
        try:
            req = urllib.request.Request(
                f"{self.base_url}/api/tags",
                method="GET",
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode("utf-8"))
                return [model.get("name") for model in data.get("models", [])]
        except Exception:
            return []
