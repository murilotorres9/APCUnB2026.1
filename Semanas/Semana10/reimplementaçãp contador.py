"""Semana 10 - Reimplementação do contador automático (semana 06) em Python.
Também demonstra laços aninhados: tabuada completa e triângulo de asteriscos.
"""


def contador_automatico(limite: int = 10) -> list[int]:
    """>>> contador_automatico(3)
    [1, 2, 3]
    """
    valores = []
    contador = 0
    for _ in range(limite):
        contador += 1
        valores.append(contador)
    return valores


def tabuada_completa(ate: int = 10) -> None:
    """Imprime a tabuada de 1 até `ate` usando laços aninhados."""
    for numero in range(1, ate + 1):
        for i in range(1, 11):
            print(f"{numero} x {i} = {numero * i}")
        print("---")


def triangulo_asteriscos(altura: int = 5) -> None:
    """Imprime um triângulo de asteriscos com `altura` linhas."""
    for i in range(1, altura + 1):
        print("*" * i)


def matriz_identidade(n: int) -> list[list[int]]:
    """Gera uma matriz identidade n x n usando laços aninhados.

    >>> matriz_identidade(3)
    [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    """
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


if __name__ == "__main__":
    print("Contador:", contador_automatico())
    print("\nTriângulo:")
    triangulo_asteriscos()
    print("\nMatriz identidade 3x3:", matriz_identidade(3))
