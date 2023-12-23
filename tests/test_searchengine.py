from unittest.mock import patch

import pytest

from app.utils.searchengine import AbstractSearch, DDGSearch, search_factory


def test_search_factory_ddg():
    with patch("app.utils.searchengine.config") as mock_config:
        mock_config.__getitem__.return_value = "DDG"
        search = search_factory()
        assert isinstance(search, DDGSearch)

def test_search_factory_unsupported():
    with patch("app.utils.searchengine.config") as mock_config:
        mock_config.__getitem__.return_value = "unsupported"
        with pytest.raises(ValueError):
            search_factory()

def test_abstract_search_instantiation():
    with pytest.raises(TypeError):
        AbstractSearch()

def test_ddg_search_search():
    with patch("app.utils.searchengine.DuckDuckGoSearchRun") as mock_search_class:
        mock_search_instance = mock_search_class.return_value
        mock_search_instance.run.return_value = "search results"
        search = DDGSearch()
        result = search.search("query")
        assert result == "search results"
        mock_search_class.assert_called_once()
        mock_search_instance.run.assert_called_once_with("query", backend="news")
