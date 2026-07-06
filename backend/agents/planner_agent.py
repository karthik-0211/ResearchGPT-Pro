from agents.llm import llm


def planner_agent(state):

    query = state.get("query", "")

    history = state.get("history", [])

    history_str = ""

    if history:

        history_str = "Conversation History:\n" + "\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in history]) + "\n\n"



    prompt = f"""

You are an INTERNAL planner and query reformulator for ResearchGPT Pro.



VERY IMPORTANT:

- The user will NEVER see this output.

- Keep it structured as requested.

- No markdown formatting.



Your task:

1. Analyze the conversation history (if any) and the latest user query.

2. Formulate a single, standalone search query that captures the complete intent of the user's latest query, resolving any pronouns or implied context from the conversation history.

3. Understand the topic and extract concise planning notes.



{history_str}

Latest User Query:

{query}



Return your response in the following format:

SEARCH_QUERY: [standalone search query]

PLANNING_NOTES: [concise planning notes]

"""



    try:

        response = llm.invoke(prompt)

        content = response.content.strip()



        search_query = query

        plan = query



        if "SEARCH_QUERY:" in content and "PLANNING_NOTES:" in content:

            parts = content.split("PLANNING_NOTES:")

            search_part = parts[0].replace("SEARCH_QUERY:", "").strip()

            plan_part = parts[1].strip()

            if search_part:

                search_query = search_part

            if plan_part:

                plan = plan_part

        else:

            if "SEARCH_QUERY:" in content:

                search_query = content.split("SEARCH_QUERY:")[1].split("\n")[0].strip()

            if "PLANNING_NOTES:" in content:

                plan = content.split("PLANNING_NOTES:")[1].strip()



    except Exception as e:

        print("Planner Error:", e)

        search_query = query

        plan = query



    return {

        **state,

        "search_query": search_query,

        "plan": plan

    }