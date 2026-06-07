import chainlit as cl

from graph.workflows.research_router import research_router

pdf_path = None


@cl.on_chat_start
async def start():

    await cl.Message(
        content="""
# 🤖 Research Assistant

Upload a PDF or ask any question.
"""
    ).send()


@cl.on_message
async def main(message: cl.Message):

    global pdf_path

    if message.elements:

        for element in message.elements:

            if element.mime == "application/pdf":

                pdf_path = element.path

                await cl.Message(
                    content=f"📄 PDF Loaded: {element.name}"
                ).send()

                return

    response = research_router.invoke(
        {
            "query": message.content,
            "file_path": pdf_path
        }
    )

    answer = response.get(
        "final_answer",
        "No answer generated."
    )

    verification = response.get(
        "verification_status",
        "UNKNOWN"
    )

    confidence = response.get(
        "confidence_score",
        0
    )

    feedback = response.get(
        "critic_feedback",
        ""
    )

    final_response = f"""
{answer}

---

### Quality Check

**Verification:** {verification}

**Confidence:** {confidence}%

**Reviewer Notes:** {feedback}
"""

    await cl.Message(
        content=final_response
    ).send()