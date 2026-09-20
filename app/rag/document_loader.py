from pathlib import Path
from typing import List

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
)


def load_document(file_path: str):
    """
    Load a PDF or TXT document and return LangChain documents.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    extension = path.suffix.lower()

    if extension == ".pdf":
        loader = PyPDFLoader(str(path))

    elif extension == ".txt":
        loader = TextLoader(
            str(path),
            encoding="utf-8"
        )

    else:
        raise ValueError(
            f"Unsupported file type: {extension}. "
            "Currently supported: .pdf and .txt"
        )

    documents = loader.load()

    return documents


def load_documents(folder_path: str) -> List:
    """
    Load all supported documents from a folder.
    """

    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(
            f"Folder not found: {folder_path}"
        )

    documents = []

    for file_path in folder.iterdir():

        if file_path.suffix.lower() in [".pdf", ".txt"]:

            try:
                loaded_documents = load_document(
                    str(file_path)
                )

                documents.extend(loaded_documents)

                print(
                    f"Loaded: {file_path.name} "
                    f"({len(loaded_documents)} pages/documents)"
                )

            except Exception as error:
                print(
                    f"Failed to load {file_path.name}: {error}"
                )

    return documents