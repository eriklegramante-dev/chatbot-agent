"""
Módulo de Ferramentas (Tools) Matemáticas com Guardrails.
Contém as operações básicas protegidas contra argumentos inválidos (textos).
"""

def somar(a: float, b: float) -> float or str:
    """
    Soma dois números reais (a e b) e retorna o resultado.
    Regra: Ambos os argumentos devem ser números estritos.
    Use esta ferramenta quando o usuário pedir adição ou soma.
    """
    try:
        return float(float(a) + float(b))
    except (ValueError, TypeError):
        return "Erro: Argumentos inválidos. Esta ferramenta aceita apenas números reais, não textos."

def subtrair(a: float, b: float) -> float or str:
    """
    Subtrai o segundo número (b) do primeiro número (a) e retorna o resultado.
    Regra: Ambos os argumentos devem ser números estritos.
    Use esta ferramenta quando o usuário pedir subtração ou diferença.
    """
    try:
        return float(float(a) - float(b))
    except (ValueError, TypeError):
        return "Erro: Argumentos inválidos. Esta ferramenta aceita apenas números reais, não textos."

def multiplicar(a: float, b: float) -> float or str:
    """
    Multiplica dois números reais (a e b) e retorna o resultado.
    Regra: Ambos os argumentos devem ser números estritos.
    Use esta ferramenta quando o usuário pedir multiplicação ou produto.
    """
    try:
        return float(float(a) * float(b))
    except (ValueError, TypeError):
        return "Erro: Argumentos inválidos. Esta ferramenta aceita apenas números reais, não textos."

def dividir(a: float, b: float) -> float or str:
    """
    Divide o primeiro número (a) pelo segundo número (b) e retorna o resultado.
    Regras: Ambos os argumentos devem ser números estritos e 'b' não pode ser zero.
    Use esta ferramenta quando o usuário pedir divisão ou quociente.
    """
    try:
        num_a = float(a)
        num_b = float(b)
        if num_b == 0:
            return "Erro: Divisão por zero não é permitida."
        return float(num_a / num_b)
    except (ValueError, TypeError):
        return "Erro: Argumentos inválidos. Esta ferramenta aceita apenas números reais, não textos."