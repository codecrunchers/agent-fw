from abc import ABC, abstractmethod
from langchain import OpenAI
from app import config


# LLM factory
def llm_factory():
    if config["file_loader_type"] == "unstructured":
        return OpenAILLM()
    else:
        raise ValueError("Unsupported database type")


# Abstract base class for databases
class AbstractLLM(ABC):
    @abstractmethod
    def llm(self):
        pass


class OpenAILLM(AbstractLLM):
    def llm(self):
        return OpenAI(temperature=0)
