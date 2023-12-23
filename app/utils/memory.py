from abc import ABC, abstractmethod
from langchain.memory import ConversationBufferMemory
from app import config


# memory factory
def memory_factory():
    if config["memory"] == "in_mem":
        return InMemMemory()
    else:
        raise ValueError("Unsupported memory")


class AbstractMemory(ABC):
    @abstractmethod
    def save(self, session_id):
        pass

    @abstractmethod
    def load(self, sesss):
        pass


class InMemMemory(AbstractMemory):
    def save(self, session_id, user, ai):
        memory = ConversationBufferMemory(memory_key=session_id)
        memory.chat_memory.add_user_message(user)
        memory.chat_memory.add_ai_message(ai)

    def load(self, session_id):
        pass
