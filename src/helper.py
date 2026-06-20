from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings


def load_pdf_file(data):
    loader = PyPDFLoader(data)
    documents = loader.load()
    return documents


def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20
    )

    text_chunks = text_splitter.split_documents(extracted_data)

    return text_chunks


def get_gemini_embeddings():

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001"
    )

    return embeddings