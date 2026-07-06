from agents.llm import llm


def clean_text(text):

    if not text:
        return ""

    return text.strip()




def report_agent(state):

    query = state.get("query", "")

    summary = clean_text(

        state.get("summary", "")

    )


    factcheck = clean_text(

        state.get("factcheck", "")

    )



    prompt = f"""

You are ResearchGPT Pro.

Prepare the FINAL, highly detailed, comprehensive, and complete markdown report shown to the user.


User's Original Request: {query}


Rules:

1. Directly and thoroughly answer or address the User's Original Request using the Research Summary and Verified Information.

2. Write naturally like ChatGPT.

3. Use sections, clear headings (##, ###), bullet points, and tables to structure your output professionally.

4. Keep paragraphs detailed, clear, and comprehensive. Provide thorough explanations, rich context, and background.

5. Professional, authoritative tone.

6. Never invent facts, statistics, dates, or citations.

7. If uncertain, mention uncertainty.

8. Use rich markdown formatting where helpful. Do not restrict formatting.



Research Summary:

{summary}



Verified Information:

{factcheck}



Generate the final comprehensive and detailed report.

"""



    try:


        response = llm.invoke(prompt)


        report = clean_text(

            response.content

        )




        # If LLM gives empty output

        if len(report) < 30:


            # Prefer factcheck ONLY if it is meaningful

            if (

                len(factcheck) > 30

                and

                "don't have enough"

                not in factcheck.lower()

            ):

                report = factcheck



            elif len(summary) > 30:

                report = summary




        if len(report) < 30:

            report = (

                "I don't have enough reliable "

                "information to answer this."

            )





    except Exception as e:


        print(

            "Report Agent Error:",

            e

        )



        if (

            len(factcheck) > 30

            and

            "don't have enough"

            not in factcheck.lower()

        ):

            report = factcheck


        elif len(summary) > 30:

            report = summary


        else:

            report = (

                "I don't have enough reliable "

                "information to answer this."

            )



    return {

        **state,

        "report": report,


        "agent_status": {

            **state.get(

                "agent_status",

                {}

            ),

            "report": "completed"

        }

    }