"""
Semana 07 - Abstração e modularização
Refatoração dos problemas clássicos usando funções (equivalente aos
"blocos customizados" do OctoStudio).
"""


def fatorial(n: int) -> int:
    """Calcula o fatorial de n de forma iterativa.

    >>> fatorial(0)
    1
    >>> fatorial(5)
    120
    """
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado


def eh_primo(n: int) -> bool:
    """Verifica se n é primo.

    >>> eh_primo(7)
    True
    >>> eh_primo(8)
    False
    >>> eh_primo(1)
    False
    """
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def fibonacci(n: int) -> list[int]:
    """Retorna os primeiros n termos da sequência de Fibonacci.

    >>> fibonacci(5)
    [0, 1, 1, 2, 3]
    """
    seq = []
    a, b = 0, 1
    for _ in range(n):
        seq.append(a)
        a, b = b, a + b
    return seq


if __name__ == "__main__":
    print("5! =", fatorial(5))
    print("Primos até 20:", [n for n in range(2, 21) if eh_primo(n)])
    print("Fibonacci(10):", fibonacci(10))
