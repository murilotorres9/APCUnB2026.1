# Semana 14 — Recursão, complexidade e análise de desempenho escolar (SAEB)

**Conceito principal:** recursão (caso base/caso recursivo), iteração vs
recursão, complexidade O(n)/O(n²)/O(log n), algoritmos de ordenação.

## Arquivos

- **`fatorial_recursivo.py`** — fatorial recursivo (para rastrear no Python
  Tutor) e versão iterativa para comparação; demonstra o `RecursionError`
  ao ultrapassar o limite de pilha.
- **`iteracao_vs_recursao.md`** — comparação de legibilidade, memória e
  risco de estouro de pilha.
- **`bubble_sort.py`** — Bubble Sort implementado, com medição de tempo
  para N = 100, 1000, 10000 comparado ao `list.sort()` nativo.
- **`selection_sort.py`** — Selection Sort implementado, passo a passo.
- **`grafico_complexidade.py`** — gera `grafico_complexidade.png` comparando
  bubble_sort (O(n²)) com `list.sort()` (O(n log n)) usando `matplotlib`.
- **`analisador_saeb.py`** — Simulador 10: carrega os microdados (amostra
  da semana 11), ordena escolas por proficiência reaproveitando
  `bubble_sort`, e usa recursão para sumarização hierárquica: média por
  município, média por rede, e ranking cruzado município × rede.
- **`como_ensinar_recursao_ordenacao.md`** — atividades desplugadas
  (cartas de baralho para recursão, dança das trocas para ordenação) +
  uso do VisuAlgo.net como complemento.

## Como rodar

```bash
python3 fatorial_recursivo.py
python3 bubble_sort.py              # mede tempo para N=100,1000,10000
python3 selection_sort.py
python3 grafico_complexidade.py     # requer matplotlib, gera o PNG
python3 analisador_saeb.py

python3 -m doctest fatorial_recursivo.py -v
python3 -m doctest bubble_sort.py -v
python3 -m doctest selection_sort.py -v
python3 -m doctest analisador_saeb.py -v
```

## Python Tutor / VisuAlgo

- **Python Tutor:** cole `fatorial_recursivo(5)` em https://pythontutor.com/
  e observe a pilha de chamadas crescendo (5 quadros empilhados) e depois
  desempilhando com os resultados multiplicados.
  **Link:** _(cole aqui o link gerado)_
- **VisuAlgo:**veja as animações de Bubble Sort, Selection Sort e busca
  binária em https://visualgo.net/pt e compare com o comportamento do
  código desta semana.

## Reflexão breve

_(o que ficou mais claro sobre recursão depois de ver o Python Tutor: a
"pilha crescendo" ou a "pilha desempilhando"? o gráfico de complexidade
confirmou a expectativa teórica de O(n²) vs O(n log n)?)_
