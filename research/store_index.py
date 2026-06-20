# UPLOAD DATA FILE
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import os
from dotenv import load_dotenv

from langchain_pinecone import PineconeVectorStore

from src.helper import (
    load_pdf_file,
    text_split,
    get_gemini_embeddings
)

load_dotenv()

print("Loading PDF...")

documents = load_pdf_file(
    "data/Gale Encyclopedia of Medicine Vol. 1 (A-B).pdf"
)

print(f"Pages loaded: {len(documents)}")

print("Splitting into chunks...")

text_chunks = text_split(documents)

print(f"Chunks created: {len(text_chunks)}")

print("Creating embeddings and uploading to Pinecone...")

embeddings = get_gemini_embeddings()

docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    embedding=embeddings,
    index_name="medical-chatbot"
)

print("Upload completed successfully!")