from langchain.llms import OpenAI
from langchain.utilities import SQLDatabase
from app.utils.config import get_environment_config
from langchain_experimental.sql import SQLDatabaseChain
from abc import ABC, abstractmethod


# Database factory
def database_factory():
    config = get_environment_config()
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
    def query(self, query):
        pass


class LocalDatabase(AbstractDatabase):
    def connect(self) -> None:
        db = SQLDatabase.from_uri(get_environment_config()["db_uri"])
        llm = OpenAI(temperature=0, verbose=True)
        self.db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

    def query(self, query: str):
        return self.db_chain.run(query)
