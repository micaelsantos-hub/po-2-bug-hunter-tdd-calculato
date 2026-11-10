# Relatório de Bugs: Calculadora Científica (`Calculadora.py`)

**Responsável pela análise:** Micael Araujo Souza Santos
**Data da análise:** 07/11/2026
**Arquivo analisado:** `Calculadora.py` (versão original, primeiro commit do repositório)

## Contexto geral (vale para todos os bugs)

| Item | Valor |
|---|---|
| Sistema operacional | Windows 11 Home 10.0.26200 |
| Python | 3.14.4 |
| NumPy | 2.5.3 |
| Forma de execução | `python Calculadora.py` no terminal (menu interativo) ou chamada direta das funções |
| Script de reprodução | `evidencias/reproduzir_bugs.py` |
| Saída do script | `evidencias/saida_reproducao.txt` |
| Tracebacks reais do programa | `evidencias/tracebacks.txt` |

Para reproduzir todos os bugs de uma vez, a partir da pasta do repositório:

```bash
python evidencias/reproduzir_bugs.py
```

## Resumo

| ID | Título | Localização | Severidade | Status |
|---|---|---|---|---|
| BUG-01 | Adição soma o primeiro número duas vezes | `adicao`, linha 4 | Crítico | Não resolvido |
| BUG-02 | Divisão por zero encerra o programa | `divisao`, linha 13 | Alto | Não resolvido |
| BUG-03 | Fatorial sempre retorna 0 | `fatorial`, linha 25 | Crítico | Em análise (escolhido para TDD) |
| BUG-04 | Fatorial de número negativo retorna 1 | `fatorial`, linhas 23 a 27 | Médio | Não resolvido |
| BUG-05 | Logaritmo natural usa função inexistente `np.ln` | `logaritmo_natural`, linha 32 | Crítico | Não resolvido |
| BUG-06 | Logaritmo base 10 calcula o logaritmo natural | `logaritmo_base10`, linha 37 | Alto | Não resolvido |
| BUG-07 | Logaritmo base 10 aceita zero e retorna `-inf` | `logaritmo_base10`, linha 35 | Médio | Não resolvido |
| BUG-08 | Opção 10 (Seno) não está implementada | `calculadora_cientifica`, linhas 93 a 102 | Alto | Não resolvido |
| BUG-09 | Opção 11 (Cosseno) chama função inexistente | `calculadora_cientifica`, linha 95 | Crítico | Não resolvido |
| BUG-10 | Opção 12 (Tangente) chama função inexistente | `calculadora_cientifica`, linha 99 | Crítico | Não resolvido |
| BUG-11 | Entrada não numérica encerra o programa | `calculadora_cientifica`, linhas 64, 65, 78, 82, 86, 90, 94 e 98 | Médio | Não resolvido |
| BUG-12 | Calculadora é executada ao importar o módulo | linha 108 | Médio | Não resolvido |
| BUG-13 | Repetir operações estoura a pilha (recursão) | `calculadora_cientifica`, linha 106 | Baixo | Não resolvido |
| BUG-14 | Erros retornados como texto no lugar do número | `raiz_quadrada`, `logaritmo_natural` e `logaritmo_base10`, linhas 20, 31 e 36 | Baixo | Não resolvido |

Critério de severidade usado:

- **Crítico:** a operação nunca dá o resultado certo ou sempre derruba o programa.
- **Alto:** o resultado é errado ou o programa cai em casos comuns.
- **Médio:** a falha só acontece em entradas de borda ou inválidas.
- **Baixo:** problema de projeto ou de manutenção, sem efeito no uso normal.

---

## BUG-01: Adição soma o primeiro número duas vezes

### Identificação do Bug
- **Título:** Adição soma o primeiro número duas vezes
- **Localização:** `Calculadora.py`, função `adicao`, linha 4

### Descrição Detalhada
- **Descrição clara do bug:** a função faz `x + np.add(x, y)`. Como `np.add(x, y)` já é `x + y`, o resultado final é `2x + y`. Toda adição feita na calculadora sai errada, a não ser quando o primeiro número é 0.
- **Contexto:** ver o contexto geral. O bug não depende de ambiente, porque é um erro de lógica.

### Passos para Reproduzir
1. Executar `python Calculadora.py`.
2. Digitar `1` (Adição).
3. Digitar `2` como primeiro número.
4. Digitar `3` como segundo número.

Também dá para reproduzir chamando `adicao(2, 3)` direto.

- **Consistência:** ocorre sempre.

### Resultado Esperado vs. Obtido
- **Esperado:** `Resultado: 5.0`
- **Obtido:** `Resultado: 7.0` (`2*2 + 3`)

### Evidências
- `evidencias/saida_reproducao.txt`, bloco `[BUG-01]`: `adicao(2, 3)` retorna `np.int64(7)`.
- **Screenshot:** `evidencias/img/bug01_adicao.png` *(captura do terminal com os passos acima)*

### Severidade e Impacto
- **Severidade:** Crítico
- **Impacto:** a operação mais básica da calculadora dá resultado errado sem nenhum aviso. O usuário não tem como perceber o erro e pode usar o valor incorreto.

### Sugestões para Correção
- Trocar por `return x + y` (ou `return np.add(x, y)`).

### Registro e Acompanhamento
- **Data de identificação:** 07/11/2026
- **Status:** Não resolvido

---

## BUG-02: Divisão por zero encerra o programa

### Identificação do Bug
- **Título:** Divisão por zero encerra o programa com `ZeroDivisionError`
- **Localização:** `Calculadora.py`, função `divisao`, linha 13

### Descrição Detalhada
- **Descrição clara do bug:** a função faz `x / y` sem verificar se `y` é zero. Como o menu converte as entradas para `float`, dividir por 0 levanta `ZeroDivisionError`. A exceção não é tratada e o programa termina. As outras funções (raiz, logaritmo) tratam entradas inválidas com uma mensagem, mas a divisão não.
- **Contexto:** ver o contexto geral.

### Passos para Reproduzir
1. Executar `python Calculadora.py`.
2. Digitar `4` (Divisão).
3. Digitar `10` como primeiro número.
4. Digitar `0` como segundo número.

- **Consistência:** ocorre sempre que o divisor é 0.

### Resultado Esperado vs. Obtido
- **Esperado:** uma mensagem como `Erro: Divisão por zero`, e a calculadora continua funcionando.
- **Obtido:** o programa fecha com o traceback abaixo.

### Evidências
- **Log de erro** (`evidencias/tracebacks.txt`):

```text
  File "Calculadora.py", line 13, in divisao
    return x / y
           ~~^~~
ZeroDivisionError: division by zero
```

- **Screenshot:** `evidencias/img/bug02_divisao.png`

### Severidade e Impacto
- **Severidade:** Alto
- **Impacto:** um erro de digitação comum derruba a aplicação inteira, e o usuário perde a sessão.

### Sugestões para Correção
- Verificar `if y == 0` antes de dividir e retornar ou levantar um erro tratado pelo menu.

### Registro e Acompanhamento
- **Data de identificação:** 07/11/2026
- **Status:** Não resolvido

---

## BUG-03: Fatorial sempre retorna 0

### Identificação do Bug
- **Título:** Fatorial sempre retorna 0
- **Localização:** `Calculadora.py`, função `fatorial`, linha 25 (`for i in range(x+1):`)

### Descrição Detalhada
- **Descrição clara do bug:** o laço `range(x+1)` começa em `i = 0`. Na primeira iteração, `fat *= 0` zera o acumulador, e a partir daí qualquer multiplicação continua dando 0. Com isso, o fatorial de qualquer número não negativo sai 0, inclusive `0!`, que deveria ser 1.
- **Contexto:** ver o contexto geral. É um erro de lógica (*off-by-one* no início do intervalo).

### Passos para Reproduzir
1. Executar `python Calculadora.py`.
2. Digitar `7` (Fatorial).
3. Digitar `5`.

Repetir com `0`.

- **Consistência:** ocorre sempre, para qualquer `x >= 0`.

### Resultado Esperado vs. Obtido
- **Esperado:** `Resultado: 120` para 5, e `Resultado: 1` para 0.
- **Obtido:** `Resultado: 0` nos dois casos.

### Evidências
- `evidencias/saida_reproducao.txt`, blocos `[BUG-03]`: `fatorial(5)` retorna `0` e `fatorial(0)` retorna `0`.
- **Screenshot:** `evidencias/img/bug03_fatorial.png`

### Severidade e Impacto
- **Severidade:** Crítico
- **Impacto:** a funcionalidade de fatorial é inútil, porque nunca retorna o valor correto.

### Sugestões para Correção
- Iniciar o laço em 1: `range(1, x + 1)`.

### Registro e Acompanhamento
- **Data de identificação:** 07/11/2026
- **Status:** Em análise. Este bug foi escolhido para ser corrigido com TDD.

---

## BUG-04: Fatorial de número negativo retorna 1

### Identificação do Bug
- **Título:** Fatorial de número negativo retorna 1 em vez de erro
- **Localização:** `Calculadora.py`, função `fatorial`, linhas 23 a 27

### Descrição Detalhada
- **Descrição clara do bug:** o fatorial não é definido para números negativos. Com `x` negativo, `range(x+1)` fica vazio, o laço não executa e a função devolve o valor inicial `1`. O usuário recebe um número como se a operação fosse válida, sem nenhum aviso.
- **Contexto:** ver o contexto geral. Esse defeito é independente do BUG-03 e continua existindo depois da correção do BUG-03.

### Passos para Reproduzir
1. Executar `python Calculadora.py`.
2. Digitar `7` (Fatorial).
3. Digitar `-3`.

- **Consistência:** ocorre sempre, para qualquer inteiro negativo.

### Resultado Esperado vs. Obtido
- **Esperado:** uma mensagem de erro, como `Erro: Fatorial de número negativo`.
- **Obtido:** `Resultado: 1`

### Evidências
- `evidencias/saida_reproducao.txt`, bloco `[BUG-04]`: `fatorial(-3)` retorna `1`.

### Severidade e Impacto
- **Severidade:** Médio
- **Impacto:** a calculadora devolve um resultado matematicamente inválido para uma entrada fora do domínio.

### Sugestões para Correção
- No início da função, levantar `ValueError` (ou retornar uma mensagem de erro) se `x < 0`.

### Registro e Acompanhamento
- **Data de identificação:** 07/11/2026
- **Status:** Não resolvido

---

## BUG-05: Logaritmo natural usa função inexistente `np.ln`

### Identificação do Bug
- **Título:** Logaritmo natural chama `np.ln`, que não existe no NumPy
- **Localização:** `Calculadora.py`, função `logaritmo_natural`, linha 32

### Descrição Detalhada
- **Descrição clara do bug:** o NumPy não tem a função `ln`. O logaritmo natural no NumPy se chama `np.log`. Por isso, qualquer entrada positiva, que passa pela validação, gera `AttributeError` e encerra o programa. A operação 8 nunca funciona.
- **Contexto:** ver o contexto geral (NumPy 2.5.3). A função `ln` também não existe em versões anteriores do NumPy.

### Passos para Reproduzir
1. Executar `python Calculadora.py`.
2. Digitar `8` (Logaritmo Natural).
3. Digitar `1`.

- **Consistência:** ocorre sempre, para qualquer `x > 0`.

### Resultado Esperado vs. Obtido
- **Esperado:** `Resultado: 0.0`
- **Obtido:** o programa fecha com `AttributeError`.

### Evidências
- **Log de erro** (`evidencias/tracebacks.txt`):

```text
  File "Calculadora.py", line 32, in logaritmo_natural
    return np.ln(x)
           ^^^^^
AttributeError: module 'numpy' has no attribute 'ln'
```

- **Screenshot:** `evidencias/img/bug05_ln.png`

### Severidade e Impacto
- **Severidade:** Crítico
- **Impacto:** a funcionalidade está totalmente indisponível e ainda derruba a aplicação.

### Sugestões para Correção
- Trocar por `np.log(x)`.

### Registro e Acompanhamento
- **Data de identificação:** 07/11/2026
- **Status:** Não resolvido

---

## BUG-06: Logaritmo base 10 calcula o logaritmo natural

### Identificação do Bug
- **Título:** Logaritmo base 10 retorna o logaritmo natural
- **Localização:** `Calculadora.py`, função `logaritmo_base10`, linha 37

### Descrição Detalhada
- **Descrição clara do bug:** a função usa `np.log(x)`, que no NumPy é o logaritmo **natural** (base *e*). O logaritmo na base 10 é `np.log10(x)`. Todo resultado da opção 9 sai multiplicado por ln(10), cerca de 2,3026.
- **Contexto:** ver o contexto geral.

### Passos para Reproduzir
1. Executar `python Calculadora.py`.
2. Digitar `9` (Logaritmo Base 10).
3. Digitar `100`.

- **Consistência:** ocorre sempre, para qualquer `x > 0` diferente de 1.

### Resultado Esperado vs. Obtido
- **Esperado:** `Resultado: 2.0`
- **Obtido:** `Resultado: 4.605170185988092`

### Evidências
- `evidencias/saida_reproducao.txt`, bloco `[BUG-06]`.
- **Screenshot:** `evidencias/img/bug06_log10.png`

### Severidade e Impacto
- **Severidade:** Alto
- **Impacto:** o resultado é errado e não vem com nenhum aviso.

### Sugestões para Correção
- Trocar por `np.log10(x)`.

### Registro e Acompanhamento
- **Data de identificação:** 07/11/2026
- **Status:** Não resolvido

---

## BUG-07: Logaritmo base 10 aceita zero e retorna `-inf`

### Identificação do Bug
- **Título:** Validação do logaritmo base 10 deixa passar o zero
- **Localização:** `Calculadora.py`, função `logaritmo_base10`, linha 35 (`if x < 0:`)

### Descrição Detalhada
- **Descrição clara do bug:** o logaritmo só é definido para `x > 0`. A condição `x < 0` deixa o zero passar. A própria mensagem de erro diz "número não positivo", e o `logaritmo_natural` usa corretamente `x <= 0`. Com `x = 0`, o NumPy retorna `-inf` e emite um `RuntimeWarning`.
- **Contexto:** ver o contexto geral.

### Passos para Reproduzir
1. Executar `python Calculadora.py`.
2. Digitar `9` (Logaritmo Base 10).
3. Digitar `0`.

- **Consistência:** ocorre sempre com `x = 0`.

### Resultado Esperado vs. Obtido
- **Esperado:** `Resultado: Erro: Logaritmo de número não positivo`
- **Obtido:** `Resultado: -inf`, mais o aviso:

### Evidências
- **Log de aviso** (`evidencias/tracebacks.txt`):

```text
Resultado: -inf
Calculadora.py:37: RuntimeWarning: divide by zero encountered in log
  return np.log(x)
```

### Severidade e Impacto
- **Severidade:** Médio
- **Impacto:** a calculadora mostra um valor sem significado (`-inf`) no lugar da mensagem de erro já prevista.

### Sugestões para Correção
- Trocar a condição por `if x <= 0:`.

### Registro e Acompanhamento
- **Data de identificação:** 07/11/2026
- **Status:** Não resolvido

---

## BUG-08: Opção 10 (Seno) não está implementada

### Identificação do Bug
- **Título:** Menu oferece "10. Seno", mas a opção é tratada como inválida
- **Localização:** `Calculadora.py`, função `menu` (linha 52) e `calculadora_cientifica` (cadeia de `elif` nas linhas 63 a 102, onde não há ramo para `'10'`). A função `seno` também não existe.

### Descrição Detalhada
- **Descrição clara do bug:** o menu mostra a opção 10 (Seno), mas `calculadora_cientifica` não tem um ramo para `'10'`. A escolha cai no `else` e o programa exibe "Operação inválida". Uma funcionalidade anunciada não existe.
- **Contexto:** ver o contexto geral.

### Passos para Reproduzir
1. Executar `python Calculadora.py`.
2. Digitar `10` (Seno).

- **Consistência:** ocorre sempre.

### Resultado Esperado vs. Obtido
- **Esperado:** pedir o ângulo e mostrar o seno (por exemplo, 30° resulta em `0.5`).
- **Obtido:** `Operação inválida. Tente novamente.`

### Evidências
- `evidencias/saida_reproducao.txt`, bloco `[BUG-08]`.
- **Screenshot:** `evidencias/img/bug08_seno.png`

### Severidade e Impacto
- **Severidade:** Alto
- **Impacto:** a funcionalidade anunciada está indisponível, e a mensagem engana o usuário, que acha que escolheu a opção errada.

### Sugestões para Correção
- Criar `def seno(x, radianos=False)` com `np.sin` (convertendo graus com `np.radians`) e adicionar o ramo `elif escolha == '10':`.

### Registro e Acompanhamento
- **Data de identificação:** 07/11/2026
- **Status:** Não resolvido

---

## BUG-09: Opção 11 (Cosseno) chama função inexistente

### Identificação do Bug
- **Título:** Opção 11 chama `cosseno()`, que não foi definida
- **Localização:** `Calculadora.py`, função `calculadora_cientifica`, linha 95

### Descrição Detalhada
- **Descrição clara do bug:** o ramo `'11'` pede o ângulo e chama `cosseno(x)`, mas essa função não existe no arquivo. O resultado é `NameError`, e o programa termina.
- **Contexto:** ver o contexto geral.

### Passos para Reproduzir
1. Executar `python Calculadora.py`.
2. Digitar `11` (Cosseno).
3. Digitar `0`.

- **Consistência:** ocorre sempre.

### Resultado Esperado vs. Obtido
- **Esperado:** `Resultado: 1.0`
- **Obtido:** o programa fecha com `NameError`.

### Evidências
- **Log de erro** (`evidencias/tracebacks.txt`):

```text
  File "Calculadora.py", line 95, in calculadora_cientifica
    print("Resultado:", cosseno(x))
                        ^^^^^^^
NameError: name 'cosseno' is not defined
```

- **Screenshot:** `evidencias/img/bug09_cosseno.png`

### Severidade e Impacto
- **Severidade:** Crítico
- **Impacto:** a funcionalidade está indisponível e derruba a aplicação.

### Sugestões para Correção
- Criar `def cosseno(x, radianos=False)` usando `np.cos(np.radians(x))` quando o ângulo estiver em graus.

### Registro e Acompanhamento
- **Data de identificação:** 07/11/2026
- **Status:** Não resolvido

---

## BUG-10: Opção 12 (Tangente) chama função inexistente

### Identificação do Bug
- **Título:** Opção 12 chama `tangente()`, que não foi definida
- **Localização:** `Calculadora.py`, função `calculadora_cientifica`, linha 99

### Descrição Detalhada
- **Descrição clara do bug:** o ramo `'12'` chama `tangente(x, radianos=False)`, mas a função não existe. O resultado é `NameError`, e o programa termina. Outro ponto que precisa de atenção: a tangente não é definida em 90° + k·180°.
- **Contexto:** ver o contexto geral.

### Passos para Reproduzir
1. Executar `python Calculadora.py`.
2. Digitar `12` (Tangente).
3. Digitar `45`.

- **Consistência:** ocorre sempre.

### Resultado Esperado vs. Obtido
- **Esperado:** `Resultado: 1.0` (com uma pequena diferença de ponto flutuante).
- **Obtido:** o programa fecha com `NameError`.

### Evidências
- **Log de erro** (`evidencias/tracebacks.txt`):

```text
  File "Calculadora.py", line 99, in calculadora_cientifica
    print("Resultado:", tangente(x, radianos=False))
                        ^^^^^^^^
NameError: name 'tangente' is not defined
```

### Severidade e Impacto
- **Severidade:** Crítico
- **Impacto:** a funcionalidade está indisponível e derruba a aplicação.

### Sugestões para Correção
- Criar `def tangente(x, radianos=False)` com `np.tan`, convertendo graus e tratando os ângulos em que a tangente não existe.

### Registro e Acompanhamento
- **Data de identificação:** 07/11/2026
- **Status:** Não resolvido

---

## BUG-11: Entrada não numérica encerra o programa

### Identificação do Bug
- **Título:** Digitar texto no lugar de número gera `ValueError` não tratado
- **Localização:** `Calculadora.py`, função `calculadora_cientifica`, conversões `float(input(...))` e `int(input(...))` nas linhas 64, 65, 78, 82, 86, 90, 94 e 98

### Descrição Detalhada
- **Descrição clara do bug:** nenhuma conversão de entrada está protegida por `try/except`. Se o usuário digitar uma letra, deixar o campo vazio, ou digitar um decimal no fatorial (`int("2.5")`), o programa termina com `ValueError`.
- **Contexto:** ver o contexto geral.

### Passos para Reproduzir
1. Executar `python Calculadora.py`.
2. Digitar `1` (Adição).
3. Digitar `abc` como primeiro número.

- **Consistência:** ocorre sempre com uma entrada não numérica.

### Resultado Esperado vs. Obtido
- **Esperado:** uma mensagem como `Entrada inválida, digite um número`, pedindo o valor de novo.
- **Obtido:** o programa fecha com o traceback abaixo.

### Evidências
- **Log de erro** (`evidencias/tracebacks.txt`):

```text
  File "Calculadora.py", line 64, in calculadora_cientifica
    x = float(input("Digite o primeiro número: "))
        ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ValueError: could not convert string to float: 'abc'
```

### Severidade e Impacto
- **Severidade:** Médio
- **Impacto:** a calculadora é frágil, e um erro de digitação faz o usuário perder a sessão.

### Sugestões para Correção
- Criar uma função auxiliar `ler_numero(mensagem, tipo=float)` que repete a pergunta até receber um valor válido.

### Registro e Acompanhamento
- **Data de identificação:** 07/11/2026
- **Status:** Não resolvido

---

## BUG-12: Calculadora é executada ao importar o módulo

### Identificação do Bug
- **Título:** `import Calculadora` abre o menu e espera entrada do teclado
- **Localização:** `Calculadora.py`, linha 108 (`calculadora_cientifica()` no nível do módulo)

### Descrição Detalhada
- **Descrição clara do bug:** a chamada `calculadora_cientifica()` está solta no fim do arquivo, sem a proteção `if __name__ == "__main__":`. Por isso, qualquer `import Calculadora` (por exemplo, num arquivo de testes) exibe o menu e trava esperando o teclado. Isso impede reutilizar as funções e atrapalha os testes automatizados.
- **Contexto:** ver o contexto geral. Com `python -m unittest`, o import fica parado esperando entrada. Com `pytest`, que bloqueia a leitura do teclado, o import falha com erro.

### Passos para Reproduzir
1. Na pasta do repositório, executar `python -c "import Calculadora"`.

- **Consistência:** ocorre sempre.

### Resultado Esperado vs. Obtido
- **Esperado:** o import termina em silêncio e deixa as funções disponíveis.
- **Obtido:** o menu é exibido e o programa fica esperando `Digite o número da operação:`.

### Evidências
- `evidencias/saida_reproducao.txt`, bloco `[BUG-12]`: o import exibiu 16 linhas de menu e chamou `input()`.
- Para contornar o bug, os testes (`test_calculadora.py`) simulam a entrada `0` durante o import.

### Severidade e Impacto
- **Severidade:** Médio
- **Impacto:** não afeta quem usa o programa pelo terminal, mas impede a reutilização do código e dificulta testes automatizados.

### Sugestões para Correção
- Trocar a linha 108 por:

  ```python
  if __name__ == "__main__":
      calculadora_cientifica()
  ```

### Registro e Acompanhamento
- **Data de identificação:** 07/11/2026
- **Status:** Não resolvido (contornado nos testes)

---

## BUG-13: Repetir operações estoura a pilha (recursão)

### Identificação do Bug
- **Título:** O laço "Deseja realizar outra operação?" é feito com recursão e gera `RecursionError`
- **Localização:** `Calculadora.py`, função `calculadora_cientifica`, linha 106

### Descrição Detalhada
- **Descrição clara do bug:** para continuar usando a calculadora, a função chama a si mesma em vez de usar um laço `while`. Cada operação adiciona um nível à pilha de chamadas. O limite padrão do Python é de cerca de 1000 níveis, e ao passar dele o programa termina com `RecursionError`. Além disso, a memória cresce a cada operação.
- **Contexto:** ver o contexto geral. Limite de recursão padrão: `sys.getrecursionlimit() == 1000`.

### Passos para Reproduzir
1. Executar `python Calculadora.py`.
2. Fazer qualquer operação e responder `s` para continuar.
3. Repetir cerca de 1000 vezes. O script de reprodução automatiza isso com 1100 repetições.

- **Consistência:** ocorre sempre depois de cerca de 995 operações seguidas.

### Resultado Esperado vs. Obtido
- **Esperado:** a calculadora continua funcionando indefinidamente.
- **Obtido:** `RecursionError: maximum recursion depth exceeded` depois de 995 operações.

### Evidências
- `evidencias/saida_reproducao.txt`, bloco `[BUG-13]`.

### Severidade e Impacto
- **Severidade:** Baixo
- **Impacto:** só aparece em sessões muito longas, mas é um defeito de projeto que pode derrubar o programa.

### Sugestões para Correção
- Trocar a recursão por `while True:` e usar `break` quando a resposta for diferente de `s`.

### Registro e Acompanhamento
- **Data de identificação:** 07/11/2026
- **Status:** Não resolvido

---

## BUG-14: Erros retornados como texto no lugar do número

### Identificação do Bug
- **Título:** Funções matemáticas retornam uma *string* de erro em vez de levantar exceção
- **Localização:** `Calculadora.py`, `raiz_quadrada` (linha 20), `logaritmo_natural` (linha 31) e `logaritmo_base10` (linha 36)

### Descrição Detalhada
- **Descrição clara do bug:** em caso de entrada inválida, essas funções retornam um texto como `"Erro: Raiz quadrada de número negativo"`, quando deveriam levantar uma exceção. Assim, a mesma função às vezes devolve um número e às vezes um texto. Quem usa o resultado em outra conta recebe um `TypeError` longe da origem do problema, ou pode até tratar o texto como resultado válido.
- **Contexto:** ver o contexto geral.

### Passos para Reproduzir
1. Importar a função `raiz_quadrada` (ver BUG-12).
2. Executar `raiz_quadrada(-4) + 1`.

- **Consistência:** ocorre sempre.

### Resultado Esperado vs. Obtido
- **Esperado:** `raiz_quadrada(-4)` levanta `ValueError("Raiz quadrada de número negativo")`, e o menu mostra a mensagem.
- **Obtido:** a função retorna uma string, e a conta seguinte falha com `TypeError: can only concatenate str (not "int") to str`.

### Evidências
- `evidencias/saida_reproducao.txt`, bloco `[BUG-14]`.

### Severidade e Impacto
- **Severidade:** Baixo
- **Impacto:** pelo terminal o usuário vê a mensagem normalmente. O problema aparece quando as funções são reutilizadas ou testadas.

### Sugestões para Correção
- Levantar `ValueError` nas funções e tratar com `try/except` em `calculadora_cientifica`, exibindo a mensagem.

### Registro e Acompanhamento
- **Data de identificação:** 07/11/2026
- **Status:** Não resolvido
