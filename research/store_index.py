import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from src.helper import load_pdf_file, text_split, get_embeddings

load_dotenv()

print("Loading PDF...")
extracted_data = load_pdf_file("data/Gale Encyclopedia of Medicine Vol. 1 (A-B).pdf")

print("Splitting into chunks...")
text_chunks = text_split(extracted_data)

print("Initializing Stable Embeddings...")
embeddings = get_embeddings()

print("Connecting to Pinecone and uploading vectors...")
docsearch = PineconeVectorStore.from_documents(
    documents=text_chunks,
    embedding=embeddings,
    index_name="medical-chatbot",
    pinecone_api_key=os.getenv("PINECONE_API_KEY")
)

print("Upload completed successfully!")