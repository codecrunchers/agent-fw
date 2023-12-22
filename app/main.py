from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain import PromptTemplate
from langchain.chains import LLMChain
from app import langchain_llm, db_instance, files

# FASTAPI
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# LANGCHAIN
# langchain_llm = LLM

summarize_template_string = """
        Provide a summary for the following text:
        {text}
"""

summarize_prompt = PromptTemplate(
    template=summarize_template_string,
    input_variables=["text"],
)

summarize_chain = LLMChain(
    llm=langchain_llm,
    prompt=summarize_prompt,
)


@app.post("/summarize-text")
async def summarize_text(text: str):
    summary = summarize_chain.run(text=text)
    return {"summary": summary}


@app.get("/query-db")
async def query_db(text: str):
    response = db_instance.query(text)
    return {"summary": response}


@app.get("/getdoc")
async def get_doc(uri):
    response = await files.parse(uri)
    return {"summary": response}
