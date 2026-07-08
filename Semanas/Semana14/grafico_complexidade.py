"""
Semana 14 - Gráfico comparativo de complexidade
Gera um gráfico comparando o tempo de bubble_sort() (O(n²)) com list.sort()
nativo (O(n log n)) para diferentes tamanhos de entrada.

Requer matplotlib: pip install matplotlib --break-system-packages
"""

import matplotlib.pyplot as plt

from bubble_sort import medir_tempo_bubble_sort, medir_tempo_sort_nativo

TAMANHOS = [100, 300, 600, 1000, 2000]


def coletar_dados() -> tuple[list[float], list[float]]:
    tempos_bubble = [medir_tempo_bubble_sort(n) for n in TAMANHOS]
    tempos_nativo = [medir_tempo_sort_nativo(n) for n in TAMANHOS]
    return tempos_bubble, tempos_nativo


def gerar_grafico(caminho_saida: str = "grafico_complexidade.png") -> None:
    tempos_bubble, tempos_nativo = coletar_dados()

    plt.figure(figsize=(8, 5))
    plt.plot(TAMANHOS, tempos_bubble, marker="o", label="bubble_sort (O(n²))")
    plt.plot(TAMANHOS, tempos_nativo, marker="o", label="list.sort() (O(n log n))")
    plt.xlabel("Tamanho da lista (N)")
    plt.ylabel("Tempo (segundos)")
    plt.title("Comparação de tempo: Bubble Sort vs list.sort()")
    plt.legend()
    plt.grid(True)
    plt.savefig(caminho_saida)
    print(f"Gráfico salvo em {caminho_saida}")


if __name__ == "__main__":
    gerar_grafico()
