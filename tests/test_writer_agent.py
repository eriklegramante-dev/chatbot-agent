from src.agents.writer import run_writer


def test_writer_formatting():
    response = run_writer("Quanto é 5 + 5?", "10")
    assert "10" in response
    assert len(response) <= 100
