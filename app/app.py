import streamlit as st
import tempfile
import os

from graph.workflows.research_router import research_router

# ---------------------------
# Page Config
# ---------------------------

st.set_page_config(
    page_title="Research Assistant",
    page_icon="🤖",
    layout="wide"
)

# ---------------------------
# Custom Styling
# ---------------------------

st.markdown("""
<style>

.block-container {
    padding-top: 1rem;
}

[data-testid="stSidebar"] {
    background-color: #202123;
}

[data-testid="stSidebar"] * {
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# Session State
# ---------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_path" not in st.session_state:
    st.session_state.pdf_path = None

if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None

# ---------------------------
# Sidebar
# ---------------------------

with st.sidebar:

    st.title("🤖 Research Assistant")

    uploaded_pdf = st.file_uploader(
        "📄 Upload PDF",
        type=["pdf"]
    )

    if uploaded_pdf:

        temp_dir = tempfile.gettempdir()

        pdf_path = os.path.join(
            temp_dir,
            uploaded_pdf.name
        )

        with open(pdf_path, "wb") as f:
            f.write(uploaded_pdf.getbuffer())

        st.session_state.pdf_path = pdf_path
        st.session_state.pdf_name = uploaded_pdf.name

        st.success(
            f"Loaded: {uploaded_pdf.name}"
        )

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []

        st.rerun()

# ---------------------------
# Header
# ---------------------------

st.title("🤖 Research Assistant")

if st.session_state.pdf_name:

    st.info(
        f"📄 Active PDF: {st.session_state.pdf_name}"
    )

# ---------------------------
# Display Chat History
# ---------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ---------------------------
# Chat Input
# ---------------------------

prompt = st.chat_input(
    "Ask anything..."
)

# ---------------------------
# Process Query
# ---------------------------

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Researching..."):

            try:

                response = research_router.invoke(
                    {
                        "query": prompt,
                        "file_path": st.session_state.pdf_path
                    }
                )

                answer = response.get(
                    "final_answer",
                    "No answer generated."
                )

                if isinstance(answer, list):
                    answer = str(answer)

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

                st.markdown(answer)

                with st.expander(
                    "🔍 Quality Check"
                ):

                    st.metric(
                        "Confidence",
                        f"{confidence}%"
                    )

                    st.metric(
                        "Verification",
                        verification
                    )

                    if feedback:
                        st.write(feedback)

                if st.session_state.pdf_path:

                    st.success(
                        "PDF Mode Used (No Web Search)"
                    )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:

                st.error(str(e))