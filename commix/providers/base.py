"""
Base provider interface for AI backends.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseProvider(ABC):
    """Abstract base class for AI providers."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate text from the AI provider."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available and configured."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider name."""
        pass

    def format_commit_prompt(self, diff: str, style: str = "conventional", 
                            language: str = "en", use_gitmoji: bool = False) -> str:
        """Format the prompt for commit message generation."""
        style_desc = {
            "conventional": "Conventional Commits format: type(scope): description",
            "gitmoji": "Gitmoji format: 🎨 type: description",
            "simple": "Simple format: description",
        }

        emoji_desc = ""
        if use_gitmoji:
            emoji_desc = """
Use appropriate gitmoji emojis:
✨ feat: new feature
🐛 fix: bug fix
📝 docs: documentation
💄 style: formatting
♻️ refactor: code refactoring
🔥 remove: remove code/files
✅ test: add/update tests
🚀 deploy: deployment
🔒 security: security fix
⚡ perf: performance
"""

        return f"""Analyze the following git diff and generate a commit message.

Preferred style: {style_desc.get(style, style_desc['conventional'])}

{f'Language: {language}' if language != 'en' else ''}
{emoji_desc}

Git diff to analyze:
```
{diff}
```

Generate a clear, concise commit message following the specified format.
- First line should be under 72 characters
- Use imperative mood
- Be specific about what changed and why
- If multiple changes, focus on the main one

Return ONLY the commit message, no explanations:"""
