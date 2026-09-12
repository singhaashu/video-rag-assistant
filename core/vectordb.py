from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
# from langchain_ollama import OllamaEmbeddings
# embeddings = OllamaEmbeddings(model="nomic-embed-text")
import os
from dotenv import  load_dotenv
load_dotenv()

from langchain_openai import OpenAIEmbeddings
api_key=os.getenv('OPENAI_APIKEY')
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=api_key)

CHROMA_DIR='vector_db'
COLLECTION_NAME = "meeting_transcript"

def build_vector(trans_script:str):

    splitter=RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks=splitter.split_text(trans_script)

    documents = [
        Document(page_content=chunk, metadata={'chunk_index' : i})
        for i,chunk in enumerate(chunks)
    ]

    vector_store=Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory=CHROMA_DIR,
    collection_name=COLLECTION_NAME
   )

    return  vector_store

def load_vector():
    vector_store=Chroma(
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
        collection_name=COLLECTION_NAME,
    )
    return vector_store

    
 
