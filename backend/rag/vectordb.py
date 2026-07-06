from langchain_huggingface import HuggingFaceEmbeddings

from langchain_chroma import Chroma


_embeddings = None
_vectordb = None

def get_embeddings():
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    return _embeddings

def get_vectordb():
    global _vectordb
    if _vectordb is None:
        _vectordb = Chroma(
            persist_directory="chroma_db",
            embedding_function=get_embeddings()
        )
    return _vectordb