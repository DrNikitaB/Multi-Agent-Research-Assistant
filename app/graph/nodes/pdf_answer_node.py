from agents.researcher import llm


def pdf_answer_node(state):

    query = state["query"]

    context = state["retrieved_chunks"]

    prompt = f"""
You are a PDF Research Assistant.

Answer ONLY using provided context.

If answer does not exist in context say:

Information not found in uploaded PDF.

CONTEXT:
{context}

QUESTION:
{query}
"""

    response = llm.invoke(prompt)

    answer = getattr(
        response,
        "content",
        str(response)
    )

    return {
        "final_answer": answer
    }