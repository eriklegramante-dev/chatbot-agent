"""
Central orchestrator module responsible for routing messages and managing conversation state.
"""

from src.agents.mathematician import run_mathematician
from src.agents.writer import run_writer
from src.memory.memory_manager import MemoryManager


class ChatbotOrchestrator:
    """
    Coordinates interactions between Memory, Fast-Path rules, and CrewAI Agents.
    """

    GREETING_KEYWORDS = {
        "ola",
        "olá",
        "oi",
        "hello",
        "hey",
        "bom dia",
        "boa tarde",
        "boa noite",
    }

    def __init__(self, memory_manager: MemoryManager = None) -> None:
        """
        Initializes the orchestrator with a memory manager instance.
        """
        self.memory = memory_manager or MemoryManager()

    def process_message(self, session_id: str, user_message: str) -> str:
        """
        Processes an incoming user message, applies fast-path checks, invokes agents when needed,
        and manages conversation history per session.

        :param session_id: Unique identifier for the user session (from Next.js).
        :param user_message: The input message sent by the user.
        :return: Final string response to be returned to the frontend.
        """
        cleaned_prompt = user_message.strip().lower()

        if cleaned_prompt in self.GREETING_KEYWORDS:
            greeting_response = (
                "Olá! Sou seu assistente de matemática. Como posso te ajudar hoje?"
            )
            self._save_interaction(session_id, user_message, greeting_response)
            return greeting_response

        chat_history_str = self.memory.get_formatted_history(session_id)

        try:
            calc_result = run_mathematician(
                user_prompt=user_message, chat_history=chat_history_str
            )

            final_response = run_writer(
                user_prompt=user_message, calc_result=calc_result
            )

        except Exception as err:
            final_response = (
                "Desculpe, ocorreu um erro ao processar sua solicitação matemática."
            )

        self._save_interaction(session_id, user_message, final_response)

        return final_response

    def _save_interaction(
        self, session_id: str, user_message: str, assistant_response: str
    ) -> None:
        """
        Helper method to store user and assistant messages in session memory.
        """
        self.memory.add_user_message(session_id, user_message)
        self.memory.add_assistant_message(session_id, assistant_response)