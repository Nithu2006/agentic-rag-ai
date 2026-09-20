from pathlib import Path
import pickle

import faiss
import numpy as np

from app.rag.embeddings import embed_documents


VECTOR_DB_PATH = Path("data/vector_db")

INDEX_FILE = VECTOR_DB_PATH / "faiss.index"
DOCUMENTS_FILE = VECTOR_DB_PATH / "documents.pkl"


def create_vector_store(documents):
    """
    Create a FAISS vector index and store document chunks.
    """

    VECTOR_DB_PATH.mkdir(
        parents=True,
        exist_ok=True
    )

    texts = []
    metadatas = []

    for document in documents:
        texts.append(document.page_content)

        metadata = document.metadata or {}

        clean_metadata = {
            str(key): str(value)
            for key, value in metadata.items()
        }

        metadatas.append(clean_metadata)

    if not texts:
        raise ValueError("No documents available to index.")

    vectors = embed_documents(texts)

    vectors = np.array(
        vectors,
        dtype="float32"
    )

    dimension = vectors.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(vectors)

    with open(DOCUMENTS_FILE, "wb") as file:
        pickle.dump(
            {
                "texts": texts,
                "metadatas": metadatas,
            },
            file
        )

    faiss.write_index(
        index,
        str(INDEX_FILE)
    )

    return index