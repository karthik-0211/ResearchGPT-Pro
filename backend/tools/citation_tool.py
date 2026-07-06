from rag.vectordb import get_vectordb


def retrieve_docs(query):

    try:

        docs = get_vectordb().similarity_search(

            query,

            k=5

        )


        if not docs:

            return []


        results = []


        for d in docs:

            if hasattr(d,"page_content"):

                text=d.page_content.strip()

                if text:

                    results.append(text)


        return results



    except Exception as e:


        print(

            "RAG Retrieval Error:",

            e

        )


        return []