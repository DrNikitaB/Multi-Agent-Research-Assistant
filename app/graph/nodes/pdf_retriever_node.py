
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def pdf_retriever_node(state):

    query = state["query"]

    embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

    db = FAISS.load_local(
        state["vector_store_path"],
        embeddings,
        allow_dangerous_deserialization=True
    )

    docs = db.similarity_search(
        query,
        k=5
    )

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    return {
        "retrieved_chunks": context
    }