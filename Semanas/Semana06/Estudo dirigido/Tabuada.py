"""Semana 06 - Estudo dirigido: tabuada do 7 usando for e range()."""


def tabuada(numero: int, limite: int = 10) -> list[str]:
    """Gera as linhas da tabuada de `numero` de 1 até `limite`.

    >>> tabuada(7, 3)
    ['7 x 1 = 7', '7 x 2 = 14', '7 x 3 = 21']
    """
    linhas = []
    for i in range(1, limite + 1):
        linhas.append(f"{numero} x {i} = {numero * i}")
    return linhas


if __name__ == "__main__":
    for linha in tabuada(7):
        print(linha)
