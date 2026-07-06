import os

_embeddings = None
_vectordb = None

def get_embeddings():
    global _embeddings
    if _embeddings is None:
        from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings
        hf_token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACEHUB_API_TOKEN")
        _embeddings = HuggingFaceEndpointEmbeddings(
            model="sentence-transformers/all-MiniLM-L6-v2",
            task="feature-extraction",
            huggingfacehub_api_token=hf_token
        )
    return _embeddings

def get_vectordb():
    global _vectordb
    if _vectordb is None:
        from langchain_chroma import Chroma
        _vectordb = Chroma(
            persist_directory="chroma_db",
            embedding_function=get_embeddings()
        )
    return _vectordb