# Semana 14 — Iteração vs recursão

| Critério | Iteração (`for`/`while`) | Recursão |
|---|---|---|
| Legibilidade | mais direta para quem já pensa "passo a passo" | mais natural para problemas definidos em termos de si mesmos (ex.: fatorial, árvores, sumarização hierárquica) |
| Memória | usa uma quantidade constante de memória (não empilha) | cada chamada empilha um novo quadro na pilha de chamadas — usa O(n) de memória extra |
| Risco de estouro de pilha | não existe | existe: Python tem um limite padrão de recursão (`sys.getrecursionlimit()`, geralmente 1000); ultrapassar gera `RecursionError` |
| Quando preferir | laços simples, contadores, acumuladores | problemas naturalmente hierárquicos/recursivos (percorrer estrutura de pastas, sumarizar por categoria dentro de categoria) |

**Demonstração:** `fatorial_recursivo.py` mostra o mesmo cálculo nas duas
formas e o momento exato em que a versão recursiva estoura a pilha
(`fatorial_recursivo(5000)` levanta `RecursionError`), enquanto a versão
iterativa não tem esse problema.

**No analisador SAEB desta semana:** a sumarização por município e por rede
foi feita com recursão (`media_por_municipio_recursiva`,
`media_por_rede_recursiva`) porque o problema já é naturalmente hierárquico
— resolver um grupo e "concatenar" com o resultado dos grupos restantes é
exatamente o padrão caso-base/caso-recursivo.
