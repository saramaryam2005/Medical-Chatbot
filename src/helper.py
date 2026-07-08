import os
from langchain_pdf_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def load_pdf_file(data):
    loader = PyPDFLoader(data)
    documents = loader.load()
    return documents

def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks

def get_embeddings():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="text-embedding-004",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )
    return embeddings