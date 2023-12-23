from fastapi import Depends
from app import langchain_llm, files, vectorstore, logger, app, get_session_id, prompt


@app.get("/analyse")
async def get_doc(uri, query, session_id: str = Depends(get_session_id)):
    #    await files.process(uri, vectorstore)
    #    vstore = vectorstore.load(uri)
    #    qa = RetrievalQA.from_chain_type(
    #        llm=langchain_llm,
    #        chain_type="stuff",
    #        prompt=prompt,
    #        retriever=vstore.as_retriever(),
    #    )
    #    result = qa.run(query)
    return {"summary": session_id}
