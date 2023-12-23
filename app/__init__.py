from app.utils.config import config_factory

# Leave me here
config = config_factory().get()

import sys
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import secrets
import logging
from app.utils.searchengine import search_factory
from fastapi import Request


from app.utils.vectorstore import vectorstore_factory
from app.utils.db import database_factory
from app.utils.files import file_loader_factory
from app.utils.llm import llm_factory
from app.utils.prompt import prompt_factory
from app.utils.memory import memory_factory

# Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

# Tools
search = search_factory()
db_instance = database_factory()
db_instance.connect()
langchain_llm = llm_factory().llm()
files = file_loader_factory()
vectorstore = vectorstore_factory()
prompt = prompt_factory()
memory = memory_factory()

# FASTAPI
app = FastAPI(title="CAIRunner")
logger.info("CAI is starting up")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Check if a session ID is already set
        session_id = request.cookies.get("session_id")
        if not session_id:
            # Generate a new session ID
            session_id = secrets.token_urlsafe()
            request.state.session_id = session_id
            response = await call_next(request)
            response.set_cookie(key="session_id", value=session_id)
            return response
        else:
            # Use the existing session ID
            request.state.session_id = session_id
            return await call_next(request)


app.add_middleware(SessionMiddleware)


def get_session_id(request: Request):
    return getattr(request.state, "session_id", None)
