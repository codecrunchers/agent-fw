from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from abc import ABC, abstractmethod
from app import config
from app.utils.llm import llm_factory
from app.utils.memory import memory_factory


# Database factory
def database_factory():
    if config["db_type"] == "dev":
        return LocalDatabase()
    else:
        raise ValueError("Unsupported database type")


# Abstract base class for databases
class AbstractDatabase(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    async def query(self, query):
        pass


PROMPT_SUFFIX = """Use any tables:
Previous Conversation:
{chat_history}

Question: {input}"""

_DEFAULT_TEMPLATE = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer. Unless the user specifies in his question a specific number of examples he wishes to obtain, always limit your query to at most {top_k} results. You can order the results by a relevant column to return the most interesting examples in the database.

Never query for all the columns from a specific table, only ask for a the few relevant columns given the question.

Pay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.

Use the following format:

Question: Question here
SQLQuery: SQL Query to run
SQLResult: Result of the SQLQuery
Answer: Final answer here

"""
PROMPT = PromptTemplate.from_template(
    _DEFAULT_TEMPLATE + PROMPT_SUFFIX,
)


class LocalDatabase(AbstractDatabase):
    def connect(self) -> None:
        db = SQLDatabase.from_uri(config["db_uri"])
        llm = llm_factory().llm()
        self.db_chain = SQLDatabaseChain.from_llm(
            llm, db, prompt=PROMPT, verbose=True, memory=memory_factory().load("")
        )

    def db(self):
        return self.db_chain

    async def query(self, query: str):
        return self.db_chain.run(query)
