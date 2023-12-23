from abc import ABC, abstractmethod
from langchain.tools import DuckDuckGoSearchRun
# Moved config import inside search_factory


# search factory
def search_factory():
    from app import config
    if config["search"] == "DDG":
        return DDGSearch()
    else:
        raise ValueError("Unsupported search")


class AbstractSearch(ABC):
    @abstractmethod
    def search(self, query):
        pass


class DDGSearch(AbstractSearch):
    def search(self, query):
        search = DuckDuckGoSearchRun()
        return search.run(query, backend="news")
