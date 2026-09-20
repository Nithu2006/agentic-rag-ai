import re
from typing import List, Dict


def tokenize(text: str) -> set:
    """
    Convert text into normalized words.
    """

    words = re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text.lower()
    )

    # Remove very common words
    stop_words = {
        "the",
        "is",
        "a",
        "an",
        "and",
        "or",
        "of",
        "to",
        "in",
        "on",
        "for",
        "with",
        "what",
        "how",
        "why",
        "are",
        "was",
        "were",
        "this",
        "that",
    }

    return {
        word
        for word in words
        if word not in stop_words
    }


def calculate_support_score(
    answer: str,
    evidence: str,
) -> float:
    """
    Measure how much of the answer is supported
    by the available evidence.

    This is a lightweight verification method,
    not a full semantic fact checker.
    """

    answer_words = tokenize(answer)
    evidence_words = tokenize(evidence)

    if not answer_words:
        return 0.0

    supported_words = (
        answer_words.intersection(
            evidence_words
        )
    )

    return len(supported_words) / len(
        answer_words
    )


def verify_answer(
    answer: str,
    retrieved_documents: List[Dict],
    web_results: List[Dict],
) -> Dict:
    """
    Verification Agent.

    Checks whether the generated answer has
    textual support in local or web evidence.
    """

    evidence_parts = []

    # -----------------------------------------
    # LOCAL DOCUMENT EVIDENCE
    # -----------------------------------------

    for document in retrieved_documents:

        content = document.get(
            "content",
            ""
        )

        if content:
            evidence_parts.append(
                content
            )

    # -----------------------------------------
    # WEB EVIDENCE
    # -----------------------------------------

    for result in web_results:

        snippet = result.get(
            "snippet",
            ""
        )

        if snippet:
            evidence_parts.append(
                snippet
            )

    evidence = " ".join(
        evidence_parts
    )

    # -----------------------------------------
    # CALCULATE SUPPORT
    # -----------------------------------------

    support_score = calculate_support_score(
        answer,
        evidence
    )

    # -----------------------------------------
    # VERIFICATION STATUS
    # -----------------------------------------

    if support_score >= 0.50:

        status = "verified"

    elif support_score >= 0.25:

        status = "partially_verified"

    else:

        status = "low_support"

    return {
        "status": status,
        "support_score": round(
            support_score,
            3
        ),
        "evidence_available": bool(
            evidence.strip()
        ),
        "evidence_count": len(
            evidence_parts
        ),
    }