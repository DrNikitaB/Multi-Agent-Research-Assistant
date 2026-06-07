import os
import fitz

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS



def pdf_embedding_node(state):

    pdf_path = state["file_path"]

    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_text(text)

    embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

    vector_db = FAISS.from_texts(
        chunks,
        embeddings
    )

    db_path = "faiss_index"

    vector_db.save_local(db_path)

    return {
        "pdf_text": text,
        "vector_store_path": db_path
    }