"""Script de reprodução dos defeitos registrados em Bugs.md.

Executa cada função da calculadora com as entradas descritas nos relatórios
e imprime o resultado esperado ao lado do resultado obtido (ou da exceção).

Uso (a partir da pasta raiz do repositório):
    python evidencias/reproduzir_bugs.py
"""

import builtins
import contextlib
import io
import os
import sys
import traceback
import warnings
from unittest import mock

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

LINHAS_DO_MENU = {
    "Bem-vindo à Calculadora Científica",
    "Escolha a operação que deseja realizar:",
}


def sem_menu(texto):
    """Remove as linhas do menu da saída capturada para facilitar a leitura."""
    linhas = []
    for linha in texto.splitlines():
        eh_item_do_menu = linha[:3].rstrip(". ").isdigit() and ". " in linha[:4]
        if linha in LINHAS_DO_MENU or eh_item_do_menu:
            continue
        linhas.append(linha)
    return linhas


def resumo_excecao(erro):
    return traceback.format_exception_only(type(erro), erro)[-1].strip()


# BUG-12: no código original a calculadora é executada assim que o módulo é
# importado. Para conseguir importar as funções, a entrada do usuário é
# simulada com "0" (opção "Sair").
saida_import = io.StringIO()
with mock.patch.object(builtins, "input", return_value="0"), contextlib.redirect_stdout(saida_import):
    import Calculadora as calc

print("[BUG-12] import Calculadora")
print("    Esperado: nenhuma saída e nenhuma leitura de teclado")
print(f"    Obtido:   o menu foi exibido ({len(saida_import.getvalue().splitlines())} linhas) "
      "e input() foi chamado; última linha: "
      f"{saida_import.getvalue().splitlines()[-1]!r}")
print()


def verificar(bug, chamada, esperado, funcao):
    print(f"[{bug}] {chamada}")
    print(f"    Esperado: {esperado}")
    with warnings.catch_warnings(record=True) as avisos:
        warnings.simplefilter("always")
        try:
            print(f"    Obtido:   {funcao()!r}")
        except Exception as erro:  # noqa: BLE001 - qualquer exceção é evidência
            print(f"    Obtido:   exceção -> {resumo_excecao(erro)}")
    for aviso in avisos:
        print(f"    Aviso:    {aviso.category.__name__}: {aviso.message}")
    print()


def verificar_menu(bug, entradas, descricao, esperado):
    print(f"[{bug}] Menu: {descricao} (entradas digitadas: {entradas})")
    print(f"    Esperado: {esperado}")
    saida = io.StringIO()
    erro_capturado = None
    with mock.patch.object(builtins, "input", side_effect=list(entradas)), contextlib.redirect_stdout(saida):
        try:
            calc.calculadora_cientifica()
        except Exception as erro:  # noqa: BLE001
            erro_capturado = erro
    for linha in sem_menu(saida.getvalue()):
        print(f"    Saída:    {linha}")
    if erro_capturado is not None:
        print(f"    Obtido:   exceção -> {resumo_excecao(erro_capturado)}")
    print()


verificar("BUG-01", "adicao(2, 3)", "5", lambda: calc.adicao(2, 3))
verificar("BUG-02", "divisao(10.0, 0.0)", "mensagem de erro tratada", lambda: calc.divisao(10.0, 0.0))
verificar("BUG-03", "fatorial(5)", "120", lambda: calc.fatorial(5))
verificar("BUG-03", "fatorial(0)", "1", lambda: calc.fatorial(0))
verificar("BUG-04", "fatorial(-3)", "erro: fatorial de número negativo", lambda: calc.fatorial(-3))
verificar("BUG-05", "logaritmo_natural(1)", "0.0", lambda: calc.logaritmo_natural(1))
verificar("BUG-06", "logaritmo_base10(100)", "2.0", lambda: calc.logaritmo_base10(100))
verificar("BUG-07", "logaritmo_base10(0)", "mensagem de erro: número não positivo", lambda: calc.logaritmo_base10(0))
verificar("BUG-14", "raiz_quadrada(-4) + 1", "erro sinalizado por exceção, não por texto",
          lambda: calc.raiz_quadrada(-4) + 1)

verificar_menu("BUG-08", ["10", "n"], "opção 10 (Seno)", "seno do ângulo informado")
verificar_menu("BUG-09", ["11", "0", "n"], "opção 11 (Cosseno), ângulo 0", "Resultado: 1.0")
verificar_menu("BUG-10", ["12", "45", "n"], "opção 12 (Tangente), ângulo 45", "Resultado: 1.0")
verificar_menu("BUG-11", ["1", "abc"], "opção 1 com texto no lugar do número",
               "mensagem pedindo um número válido")

# BUG-13: cada "s" em "Deseja realizar outra operação?" faz uma nova chamada
# recursiva. Depois de ~1000 operações a pilha do Python estoura.
entradas = ["99", "s"] * 1100
saida = io.StringIO()
print("[BUG-13] Menu: 1100 operações seguidas respondendo 's' para continuar")
print("    Esperado: a calculadora continua funcionando")
with mock.patch.object(builtins, "input", side_effect=entradas), contextlib.redirect_stdout(saida):
    try:
        calc.calculadora_cientifica()
        resultado = "sem erro"
    except RecursionError as erro:
        resultado = f"exceção -> {resumo_excecao(erro)}"
operacoes = saida.getvalue().count("Operação inválida")
print(f"    Obtido:   {resultado} (após {operacoes} operações)")
print()
