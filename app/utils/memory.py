from abc import ABC, abstractmethod
from langchain.memory import ConversationBufferMemory
from app import config


# memory factory
def memory_factory():
    if config["memory"] == "in_mem":
        return InMemMemory()
    if config["memory"] == "local":
        return OnDiskLocalMemory()
    else:
        raise ValueError("Unsupported memory")


class AbstractMemory(ABC):
    @abstractmethod
    def save(self, session_id, user, ai):
        pass

    @abstractmethod
    def load(self, session_id):
        pass


class InMemMemory(AbstractMemory):
    memory = None

    def __init__(self):
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )

    def save(self, session_id, user, ai):
        self.memory.chat_memory.add_user_message(user)
        if ai:
            self.memory.chat_memory.add_ai_message(ai)

    def load(self, session_id):
        return self.memory


class OnDiskLocalMemory(AbstractMemory):
    def save(self, session_id, user, ai):
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        self.memory.chat_memory.add_user_message(user)
        if ai:
            self.memory.chat_memory.add_ai_message(ai)

    def load(self, session_id):
        return ConversationBufferMemory(memory_key="chat_history", return_messages=True)
