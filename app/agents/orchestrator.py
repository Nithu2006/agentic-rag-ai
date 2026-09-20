from app.agents.web_search_agent import run_web_search
from app.agents.retrieval_agent import run_retrieval
from app.agents.planner_agent import create_plan
from app.agents.response_agent import generate_response
from app.agents.verification_agent import verify_answer


def run_agent_pipeline(query: str):
    """
    Main Agentic RAG pipeline.

    Flow:

    User Query
        ↓
    Planner Agent
        ↓
    Local Retrieval Agent
        ↓
    Check Relevance
        ↓
    Web Search Agent (if needed)
        ↓
    Response Agent
        ↓
    Verification Agent
        ↓
    Final Response
    """

    # ==================================================
    # STEP 1: PLANNER AGENT
    # ==================================================

    plan = create_plan(
        query
    )


    # ==================================================
    # STEP 2: LOCAL RETRIEVAL AGENT
    # ==================================================

    retrieved_documents = run_retrieval(
        query
    )


    # ==================================================
    # STEP 3: CHECK LOCAL RETRIEVAL
    # ==================================================

    use_web_search = False

    if not retrieved_documents:

        use_web_search = True

    else:

        useful_documents = [
            document
            for document in retrieved_documents
            if document.get(
                "final_score",
                0
            ) > 0.10
        ]

        if not useful_documents:

            use_web_search = True


    # ==================================================
    # STEP 4: WEB SEARCH FALLBACK
    # ==================================================

    web_results = []

    if use_web_search:

        web_response = run_web_search(
            query
        )

        web_results = web_response.get(
            "results",
            []
        )


    # ==================================================
    # STEP 5: RESPONSE AGENT
    # ==================================================

    response = generate_response(
        query=query,
        retrieved_documents=retrieved_documents,
        web_results=web_results,
    )


    # ==================================================
    # STEP 6: VERIFICATION AGENT
    # ==================================================

    verification = verify_answer(
        answer=response.get(
            "answer",
            ""
        ),
        retrieved_documents=retrieved_documents,
        web_results=web_results,
    )


    # ==================================================
    # STEP 7: CALCULATE FINAL CONFIDENCE
    # ==================================================

    original_confidence = float(
        response.get(
            "confidence",
            0.0
        )
    )

    verification_score = float(
        verification.get(
            "support_score",
            0.0
        )
    )

    final_confidence = (
        0.6 * original_confidence
        + 0.4 * verification_score
    )


    # ==================================================
    # STEP 8: UPDATE RESPONSE
    # ==================================================

    response["plan"] = plan

    response["verification"] = verification

    response["confidence"] = round(
        final_confidence,
        3
    )


    # ==================================================
    # STEP 9: RETURN FINAL PIPELINE STATE
    # ==================================================

    return response