from langgraph.graph import (
    StateGraph,
    END
)

from graph.state import ResearchState

from graph.nodes.pdf_embedding_node import pdf_embedding_node
from graph.nodes.pdf_retriever_node import pdf_retriever_node
from graph.nodes.pdf_answer_node import pdf_answer_node
from graph.nodes.verification_node import verification_node

graph = StateGraph(ResearchState)

graph.add_node(
    "pdf_embedding",
    pdf_embedding_node
)

graph.add_node(
    "pdf_retriever",
    pdf_retriever_node
)

graph.add_node(
    "pdf_answer",
    pdf_answer_node
)

graph.add_node(
    "verification_node",
    verification_node
)

graph.set_entry_point(
    "pdf_embedding"
)

graph.add_edge(
    "pdf_embedding",
    "pdf_retriever"
)

graph.add_edge(
    "pdf_retriever",
    "pdf_answer"
)

graph.add_edge(
    "pdf_answer",
    "verification_node"
)

graph.add_edge(
    "verification_node",
    END
)

research_graph = graph.compile()