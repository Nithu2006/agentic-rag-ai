from typing import Dict, List


class ConversationMemory:
    """
    Simple in-memory conversation history.
    """

    def __init__(self):
        self.conversations: Dict[str, List[Dict]] = {}

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
    ):
        """
        Add a message to a conversation.
        """

        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []

        self.conversations[conversation_id].append(
            {
                "role": role,
                "content": content,
            }
        )

    def get_history(
        self,
        conversation_id: str,
    ) -> List[Dict]:
        """
        Return conversation history.
        """

        return self.conversations.get(
            conversation_id,
            []
        )

    def clear_history(
        self,
        conversation_id: str,
    ):
        """
        Clear a conversation.
        """

        if conversation_id in self.conversations:
            del self.conversations[conversation_id]


memory = ConversationMemory()