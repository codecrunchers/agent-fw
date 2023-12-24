@app.get("/analyse/{query}")
async def analyse(request: Request, query):
    _prompt = prompt.generate()
    conversation = LLMChain(
        llm=langchain_llm, prompt=_prompt, verbose=True, memory=request.state.mem
    )
    response = conversation({"question": query.strip()})
    return {"summary": response["text"].strip()}
