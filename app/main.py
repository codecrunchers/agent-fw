from fastapi import File, Request, UploadFile
from langchain.chains import LLMChain
from langchain.memory import vectorstore
from app import langchain_llm, app, prompt, files, vectorstore, logger


@app.post("/upload")
async def upload(file: bytes = File(...)):
    import io

    f = io.BytesIO(file)
    await files.process_upload(f, vectorstore)
    return {"summary": "File proecessed"}


@app.get("/analyse/{query}")
async def analyse(request: Request, query):
    _prompt = prompt.generate()
    conversation = LLMChain(
        llm=langchain_llm, prompt=_prompt, verbose=True, memory=request.state.mem
    )
    response = conversation({"question": query.strip()})
    return {"summary": response["text"].strip()}
