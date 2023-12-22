from app.utils.db import database_factory
from app.utils.files import file_loader_factory
from app.utils.llm import llm_factory


db_instance = database_factory()
db_instance.connect()
langchain_llm = llm_factory.llm()
files = file_loader_factory()
