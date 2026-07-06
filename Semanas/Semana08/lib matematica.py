"""
Semana 08 - Funções e biblioteca de blocos reutilizáveis
Biblioteca de funções matemáticas básicas, todas documentadas com docstrings
e testáveis via doctest (usada e ampliada na semana 13).
"""


def media(numeros: list[float]) -> float:
    """Calcula a média aritmética de uma lista de números.

    >>> media([2, 4, 6])
    4.0
    """
    return sum(numeros) / len(numeros)


def mdc(a: int, b: int) -> int:
    """Calcula o Máximo Divisor Comum entre a e b (algoritmo de Euclides).

    >>> mdc(48, 18)
    6
    >>> mdc(17, 5)
    1
    """
    while b:
        a, b = b, a % b
    return a


def mmc(a: int, b: int) -> int:
    """Calcula o Mínimo Múltiplo Comum entre a e b.

    >>> mmc(4, 6)
    12
    """
    return a * b // mdc(a, b)


def eh_primo(n: int) -> bool:
    """Verifica se n é um número primo.

    >>> eh_primo(13)
    True
    >>> eh_primo(15)
    False
    """
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
