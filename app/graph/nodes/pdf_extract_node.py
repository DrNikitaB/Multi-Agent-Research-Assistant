import fitz


def pdf_extract_node(state):

    pdf_path = state["file_path"]

    doc = fitz.open(pdf_path)

    text = ""

    for page in doc:
        text += page.get_text()

    return {
        "pdf_text": text
    }