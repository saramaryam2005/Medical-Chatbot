import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore

from src.helper import get_embeddings

load_dotenv()

print("Loading embeddings...")

embeddings = get_embeddings()

print("Connecting to Pinecone...")

vectorstore = PineconeVectorStore(
    index_name="medical-chatbot",
    embedding=embeddings,
    pinecone_api_key=os.getenv("PINECONE_API_KEY")
)

query = input("Ask a medical question: ")

docs = vectorstore.similarity_search(
    query,
    k=3
)

print("\nRetrieved Documents:\n")

for i, doc in enumerate(docs, start=1):
    print("=" * 50)
    print(f"Document {i}")

    print("\nMetadata:")
    print(doc.metadata)

    print("\nContent:")
    print(doc.page_content[:500])

    print()