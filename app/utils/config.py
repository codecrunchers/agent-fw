# Configuration class or method
from abc import ABC, abstractmethod
import os


# Config factory
def config_factory():
    config = os.getenv("ENV", "dev")
    if config == "dev":
        return InMemConfig()
    else:
        raise ValueError("Unsupported database type")


# Abstract base class for databases
class AbstractConfig(ABC):
    @abstractmethod
    def get(self):
        pass


class InMemConfig(AbstractConfig):
    def get(self):
        # Logic to determine the environment and get config
        return {
            "db_type": "dev",
            "db_uri": "sqlite:///Chinook.db",
            "file_loader_type": "unstructured",
        }
