from latgchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app import langchain_llm, files, vectorstore, app
from langchain.chains import RetrievalQA


@app.get("/analyse")
async def get_doc(uri, query):
    response = await files.process(uri, vectorstore)
    vstore = vectorstore.load(uri)

#    search = search.search("")

    qa = RetrievalQA.from_chain_type(
        llm=langchain_llm,
        chain_type="stuff",
        retriever=vstore.as_retriever(),
    )
    result = qa.run(query)
    return {"summary": result}
