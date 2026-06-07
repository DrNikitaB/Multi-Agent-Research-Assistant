from langgraph.graph import (
    StateGraph,
    END
)
from graph.state import ResearchState
from graph.nodes.router_node import (
    router_node,
    route_decision,
    simple_workflow_node,
    deep_workflow_node,
    pdf_workflow_node
)
graph = StateGraph(ResearchState)

graph.add_node(
    "router",
    router_node
)
graph.add_node(
    "pdf",
    pdf_workflow_node
)
graph.add_node(
    "simple",
    simple_workflow_node
)

graph.add_node(
    "deep",
    deep_workflow_node
)

graph.set_entry_point("router")

graph.add_conditional_edges(
    "router",
    route_decision,
    {
        "simple": "simple",
        "deep": "deep",
        "pdf": "pdf"
    }
)

graph.add_edge("simple", END)
graph.add_edge("deep", END)
graph.add_edge(
    "pdf",
    END
)
research_router = graph.compile()