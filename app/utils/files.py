from langchain.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from abc import ABC, abstractmethod
from app import config
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS


# File Parser factory
def file_loader_factory():
    if config["file_loader_type"] == "unstructured":
        return UnstructuredFileInterpreter()
    else:
        raise ValueError("Unsupported file loader type")


class AbstractFileLoader(ABC):
    @abstractmethod
    async def parse(self, uri):
        pass

    @abstractmethod
    async def persist(self, db):
        pass

    @abstractmethod
    async def retrieve(self, db):
        pass


class UnstructuredFileInterpreter:
    async def parse(self, uri):
        loader = UnstructuredPDFLoader(uri)
        self.documents = loader.load()
        self.key = uri

    # TODO: Embedding Abstraction
    async def persist(self, db):
        docs = chunker(self.documents)
        # Create vectors
        self.get_vectorstore(docs).save_local(uri_to_hash_key(self.key))

    async def retrieve(self, db):
        embeddings = OpenAIEmbeddings()
        persisted_vectorstore = FAISS.load_local(uri_to_hash_key(self.key), embeddings)
        return persisted_vectorstore

    async def get_vectorstore(self, chunks):
        embeddings = OpenAIEmbeddings()
        return FAISS.from_documents(chunks, embeddings)


async def chunker(documents):
    text_splitter = CharacterTextSplitter(
        chunk_size=1000, chunk_overlap=30, separator="\n"
    )
    return text_splitter.split_documents(documents=documents)


