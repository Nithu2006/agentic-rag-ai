import requests
from typing import Optional


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

OLLAMA_MODEL = "llama3.2:3b"


def generate_with_ollama(
    prompt: str,
    model: str = OLLAMA_MODEL,
) -> Optional[str]:
    """
    Generate a response using a locally running
    Ollama language model.
    """

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()

        return data.get(
            "response",
            ""
        ).strip()

    except requests.RequestException as error:

        print(
            f"Ollama request failed: {error}"
        )

        return None

    except Exception as error:

        print(
            f"LLM processing error: {error}"
        )

        return None


def generate_rag_response(
    query: str,
    context: str,
    conversation_history: str = "",
) -> Optional[str]:
    """
    Generate an answer using RAG context
    and previous conversation history.
    """

    if conversation_history:

        history_section = f"""
Previous Conversation:
----------------
{conversation_history}
----------------
"""

    else:

        history_section = """
Previous Conversation:
None
"""

    prompt = f"""
You are an AI assistant answering questions
using the provided context.

Use the retrieved context as your primary
source of information.

You may use the previous conversation to
understand references such as "it", "they",
"this", or follow-up questions.

Do not invent facts.

If the provided context does not contain
enough information to answer the question,
clearly state that the available information
is insufficient.

{history_section}

Retrieved Context:
----------------
{context}
----------------

Current User Question:
{query}

Answer:
"""

    return generate_with_ollama(
        prompt
    )