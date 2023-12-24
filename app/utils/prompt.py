from abc import ABC, abstractmethod
from app import config
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
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
    template = """You are a music expert in the field of heavy metal, specialisaing in Iron Maiden
            You can use this data to answer questions related to bands, their activities, and album details.
            <source1>
            {source1}
            </source1>

            Source 2: information about Bands
            <source2>
            {source2}
            </source2>

            From the database
            {query}
            """

    general_user_template = "human:```{question}```"

    def __init__(self, prompt=None):
        self.prompt_template = self.template if not prompt else prompt

    def generate(self):
        #        prompt = ChatPromptTemplate.from_messages(
        #            messages=[
        #                SystemMessagePromptTemplate.from_template(self.prompt_template),
        #                MessagesPlaceholder(variable_name="chat_history"),
        #                HumanMessagePromptTemplate.from_template(self.general_user_template),
        #            ]
        #
        #        )

        prompt = PromptTemplate(
            input_variables=["context", "query"], template=self.prompt_template
        )

        return prompt
