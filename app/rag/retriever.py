from pathlib import Path
import pickle

import faiss
import numpy as np

from app.rag.embeddings import embed_query
from app.rag.reranker import rerank_documents


VECTOR_DB_PATH = Path("data/vector_db")

INDEX_FILE = VECTOR_DB_PATH / "faiss.index"
DOCUMENTS_FILE = VECTOR_DB_PATH / "documents.pkl"


def retrieve_documents(
    query: str,
    top_k: int = 5,
):
    """
    Retrieve and rerank relevant document chunks.
    """

    if not INDEX_FILE.exists():
        raise FileNotFoundError(
            "FAISS index not found. Create the vector store first."
        )

    if not DOCUMENTS_FILE.exists():
        raise FileNotFoundError(
            "Document data not found. Create the vector store first."
        )

    index = faiss.read_index(
        str(INDEX_FILE)
    )

    with open(DOCUMENTS_FILE, "rb") as file:
        data = pickle.load(file)

    query_vector = embed_query(query)

    query_vector = np.array(
        [query_vector],
        dtype="float32"
    )

    number_to_retrieve = min(
        top_k,
        index.ntotal
    )

    distances, indices = index.search(
        query_vector,
        number_to_retrieve
    )

    results = []

    for distance, index_id in zip(
        distances[0],
        indices[0],
    ):
        if index_id == -1:
            continue

        results.append(
            {
                "content": data["texts"][index_id],
                "metadata": data["metadatas"][index_id],
                "distance": float(distance),
            }
        )

    return rerank_documents(
        query,
        results
    )