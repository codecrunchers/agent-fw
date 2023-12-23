from unittest.mock import Mock, patch

import pytest

from app.utils.db import AbstractDatabase, LocalDatabase, database_factory


def test_database_factory_dev():
    with patch("app.utils.config") as mock_config:
        mock_config.return_value = {"db_type": "dev"}
        db = database_factory()
        assert isinstance(db, LocalDatabase)


def test_database_factory_unsupported():
    with patch("app.utils.config") as mock_config:
        mock_config.return_value = {"db_type": "unsupported"}
        with pytest.raises(ValueError):
            database_factory()


def test_abstract_database_instantiation():
    with pytest.raises(TypeError):
        AbstractDatabase()


def test_local_database_connect():
    with patch("app.utils.db.SQLDatabase") as mock_sql_database, \
            patch("app.utils.db.OpenAI") as mock_open_ai, \
            patch("app.utils.db.SQLDatabaseChain") as mock_sql_database_chain:
        mock_sql_database.from_uri.return_value = Mock()
        mock_open_ai.return_value = Mock()
        mock_sql_database_chain.from_llm.return_value = Mock()

        db = LocalDatabase()
        db.connect()

        mock_sql_database.from_uri.assert_called_once()
        mock_open_ai.assert_called_once()
        mock_sql_database_chain.from_llm.assert_called_once()


@pytest.mark.asyncio
async def test_local_database_query():
    with patch("app.utils.db.SQLDatabaseChain") as mock_sql_database_chain:
        mock_sql_database_chain_instance = Mock()
        mock_sql_database_chain.from_llm.return_value = mock_sql_database_chain_instance

        db = LocalDatabase()
        db.connect()
        await db.query("SELECT * FROM table")

        mock_sql_database_chain_instance.run.assert_called_once_with("SELECT * FROM table")
