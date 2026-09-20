from app.rag.retriever import retrieve_documents


def run_retrieval(
    query: str,
    top_k: int = 5,
):
    """
    Retrieval Agent.

    Searches the local FAISS knowledge base
    and returns relevant documents.
    """

    try:

        documents = retrieve_documents(
            query=query,
            top_k=top_k,
        )

        return documents

    except FileNotFoundError:

        return []

    except Exception as error:

        print(
            f"Retrieval error: {error}"
        )

        return []