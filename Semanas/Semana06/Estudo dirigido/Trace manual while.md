# Estudo dirigido — Repetição (Semana 6)

## Parte 1 — for vs while
```
Pseudocódigo A:
    para i de 1 até 5
        imprimir i
```
Usa **for**, porque o número de repetições é conhecido antecipadamente (5 vezes).

```
Pseudocódigo B:
    ler número
    enquanto número != 0
        imprimir número
        ler número
```
Usa **while**, porque não sabemos quantas vezes vai repetir — depende da entrada do usuário até aparecer o valor 0.

## Parte 2 — Trace manual (acumulador com while)

### Variação 1
```python
soma = 0
i = 1
while i <= 4:
    soma += i
    i += 1
print(soma)
```
**Saída prevista:** 10  (1+2+3+4)

### Variação 2
```python
soma = 0
i = 5
while i > 0:
    soma += i
    i -= 1
print(soma)
```
**Saída prevista:** 15 (5+4+3+2+1)

### Variação 3
```python
produto = 1
i = 1
while i <= 4:
    produto *= i
    i += 1
print(produto)
```
**Saída prevista:** 24 (4!)
