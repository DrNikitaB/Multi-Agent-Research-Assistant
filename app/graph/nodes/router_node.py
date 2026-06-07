from graph.state import ResearchState
from agents.classifier import classify_query
from graph.workflows import deep_research
from graph.workflows import simple_research
from graph.workflows import pdf_research
from core.logging import logger

def router_node(state):

    if state.get("file_path"):

        return {
            "route": "pdf"
        }

    route = classify_query(
        state["query"]
    )

    return {
        "route": route
    }

def route_decision(state):

    route = state["route"]

    if route == "pdf":
        return "pdf"

    if route in ["DEEP", "deep"]:
        return "deep"

    return "simple"


def simple_workflow_node(state):

    logger.info(
        "Simple Workflow Initiated !!"
    )

    result = simple_research.research_graph.invoke(
        {
            "query": state["query"]
        }
    )



    
    return result


def deep_workflow_node(state):

    logger.info(
        "Deep Workflow Initiated !!"
    )
    
    result = deep_research.research_graph.invoke(
        {
            "query": state["query"]
        }
    )


    return result

def pdf_workflow_node(state):

    result = pdf_research.research_graph.invoke(
        {
            "query": state["query"],
            "file_path": state["file_path"]
        }
    )

    return result