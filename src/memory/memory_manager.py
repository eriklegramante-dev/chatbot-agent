"""
Session memory manager for storing and formatting multi-user conversation history.
"""

from typing import Dict, List


class MemoryManager:
    """
    In-memory session manager supporting multiple isolated user sessions.
    """

    def __init__(self, max_history_turns: int = 5) -> None:
        """
        Initializes the memory manager storage dictionary.

        :param max_history_turns: Maximum conversation turns (user + assistant pairs) to keep.
        """
        self._sessions: Dict[str, List[Dict[str, str]]] = {}
        self.max_history_turns = max_history_turns

    def add_user_message(self, session_id: str, message: str) -> None:
        """
        Adds a user message to a specific session history.

        :param session_id: Unique identifier for the user session.
        :param message: Raw text message content.
        """
        self._ensure_session_exists(session_id)
        self._sessions[session_id].append({"role": "user", "content": message.strip()})
        self._trim_history(session_id)

    def add_assistant_message(self, session_id: str, message: str) -> None:
        """
        Adds an assistant response to a specific session history.

        :param session_id: Unique identifier for the user session.
        :param message: Raw response content.
        """
        self._ensure_session_exists(session_id)
        self._sessions[session_id].append(
            {"role": "assistant", "content": message.strip()}
        )
        self._trim_history(session_id)

    def get_formatted_history(self, session_id: str) -> str:
        """
        Returns the formatted conversation history for the specified session.

        :param session_id: Unique identifier for the user session.
        :return: Formatted multiline string of conversation context.
        """
        history = self._sessions.get(session_id, [])
        if not history:
            return ""

        formatted_lines = []
        for msg in history:
            role = "User" if msg["role"] == "user" else "Assistant"
            formatted_lines.append(f"{role}: {msg['content']}")

        return "\n".join(formatted_lines)

    def clear(self, session_id: str) -> None:
        """
        Clears history for a specific session.

        :param session_id: Unique identifier for the user session.
        """
        if session_id in self._sessions:
            del self._sessions[session_id]

    def _ensure_session_exists(self, session_id: str) -> None:
        """
        Internal helper to initialize a new session list if absent.
        """
        if session_id not in self._sessions:
            self._sessions[session_id] = []

    def _trim_history(self, session_id: str) -> None:
        """
        Trims session history to retain only the last N conversation turns.
        """
        max_messages = self.max_history_turns * 2
        if len(self._sessions[session_id]) > max_messages:
            self._sessions[session_id] = self._sessions[session_id][-max_messages:]
