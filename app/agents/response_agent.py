from typing import List, Dict

from app.services.llm_service import generate_rag_response
from app.services.conversation_memory import (
    conversation_memory
)


def build_context(
    retrieved_documents: List[Dict],
    web_results: List[Dict],
) -> str:
    """
    Build the context that will be provided
    to the local LLM.
    """

    context_parts = []

    # -----------------------------------------
    # LOCAL RAG DOCUMENTS
    # -----------------------------------------

    for index, document in enumerate(
        retrieved_documents,
        start=1
    ):

        content = document.get(
            "content",
            ""
        )

        if content:

            context_parts.append(
                f"[Local Source {index}]\n"
                f"{content}"
            )

    # -----------------------------------------
    # WEB SEARCH RESULTS
    # -----------------------------------------

    for index, result in enumerate(
        web_results,
        start=1
    ):

        title = result.get(
            "title",
            "Web Source"
        )

        snippet = result.get(
            "snippet",
            ""
        )

        if snippet:

            context_parts.append(
                f"[Web Source {index}: {title}]\n"
                f"{snippet}"
            )

    return "\n\n".join(
        context_parts
    )


def create_citations(
    retrieved_documents: List[Dict],
    web_results: List[Dict],
) -> List[Dict]:
    """
    Create citations from local and web sources.
    """

    citations = []

    # -----------------------------------------
    # LOCAL SOURCES
    # -----------------------------------------

    for document in retrieved_documents:

        metadata = document.get(
            "metadata",
            {}
        )

        source = metadata.get(
            "source",
            "Local document"
        )

        citations.append(
            {
                "title": str(source),
                "url": "",
            }
        )

    # -----------------------------------------
    # WEB SOURCES
    # -----------------------------------------

    for result in web_results:

        citations.append(
            {
                "title": result.get(
                    "title",
                    "Web Source"
                ),
                "url": result.get(
                    "url",
                    ""
                ),
            }
        )

    return citations


def generate_response(
    query: str,
    retrieved_documents: List[Dict],
    web_results: List[Dict],
):
    """
    Response Agent.

    Uses retrieved evidence as context and
    generates a natural-language answer using
    the local Ollama LLM.

    Conversation memory is also provided to
    the LLM so that follow-up questions can
    use previous conversation context.
    """

    # -----------------------------------------
    # BUILD CONTEXT
    # -----------------------------------------

    context = build_context(
        retrieved_documents,
        web_results,
    )

    # -----------------------------------------
    # NO INFORMATION
    # -----------------------------------------

    if not context.strip():

        return {
            "query": query,
            "plan": [
                "Analyze the user query",
                "Search the local knowledge base",
                "Attempt web search",
                "No relevant information found",
            ],
            "retrieved_documents": [],
            "web_results": [],
            "answer": (
                "I could not find relevant information "
                "in the available knowledge sources."
            ),
            "confidence": 0.0,
            "citations": [],
        }

    # -----------------------------------------
    # GET CONVERSATION HISTORY
    # -----------------------------------------

    conversation_history = (
        conversation_memory.get_history_text()
    )

    # -----------------------------------------
    # GENERATE LLM ANSWER
    # -----------------------------------------

    answer = generate_rag_response(
        query=query,
        context=context,
        conversation_history=conversation_history,
    )

    # -----------------------------------------
    # LLM FAILURE FALLBACK
    # -----------------------------------------

    if not answer:

        if retrieved_documents:

            answer = retrieved_documents[0].get(
                "content",
                "No relevant information found."
            )

        elif web_results:

            answer = web_results[0].get(
                "snippet",
                "No useful web information found."
            )

        else:

            answer = (
                "I could not generate an answer "
                "from the available information."
            )

    # -----------------------------------------
    # STORE CONVERSATION
    # -----------------------------------------

    conversation_memory.add_message(
        role="user",
        content=query,
    )

    conversation_memory.add_message(
        role="assistant",
        content=answer,
    )

    # -----------------------------------------
    # CREATE CITATIONS
    # -----------------------------------------

    citations = create_citations(
        retrieved_documents,
        web_results,
    )

    # -----------------------------------------
    # CALCULATE CONFIDENCE
    # -----------------------------------------

    if retrieved_documents:

        best_score = float(
            retrieved_documents[0].get(
                "final_score",
                0.0
            )
        )

        confidence = min(
            0.95,
            max(
                0.40,
                best_score
            )
        )

    elif web_results:

        confidence = 0.60

    else:

        confidence = 0.0

    # -----------------------------------------
    # RETURN RESPONSE
    # -----------------------------------------

    return {
        "query": query,
        "plan": [
            "Analyze the user query",
            "Retrieve relevant information",
            "Rerank retrieved information",
            "Build evidence context",
            "Retrieve conversation history",
            "Generate response using local LLM",
            "Store conversation memory",
            "Verify the generated answer",
        ],
        "retrieved_documents": retrieved_documents,
        "web_results": web_results,
        "answer": answer,
        "confidence": confidence,
        "citations": citations,
    }