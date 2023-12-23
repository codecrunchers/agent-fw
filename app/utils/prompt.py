from abc import ABC, abstractmethod
from langchain_core.prompts import PromptTemplate
from app import config


# prompt factory
def prompt_factory():
    if config["prompt"] == "string":
        return StringPrompt()
    else:
        raise ValueError("Unsupported prompt")


class AbstractPrompt(ABC):
    @abstractmethod
    def generate(self, history, question):
        pass


class StringPrompt(AbstractPrompt):
    template = """You are a document fraud expert reasoning about the legitimacy of a document and the owner having conversation with a fraud analyst.

    Previous conversation:
    {chat_history}

    New human question: {question}
    Response:"""

    def __init__(self, prompt=None):
        self.prompt_template = self.template

    def generate(self):
        prompt = PromptTemplate.from_template(self.prompt_template)
        return prompt
