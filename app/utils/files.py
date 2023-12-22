from langchain.document_loaders import UnstructuredPDFLoader
from app.utils.config import get_environment_config
from abc import ABC, abstractmethod


# Database factory
def file_loader_factory():
    config = get_environment_config()
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
