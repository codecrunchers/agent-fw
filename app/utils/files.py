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
    def process(self):
        pass


class UnstructuredFileInterpreter:
    async def parse(self, uri):
        loader = UnstructuredPDFLoader(uri)
        self.documents = loader.load()
        self.key = uri

    async def process(self, uri, db):
        await self.parse(uri)
        embeddings = OpenAIEmbeddings()
        vs = FAISS.from_documents(chunker(self.documents), embeddings)
        db.save(vs, uri)


async def chunker(documents):
    text_splitter = CharacterTextSplitter(
        chunk_size=1000, chunk_overlap=30, separator="\n"
    )
    return text_splitter.split_documents(documents=documents)
