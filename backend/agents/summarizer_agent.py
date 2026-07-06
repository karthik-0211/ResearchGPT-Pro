from agents.llm import llm


def clean_text(text):

    if not text:
        return ""

    return text.strip()




def summarizer_agent(state):

    query = state.get("query", "")

    notes = clean_text(

        state.get(

            "research_notes",

            ""

        )

    )


    pdf_summary = clean_text(

        state.get(

            "pdf_summary",

            ""

        )

    )



    combined_context = f"""

Research Notes:

{notes}



PDF Summary:

{pdf_summary}

"""



    prompt = f"""

You are ResearchGPT Pro.

You are an expert AI research summarizer similar to ChatGPT.


User's Request: {query}


Your task:

Address the User's Request by creating a detailed, professional, and comprehensive response formatted in markdown.

If the user has uploaded a PDF, prioritize the PDF content/summary to answer or summarize as requested.


IMPORTANT RULES:



1. Use ONLY the supplied information.



2. NEVER invent:

- Facts

- Dates

- Statistics

- Citations

- References

- Research papers



3. If information is uncertain:

Clearly mention uncertainty.



4. Write naturally like ChatGPT.



5. Use rich markdown formatting (headings like ## and ###, bold text, bullet points) to structure the summary beautifully.



6. Avoid repetition.



Available Information:

{combined_context}

"""



    try:


        response = llm.invoke(

            prompt

        )



        summary = clean_text(

            response.content

        )



        if len(summary) < 50:



            summary = combined_context



        if len(summary) < 50:



            summary = (

                "I don't have enough reliable "

                "information to answer this."

            )




    except Exception as e:


        print(

            "Summarizer Error:",

            e

        )



        summary = (

            clean_text(combined_context)

            or

            "I don't have enough reliable "

            "information to answer this."

        )




    return {

        **state,

        "summary": summary,


        "agent_status": {

            **state.get(

                "agent_status",

                {}

            ),

            "summarizer": "completed"

        }

    }