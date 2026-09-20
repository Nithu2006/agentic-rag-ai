from typing import List, Dict


def calculate_retrieval_metrics(
    retrieved_documents: List[Dict],
) -> Dict:
    """
    Calculate basic retrieval metrics.
    """

    total_documents = len(
        retrieved_documents
    )

    if total_documents == 0:
        return {
            "documents_retrieved": 0,
            "average_score": 0.0,
            "retrieval_quality": 0.0,
        }

    scores = []

    for document in retrieved_documents:
        score = document.get(
            "final_score",
            0.0
        )

        scores.append(score)

    average_score = sum(scores) / len(scores)

    return {
        "documents_retrieved": total_documents,
        "average_score": round(
            average_score,
            4
        ),
        "retrieval_quality": round(
            min(average_score, 1.0),
            4
        ),
    }


def calculate_response_metrics(
    answer: str,
    confidence: float,
) -> Dict:
    """
    Calculate basic response metrics.
    """

    answer_length = len(
        answer.strip()
    ) if answer else 0

    return {
        "answer_length": answer_length,
        "confidence": round(
            confidence,
            4
        ),
        "has_answer": bool(
            answer and answer.strip()
        ),
    }


def evaluate_pipeline(
    retrieved_documents: List[Dict],
    answer: str,
    confidence: float,
) -> Dict:
    """
    Evaluate the complete RAG response.
    """

    retrieval_metrics = (
        calculate_retrieval_metrics(
            retrieved_documents
        )
    )

    response_metrics = (
        calculate_response_metrics(
            answer,
            confidence
        )
    )

    return {
        "retrieval": retrieval_metrics,
        "response": response_metrics,
    }