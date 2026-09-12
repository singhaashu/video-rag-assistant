from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(""" 
You are a helpful AI assistant.

Answer the question only from the provided context.
If the answer is not found in the context, say:
"I couldn't find this information in the provided transcript."

Context:
{context}

Question:
{question}

Answer:
""")
