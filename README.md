# Bug Hunter & TDD Calculator

Atividade de **identificação de defeitos** e **correção com TDD** (Test-Driven Development) feita sobre o esboço de uma calculadora científica em Python.

**Discente:** Micael Araujo Souza Santos

## Conteúdo do repositório

| Arquivo / pasta | Descrição |
|---|---|
| `Calculadora.py` | Código da calculadora científica (original, com o BUG-03 corrigido) |
| [`Bugs.md`](Bugs.md) | **Relatório de bugs**: 14 defeitos documentados e a documentação da correção do BUG-03 com TDD |
| `test_calculadora.py` | Testes automatizados (framework `unittest`) |
| `evidencias/reproduzir_bugs.py` | Script que reproduz todos os defeitos do relatório |
| `evidencias/saida_reproducao.txt` | Saída do script com o código original (evidência do "antes") |
| `evidencias/tracebacks.txt` | Mensagens de erro reais geradas pelo programa original |
| `evidencias/img/` | Capturas de tela dos bugs |
| `evidencias/tdd_1_red.txt`, `tdd_2_green.txt`, `tdd_3_refactor.txt` | Saída dos testes em cada fase do ciclo TDD |
| `evidencias/pytest_final.txt` | Execução final dos testes com o pytest |
| `requirements.txt` | Dependências (NumPy) |

## Como executar

Requisitos: Python 3.10 ou superior.

```bash
pip install -r requirements.txt
```

Para executar a calculadora:

```bash
python Calculadora.py
```

Para executar os testes:

```bash
python -m unittest -v
```

Os testes também rodam com `pytest -v`, se o pytest estiver instalado.

Para reproduzir os bugs documentados:

```bash
python evidencias/reproduzir_bugs.py
```

## Resumo dos bugs encontrados

| ID | Bug | Severidade | Status |
|---|---|---|---|
| BUG-01 | Adição calcula `2x + y` | Crítico | Não resolvido |
| BUG-02 | Divisão por zero derruba o programa | Alto | Não resolvido |
| BUG-03 | Fatorial sempre retorna 0 | Crítico | **Resolvido (TDD)** |
| BUG-04 | Fatorial de negativo retorna 1 | Médio | Não resolvido |
| BUG-05 | `np.ln` não existe (logaritmo natural) | Crítico | Não resolvido |
| BUG-06 | Log base 10 calcula o logaritmo natural | Alto | Não resolvido |
| BUG-07 | Log base 10 aceita zero (`-inf`) | Médio | Não resolvido |
| BUG-08 | Opção Seno não implementada | Alto | Não resolvido |
| BUG-09 | `cosseno()` não definida | Crítico | Não resolvido |
| BUG-10 | `tangente()` não definida | Crítico | Não resolvido |
| BUG-11 | Entrada não numérica derruba o programa | Médio | Não resolvido |
| BUG-12 | Menu executa ao importar o módulo | Médio | Não resolvido |
| BUG-13 | Recursão no "continuar" estoura a pilha | Baixo | Não resolvido |
| BUG-14 | Erros retornados como texto | Baixo | Não resolvido |

Os detalhes de cada bug estão em [`Bugs.md`](Bugs.md).

## Ciclo TDD aplicado ao BUG-03

O histórico de commits mostra cada fase do ciclo:

1. **Vermelho:** `Adiciona testes do fatorial que falham (TDD: fase vermelha)`. Quatro testes falham com `AssertionError: 0 != 120` e similares.
2. **Verde:** `Corrige fatorial que sempre retornava 0 (TDD: fase verde)`. Mudança de uma linha só (`range(x+1)` para `range(1, x+1)`), e todos os testes passam.
3. **Refatoração:** `Refatora função fatorial mantendo os testes passando (TDD: refatoração)`. Nomes mais claros e uma docstring, com os testes continuando verdes.

Para ver cada fase:

```bash
git log --oneline
```

## Reflexão: o processo pela ótica do Scrum

Fiz a atividade sozinho, mas organizei o trabalho como um **Sprint** curto. Fui ao mesmo tempo Product Owner, Scrum Master e time de desenvolvimento.

**Product Backlog.** A proposta da atividade funcionou como a visão do produto. Os 14 bugs encontrados viraram itens do backlog. A severidade de cada relatório (crítico, alto, médio, baixo) serviu de critério de priorização, que é o papel do Product Owner.

**Sprint Planning.** A meta do Sprint foi: "entregar o relatório completo dos defeitos e um bug corrigido com TDD, versionado no GitHub". Escolhi o BUG-03 porque é crítico, tem causa bem delimitada e tem comportamento esperado objetivo (`5! = 120`). Isso torna o bug ideal para escrever testes antes do código. Bugs maiores, como implementar seno, cosseno e tangente, ficaram no backlog para Sprints futuros.

**Sprint Backlog e incrementos.** O trabalho foi dividido em tarefas pequenas, e cada uma terminou em um commit:

1. versionar o código original;
2. registrar os bugs e as evidências;
3. escrever os testes que falham;
4. fazer a correção mínima;
5. refatorar;
6. documentar.

Cada commit é um incremento verificável, e o histórico do Git funciona como registro do progresso, parecido com um quadro de tarefas.

**Definition of Done.** Considerei a correção pronta quando:

- todos os testes passam, os novos e os de regressão;
- o bug não aparece mais no script de reprodução;
- o relatório foi atualizado para "Resolvido";
- o código está no repositório remoto.

O TDD se encaixa bem aqui, porque o teste passando é um critério de aceitação objetivo e automatizado.

**Daily e inspeção.** Rodar os testes a cada mudança cumpriu, em escala menor, o papel de inspeção contínua do Scrum. O feedback é imediato e mostra se o caminho está certo. Um momento de **adaptação** real foi perceber que o BUG-12 (o menu executa no import) impedia os testes. Em vez de aumentar o escopo e corrigir dois bugs no mesmo ciclo, contornei o problema nos testes e mantive o BUG-12 no backlog. Isso respeita a meta do Sprint e mantém a mudança pequena.

Outro ajuste aconteceu no meio do Sprint. Faltavam as capturas de tela dos bugs, então desfiz a correção localmente, tirei os prints com o código original e só depois fiz o commit da correção. Isso mostra a importância de checar a Definition of Done de cada item antes de avançar.

**Sprint Review e Retrospectiva.**
- *O que funcionou:* escrever o relatório de bugs antes de mexer no código deu clareza sobre o problema. O script de reprodução tornou as evidências repetíveis. O ciclo vermelho, verde e refatoração deu segurança para mudar o código.
- *O que melhorar:* o código original não tinha nenhum teste nem estava preparado para ser testado (BUG-12). Num projeto real, a prática seria exigir testes desde o primeiro incremento. Também valeria uma revisão por pares, por Pull Request, antes de integrar a correção.
- *Próximo Sprint:* corrigir com TDD os outros bugs críticos (BUG-01, 05, 09 e 10) e o BUG-12, que facilita todos os testes seguintes.

## Referências

- PRESSMAN, Roger S.; MAXIM, Bruce R. *Engenharia de Software: uma abordagem profissional*. 9. ed. Porto Alegre: AMGH, 2021.
- LARMAN, Craig. *Utilizando UML e padrões: uma introdução à análise e ao projeto orientados a objetos e ao desenvolvimento iterativo*. 3. ed. Porto Alegre: Bookman, 2007.
- Documentação do `unittest`: https://docs.python.org/3/library/unittest.html
- Documentação do GitHub: https://docs.github.com/pt
