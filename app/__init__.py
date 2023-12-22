import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.utils.config import config_factory

import logging
from app.utils.searchengine import search_factory

# Leave me here
config = config_factory().get()

from app.utils.vectorstore import vectorstore_factory
from app.utils.db import database_factory
from app.utils.files import file_loader_factory
from app.utils.llm import llm_factory

search = search_factory()
db_instance = database_factory()
db_instance.connect()
langchain_llm = llm_factory().llm()
files = file_loader_factory()
vectorstore = vectorstore_factory()


# FASTAPI
app = FastAPI(title="CAIRunner")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info("CAI is starting up")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
