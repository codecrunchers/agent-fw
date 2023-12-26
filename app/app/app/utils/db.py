from langchain.llms import OpenAI
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from abc import ABC, abstractmethod
from app import config


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


class LocalDatabase(AbstractDatabase):
    def connect(self) -> None:
        db = SQLDatabase.from_uri(config["db_uri"])
        llm = OpenAI(temperature=0, verbose=True)
        try:
            self.db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
        except Exception as e:
            print(f"!!!!!!!!!!!       {e}     !!!!!!!!!!!")
    async def query(self, query: str):
        return self.db_chain.run(query)
