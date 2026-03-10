"""
Tests for commix configuration module.
"""
import pytest
import tempfile
import os
from pathlib import Path

from commix.config import Config


class TestConfig:
    """Test configuration module."""

    def test_default_config(self):
        """Test default configuration values."""
        config = Config()
        assert config.provider == "openai"
        assert config.commit_style == "conventional"
        assert config.language == "en"
        assert config.gitmoji_enabled is False

    def test_get_nested_value(self):
        """Test getting nested configuration values."""
        config = Config()
        assert config.get("openai.model") == "gpt-4o-mini"
        assert config.get("commit.max_length") == 72
        assert config.get("nonexistent", "default") == "default"

    def test_set_nested_value(self):
        """Test setting nested configuration values."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create config in temp directory
            config = Config(config_path=Path(tmpdir) / "config.yaml")
            config.set("commit.language", "zh")
            assert config.get("commit.language") == "zh"

    def test_env_var_override(self):
        """Test environment variable overrides."""
        original_env = os.environ.get("COMMIX_PROVIDER")
        try:
            os.environ["COMMIX_PROVIDER"] = "claude"
            config = Config()
            assert config.provider == "claude"
        finally:
            if original_env:
                os.environ["COMMIX_PROVIDER"] = original_env
            elif "COMMIX_PROVIDER" in os.environ:
                del os.environ["COMMIX_PROVIDER"]
