"""Configuration management for Google Search Crawler."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class Config:
    """Configuration for Google Search Crawler.

    Attributes:
        tld: Top-level domain (e.g., 'com', 'co.uk')
        lang: Language code (e.g., 'en', 'vi')
        safe: Safe search mode ('off', 'medium', 'high')
        num: Number of results per page (max 100)
        pause: Pause duration between requests in seconds
        user_agent: User agent string (None for random)
        timeout: HTTP request timeout in seconds
        max_retries: Maximum number of retry attempts
        retry_delay: Initial retry delay in seconds
        cache_dir: Directory for caching results
        log_level: Logging level
    """

    tld: str = "com"
    lang: str = "en"
    safe: str = "off"
    num: int = 10
    pause: float = 2.0
    user_agent: str | None = None
    timeout: int = 10
    max_retries: int = 3
    retry_delay: float = 1.0
    cache_dir: Path = field(default_factory=lambda: Path.home() / ".cache" / "google-crawler")
    log_level: str = "INFO"

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        # Validate num
        if not 1 <= self.num <= 100:
            raise ValueError("num must be between 1 and 100")

        # Validate pause
        if self.pause < 0:
            raise ValueError("pause must be non-negative")

        # Validate safe
        if self.safe not in ("off", "medium", "high"):
            raise ValueError("safe must be 'off', 'medium', or 'high'")

        # Validate timeout
        if self.timeout <= 0:
            raise ValueError("timeout must be positive")

        # Validate max_retries
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")

        # Ensure cache directory exists
        if isinstance(self.cache_dir, str):
            self.cache_dir = Path(self.cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def from_yaml(cls, path: str | Path) -> Config:
        """Load configuration from a YAML file.

        Args:
            path: Path to YAML configuration file

        Returns:
            Config instance

        Raises:
            FileNotFoundError: If the file doesn't exist
            yaml.YAMLError: If the file is not valid YAML
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")

        with open(path) as f:
            data = yaml.safe_load(f)

        return cls(**data)

    @classmethod
    def from_env(cls) -> Config:
        """Load configuration from environment variables.

        Environment variables should be prefixed with GOOGLE_CRAWLER_
        For example: GOOGLE_CRAWLER_TLD=com

        Returns:
            Config instance
        """
        env_config: dict[str, Any] = {}

        # Map environment variables to config fields
        env_mapping = {
            "GOOGLE_CRAWLER_TLD": "tld",
            "GOOGLE_CRAWLER_LANG": "lang",
            "GOOGLE_CRAWLER_SAFE": "safe",
            "GOOGLE_CRAWLER_NUM": ("num", int),
            "GOOGLE_CRAWLER_PAUSE": ("pause", float),
            "GOOGLE_CRAWLER_USER_AGENT": "user_agent",
            "GOOGLE_CRAWLER_TIMEOUT": ("timeout", int),
            "GOOGLE_CRAWLER_MAX_RETRIES": ("max_retries", int),
            "GOOGLE_CRAWLER_RETRY_DELAY": ("retry_delay", float),
            "GOOGLE_CRAWLER_CACHE_DIR": "cache_dir",
            "GOOGLE_CRAWLER_LOG_LEVEL": "log_level",
        }

        for env_key, field_info in env_mapping.items():
            value = os.getenv(env_key)
            if value is not None:
                if isinstance(field_info, tuple):
                    field_name, field_type = field_info
                    env_config[field_name] = field_type(value)
                else:
                    env_config[field_info] = value

        return cls(**env_config)

    def to_yaml(self, path: str | Path) -> None:
        """Save configuration to a YAML file.

        Args:
            path: Path to save the configuration
        """
        path = Path(path)
        data = {
            "tld": self.tld,
            "lang": self.lang,
            "safe": self.safe,
            "num": self.num,
            "pause": self.pause,
            "user_agent": self.user_agent,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
            "retry_delay": self.retry_delay,
            "cache_dir": str(self.cache_dir),
            "log_level": self.log_level,
        }

        with open(path, "w") as f:
            yaml.dump(data, f, default_flow_style=False)


# Default global configuration
_default_config = Config()


def get_config() -> Config:
    """Get the current global configuration.

    Returns:
        Current Config instance
    """
    return _default_config


def set_config(config: Config) -> None:
    """Set the global configuration.

    Args:
        config: New Config instance to use globally
    """
    global _default_config
    _default_config = config
