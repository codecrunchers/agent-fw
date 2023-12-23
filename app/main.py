from fastapi import Request
from langchain.chains import LLMChain
from app import (
    langchain_llm,
    app,
    prompt,
)


@app.get("/analyse/{query}/{uri}")
async def analyse(request: Request, query, uri):
    _prompt = prompt.generate()
    conversation = LLMChain(
        llm=langchain_llm, prompt=_prompt, verbose=True, memory=request.state.mem
    )
    response = conversation({"question": query})
    return {"summary": response["text"]}
