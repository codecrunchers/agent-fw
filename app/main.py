from latgchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app import langchain_llm, files, vectorstore
from fastapi import FastAPI
from langchain.chains import RetrievalQA

app = FastAPI()

async def main(uri, query):
    response = await files.process(uri, vectorstore)
    vstore = vectorstore.load(uri)
    # search = search.search("")
    qa = RetrievalQA.from_chain_type(
        llm=langchain_llm,
        chain_type="stuff",
        retriever=vstore.as_retriever(),
    )
    result = qa.run(query)
    # the rest of the code goes here
    return {"summary": result}

@app.get("/analyse")
async def get_doc(uri, query):
    return await main(uri, query)
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
