"""Tests for configuration module."""


import pytest
import yaml

from google.config import Config


class TestConfig:
    """Test Config class."""

    def test_default_config(self):
        """Test default configuration values."""
        config = Config()
        assert config.tld == "com"
        assert config.lang == "en"
        assert config.safe == "off"
        assert config.num == 10
        assert config.pause == 2.0
        assert config.timeout == 10
        assert config.max_retries == 3

    def test_custom_config(self):
        """Test custom configuration values."""
        config = Config(
            tld="co.uk",
            lang="fr",
            num=20,
            pause=1.0,
        )
        assert config.tld == "co.uk"
        assert config.lang == "fr"
        assert config.num == 20
        assert config.pause == 1.0

    def test_invalid_num(self):
        """Test validation of num parameter."""
        with pytest.raises(ValueError, match="num must be between 1 and 100"):
            Config(num=0)

        with pytest.raises(ValueError, match="num must be between 1 and 100"):
            Config(num=101)

    def test_invalid_pause(self):
        """Test validation of pause parameter."""
        with pytest.raises(ValueError, match="pause must be non-negative"):
            Config(pause=-1.0)

    def test_invalid_safe(self):
        """Test validation of safe parameter."""
        with pytest.raises(ValueError, match="safe must be"):
            Config(safe="invalid")

    def test_invalid_timeout(self):
        """Test validation of timeout parameter."""
        with pytest.raises(ValueError, match="timeout must be positive"):
            Config(timeout=0)

    def test_invalid_max_retries(self):
        """Test validation of max_retries parameter."""
        with pytest.raises(ValueError, match="max_retries must be non-negative"):
            Config(max_retries=-1)

    def test_from_yaml(self, tmp_path):
        """Test loading configuration from YAML file."""
        config_file = tmp_path / "config.yaml"
        config_data = {
            "tld": "co.jp",
            "lang": "ja",
            "num": 50,
            "pause": 3.0,
        }
        with open(config_file, "w") as f:
            yaml.dump(config_data, f)

        config = Config.from_yaml(config_file)
        assert config.tld == "co.jp"
        assert config.lang == "ja"
        assert config.num == 50
        assert config.pause == 3.0

    def test_from_yaml_not_found(self):
        """Test loading from non-existent YAML file."""
        with pytest.raises(FileNotFoundError):
            Config.from_yaml("/nonexistent/config.yaml")

    def test_to_yaml(self, tmp_path):
        """Test saving configuration to YAML file."""
        config = Config(tld="com.au", lang="en", num=25)
        config_file = tmp_path / "output_config.yaml"

        config.to_yaml(config_file)

        assert config_file.exists()
        with open(config_file) as f:
            data = yaml.safe_load(f)

        assert data["tld"] == "com.au"
        assert data["lang"] == "en"
        assert data["num"] == 25

    def test_cache_dir_creation(self, tmp_path):
        """Test that cache directory is created."""
        cache_dir = tmp_path / "cache" / "nested"
        config = Config(cache_dir=cache_dir)
        assert config.cache_dir.exists()
        assert config.cache_dir == cache_dir

    def test_from_env(self, monkeypatch):
        """Test loading configuration from environment variables."""
        monkeypatch.setenv("GOOGLE_CRAWLER_TLD", "co.uk")
        monkeypatch.setenv("GOOGLE_CRAWLER_LANG", "en-gb")
        monkeypatch.setenv("GOOGLE_CRAWLER_NUM", "30")
        monkeypatch.setenv("GOOGLE_CRAWLER_PAUSE", "1.5")

        config = Config.from_env()
        assert config.tld == "co.uk"
        assert config.lang == "en-gb"
        assert config.num == 30
        assert config.pause == 1.5
