from langchain_core.documents import Document

from langchain_text_splitters import (

    RecursiveCharacterTextSplitter

)

from rag.vectordb import vectordb


documents = [

"""
LangGraph enables

stateful multi-agent workflows.
""",

"""
Retrieval Augmented Generation

combines retrieval

and generation.
""",

"""
AI Agents can collaborate

using graph based workflows.
"""

]


splitter = RecursiveCharacterTextSplitter(

    chunk_size=500,

    chunk_overlap=50

)


all_docs = []


for doc in documents:

    chunks = splitter.split_text(doc)

    for chunk in chunks:

        all_docs.append(

            Document(

                page_content=chunk

            )

        )


vectordb.add_documents(

    all_docs

)


print(

    "Documents added."

)