"""
Semana 12 - Tuplas: imutabilidade e uso como registros/structs

Uma tupla é como uma lista, mas imutável: depois de criada, não é possível
alterar, adicionar ou remover elementos. Isso a torna ideal para representar
um "registro" (struct) — um conjunto fixo de campos que não deveria mudar
de forma acidental, como as coordenadas de um ponto ou os dados de uma
escola num determinado instante.
"""


def demonstrar_imutabilidade() -> None:
    """Mostra que tentar alterar uma tupla gera erro."""
    ponto = (10, 20)
    print("Tupla ponto:", ponto)
    print("ponto[0]:", ponto[0])

    try:
        ponto[0] = 99  # type: ignore[index]
    except TypeError as e:
        print(f"Erro ao tentar alterar: {e}")


# "struct" de escola representado como tupla (código_inep, nome, proficiência)
Escola = tuple[str, str, float]


def criar_escola(codigo_inep: str, nome: str, proficiencia: float) -> Escola:
    """Cria um registro de escola como tupla — imutável por design.

    >>> criar_escola("53000010", "CE 01 Brasília", 265.4)
    ('53000010', 'CE 01 Brasília', 265.4)
    """
    return (codigo_inep, nome, proficiencia)


def desempacotar_escola(escola: Escola) -> None:
    """Desempacotamento de tupla — cada campo vira uma variável nomeada.

    >>> desempacotar_escola(("53000010", "CE 01 Brasília", 265.4))
    Código: 53000010, Nome: CE 01 Brasília, Proficiência: 265.4
    """
    codigo, nome, proficiencia = escola
    print(f"Código: {codigo}, Nome: {nome}, Proficiência: {proficiencia}")


if __name__ == "__main__":
    print("=== Imutabilidade ===")
    demonstrar_imutabilidade()

    print("\n=== Tupla como struct de escola ===")
    escola1 = criar_escola("53000010", "CE 01 Brasília", 265.4)
    desempacotar_escola(escola1)

    print("\n=== Lista de tuplas (registros) ===")
    escolas = [
        criar_escola("53000010", "CE 01 Brasília", 265.4),
        criar_escola("53000021", "CE 02 Brasília", 241.8),
    ]
    for escola in escolas:
        desempacotar_escola(escola)
