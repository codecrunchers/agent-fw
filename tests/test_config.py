from unittest.mock import Mock, patch

import pytest

from app.utils.config import AbstractConfig, InMemConfig, config_factory


def test_config_factory_dev():
    with patch("os.getenv") as mock_getenv:
        mock_getenv.return_value = "dev"
        config = config_factory()
        assert isinstance(config, InMemConfig)

def test_config_factory_unsupported():
    with patch("os.getenv") as mock_getenv:
        mock_getenv.return_value = "unsupported"
        with pytest.raises(ValueError):
            config_factory()

def test_abstract_config_instantiation():
    with pytest.raises(TypeError):
        AbstractConfig()

def test_in_mem_config_get():
    config = InMemConfig()
    result = config.get()
    expected_output = {
        "db_type": "dev",
        "db_uri": "sqlite:///Chinook.db",
        "file_loader_type": "unstructured",
        "llm": "OpenAI",
        "vectorstore": "FAISSLOCAL",
        "search": "DDG",
    }
    assert result == expected_output
