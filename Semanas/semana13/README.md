# Semana 13 — Testes, depuração e desenvolvimento sistemático

**Conceito principal:** ciclo completo de desenvolvimento (análise → projeto
→ codificação → teste → refatoração), depuração sistemática, doctests.

> A segunda-feira desta semana é **prova teórica** (sem entrega de
> repositório) cobrindo pseudocódigo, análise de algoritmos, estruturas de
> controle, funções e estruturas de dados.

## Arquivos

- **`ciclo_desenvolvimento.md`** — exemplo completo do ciclo de
  desenvolvimento aplicado a um problema pequeno (cálculo de troco).
- **`debugging/`** — 5 programas de depuração, cada um com a versão
  corrigida, o bug documentado no docstring (sintoma + causa raiz +
  correção) e doctests comprovando a correção:
  - `bug1_typeerror.py` — conversão de tipo faltando
  - `bug2_off_by_one.py` — erro de limite em `range()`
  - `bug3_default_mutavel.py` — argumento default mutável compartilhado
  - `bug4_indexerror.py` — índice fora do intervalo em laço `while`
  - `bug5_condicao_invertida.py` — `or` usado no lugar de `and`
- **`relatorio_erros.md`** — tabela resumindo os 5 bugs encontrados/corrigidos.
- **`lib_matematica.py`** — versão final da biblioteca (semana 08) com
  doctests completos, incluindo casos-limite.
- **`sensor_tinkercad.md`** — documentação do circuito Arduino + sensor
  ultrassônico com a função `medir()`.

## Como rodar

```bash
python3 -m doctest lib_matematica.py -v
for f in debugging/*.py; do python3 -m doctest "$f"; done
```


