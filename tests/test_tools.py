import sys
import os

import pytest
from src.tools import somar, subtrair, multiplicar, dividir


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_soma_numeros_validos():
    assert somar(5, 4) == 9.0
    assert somar(-1, 1) == 0.0

def test_subtracao_numeros_validos():
    assert subtrair(10, 2) == 8.0

def test_multiplicacao_numeros_validos():
    assert multiplicar(3, 4) == 12.0

def test_divisao_valida_e_por_zero():
    assert dividir(10, 2) == 5.0
    assert "Erro: Divisão por zero" in dividir(5, 0)

def test_guardrail_inputs_invalidos_texto():
    erro_esperado = "Erro: Argumentos inválidos"
    
    assert erro_esperado in somar("5", "batata")
    assert erro_esperado in dividir("palavra", 2)