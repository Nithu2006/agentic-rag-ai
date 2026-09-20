from typing import List


def create_plan(query: str) -> List[str]:
    """
    Create a simple execution plan for the Agentic RAG system.
    """

    query = query.strip()

    plan = [
        "Analyze the user query",
        "Search the local knowledge base",
        "Evaluate the relevance of retrieved information",
        "Use web search if local information is insufficient",
        "Generate the final response",
    ]

    return plan