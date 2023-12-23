
@app.get("/file_query}")
async def get_doc(request: Request, query, uri):
    await files.process(uri, vectorstore)
     vstore = vectorstore.load(uri)

     qa = RetrievalQA.from_chain_type(
             llm=langchain_llm,
             chain_type="stuff",
             retriever=vstore.as_retriever(),
             )
     result = qa.run(query)
