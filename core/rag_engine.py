from langchain_core.output_parsers import StrOutputParser
from core.prompt import prompt
from langchain_core.runnables import RunnablePassthrough,RunnableLambda
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

import os 
api_key=os.getenv('OPENAI_APIKEY')

llm = ChatOpenAI(model="gpt-5-nano",
                 api_key=api_key)

parser = StrOutputParser()
 

def format_docs(docs):
      return "\n\n".join(doc.page_content for doc in docs)



def create_rag_chain(vector_store, k=4):
    retriever = vector_store.as_retriever(
         search_kwargs={"k": k})
 
    chain = (
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        }
        | prompt         
        | llm
        | parser
    )
    return chain
 

def ask_question(vector_store, question, k=4):
    chain = create_rag_chain(vector_store, k=k)
    response = chain.invoke(question)
 
    if "NO_CONTEXT_FOUND" in response or response.strip() == "":
        return "No documents were retrieved from the vector store — check that it was populated correctly."
 
    return response