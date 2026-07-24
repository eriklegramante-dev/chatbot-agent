from src.utils.validation import is_invalid_mixed_prompt


def test_validation_guardrails():
    assert is_invalid_mixed_prompt("1 + 1") == False
    assert is_invalid_mixed_prompt("Quanto é 5 + 4?") == False

    # Deve bloquear nomes próprios misturados com matemática
    assert is_invalid_mixed_prompt("Neymar + 10") == True
    assert is_invalid_mixed_prompt("內馬爾 + 45") == True
