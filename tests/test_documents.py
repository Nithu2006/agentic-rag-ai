from langchain_core.documents import Document

from app.rag.document_processor import (
    clean_documents,
)

from app.rag.chunker import (
    split_documents,
)


def test_clean_documents():

    documents = [
        Document(
            page_content="   Machine   Learning   "
        ),
        Document(
            page_content="   "
        ),
    ]

    cleaned = clean_documents(
        documents
    )

    assert len(cleaned) == 1

    assert cleaned[0].page_content == (
        "Machine Learning"
    )


def test_split_documents():

    documents = [
        Document(
            page_content=(
                "Artificial intelligence is a field "
                "of computer science. "
                "Machine learning is a subset "
                "of artificial intelligence."
            )
        )
    ]

    chunks = split_documents(
        documents,
        chunk_size=50,
        chunk_overlap=10,
    )

    assert len(chunks) > 0

    assert "chunk_id" in (
        chunks[0].metadata
    )