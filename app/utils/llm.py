from langchain import OpenAI
from app.utils.config import get_environment_config


# LLM factory
def llm_factory():
    config = get_environment_config()
    if config["file_loader_type"] == "unstructured":
        return OpenAILLM()
    else:
        raise ValueError("Unsupported database type")


# Abstract base class for databases
class AbstractLLM(ABC):
    @abstractmethod
    def llm(self):
        pass


class OpenAILLM(AbstractLLM):
    def llm(self):
        return OpenAI(temperature=0)
