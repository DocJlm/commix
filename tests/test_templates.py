"""
Tests for template module.
"""
import pytest

from commix.templates import TemplateEngine, COMMIT_TYPES


class TestTemplateEngine:
    """Test template engine."""

    def test_default_templates(self):
        """Test default templates exist."""
        engine = TemplateEngine()
        assert "conventional" in engine.templates
        assert "gitmoji" in engine.templates
        assert "simple" in engine.templates

    def test_render_conventional(self):
        """Test conventional template rendering."""
        engine = TemplateEngine()
        result = engine.render(
            "conventional",
            {
                "emoji": "✨",
                "type": "feat",
                "scope": "auth",
                "description": "add OAuth2 login",
                "body": "Implement OAuth2 with Google and GitHub providers",
            },
        )
        assert "feat(auth): add OAuth2 login" in result
        assert "Implement OAuth2 with Google and GitHub providers" in result

    def test_render_gitmoji(self):
        """Test gitmoji template rendering."""
        engine = TemplateEngine()
        result = engine.render(
            "gitmoji",
            {
                "emoji": "✨",
                "type": "feature",
                "description": "add new login",
                "body": "Added OAuth2 support",
            },
        )
        assert "✨" in result
        assert "add new login" in result


class TestCommitTypes:
    """Test commit type definitions."""

    def test_commit_types_exist(self):
        """Test all expected commit types exist."""
        expected_types = [
            "feat",
            "fix",
            "docs",
            "style",
            "refactor",
            "perf",
            "test",
            "build",
            "ci",
            "chore",
        ]
        for commit_type in expected_types:
            assert commit_type in COMMIT_TYPES

    def test_commit_types_are_strings(self):
        """Test all commit type descriptions are strings."""
        for commit_type, description in COMMIT_TYPES.items():
            assert isinstance(commit_type, str)
            assert isinstance(description, str)
            assert len(description) > 0
