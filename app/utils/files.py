from langchain.document_loaders import UnstructuredPDFLoader
from abc import ABC, abstractmethod
from app import config


# Database factory
def file_loader_factory():
    if config["file_loader_type"] == "unstructured":
        return UnstructuredFileInterpreter()
    else:
        raise ValueError("Unsupported database type")


# Abstract base class for databases
class AbstractFileLoader(ABC):
    @abstractmethod
    def parse(self, uri):
        pass


class UnstructuredFileInterpreter:
    async def parse(self, uri):
        loader = UnstructuredPDFLoader(uri)
        return loader.load()[:1]
