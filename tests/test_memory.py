from src.memory.memory_manager import MemoryManager


def test_memory_formatting_and_limit():
    memory = MemoryManager(max_history_turns=2)

    memory.add_user_message("1 + 1")
    memory.add_assistant_message("2")

    formatted = memory.get_formatted_history()
    assert "User: 1 + 1" in formatted
    assert "Assistant: 2" in formatted

    memory.add_user_message("2 + 2")
    memory.add_assistant_message("4")
    memory.add_user_message("3 + 3")
    memory.add_assistant_message("6")

    assert "1 + 1" not in memory.get_formatted_history()
    assert "3 + 3" in memory.get_formatted_history()
