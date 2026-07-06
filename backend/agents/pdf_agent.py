from tools.pdf_reader import read_pdf

from agents.llm import llm



def clean_text(text):

    if not text:

        return ""


    text = (

        text

        .replace("**", "")

        .replace("***", "")

        .replace("###", "")

        .replace("##", "")

        .replace("#", "")

        .replace("```", "")

        .replace("*", "")

    )


    return text.strip()




def pdf_agent(state):

    pdf_path = state.get(

        "pdf_path"

    )

    query = state.get("query", "")



    # No PDF uploaded

    if not pdf_path:

        return {

            **state,

            "pdf_summary": ""

        }



    try:


        pdf_text = read_pdf(

            pdf_path

        )



        if not pdf_text:

            return {

                **state,

                "pdf_summary":

                "The uploaded document could not be read or was empty."

            }



        # limit tokens

        pdf_text = pdf_text[:20000]




        prompt = f"""

You are ResearchGPT Pro.

You are an expert Document Research Assistant.


IMPORTANT RULES:

1. Use the provided document content to address the User's Request.

2. If the user is asking to summarize the document (e.g. "summarize this", "give me a summary"), provide a comprehensive summary of the document focusing on the main topic, key findings, methodology, and conclusion.

3. If the user is asking a specific question, answer it directly and thoroughly using the relevant details in the document.

4. Use ONLY information available in the document. Do not assume or extrapolate. If the information to answer the query is not in the document, state "Not mentioned in the document."

5. Explain naturally like ChatGPT.

6. Use short paragraphs and professional English.

7. DO NOT use markdown headers (#, ##, ###), bold (**), or code blocks. Return plain text only.


User's Request:

{query}


Document Content:

{pdf_text}


Return plain text only.

"""




        response = llm.invoke(

            prompt

        )



        summary = clean_text(

            response.content

        )



        if len(summary) < 20:

            summary = (

                "I don't have enough "

                "reliable information."

            )





    except Exception as e:


        print(

            "PDF Agent Error:",

            e

        )



        summary = (

            "I don't have enough "

            "reliable information."

        )





    return {

        **state,

        "pdf_summary": summary

    }