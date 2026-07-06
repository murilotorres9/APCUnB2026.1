"""
Semana 09 - Introdução ao Python: reimplementando os simuladores
Reimplementação textual da calculadora interativa OctoStudio (semana 03).
"""


def somar(a: float, b: float) -> float:
    """
    >>> somar(2, 3)
    5
    """
    return a + b


def subtrair(a: float, b: float) -> float:
    """
    >>> subtrair(5, 3)
    2
    """
    return a - b


def multiplicar(a: float, b: float) -> float:
    """
    >>> multiplicar(4, 3)
    12
    """
    return a * b


def dividir(a: float, b: float) -> float:
    """Divide a por b, levantando erro claro em caso de divisão por zero.

    >>> dividir(10, 2)
    5.0
    >>> dividir(1, 0)
    Traceback (most recent call last):
        ...
    ZeroDivisionError: divisão por zero não é permitida
    """
    if b == 0:
        raise ZeroDivisionError("divisão por zero não é permitida")
    return a / b


OPERACOES = {
    "+": somar,
    "-": subtrair,
    "*": multiplicar,
    "/": dividir,
}


def calculadora_interativa() -> None:
    """Loop principal da calculadora: repete até o usuário digitar 'sair'."""
    print("Calculadora — operações: + - * /  (digite 'sair' para encerrar)")
    while True:
        entrada = input("Operação (ex: 4 + 5): ")
        if entrada.strip().lower() == "sair":
            print("Até mais!")
            break
        try:
            a_str, op, b_str = entrada.split()
            a, b = float(a_str), float(b_str)
            resultado = OPERACOES[op](a, b)
            print(f"= {resultado}")
        except (ValueError, KeyError):
            print("Entrada inválida. Use o formato: 4 + 5")
        except ZeroDivisionError as e:
            print(f"Erro: {e}")


if __name__ == "__main__":
    calculadora_interativa()
