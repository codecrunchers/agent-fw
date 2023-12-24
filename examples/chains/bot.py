@app.get("/analyse/{query}")
async def analyse(request: Request, query):
    _prompt = prompt.generate()
    vstore = vectorstore.load("key")

    question_generator = LLMChain(
        llm=langchain_llm, prompt=_prompt, memory=memory.load(request.state.session_id)
    )
    from langchain.chains.question_answering import load_qa_chain

    doc_chain = load_qa_chain(langchain_llm, chain_type="stuff")

    chain = ConversationalRetrievalChain(
        retriever=vstore.as_retriever(),
        question_generator=question_generator,
        combine_docs_chain=doc_chain,
        response_if_no_docs_found=None,
    )

    response = chain({"question": query.strip(), "chat_history": []})
    return {"summary": response["answer"]}
