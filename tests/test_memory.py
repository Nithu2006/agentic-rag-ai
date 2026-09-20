from app.services.conversation_memory import (
    ConversationMemory,
)


def test_add_message():

    memory = ConversationMemory()

    memory.add_message(
        "user",
        "What is machine learning?"
    )

    memory.add_message(
        "assistant",
        "Machine learning is a subset of AI."
    )

    history = memory.get_history()

    assert len(history) == 2

    assert history[0]["role"] == "user"

    assert history[1]["role"] == "assistant"


def test_history_text():

    memory = ConversationMemory()

    memory.add_message(
        "user",
        "What is AI?"
    )

    memory.add_message(
        "assistant",
        "AI is artificial intelligence."
    )

    history = memory.get_history_text()

    assert "user: What is AI?" in history

    assert (
        "assistant: AI is artificial intelligence."
        in history
    )


def test_clear_memory():

    memory = ConversationMemory()

    memory.add_message(
        "user",
        "Hello"
    )

    memory.clear()

    assert memory.get_history() == []