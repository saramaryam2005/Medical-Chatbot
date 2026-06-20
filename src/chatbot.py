import os
from dotenv import load_dotenv

from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore

from langchain_google_genai import ChatGoogleGenerativeAI

from src.helper import get_embeddings
from src.prompt import system_prompt

load_dotenv()

# -----------------------------
# 1. Initialize embeddings
# -----------------------------
embeddings = get_embeddings()

# -----------------------------
# 2. Connect Pinecone
# -----------------------------
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index_name = "medical-chatbot"

vectorstore = PineconeVectorStore(
    index_name=index_name,
    embedding=embeddings,
    pinecone_api_key=os.getenv("PINECONE_API_KEY")
)

# -----------------------------
# 3. Gemini LLM
# -----------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.2
)

# -----------------------------
# 4. Chat loop
# -----------------------------
print("Medical Chatbot is ready! Ask your question...\n")

while True:
    query = input("You: ")

    if query.lower() in ["exit", "quit"]:
        break

    # Step 1: retrieve similar docs
    docs = vectorstore.similarity_search(query, k=3)

    context = "\n\n".join([doc.page_content for doc in docs])

    # Step 2: build prompt
    prompt = system_prompt.format(
        context=context,
        question=query
    )

    # Step 3: get answer from Gemini
    
    response = llm.invoke(prompt)

    print("\nBot:", response.content)
    print("-" * 80)