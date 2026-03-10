"""
Template system for commix.
"""
from pathlib import Path
from typing import Dict, Optional


class TemplateEngine:
    """Simple template engine for commit messages."""

    DEFAULT_TEMPLATES = {
        "conventional": "{emoji}{type}({scope}): {description}\n\n{body}",
        "gitmoji": "{emoji} {type}: {description}\n\n{body}",
        "simple": "{description}\n\n{body}",
    }

    def __init__(self, template_dir: Optional[Path] = None):
        self.template_dir = template_dir or Path.cwd() / ".commix"
        self.templates = self.DEFAULT_TEMPLATES.copy()

    def load_project_template(self) -> None:
        """Load project-specific template."""
        template_file = self.template_dir / "template.md"
        if template_file.exists():
            with open(template_file, "r") as f:
                self.templates["custom"] = f.read()

    def render(
        self,
        template_name: str,
        context: Dict[str, str],
    ) -> str:
        """Render a template with context."""
        template = self.templates.get(template_name, self.templates["simple"])

        for key, value in context.items():
            placeholder = f"{{{key}}}"
            template = template.replace(placeholder, str(value))

        return template

    def register_template(self, name: str, template: str) -> None:
        """Register a new template."""
        self.templates[name] = template


# Template variables
AVAILABLE_VARIABLES = [
    "{emoji} - Gitmoji emoji prefix",
    "{type} - Commit type (feat, fix, docs, etc.)",
    "{scope} - Scope of the change (optional)",
    "{description} - Short description",
    "{body} - Detailed body (optional)",
    "{breaking} - Breaking changes (optional)",
    "{issues} - Related issues (optional)",
    "{author} - Commit author",
    "{date} - Commit date",
]


# Commit types following Conventional Commits
COMMIT_TYPES = {
    "feat": "A new feature",
    "fix": "A bug fix",
    "docs": "Documentation only changes",
    "style": "Changes that do not affect the meaning of the code",
    "refactor": "A code change that neither fixes a bug nor adds a feature",
    "perf": "A code change that improves performance",
    "test": "Adding missing tests or correcting existing tests",
    "build": "Changes that affect the build system or external dependencies",
    "ci": "Changes to our CI configuration files and scripts",
    "chore": "Other changes that don't modify src or test files",
    "revert": "Reverts a previous commit",
    "security": "Security-related changes",
    "remove": "Removal of code or files",
    "deploy": "Deployment-related changes",
}
