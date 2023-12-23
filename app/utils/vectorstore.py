from abc import ABC, abstractmethod
import hashlib
import logging

from langchain.text_splitter import CharacterTextSplitter
from app import config
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

logger = logging.getLogger(__name__)


# VStore factory
def vectorstore_factory():
    if config["vectorstore"] == "FAISSLOCAL":
        return FAISSLocal()
    else:
        raise ValueError("Unsupported VStore")


class AbstractVectorStore(ABC):
    @abstractmethod
    def save(self, vs, uri):
        pass

    @abstractmethod
    def load(self, uri):
        pass


class FAISSLocal(AbstractVectorStore):
    def save(self, data, uri):
        embeddings = OpenAIEmbeddings()
        vs = FAISS.from_documents(chunker(data), embeddings)
        vs.save_local(uri_to_hash_key(uri))
        return uri_to_hash_key(uri)

    def load(self, uri):
        embeddings = OpenAIEmbeddings()
        persisted_vectorstore = FAISS.load_local(uri_to_hash_key(uri), embeddings)
        return persisted_vectorstore


def uri_to_hash_key(uri):
    """Convert a URI to a safe hash table key using SHA-256."""
    # Use SHA-256 hashing
    hash_object = hashlib.sha256(uri.encode())
    # Convert the hash object to a hexadecimal string
    hash_hex = hash_object.hexdigest()
    return hash_hex


def chunker(documents):
    text_splitter = CharacterTextSplitter(
        chunk_size=1000, chunk_overlap=30, separator="\n"
    )
    return text_splitter.split_documents(documents=documents)
