from src.orchestrators.orchestrator import ChatbotOrchestrator
from src.memory.memory_manager import MemoryManager


def test_orchestrator_end_to_end_flow():
    memory = MemoryManager()
    orchestrator = ChatbotOrchestrator(memory_manager=memory)

    session_id = "test_e2e_session"

    response1 = orchestrator.process_message(
        session_id=session_id, user_message="Quanto é 5 + 5?"
    )
    assert "10" in response1

    response2 = orchestrator.process_message(
        session_id=session_id, user_message="subtraia por 3"
    )
    assert "7" in response2

    history = memory.get_formatted_history(session_id=session_id)
    assert "5 + 5" in history
    assert "subtraia por 3" in history
