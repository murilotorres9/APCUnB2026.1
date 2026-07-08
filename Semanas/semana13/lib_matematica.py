"""
Semana 13 - lib_matematica.py com doctests completos

Versão final da biblioteca iniciada na semana 08, agora com casos de teste
adicionais cobrindo casos-limite (edge cases) para cada função, como parte
do ciclo de desenvolvimento sistemático: análise -> projeto -> codificação
-> teste -> refatoração.
"""


def media(numeros: list[float]) -> float:
    """Calcula a média aritmética de uma lista de números.

    >>> media([2, 4, 6])
    4.0
    >>> media([5])
    5.0
    >>> media([-2, 2])
    0.0
    """
    return sum(numeros) / len(numeros)


def mdc(a: int, b: int) -> int:
    """Calcula o Máximo Divisor Comum entre a e b (algoritmo de Euclides).

    >>> mdc(48, 18)
    6
    >>> mdc(17, 5)
    1
    >>> mdc(0, 7)
    7
    >>> mdc(10, 10)
    10
    """
    while b:
        a, b = b, a % b
    return a


def mmc(a: int, b: int) -> int:
    """Calcula o Mínimo Múltiplo Comum entre a e b.

    >>> mmc(4, 6)
    12
    >>> mmc(5, 1)
    5
    >>> mmc(7, 7)
    7
    """
    return a * b // mdc(a, b)


def eh_primo(n: int) -> bool:
    """Verifica se n é um número primo.

    >>> eh_primo(13)
    True
    >>> eh_primo(15)
    False
    >>> eh_primo(2)
    True
    >>> eh_primo(1)
    False
    >>> eh_primo(0)
    False
    >>> eh_primo(-5)
    False
    """
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def fatorial(n: int) -> int:
    """Calcula o fatorial de n de forma iterativa.

    >>> fatorial(0)
    1
    >>> fatorial(1)
    1
    >>> fatorial(5)
    120
    """
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado


if __name__ == "__main__":
    import doctest
    resultado = doctest.testmod(verbose=True)
    print(f"\n{resultado.attempted - resultado.failed}/{resultado.attempted} testes passaram")
