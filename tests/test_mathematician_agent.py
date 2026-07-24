from src.agents.mathematician import run_mathematician


def test_mathematician_direct_calculation():
    result = run_mathematician("Quanto é 5 + 5?")
    assert "10" in result


def test_mathematician_context_continuation():
    result = run_mathematician(
        "subtraia por 3", chat_history="User: 5 + 5\nAssistant: 10"
    )
    assert "7" in result
