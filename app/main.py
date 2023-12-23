from fastapi import File, Request, UploadFile
from langchain.chains import ConversationalRetrievalChain, LLMChain
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

    question_generator = LLMChain(llm=langchain_llm, prompt=_prompt)
    from langchain.chains.qa_with_sources import load_qa_with_sources_chain

    doc_chain = load_qa_with_sources_chain(langchain_llm, chain_type="map_reduce")

    chain = ConversationalRetrievalChain(
        retriever=vstore.as_retriever(),
        question_generator=question_generator,
        combine_docs_chain=doc_chain,
    )

    bot = ConversationalRetrievalChain.from_llm(
        langchain_llm, vstore.as_retriever(), memory=request.state.mem, verbose=False
    )
    history = memory
    response = bot(
        {
            "question": query.strip(),
            "chat_history": history.load(request.state.session_id),
        }
    )
    return {"summary": response["answer"]}
