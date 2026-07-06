from langchain_huggingface import HuggingFaceEmbeddings

from langchain_chroma import Chroma


embeddings = HuggingFaceEmbeddings(

    model_name=

    "sentence-transformers/all-MiniLM-L6-v2"

)


vectordb = Chroma(

    persist_directory="chroma_db",

    embedding_function=embeddings

)