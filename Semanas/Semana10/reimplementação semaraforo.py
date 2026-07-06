"""Semana 10 - Reimplementação do semáforo inteligente (semana 05) em Python."""


def proximo_estado(estado: str) -> str:
    """Retorna o próximo estado do semáforo.

    >>> proximo_estado("vermelho")
    'verde'
    >>> proximo_estado("verde")
    'amarelo'
    >>> proximo_estado("amarelo")
    'vermelho'
    """
    transicoes = {"vermelho": "verde", "verde": "amarelo", "amarelo": "vermelho"}
    return transicoes[estado]


if __name__ == "__main__":
    estado = "vermelho"
    for _ in range(6):
        print(estado)
        estado = proximo_estado(estado)
