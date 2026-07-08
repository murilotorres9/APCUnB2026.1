# Semana 13 — Ciclo completo de desenvolvimento sistemático

Aplicando o ciclo **análise → projeto → codificação → teste → refatoração**
a um problema pequeno: "dado um valor em centavos, calcular o troco usando
o menor número de moedas possível (25, 10, 5, 1 centavos)".

## 1. Análise
- Entrada: um valor inteiro em centavos (ex: 87)
- Saída: quantas moedas de cada valor usar
- Restrição: minimizar o número total de moedas

## 2. Projeto (pseudocódigo)
```
para cada valor de moeda (do maior para o menor: 25, 10, 5, 1)
    quantidade <- valor_restante // valor_moeda
    guardar quantidade
    valor_restante <- valor_restante % valor_moeda
```

## 3. Codificação (primeira versão)
```python
def calcular_troco_v1(centavos):
    moedas = [25, 10, 5, 1]
    resultado = {}
    for moeda in moedas:
        resultado[moeda] = centavos // moeda
        centavos = centavos % moeda
    return resultado
```

## 4. Teste
```python
>>> calcular_troco_v1(87)
{25: 3, 10: 1, 5: 0, 1: 2}
```
Conferindo manualmente: 3×25 + 1×10 + 0×5 + 2×1 = 75+10+0+2 = 87 ✓

Caso-limite testado: `calcular_troco_v1(0)` deve retornar todas as
quantidades zeradas — testado e passou.

## 5. Refatoração
A primeira versão já funciona, mas o nome `resultado` não é muito
descritivo, e não há docstring. Versão final:

```python
def calcular_troco(centavos: int) -> dict[int, int]:
    """Calcula a quantidade mínima de moedas (25, 10, 5, 1 centavos)
    para compor um valor em centavos.

    >>> calcular_troco(87)
    {25: 3, 10: 1, 5: 0, 1: 2}
    >>> calcular_troco(0)
    {25: 0, 10: 0, 5: 0, 1: 0}
    """
    moedas = [25, 10, 5, 1]
    quantidade_por_moeda = {}
    for moeda in moedas:
        quantidade_por_moeda[moeda] = centavos // moeda
        centavos %= moeda
    return quantidade_por_moeda
```

**Reflexão:** o ciclo não é linear na prática — o teste do caso `0`
revelou que era preciso confirmar que o loop funciona mesmo quando não
sobra valor algum, o que já estava certo, mas só a etapa de teste deu essa
confiança antes de "dar por pronto".
