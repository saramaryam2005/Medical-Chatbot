import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

app = Flask(__name__)

# Fetching keys safely from environment variables for GitHub protection
PINECONE_KEY = os.getenv("PINECONE_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# Direct Gemini Setup
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.4,
    google_api_key=GEMINI_KEY
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chat():
    try:
        user_message = request.form["msg"]

        pc = Pinecone(api_key=PINECONE_KEY)
        index = pc.Index("medical-chatbot")
        
        query_response = index.query(
            vector=[0.0] * 384, 
            top_k=1,
            include_metadata=True
        )

        context = ""
        for match in query_response.get('matches', []):
            if 'metadata' in match:
                context += match['metadata'].get('text', '') or match['metadata'].get('context', '') or ""

        final_prompt = f"You are an expert medical AI assistant. Answer the question accurately using the context if available.\n\nContext:\n{context}\n\nQuestion: {user_message}"
        response = llm.invoke(final_prompt)
        
        return jsonify({
            "answer": response.content,
            "sources": ["Medical Reference Database"]
        })
    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)}", "sources": []})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)