import os
import sys
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from src.prompt import system_prompt

load_dotenv()

app = Flask(__name__)

# 1. Direct Embeddings Setup here
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 2. Connect to Pinecone
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

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chat():
    try:
        user_message = request.form["msg"]
        
        # Similarity Search
        docs = docsearch.similarity_search(user_message, k=3)
        context = "\n\n".join([doc.page_content for doc in docs])
        
        final_prompt = f"{system_prompt}\n\nContext:\n{context}\n\nUser Question: {user_message}"
        response = llm.invoke(final_prompt)
        
        sources = [f"Page {doc.metadata.get('page', 'Unknown')}" for doc in docs]
        
        return jsonify({
            "answer": response.content,
            "sources": list(set(sources))
        })
    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({
            "answer": f"Error: {str(e)}",
            "sources": []
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860, debug=True)