from pathlib import Path

from app.rag.document_loader import load_document
from app.rag.document_processor import clean_documents
from app.rag.chunker import split_documents
from app.rag.vector_store import create_vector_store


DOCUMENT_FOLDER = Path("data/documents")


def process_uploaded_document(file_path: str):
    """
    Process all documents in the document folder
    and rebuild the FAISS vector store.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    DOCUMENT_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    all_documents = []

    # Load every PDF/TXT file in the documents folder
    for document_file in DOCUMENT_FOLDER.iterdir():

        if document_file.suffix.lower() not in [
            ".pdf",
            ".txt"
        ]:
            continue

        try:

            documents = load_document(
                str(document_file)
            )

            documents = clean_documents(
                documents
            )

            all_documents.extend(
                documents
            )

        except Exception as error:

            print(
                f"Failed to process "
                f"{document_file.name}: {error}"
            )

    if not all_documents:
        raise ValueError(
            "No usable documents found."
        )

    # Create chunks from ALL documents
    chunks = split_documents(
        all_documents
    )

    if not chunks:
        raise ValueError(
            "No chunks were created."
        )

    # Rebuild FAISS using all documents
    create_vector_store(
        chunks
    )

    return {
        "filename": path.name,
        "documents_loaded": len(all_documents),
        "chunks_created": len(chunks),
        "total_documents": len([
            file
            for file in DOCUMENT_FOLDER.iterdir()
            if file.suffix.lower() in [
                ".pdf",
                ".txt"
            ]
        ]),
        "status": "success",
    }