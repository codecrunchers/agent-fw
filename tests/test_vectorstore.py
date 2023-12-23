from unittest.mock import Mock, patch

import pytest

from app.utils.vectorstore import (AbstractVectorStore, FAISSLocal, chunker,
                                   uri_to_hash_key, vectorstore_factory)


def test_vectorstore_factory_faiislocal():
    with patch("app.utils.vectorstore.config") as mock_config:
        mock_config.__getitem__.return_value = "FAISSLOCAL"
        vstore = vectorstore_factory()
        assert isinstance(vstore, FAISSLocal)


def test_vectorstore_factory_unsupported():
    with patch("app.utils.vectorstore.config") as mock_config:
        mock_config.__getitem__.return_value = "unsupported"
        with pytest.raises(ValueError):
            vectorstore_factory()


def test_abstract_vectorstore_instantiation():
    with pytest.raises(TypeError):
        AbstractVectorStore()


def test_faiislocal_save():
    with patch("app.utils.vectorstore.OpenAIEmbeddings") as mock_embeddings_class, \
         patch("app.utils.vectorstore.FAISS") as mock_faiss_class:
        mock_embeddings_instance = Mock()
        mock_embeddings_class.return_value = mock_embeddings_instance
        mock_faiss_instance = Mock()
        mock_faiss_class.from_documents.return_value = mock_faiss_instance

        vstore = FAISSLocal()
        vstore.save(["document"], "uri")

        mock_embeddings_class.assert_called_once()
        mock_faiss_class.from_documents.assert_called_once_with(chunker(["document"]), mock_embeddings_instance)
        mock_faiss_instance.save_local.assert_called_once_with(uri_to_hash_key("uri"))


def test_faiislocal_load():
    with patch("app.utils.vectorstore.OpenAIEmbeddings") as mock_embeddings_class, \
         patch("app.utils.vectorstore.FAISS") as mock_faiss_class:
        mock_embeddings_instance = Mock()
        mock_embeddings_class.return_value = mock_embeddings_instance
        mock_persisted_vectorstore = Mock()
        mock_faiss_class.load_local.return_value = mock_persisted_vectorstore

        vstore = FAISSLocal()
        result = vstore.load("uri")

        mock_embeddings_class.assert_called_once()
        mock_faiss_class.load_local.assert_called_once_with(uri_to_hash_key("uri"), mock_embeddings_instance)
        assert result == mock_persisted_vectorstore


def test_uri_to_hash_key():
    uri = "test_uri"
    expected_output = "5311b191288b1b0933b8030926a2e09a7bb8e8e2f3e8d5f0b72b5a90a3a5e675"
    assert uri_to_hash_key(uri) == expected_output


def test_chunker():
    documents = ["document1", "document2"]
    expected_output = ["document1", "document2"]
    assert list(chunker(documents)) == expected_output
