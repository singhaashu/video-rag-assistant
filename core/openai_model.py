from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

import os 
api_key=os.getenv('OPENAI_APIKEY')
llm = ChatOpenAI(model="gpt-5-nano",
                 api_key=api_key)

def openai_llm(text: str) -> str:
    response = llm.invoke(text)
    return response.content


 # import requests

# def ollama_llm(text, model="gemma3:1b"):
#     """text: a plain string prompt (already formatted)."""
#     response = requests.post(
#         "http://localhost:11434/api/chat",
#         json={
#             "model": model,
#             "messages": [{"role": "user", "content": text}],
#             "stream": False,
#         },
#     )
#     response.raise_for_status()
#     return response.json()["message"]["content"]
 