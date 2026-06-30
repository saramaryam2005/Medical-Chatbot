

import os
from dotenv import load_dotenv

from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI

from src.helper import get_embeddings
from src.prompt import system_prompt

load_dotenv()


vectorstore = None
llm = None


def initialize():

    global vectorstore, llm

    if vectorstore is None:

        print("Loading embeddings...")

        embeddings = get_embeddings()

        print("Connecting to Pinecone...")

        vectorstore = PineconeVectorStore(
            index_name="medical-chatbot",
            embedding=embeddings,
            pinecone_api_key=os.getenv("PINECONE_API_KEY")
        )

    if llm is None:

        print("Loading Gemini...")

        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.2
        )


def get_response(query):

    initialize()

    docs = vectorstore.similarity_search(
        query,
        k=5
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = system_prompt.format(
        context=context,
        question=query
    )

    response = llm.invoke(prompt)

    # Extract source page numbers
    pages = []

    for doc in docs:

        page = doc.metadata.get("page_label")

        if page and page not in pages:
            pages.append(page)

    return {
        "answer": response.content,
        "sources": pages
    }