from graph.state import ResearchState
from tools.web_search import web_search

def search_node(state: ResearchState):

    results = web_search(state["rewritten_query"])

    return {
        "search_results": results
    }