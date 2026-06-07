from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from core.settings import CHAT_MODEL_NAME

import json
import re

llm = ChatGoogleGenerativeAI(
    model=CHAT_MODEL_NAME,
    temperature=0
)

parser = StrOutputParser()


def verification_node(state):

    print("===== VERIFICATION NODE EXECUTED =====")

    answer = state.get("final_answer", "")

    context = ""

    if state.get("formatted_context"):
        context = state["formatted_context"]

    elif state.get("synthesis_context"):
        context = state["synthesis_context"]

    elif state.get("pdf_text"):
        context = state["pdf_text"][:30000]
    prompt = f"""
You are a fact verification agent.

CONTEXT:
{context}

ANSWER:
{answer}

Evaluate:

1. Is the answer supported by context?
2. Any hallucinated statements?
3. Any unsupported claims?

Return ONLY valid JSON.

Example:

{{
    "verification_status": "VERIFIED",
    "confidence_score": 95,
    "critic_feedback": "All major claims are supported."
}}
"""

    response = (llm | parser).invoke(prompt)

    print("VERIFICATION RAW RESPONSE:")
    print(response)

    try:

        json_match = re.search(
            r"\{.*\}",
            response,
            re.DOTALL
        )

        if json_match:

            result = json.loads(
                json_match.group()
            )

            print("VERIFICATION PARSED:")
            print(result)

            return {
                "verification_status": result.get(
                    "verification_status",
                    "UNKNOWN"
                ),
                "confidence_score": result.get(
                    "confidence_score",
                    0
                ),
                "critic_feedback": result.get(
                    "critic_feedback",
                    ""
                )
            }

    except Exception as e:

        print("VERIFICATION ERROR:")
        print(str(e))

    return {
        "verification_status": "UNKNOWN",
        "confidence_score": 0,
        "critic_feedback": "Verification parsing failed."
    }