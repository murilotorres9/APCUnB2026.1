"""
Semana 14 - Recursão, complexidade e ordenação
Implementação própria de Bubble Sort, comparada com list.sort() em tempo.
"""

import random
import time


def bubble_sort(lista: list[float]) -> list[float]:
    """Ordena uma lista usando Bubble Sort (O(n²)), sem alterar o original.

    >>> bubble_sort([5, 2, 4, 1, 3])
    [1, 2, 3, 4, 5]
    """
    dados = lista.copy()
    n = len(dados)
    for i in range(n):
        trocou = False
        for j in range(n - i - 1):
            if dados[j] > dados[j + 1]:
                dados[j], dados[j + 1] = dados[j + 1], dados[j]
                trocou = True
        if not trocou:
            break
    return dados


def medir_tempo_bubble_sort(n: int) -> float:
    """Mede o tempo (segundos) para ordenar uma lista aleatória de tamanho n."""
    dados = [random.random() for _ in range(n)]
    inicio = time.perf_counter()
    bubble_sort(dados)
    return time.perf_counter() - inicio


def medir_tempo_sort_nativo(n: int) -> float:
    """Mede o tempo (segundos) do list.sort() nativo do Python (Timsort)."""
    dados = [random.random() for _ in range(n)]
    inicio = time.perf_counter()
    dados.sort()
    return time.perf_counter() - inicio


if __name__ == "__main__":
    for n in (100, 1000, 10000):
        t_bubble = medir_tempo_bubble_sort(n)
        t_nativo = medir_tempo_sort_nativo(n)
        print(f"N={n:>6}  bubble_sort={t_bubble:.4f}s  list.sort()={t_nativo:.6f}s")
