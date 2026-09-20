from typing import List

from langchain_core.documents import Document


def clean_documents(documents: List[Document]) -> List[Document]:
    """
    Clean document text and remove empty documents.
    """

    cleaned_documents = []

    for document in documents:
        text = document.page_content

        # Remove unnecessary whitespace
        text = " ".join(text.split())

        # Ignore empty documents
        if not text:
            continue

        document.page_content = text

        cleaned_documents.append(document)

    return cleaned_documents