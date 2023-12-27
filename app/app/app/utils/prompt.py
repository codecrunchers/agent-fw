from abc import ABC, abstractmethod
from app import config
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


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
    template = """You are a document fraud expert reasoning about the legitimacy of a document and the owner having conversation with a fraud analyst. \
            ---- \
            {context}\
            ---- \
            """

    general_user_template = "Question:```{question}```"

    def __init__(self, prompt=None):
        self.prompt_template = self.template

    def generate(self):
        prompt = ChatPromptTemplate.from_messages(
            messages=[
                SystemMessagePromptTemplate.from_template(self.prompt_template),
                #                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template(self.general_user_template),
            ]
        )

        return prompt
