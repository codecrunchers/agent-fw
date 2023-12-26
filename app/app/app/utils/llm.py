from abc import ABC, abstractmethod
from langchain.llms import OpenAI
from app import config


# LLM factory
def llm_factory():
    if config["llm"] == "OpenAI":
        return OpenAILLM()
    else:
        raise ValueError("Unsupported LLM")


class AbstractLLM(ABC):
    @abstractmethod
    def llm(self):
        pass


class OpenAILLM(AbstractLLM):
    def llm(self):
        return OpenAI(temperature=0)
