import re
from typing import List, Dict


def tokenize(text: str) -> set:
    """
    Convert text into a set of normalized words.
    """

    words = re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text.lower()
    )

    return set(words)


def calculate_keyword_score(
    query: str,
    document: str,
) -> float:
    """
    Calculate keyword overlap between query and document.
    """

    query_words = tokenize(query)
    document_words = tokenize(document)

    if not query_words:
        return 0.0

    overlap = query_words.intersection(
        document_words
    )

    return len(overlap) / len(query_words)


def rerank_documents(
    query: str,
    documents: List[Dict],
) -> List[Dict]:
    """
    Rerank retrieved documents using
    semantic distance + keyword relevance.
    """

    if not documents:
        return []

    reranked = []

    for document in documents:

        distance = document.get(
            "distance",
            0.0
        )

        keyword_score = calculate_keyword_score(
            query,
            document["content"]
        )

        # Convert distance into a similarity-like score.
        semantic_score = 1 / (
            1 + max(distance, 0)
        )

        final_score = (
            0.7 * semantic_score
            + 0.3 * keyword_score
        )

        updated_document = document.copy()

        updated_document["semantic_score"] = (
            semantic_score
        )

        updated_document["keyword_score"] = (
            keyword_score
        )

        updated_document["final_score"] = (
            final_score
        )

        reranked.append(
            updated_document
        )

    reranked.sort(
        key=lambda item: item["final_score"],
        reverse=True
    )

    return reranked