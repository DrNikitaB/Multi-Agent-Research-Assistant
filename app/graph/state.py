from typing import TypedDict, List, Optional


class SearchResult(TypedDict):
    title: str
    content: str
    url: str


class ExtractedContent(TypedDict):
    url: str
    raw_content: str


class Evidence(TypedDict):
    task: str
    source: str
    content: str


class ResearchState(TypedDict):

    query: str

    route: str

    file_path: Optional[str]

    pdf_text: str

    rewritten_query: str

    research_tasks: List[str]

    search_results: List[SearchResult]

    extracted_contents: List[ExtractedContent]

    vector_store_path: str

    retrieved_chunks: str
    
    evidence: List[Evidence]

    synthesis_context: str

    formatted_context: str

    final_answer: str

    # Verification Fields
    verification_status: str

    confidence_score: int

    critic_feedback: str