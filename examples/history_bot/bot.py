@app.get("/analyse/{query}/{uri}")
async def get_doc(request: Request, query, uri):
    # query_params = request.query_params
    # uri = query_params.get("uri")
    # query = query_params.get("query")

    logger.debug("Question is %s", query)

    # Process and Save Fie Embeddings
    # await files.process(uri, vectorstore)
    # vstore = vectorstore.load(uri)

    # qa = RetrievalQA.from_chain_type(
    #    llm=langchain_llm,
    #    chain_type="stuff",
    #    prompt=prompt.generate(),
    #    retriever=vstore.as_retriever(),
    # )
    # result = qa.run(query)
    mem = memory.load(get_session_id(request))
    _prompt = prompt.generate()
    conversation = LLMChain(llm=langchain_llm, prompt=_prompt, verbose=True, memory=mem)
    response = conversation({"question": query})
    logger.debug(response["text"])
    memory.save(get_session_id(request), query, response["text"])
    return {"summary": response["text"]}
