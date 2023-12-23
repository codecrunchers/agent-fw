from enum import Enum
from fastapi import File
from langchain.document_loaders import UnstructuredFileIOLoader, UnstructuredPDFLoader
from abc import ABC, abstractmethod
from app import config
from langchain.document_loaders.image import UnstructuredImageLoader
import pathlib


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
    def process(self, uri, db):
        pass

    @abstractmethod
    def process_upload(self, file, db):
        pass


class UnstructuredFileInterpreter:
    class FileType(Enum):
        PDF = 1
        IMG = 2
        JPG = 3
        PNG = 4

    async def parse(self, uri):
        if self.simple_file_type(uri) == UnstructuredFileInterpreter.FileType.PDF:
            loader = UnstructuredPDFLoader(uri)
        elif self.simple_file_type(uri) in UnstructuredFileInterpreter.FileType:
            loader = UnstructuredImageLoader(uri)
        else:
            raise Exception("Unsupported file")

        self.documents = loader.load()
        self.key = uri

    async def process(self, uri, db):
        """
        Parses and saves the document to configured vectordb
        """
        await self.parse(uri)
        db.save(self.documents, uri)

    def simple_file_type(self, uri):
        return UnstructuredFileInterpreter.FileType[
            pathlib.Path(uri).suffix.strip(".").upper()
        ]

    async def process_upload(self, file, db):
        loader = UnstructuredFileIOLoader(file)

        documents = loader.load()
        db.save(documents, "key")

        self.key = ""
