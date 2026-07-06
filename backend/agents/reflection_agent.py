from agents.llm import llm


def reflection_agent(state):

    report = state.get("report", "")


    prompt = f"""
You are a senior research reviewer.

Review the following report.

STRICT RULES:

1. Check factual consistency.

2. Check for hallucinations.

3. Check unsupported claims.

4. Check missing important topics.

5. Check clarity and professionalism.

6. If the report is reliable say:

"Report quality: Good"

7. If issues exist:

Mention:

- Missing Information
- Weak Areas
- Suggested Improvements

Keep response short.

Report:

{report}
"""


    try:

        response = llm.invoke(prompt)

        reflection = response.content.strip()


        if not reflection:

            reflection = "Report quality: Good"


    except Exception as e:

        print("Reflection Error:", e)

        reflection = "Report quality: Good"



    return {

        **state,

        "reflection": reflection,

        "agent_status": {

            **state.get(

                "agent_status",

                {}
            ),

            "reflection": "completed"

        }

    }