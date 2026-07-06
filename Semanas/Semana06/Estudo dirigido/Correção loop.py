"""
Semana 06 - Estudo dirigido
Versão CORRIGIDA de soma_notas.py.

BUG (loop infinito): a versão original tinha
    i = 0
    while i < len(notas):
        soma += notas[i]
    (faltava o incremento `i += 1` dentro do laço, então `i` nunca mudava)

Correção: adicionar `i += 1` ao final do corpo do laço.
"""


def soma_notas(notas: list[float]) -> float:
    """Soma uma lista de notas usando um laço while corretamente incrementado.

    >>> soma_notas([7, 8, 9])
    24
    """
    soma = 0
    i = 0
    while i < len(notas):
        soma += notas[i]
        i += 1  # correção do loop infinito
    return soma


if __name__ == "__main__":
    notas = [7.5, 8.0, 6.5, 9.0]
    print(f"Soma das notas: {soma_notas(notas)}")
