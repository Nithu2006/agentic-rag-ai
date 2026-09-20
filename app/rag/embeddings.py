from fastembed import TextEmbedding


_model = None


def create_embeddings():
    """
    Create a local embedding model.
    No API key is required.
    """

    global _model

    if _model is None:
        _model = TextEmbedding(
            model_name="BAAI/bge-small-en-v1.5"
        )

    return _model


def embed_documents(texts):
    """
    Create embeddings for multiple documents.
    """

    model = create_embeddings()

    return [
        list(vector)
        for vector in model.embed(texts)
    ]


def embed_query(text):
    """
    Create an embedding for a user query.
    """

    model = create_embeddings()

    return list(
        model.embed([text])
    )[0]