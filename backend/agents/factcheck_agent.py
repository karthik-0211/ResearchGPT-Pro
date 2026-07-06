from agents.llm import llm


def clean_text(text):

    if not text:
        return ""

    return text.strip()




def factcheck_agent(state):

    query = state.get("query", "")

    summary = state.get(

        "summary",

        ""

    )


    web_results = state.get(

        "web_results",

        []

    )[:5]


    rag_results = state.get(

        "rag_results",

        []

    )[:3]


    pdf_summary = state.get(

        "pdf_summary",

        ""

    )



    pdf_evidence = ""

    if pdf_summary:

        pdf_evidence = f"\nUploaded PDF Evidence (Highly Trusted):\n{pdf_summary}\n"



    prompt = f"""

You are ResearchGPT Pro.

You are an expert fact checker.


User's Request: {query}


Your job:

1. Verify the research summary against the provided evidence (Web Evidence, Knowledge Base, and Uploaded PDF Evidence).

2. The Uploaded PDF Evidence is trusted and verified. If the research summary contains facts from the PDF, they are considered verified and MUST be preserved.

3. Remove false or unsupported claims that are not backed by any of the evidence.

4. Keep verified explanations.

5. Preserve useful content.

6. Mention uncertainty if evidence is weak.

7. Never invent facts, statistics, dates, citations, or references.


Research Summary:

{summary}


Web Evidence:

{web_results}


Knowledge Base:

{rag_results}

{pdf_evidence}


Return:

Verified Information

Important Limitations

Uncertain Areas

"""



    try:


        response = llm.invoke(

            prompt

        )



        verified = clean_text(

            response.content

        )



        if len(verified) < 30:

            verified = clean_text(summary)




    except Exception as e:


        print(

            "FactCheck Error:",

            e

        )



        verified = clean_text(summary)




    return {

        **state,

        "factcheck": verified,


        "agent_status": {

            **state.get(

                "agent_status",

                {}

            ),

            "factcheck": "completed"

        }

    }