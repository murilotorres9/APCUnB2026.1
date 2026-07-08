"""
Semana 14 - Recursão: caso base e caso recursivo
Fatorial recursivo, feito para ser colado no Python Tutor (pythontutor.com)
e observar a pilha de chamadas crescendo e desempilhando.
"""


def fatorial_recursivo(n: int) -> int:
    """Calcula o fatorial de n recursivamente.

    Caso base: fatorial(0) = 1 (ou fatorial(1) = 1)
    Caso recursivo: fatorial(n) = n * fatorial(n - 1)

    >>> fatorial_recursivo(0)
    1
    >>> fatorial_recursivo(1)
    1
    >>> fatorial_recursivo(5)
    120
    """
    if n <= 1:                              # caso base
        return 1
    return n * fatorial_recursivo(n - 1)    # caso recursivo


def fatorial_iterativo(n: int) -> int:
    """Mesma função, versão iterativa — para comparar legibilidade e uso
    de memória com a versão recursiva.

    >>> fatorial_iterativo(5)
    120
    """
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado


if __name__ == "__main__":
    print("fatorial_recursivo(5) =", fatorial_recursivo(5))
    print("fatorial_iterativo(5) =", fatorial_iterativo(5))

    # Risco de estouro de pilha: recursão profunda demais
    import sys
    print(f"\nLimite padrão de recursão do Python: {sys.getrecursionlimit()}")
    try:
        fatorial_recursivo(5000)
    except RecursionError as e:
        print(f"RecursionError ao tentar fatorial_recursivo(5000): {e}")
