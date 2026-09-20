from typing import List, Dict


def create_citations(
    documents: List[Dict],
) -> List[Dict]:
    """
    Create clean citations from verified documents.
    """

    citations = []

    for index, document in enumerate(
        documents,
        start=1
    ):
        metadata = document.get(
            "metadata",
            {}
        )

        source_type = document.get(
            "source_type",
            "unknown"
        )

        citation = {
            "id": index,
            "source_type": source_type,
            "title": metadata.get(
                "title",
                f"Source {index}"
            ),
            "url": metadata.get(
                "url",
                ""
            ),
            "verified": document.get(
                "verified",
                False
            ),
        }

        citations.append(citation)

    return citations