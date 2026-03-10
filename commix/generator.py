"""
Commit message generator for commix.
"""
from typing import List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from .config import Config
from .git_utils import GitUtils
from .providers import get_provider


console = Console()


# Gitmoji mappings
GITMOJI_MAP = {
    "feat": "✨",
    "fix": "🐛",
    "docs": "📝",
    "style": "💄",
    "refactor": "♻️",
    "perf": "⚡",
    "test": "✅",
    "build": "👷",
    "ci": "🔧",
    "chore": "🚚",
    "revert": "⏪",
    "security": "🔒",
    "remove": "🔥",
    "deploy": "🚀",
}


class CommitGenerator:
    """Generate commit messages using AI."""

    def __init__(self, config: Config):
        self.config = config
        self.provider = get_provider(
            config.provider,
            config.get_provider_config(config.provider),
        )

    def generate(
        self,
        diff: str,
        interactive: bool = False,
        batch: bool = False,
    ) -> Optional[str]:
        """Generate commit message(s) from git diff."""
        # Prepare prompt
        prompt = self.provider.format_commit_prompt(
            diff=diff,
            style=self.config.commit_style,
            language=self.config.language,
            use_gitmoji=self.config.gitmoji_enabled,
        )

        # Generate message
        try:
            console.print("[dim]🤖 Generating commit message...[/dim]")
            message = self.provider.generate(prompt)
        except Exception as e:
            console.print(f"[red]Error generating message: {e}[/red]")
            return None

        # Post-process
        message = self._post_process(message)

        if interactive:
            return self._interactive_mode(message)

        return message

    def _post_process(self, message: str) -> str:
        """Post-process the generated message."""
        # Clean up common artifacts
        message = message.strip()
        message = message.replace("```", "").strip()

        # Add gitmoji if enabled and not present
        if self.config.gitmoji_enabled and not any(
            message.startswith(emoji) for emoji in GITMOJI_MAP.values()
        ):
            # Try to detect commit type
            for commit_type, emoji in GITMOJI_MAP.items():
                if message.startswith(commit_type):
                    message = f"{emoji} {message}"
                    break

        # Ensure first line is not too long
        lines = message.split("\n")
        if lines and len(lines[0]) > 72:
            # Try to wrap
            first_line = lines[0]
            if ":" in first_line:
                prefix, rest = first_line.split(":", 1)
                if len(prefix) < 20:
                    lines[0] = f"{prefix}:{rest.strip()[:72 - len(prefix) - 1]}"

        return "\n".join(lines)

    def _interactive_mode(self, message: str) -> Optional[str]:
        """Interactive mode for message selection/editing."""
        console.print(Panel(message, title="📝 Generated Commit Message"))

        while True:
            choice = Prompt.ask(
                "\nWhat would you like to do?",
                choices=["accept", "edit", "regenerate", "cancel"],
                default="accept",
            )

            if choice == "accept":
                return message
            elif choice == "edit":
                console.print("[dim]Enter your commit message (press Ctrl+D to finish):[/dim]")
                lines = []
                try:
                    while True:
                        line = input()
                        lines.append(line)
                except EOFError:
                    pass

                edited_message = "\n".join(lines).strip()
                if edited_message:
                    return edited_message
            elif choice == "regenerate":
                console.print("[dim]Regenerating...[/dim]")
                # This would need to re-generate with different params
                return message
            elif choice == "cancel":
                return None

        return message

    def generate_batch(self, diff: str) -> List[str]:
        """Generate multiple commit messages for different hunks."""
        # Split diff into logical chunks
        hunks = self._split_hunks(diff)

        messages = []
        for hunk in hunks:
            prompt = self.provider.format_commit_prompt(
                diff=hunk,
                style=self.config.commit_style,
                language=self.config.language,
                use_gitmoji=self.config.gitmoji_enabled,
            )
            try:
                message = self.provider.generate(prompt)
                messages.append(self._post_process(message))
            except Exception:
                continue

        return messages

    def _split_hunks(self, diff: str) -> List[str]:
        """Split diff into logical hunks."""
        # Simple split by file for now
        hunks = []
        current_hunk = []

        for line in diff.split("\n"):
            if line.startswith("diff --git") and current_hunk:
                hunks.append("\n".join(current_hunk))
                current_hunk = [line]
            else:
                current_hunk.append(line)

        if current_hunk:
            hunks.append("\n".join(current_hunk))

        return hunks

    @staticmethod
    def infer_type(diff: str) -> str:
        """Infer commit type from diff content."""
        diff_lower = diff.lower()

        # File patterns
        if any(pattern in diff_lower for pattern in ["test", "spec", "__test__"]):
            return "test"
        if any(pattern in diff_lower for pattern in ["readme", "docs/", ".md"]):
            return "docs"
        if any(pattern in diff_lower for pattern in ["dockerfile", "docker-compose", ".yml", ".yaml"]):
            return "build"

        # Content patterns
        if "fix" in diff_lower or "bug" in diff_lower or "issue" in diff_lower:
            return "fix"
        if any(pattern in diff_lower for pattern in ["refactor", "move", "rename", "clean"]):
            return "refactor"
        if any(pattern in diff_lower for pattern in ["style", "format", "lint"]):
            return "style"
        if any(pattern in diff_lower for pattern in ["perf", "optimize", "speed"]):
            return "perf"

        # Default
        return "feat"
