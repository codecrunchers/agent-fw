from fastapi import File, Request
from langchain.chains import ConversationalRetrievalChain, LLMChain, RetrievalQA
from langchain.memory import vectorstore
from app import (
    langchain_llm,
    app,
    prompt,
    files,
    vectorstore,
    db_instance,
)
import io


@app.post("/upload")
async def upload(file: bytes = File(...)):
    f = io.BytesIO(file)
    await files.process_upload(f, vectorstore)
    return {"summary": "File processed"}


@app.get("/analyse/{query}")
async def analyse(request: Request, query):
    _prompt = prompt.generate()
    try:
        vstore = vectorstore.load("key")
    except:
        return {"summary": "Please upload a doument, drag it onto me"}

    full_chain = (
        {
            "source1": {"question": lambda x: x["question"]}
            | db_instance.db()
            | db_instance.db().run,
            "source2": (lambda x: x["question"]) | vstore.as_retriever(),
            "question": lambda x: x["question"],
        }
        | _prompt
        | langchain_llm
    )
    response = full_chain.invoke({"query": query, "question": query})
    return {"summary": response}
