from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app import langchain_llm, db_instance, files, vectorstore, app


@app.post("/summarize-text")
async def summarize_text(text: str):
    summarize_template_string = """
            Provide a summary for the following text:
            {text}
    """

    summarize_prompt = PromptTemplate(
        template=summarize_template_string,
        input_variables=["text"],
    )
    summarize_chain = LLMChain(
        llm=langchain_llm,
        prompt=summarize_prompt,
    )
    summary = summarize_chain.run(text=text)
    return {"summary": summary}


@app.get("/getdoc")
async def get_doc(uri):
    response = await files.process(vectorstore, uri)
    return {"summary": response}
