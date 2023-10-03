import langchain
from langchain import PromptTemplate, LLMChain
from langchain.llms import TextGen
model_url = "http://127.0.0.1:5000"
langchain.debug = True

template = """Question: {question}"""
prompt = PromptTemplate(template=template, input_variables=["question"])
llm = TextGen(model_url=model_url)
llm_chain = LLMChain(prompt=prompt, llm=llm)
question = "你叫怎麼名字?"

llm_chain.run(question)