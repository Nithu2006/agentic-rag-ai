from app.rag.reranker import (
    calculate_keyword_score,
    rerank_documents,
)


def test_keyword_score():

    query = "machine learning"

    document = (
        "Machine learning is a subset "
        "of artificial intelligence."
    )

    score = calculate_keyword_score(
        query,
        document
    )

    assert score > 0


def test_keyword_score_no_match():

    query = "quantum computing"

    document = (
        "Machine learning uses data "
        "to make predictions."
    )

    score = calculate_keyword_score(
        query,
        document
    )

    assert score == 0


def test_reranking():

    documents = [
        {
            "content": "Python is a programming language.",
            "distance": 0.8,
        },
        {
            "content": (
                "Machine learning is a subset "
                "of artificial intelligence."
            ),
            "distance": 0.2,
        },
    ]

    results = rerank_documents(
        "machine learning",
        documents
    )

    assert len(results) == 2

    assert results[0]["final_score"] >= (
        results[1]["final_score"]
    )