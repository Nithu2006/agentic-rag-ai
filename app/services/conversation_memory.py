from typing import List, Dict


class ConversationMemory:
    """
    Simple in-memory conversation history.

    Stores user questions and AI responses
    during the current application session.
    """

    def __init__(self, max_messages: int = 10):
        self.messages: List[Dict[str, str]] = []
        self.max_messages = max_messages

    def add_message(
        self,
        role: str,
        content: str,
    ):
        """
        Add a message to conversation history.
        """

        self.messages.append(
            {
                "role": role,
                "content": content,
            }
        )

        # Keep only the latest messages
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[
                -self.max_messages:
            ]

    def get_history(self) -> List[Dict[str, str]]:
        """
        Return conversation history.
        """

        return self.messages.copy()

    def get_history_text(self) -> str:
        """
        Convert conversation history into
        text suitable for an LLM prompt.
        """

        if not self.messages:
            return ""

        history_parts = []

        for message in self.messages:

            role = message.get(
                "role",
                "unknown"
            )

            content = message.get(
                "content",
                ""
            )

            history_parts.append(
                f"{role}: {content}"
            )

        return "\n".join(
            history_parts
        )

    def clear(self):
        """
        Clear the conversation history.
        """

        self.messages.clear()


# Global conversation memory
conversation_memory = ConversationMemory()