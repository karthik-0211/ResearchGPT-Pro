from agents.llm import llm

from tools.web_search import search_web
from tools.citation_tool import retrieve_docs



def researcher_agent(state):

    query = state.get("query", "")
    search_query = state.get("search_query", query)
    history = state.get("history", [])
    history_str = ""
    if history:
        history_str = "Conversation History:\n" + "\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in history]) + "\n\n"

    pdf_path = state.get("pdf_path")
    web_results = []
    rag_results = []

    # If PDF is uploaded and the query is a pure PDF/summarization request, skip web search and RAG
    q_lower = query.lower().strip()
    is_pure_pdf_query = False
    if pdf_path:
        if not q_lower or any(w in q_lower for w in ["summarize", "summary", "summarise", "extract", "read this", "what is this"]):
            is_pure_pdf_query = True
        elif len(q_lower.split()) <= 3 and any(w in q_lower for w in ["it", "file", "document", "pdf"]):
            is_pure_pdf_query = True

    if not is_pure_pdf_query:
        # ---------------- Web Search ----------------
        try:
            web_results = search_web(
                search_query,
                max_results=8
            )
        except Exception as e:
            print("Web Search Error:", e)
            web_results = []

        # ---------------- RAG ----------------
        try:
            rag_results = retrieve_docs(
                search_query
            )
        except Exception as e:
            print("RAG Error:", e)
            rag_results = []




    prompt = f"""

You are ResearchGPT Pro.

You are an INTERNAL Research Agent.

The user will NEVER see your output.


Rules:

1. Use:

- Your verified general knowledge

- Web Results if available

- Knowledge Base if available


2. Prefer Web Results over memory.


3. NEVER invent:

- facts

- dates

- citations

- references

- papers

- statistics


4. NEVER guess.


5. If uncertain:

Explicitly mention uncertainty.


6. Keep notes factual and detailed.


{history_str}Latest User Query:

{query}



Web Results:

{web_results}



Knowledge Base:

{rag_results}



Prepare detailed INTERNAL NOTES:


Overview


Key Concepts


Recent Developments


Applications


Challenges


Future Scope


Limitations


Sources Used


"""



    try:


        response = llm.invoke(prompt)


        notes = response.content.strip()



        if len(notes) < 30:

            notes = (

                "Insufficient reliable information."

            )




    except Exception as e:


        print(

            "Researcher Error:",

            e

        )



        notes = (

            "Insufficient reliable information."

        )





    return {

        **state,


        "research_notes": notes,


        "web_results": web_results,


        "rag_results": rag_results,


        "agent_status": {

            **state.get(

                "agent_status",

                {}

            ),

            "researcher":

            "completed"

        }

    }