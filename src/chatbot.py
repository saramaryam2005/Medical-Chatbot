import os
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from src.helper import get_embeddings
from src.prompt import system_prompt

load_dotenv()

# 1. Initialize stable Hugging Face embeddings
embeddings = get_embeddings()

# 2. Connect to Pinecone Index (384 Dimensions)
# 2. Connect to Pinecone Index (384 Dimensions)
index_name = "medical-chatbot"
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)
# 3. Setup Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.4,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

def get_response(user_message):
    """Bina kisi broken chains ke direct similarity search aur LLM prompt context handle karein"""
    try:
        # Context documents fetch karein
        docs = docsearch.similarity_search(user_message, k=3)
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # System prompt aur context ko jod kar final query banayein
        final_prompt = f"{system_prompt}\n\nContext:\n{context}\n\nUser Question: {user_message}"
        
        # Gemini se response lein
        response = llm.invoke(final_prompt)
        
        # Sources extract karein
        sources = []
        for doc in docs:
            source_page = doc.metadata.get("page", "Unknown")
            sources.append(f"Page {source_page}")
            
        return {
            "answer": response.content,
            "sources": list(set(sources))
        }
    except Exception as e:
        return {
            "answer": f"Processing error: {str(e)}",
            "sources": []
        }