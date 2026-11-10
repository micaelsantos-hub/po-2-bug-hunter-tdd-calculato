"""Testes da Calculadora Científica (framework unittest).

Executar a partir da pasta do repositório com:
    python -m unittest -v
ou, se o pytest estiver instalado:
    pytest -v
"""

import builtins
import contextlib
import io
import unittest
from unittest import mock

# BUG-12 (ainda não resolvido): Calculadora.py chama calculadora_cientifica()
# assim que é importado. Para importar as funções sem travar esperando o
# teclado, a entrada "0" (Sair) é simulada e a saída do menu é descartada.
with mock.patch.object(builtins, "input", return_value="0"), contextlib.redirect_stdout(io.StringIO()):
    import Calculadora as calc


class TestFatorial(unittest.TestCase):
    """BUG-03: o fatorial sempre retornava 0."""

    def test_fatorial_de_5_e_120(self):
        self.assertEqual(calc.fatorial(5), 120)

    def test_fatorial_de_0_e_1(self):
        self.assertEqual(calc.fatorial(0), 1)

    def test_fatorial_de_1_e_1(self):
        self.assertEqual(calc.fatorial(1), 1)

    def test_fatorial_de_10(self):
        self.assertEqual(calc.fatorial(10), 3628800)


class TestOperacoesQueJaFuncionam(unittest.TestCase):
    """Testes de regressão das funções que funcionam no código original.

    Garantem que a correção do BUG-03 não introduza novos defeitos.
    """

    def test_subtracao(self):
        self.assertEqual(calc.subtracao(10, 4), 6)

    def test_multiplicacao(self):
        self.assertEqual(calc.multiplicacao(3, 4), 12)

    def test_divisao(self):
        self.assertEqual(calc.divisao(10, 4), 2.5)

    def test_potencia(self):
        self.assertEqual(calc.potencia(2, 10), 1024)

    def test_raiz_quadrada(self):
        self.assertEqual(calc.raiz_quadrada(9), 3)


if __name__ == "__main__":
    unittest.main()
