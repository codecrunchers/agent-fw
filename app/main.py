from fastapi import File, Request
from langchain.chains import LLMChain
from app import (
    langchain_llm,
    app,
    prompt,
)


@app.post("/upload")
def get_file(file: bytes = File(...)):
    content = file.decode("utf-8")
    lines = content.split("\n")
    return {"content": lines}


@app.get("/analyse/{query}")
async def analyse(request: Request, query):
    _prompt = prompt.generate()
    conversation = LLMChain(
        llm=langchain_llm, prompt=_prompt, verbose=True, memory=request.state.mem
    )
    response = conversation({"question": query.strip()})
    return {"summary": response["text"].strip()}
