from fastapi import File, Request, UploadFile
from langchain.chains import ConversationalRetrievalChain, LLMChain, RetrievalQA
from langchain.chains.loading import _load_qa_with_sources_chain
from langchain.memory import vectorstore
from app import langchain_llm, app, prompt, files, vectorstore, logger, memory
import io


@app.post("/upload")
async def upload(file: bytes = File(...)):
    f = io.BytesIO(file)
    await files.process_upload(f, vectorstore)
    return {"summary": "File processed"}


@app.get("/analyse/{query}")
async def analyse(request: Request, query):
    _prompt = prompt.generate()
    vstore = vectorstore.load("key")
    qa = RetrievalQA.from_chain_type(
        llm=langchain_llm,
        chain_type="stuff",
        retriever=vstore.as_retriever(),
        memory=memory.load(request.state.session_id),
    )
    response = qa.run(query)
    #    import pdb

    #    pdb.set_trace()
    return {"summary": response}
