# Semana 13 — Relatório de depuração

> As 5 correções abaixo estão em `debugging/`, como prática do ciclo de
> depuração pedido pelo professor. **Se em sala o professor fornecer os 5
> programas problemáticos oficiais**, substitua os exemplos abaixo pelos
> bugs reais encontrados nesses arquivos, mantendo o mesmo formato de tabela.

| # | Arquivo | Sintoma observado | Causa raiz | Correção aplicada |
|---|---------|--------------------|------------|--------------------|
| 1 | `bug1_typeerror.py` | `TypeError` ao somar idade digitada com 1 | `input()` retorna `str`, código somava direto com `int` sem converter | Converter com `int()` antes de somar |
| 2 | `bug2_off_by_one.py` | `soma_ate(5)` retornava 10 em vez de 15 | `range(n)` exclui o próprio `n` | Trocar para `range(1, n + 1)` |
| 3 | `bug3_default_mutavel.py` | segunda chamada da função vinha com item da chamada anterior | argumento default `lista=[]` é criado uma única vez e compartilhado entre chamadas | Usar `None` como default e criar a lista dentro da função |
| 4 | `bug4_indexerror.py` | `IndexError: list index out of range` na última iteração | condição `i <= len(lista)` permite índice igual a `len(lista)`, que é inválido | Trocar para `i < len(lista)` |
| 5 | `bug5_condicao_invertida.py` | aluno com frequência baixa era aprovado só com nota alta | uso de `or` em vez de `and` entre os dois critérios de aprovação | Trocar `or` por `and` |

**Doctests da `lib_matematica.py`:** versão completa em
`semana13/lib_matematica.py`, com casos-limite adicionais para `media`,
`mdc`, `mmc`, `eh_primo` e `fatorial` — todos passando via
`python3 -m doctest lib_matematica.py`.

**Sensor ultrassônico + Arduino (Tinkercad):** ver `sensor_tinkercad.md`.

**Ciclo completo de desenvolvimento:** ver `ciclo_desenvolvimento.md`.
