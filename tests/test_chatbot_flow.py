"""
Integration tests for verifying agent memory, orchestration, and math flows.
"""

import pytest
from src.orchestrators.orchestrator import ChatbotOrchestrator


@pytest.fixture
def orchestrator() -> ChatbotOrchestrator:
    """
    Fixture providing a fresh instance of the chatbot orchestrator for tests.
    """
    return ChatbotOrchestrator()


def test_greeting_fast_path(orchestrator: ChatbotOrchestrator) -> None:
    """
    Tests if deterministic greeting inputs return an instant greeting response.
    """
    session_id = "test_session_1"
    response = orchestrator.process_message(session_id=session_id, user_message="Olá")

    assert "Olá" in response or "assistente" in response
    assert isinstance(response, str)


def test_direct_math_calculation(orchestrator: ChatbotOrchestrator) -> None:
    """
    Tests if a direct mathematical prompt correctly triggers tool execution and formatting.
    """
    session_id = "test_session_2"
    response = orchestrator.process_message(
        session_id=session_id, user_message="Quanto é 10 mais 5?"
    )

    assert "15" in response


def test_contextual_math_followup(orchestrator: ChatbotOrchestrator) -> None:
    """
    Tests if the agent correctly retains session history to perform follow-up operations.
    """
    session_id = "test_session_3"

    first_response = orchestrator.process_message(
        session_id=session_id, user_message="Quanto é 10 + 10?"
    )
    assert "20" in first_response

    second_response = orchestrator.process_message(
        session_id=session_id, user_message="Agora subtraia por 5"
    )
    assert "15" in second_response


def test_session_isolation(orchestrator: ChatbotOrchestrator) -> None:
    """
    Ensures that conversation history in User A does not bleed into User B session.
    """
    session_a = "user_a_session"
    session_b = "user_b_session"

    orchestrator.process_message(session_id=session_a, user_message="Quanto é 25 + 25?")

    response_b = orchestrator.process_message(
        session_id=session_b, user_message="Agora subtraia por 2"
    )

    assert "48" not in response_b
