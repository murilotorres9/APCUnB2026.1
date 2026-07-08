"""
Semana 11 - Estruturas de dados: listas e banco de dados simples
Simulador 8: lista de registros (escolas) com busca linear e binária,
filtragem, e estatísticas básicas sem bibliotecas externas.

Observação: escolas_amostra.csv contém dados ILUSTRATIVOS (8 escolas
fictícias no padrão dos microdados do SAEB/INEP). Para usar dados reais,
baixe os microdados em https://www.gov.br/inep/pt-br/areas-de-atuacao/
avaliacao-e-exames-educacionais/saeb/resultados e troque o CSV mantendo
as mesmas colunas.
"""

import csv


def carregar_escolas(caminho_csv: str) -> list[dict]:
    """Carrega os registros de escolas de um CSV para uma lista de dicionários."""
    with open(caminho_csv, encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        registros = []
        for linha in leitor:
            linha["proficiencia_matematica"] = float(linha["proficiencia_matematica"])
            linha["proficiencia_portugues"] = float(linha["proficiencia_portugues"])
            registros.append(linha)
        return registros


def filtrar_por_uf(escolas: list[dict], uf: str) -> list[dict]:
    """Filtra escolas por UF.

    >>> escolas = [{"uf": "DF", "escola": "A"}, {"uf": "SP", "escola": "B"}]
    >>> [e["escola"] for e in filtrar_por_uf(escolas, "DF")]
    ['A']
    """
    return [e for e in escolas if e["uf"] == uf]


def filtrar_por_rede(escolas: list[dict], rede: str) -> list[dict]:
    """Filtra escolas por rede de ensino (estadual, municipal, privada).

    >>> escolas = [{"rede": "estadual", "escola": "A"}, {"rede": "privada", "escola": "B"}]
    >>> [e["escola"] for e in filtrar_por_rede(escolas, "privada")]
    ['B']
    """
    return [e for e in escolas if e["rede"] == rede]


def busca_linear_por_nome(escolas: list[dict], nome: str) -> dict | None:
    """Busca linear O(n) por nome exato de escola.

    >>> escolas = [{"escola": "A"}, {"escola": "B"}]
    >>> busca_linear_por_nome(escolas, "B")
    {'escola': 'B'}
    >>> busca_linear_por_nome(escolas, "Z") is None
    True
    """
    for escola in escolas:
        if escola["escola"] == nome:
            return escola
    return None


def busca_binaria_por_codigo(escolas_ordenadas: list[dict], codigo: str) -> dict | None:
    """Busca binária O(log n) por código INEP, assumindo lista já ordenada
    por 'codigo_inep' (como string).

    >>> escolas = [{"codigo_inep": "1"}, {"codigo_inep": "2"}, {"codigo_inep": "3"}]
    >>> busca_binaria_por_codigo(escolas, "3")
    {'codigo_inep': '3'}
    >>> busca_binaria_por_codigo(escolas, "9") is None
    True
    """
    baixo, alto = 0, len(escolas_ordenadas) - 1
    while baixo <= alto:
        meio = (baixo + alto) // 2
        if escolas_ordenadas[meio]["codigo_inep"] == codigo:
            return escolas_ordenadas[meio]
        elif escolas_ordenadas[meio]["codigo_inep"] < codigo:
            baixo = meio + 1
        else:
            alto = meio - 1
    return None


def media(valores: list[float]) -> float:
    """
    >>> media([2, 4, 6])
    4.0
    """
    return sum(valores) / len(valores)


def desvio_padrao(valores: list[float]) -> float:
    """Calcula o desvio padrão populacional, sem bibliotecas externas.

    >>> round(desvio_padrao([2, 4, 4, 4, 5, 5, 7, 9]), 2)
    2.0
    """
    m = media(valores)
    variancia = sum((v - m) ** 2 for v in valores) / len(valores)
    return variancia ** 0.5


def resumo(escolas: list[dict]) -> None:
    """Imprime um resumo estatístico da lista de escolas."""
    notas_mat = [e["proficiencia_matematica"] for e in escolas]
    notas_port = [e["proficiencia_portugues"] for e in escolas]

    print(f"Total de escolas: {len(escolas)}")
    print(f"Matemática  — média: {media(notas_mat):.1f}  "
          f"maior: {max(notas_mat):.1f}  menor: {min(notas_mat):.1f}  "
          f"desvio: {desvio_padrao(notas_mat):.1f}")
    print(f"Português   — média: {media(notas_port):.1f}  "
          f"maior: {max(notas_port):.1f}  menor: {min(notas_port):.1f}  "
          f"desvio: {desvio_padrao(notas_port):.1f}")


if __name__ == "__main__":
    escolas = carregar_escolas("escolas_amostra.csv")

    print("=== Resumo geral ===")
    resumo(escolas)

    print("\n=== Filtragem por UF (DF) ===")
    df = filtrar_por_uf(escolas, "DF")
    print(f"{len(df)} escola(s) encontrada(s)")

    print("\n=== Filtragem por rede (estadual) ===")
    estaduais = filtrar_por_rede(escolas, "estadual")
    for e in estaduais:
        print(f"- {e['escola']}")

    print("\n=== Busca linear por nome ===")
    encontrada = busca_linear_por_nome(escolas, "CE 01 Brasília")
    print(f"Encontrada: {encontrada['escola'] if encontrada else 'nada'}")

    print("\n=== Busca binária por código INEP ===")
    escolas_ordenadas = sorted(escolas, key=lambda e: e["codigo_inep"])
    resultado = busca_binaria_por_codigo(escolas_ordenadas, "53000043")
    print(f"Encontrada: {resultado['escola'] if resultado else 'nada'}")
