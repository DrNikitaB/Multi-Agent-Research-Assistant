from agents.researcher import llm


def pdf_answer_node(state):

    query = state["query"]

    context = state["retrieved_chunks"]

    prompt = f"""
You are a professional research assistant.

Answer the user's question naturally and conversationally.

Rules:
- Use ONLY the provided PDF context.
- Do not invent information.
- Do not mention 'based on the context' repeatedly.
- Answer in a clear and human-readable manner.
- If information is unavailable, reply exactly:

Information not found in uploaded PDF.

CONTEXT:
{context}

QUESTION:
{query}
"""

    response = llm.invoke(prompt)

    answer = ""

    # Standard LangChain/Gemini response
    if hasattr(response, "content"):

        if isinstance(response.content, str):

            answer = response.content

        elif isinstance(response.content, list):

            texts = []

            for item in response.content:

                if isinstance(item, dict):

                    if item.get("type") == "text":

                        texts.append(
                            item.get("text", "")
                        )

                else:

                    texts.append(
                        str(item)
                    )

            answer = "\n".join(texts)

    # Raw string response
    elif isinstance(response, str):

        answer = response

    # Fallback
    else:

        answer = str(response)

    return {
        "final_answer": answer.strip()
    }