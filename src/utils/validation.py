import re


def is_invalid_mixed_prompt(prompt: str) -> bool:
    """
    Fast-fail validation to detect invalid expressions mixing proper names,
    random words, or non-mathematical entities directly with arithmetic operators.

    Args:
        prompt (str): Raw input from the user.

    Returns:
        bool: True if the prompt is explicitly an invalid mixed expression, False otherwise.
    """
    clean_prompt = prompt.strip()

    if not re.search(r"[\+\*\/\=]", clean_prompt):
        return False

    tokens = re.findall(r"[a-zA-Zà-úÀ-Ú\u4e00-\u9fff]+", clean_prompt.lower())

    if not tokens:
        return False

    allowed_words = {
        "e",
        "é",
        "de",
        "do",
        "da",
        "por",
        "que",
        "qual",
        "o",
        "a",
        "os",
        "as",
        "is",
        "what",
        "the",
        "of",
        # Portuguese Math Terms
        "quanto",
        "quantos",
        "somar",
        "soma",
        "subtrair",
        "subtracao",
        "subtração",
        "multiplicar",
        "multiplicacao",
        "multiplicação",
        "dividir",
        "divisao",
        "divisão",
        "resultado",
        "raiz",
        "funcao",
        "função",
        "derivada",
        "calcule",
        "calcula",
        "considere",
        "valor",
        "exato",
        "igual",
        "equacao",
        "equação",
        "limite",
        "integral",
        "vezes",
        "mais",
        "menos",
        # English Math Terms
        "add",
        "addition",
        "subtract",
        "subtraction",
        "multiply",
        "multiplication",
        "divide",
        "division",
        "plus",
        "minus",
        "times",
        "equals",
        "calculate",
        "derivative",
        "find",
        "value",
        "solve",
        "equation",
        "root",
        "function",
        "sum",
        # CJK Math Terms
        "加",
        "減",
        "乘",
        "除",
        "等於",
        "多少",
        "加上",
        "減去",
        "乘以",
        "除以",
        "計算",
        "結果",
    }

    for token in tokens:
        if token not in allowed_words:
            return True

    return False
