import os
from datetime import datetime


def save_document(data: str):

    if not data or not str(data).strip():

        raise ValueError(
            "Cannot save empty content."
        )

    output_dir = "output"

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = (
        f"Research_Data_{timestamp}.md"
    )

    filepath = os.path.join(
        output_dir,
        filename
    )

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(data)

    return filepath