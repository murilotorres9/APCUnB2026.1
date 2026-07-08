"""
Semana 14 - Algoritmos de ordenação: Selection Sort

Passo a passo: a cada posição i, encontra o menor elemento do restante da
lista (i até o fim) e troca com a posição i. Complexidade O(n²), assim como
o Bubble Sort, mas faz menos trocas (apenas 1 troca por posição).
"""


def selection_sort(lista: list[float]) -> list[float]:
    """Ordena uma lista usando Selection Sort (O(n²)), sem alterar o original.

    >>> selection_sort([5, 2, 4, 1, 3])
    [1, 2, 3, 4, 5]
    >>> selection_sort([])
    []
    >>> selection_sort([1])
    [1]
    """
    dados = lista.copy()
    n = len(dados)
    for i in range(n):
        indice_menor = i
        for j in range(i + 1, n):
            if dados[j] < dados[indice_menor]:
                indice_menor = j
        dados[i], dados[indice_menor] = dados[indice_menor], dados[i]
    return dados


if __name__ == "__main__":
    exemplo = [5, 2, 4, 1, 3]
    print("Original:     ", exemplo)
    print("Selection sort:", selection_sort(exemplo))
