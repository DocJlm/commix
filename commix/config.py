"""
Configuration management for commix.
"""
import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    """Configuration manager for commix."""

    DEFAULT_CONFIG = {
        "provider": "openai",
        "openai": {
            "model": "gpt-4o-mini",
        },
        "claude": {
            "model": "claude-3-haiku-20240307",
        },
        "ollama": {
            "base_url": "http://localhost:11434",
            "model": "llama3.2",
        },
        "commit": {
            "style": "conventional",
            "language": "en",
            "max_length": 72,
            "include_scope": True,
        },
        "gitmoji": {
            "enabled": False,
            "auto_detect": True,
        },
    }

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._get_config_path()
        self.data = self._load()

    def _get_config_path(self) -> Path:
        """Get default config path."""
        home = Path.home()
        config_dir = home / ".commix"
        config_dir.mkdir(exist_ok=True)
        return config_dir / "config.yaml"

    def _load(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if self.config_path.exists():
            with open(self.config_path, "r") as f:
                user_config = yaml.safe_load(f) or {}
        else:
            user_config = {}

        # Merge with defaults
        config = self.DEFAULT_CONFIG.copy()
        self._merge_dict(config, user_config)

        # Apply environment variables
        self._apply_env_vars(config)

        return config

    def _merge_dict(self, base: Dict, update: Dict) -> None:
        """Recursively merge dictionaries."""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_dict(base[key], value)
            else:
                base[key] = value

    def _apply_env_vars(self, config: Dict) -> None:
        """Apply environment variables to config."""
        # Provider override
        if os.getenv("COMMIX_PROVIDER"):
            config["provider"] = os.getenv("COMMIX_PROVIDER")

        # Language override
        if os.getenv("COMMIX_LANGUAGE"):
            config["commit"]["language"] = os.getenv("COMMIX_LANGUAGE")

        # API keys from environment
        if os.getenv("OPENAI_API_KEY"):
            config.setdefault("openai", {})["api_key"] = os.getenv("OPENAI_API_KEY")

        if os.getenv("ANTHROPIC_API_KEY"):
            config.setdefault("claude", {})["api_key"] = os.getenv("ANTHROPIC_API_KEY")

    def get(self, key: str, default: Any = None) -> Any:
        """Get config value by key (supports dot notation)."""
        keys = key.split(".")
        value = self.data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

    def set(self, key: str, value: Any) -> None:
        """Set config value by key (supports dot notation)."""
        keys = key.split(".")
        target = self.data
        for k in keys[:-1]:
            target = target.setdefault(k, {})
        target[keys[-1]] = value
        self.save()

    def save(self) -> None:
        """Save configuration to file."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w") as f:
            yaml.dump(self.data, f, default_flow_style=False)

    @property
    def provider(self) -> str:
        return self.data.get("provider", "openai")

    @property
    def commit_style(self) -> str:
        return self.data.get("commit", {}).get("style", "conventional")

    @property
    def language(self) -> str:
        return self.data.get("commit", {}).get("language", "en")

    @property
    def gitmoji_enabled(self) -> bool:
        return self.data.get("gitmoji", {}).get("enabled", False)

    def get_provider_config(self, provider: str) -> Dict[str, Any]:
        """Get configuration for a specific provider."""
        return self.data.get(provider, {})
