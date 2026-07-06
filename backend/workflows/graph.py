from langgraph.graph import StateGraph


from agents.planner_agent import planner_agent

from agents.researcher_agent import researcher_agent

from agents.pdf_agent import pdf_agent

from agents.summarizer_agent import summarizer_agent

from agents.factcheck_agent import factcheck_agent

from agents.report_agent import report_agent




# Shared state

workflow = StateGraph(dict)




# ---------------- Nodes ----------------


workflow.add_node(

    "planner",

    planner_agent

)



workflow.add_node(

    "researcher",

    researcher_agent

)



workflow.add_node(

    "pdf",

    pdf_agent

)



workflow.add_node(

    "summarizer",

    summarizer_agent

)



workflow.add_node(

    "factcheck",

    factcheck_agent

)



workflow.add_node(

    "report",

    report_agent

)




# ---------------- Flow ----------------


workflow.set_entry_point(

    "planner"

)




workflow.add_edge(

    "planner",

    "researcher"

)




workflow.add_edge(

    "researcher",

    "pdf"

)




workflow.add_edge(

    "pdf",

    "summarizer"

)




workflow.add_edge(

    "summarizer",

    "factcheck"

)




workflow.add_edge(

    "factcheck",

    "report"

)




# Final visible output

workflow.set_finish_point(

    "report"

)




graph = workflow.compile()