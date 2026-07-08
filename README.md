app_file: app.py
title: Medical Chatbot
emoji: 🏥
colorFrom: blue
colorTo: red
sdk: docker
app_port: 7860

# Medical AI Assistant 🩺

A Retrieval-Augmented Generation (RAG) chatbot that answers medical queries using semantic reference matching and Google's Gemini model. 
The application connects to a pre-indexed Pinecone vector database containing medical encyclopedia data, retrieves the most relevant clinical information for a user query, and generates highly accurate, context-aware responses through a Flask backend.

---

## 🚀 Live Demo

Access the running application directly on Hugging Face Spaces:  
👉 https://huggingface.co/spaces/saramaryam1226/medical-chatbot

---
🏗️ Architecture
                          ┌─────────────────────┐
                          │ Medical Reference   │
                          │   Data / Index      │
                          └──────────┬──────────┘
                                     │
                                     ▼
                             Pinecone Database
                                     ▲
                                     │
                             Direct Search / Query 
                                     ▲
                                     │
                             User Question
                                     │
                                     ▼
                            Retrieve Relevant Context
                                     │
                                     ▼
                             Prompt + Retrieved Context
                                     │
                                     ▼
                             Google Gemini LLM
                                     │
                                     ▼
                              Flask Backend (Gunicorn)
                                     │
                                     ▼
                       HTML5 • CSS3 • JavaScript (Fetch API)

| Category | Technologies |
| :--- | :--- |
| **Backend Framework** | Flask, Python 3.11 |
| **Production WSGI Server** | Gunicorn |
| **Deployment Engine** | Docker (python:3.11-slim) |
| **Frontend UI** | HTML5, CSS3, JavaScript (Inline Fetch API) |
| **LLM Orchestration** | LangChain (`langchain-google-genai`) |
| **Core GenAI Model** | Google Gemini 2.5 Flash |
| **Vector Indexing** | Pinecone (`pinecone-client`) |
| **Environment Config** | `python-dotenv` |


Workflow :-
1- User types a health or clinical question into the chatbot interface.

2- The interactive UI sends an asynchronous POST request to the Flask backend's /get route.

3- The Flask backend establishes a direct connection with the secure Pinecone vector instance.

4- Pinecone returns relevant medical text, context fragments, and corresponding page references.

5- The extracted context metadata is combined with the user's raw message into a structured prompt.

6- The combined prompt payload is dispatched to the gemini-2.5-flash model.

7- Gemini processes the data under a clinical persona and generates a precise answer.

8- The backend packages the streaming payload into a neat JSON payload containing the text and references.

9- The UI dynamically appends the medical response bubble into the chat wrapper seamlessly.
                       
