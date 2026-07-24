from src.memory.memory_manager import MemoryManager


def test_memory_formatting_and_limit():
    memory = MemoryManager(max_history_turns=2)
    session_id = "test_memory_session"

    memory.add_user_message(session_id, "1 + 1")
    memory.add_assistant_message(session_id, "2")

    formatted = memory.get_formatted_history(session_id)
    assert "User: 1 + 1" in formatted
    assert "Assistant: 2" in formatted

    memory.add_user_message(session_id, "2 + 2")
    memory.add_assistant_message(session_id, "4")
    memory.add_user_message(session_id, "3 + 3")
    memory.add_assistant_message(session_id, "6")

    history = memory.get_formatted_history(session_id)

    assert "1 + 1" not in history
    assert "3 + 3" in history
