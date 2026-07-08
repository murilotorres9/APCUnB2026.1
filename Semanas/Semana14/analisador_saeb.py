"""
Semana 14 - Simulador 10: Analisador de desempenho escolar (SAEB)
Carrega os microdados (amostra da semana 11), ordena escolas por
proficiência (reaproveitando bubble_sort da semana 14) e usa recursão para
sumarização hierárquica (município > rede > escolas).
"""

import csv

from bubble_sort import bubble_sort


def carregar_escolas(caminho_csv: str) -> list[dict]:
    with open(caminho_csv, encoding="utf-8") as f:
        registros = []
        for linha in csv.DictReader(f):
            linha["proficiencia_matematica"] = float(linha["proficiencia_matematica"])
            registros.append(linha)
        return registros


def ranking_por_proficiencia(escolas: list[dict]) -> list[dict]:
    """Ordena as escolas por proficiência em matemática (decrescente),
    reaproveitando o bubble_sort implementado nesta mesma semana."""
    chaves = [e["proficiencia_matematica"] for e in escolas]
    chaves_ordenadas = bubble_sort(chaves)[::-1]
    # reconstrói a lista de escolas na ordem das chaves ordenadas
    restantes = escolas.copy()
    ordenado = []
    for chave in chaves_ordenadas:
        for e in restantes:
            if e["proficiencia_matematica"] == chave:
                ordenado.append(e)
                restantes.remove(e)
                break
    return ordenado


def soma_recursiva(valores: list[float]) -> float:
    """Soma uma lista de valores recursivamente (caso base + caso recursivo).

    >>> soma_recursiva([1, 2, 3, 4])
    10
    >>> soma_recursiva([])
    0
    """
    if not valores:          # caso base
        return 0
    return valores[0] + soma_recursiva(valores[1:])   # caso recursivo


def media_por_municipio_recursiva(escolas: list[dict], municipios: list[str] | None = None) -> dict:
    """Calcula, recursivamente, a média de proficiência por município.

    A cada chamada resolve um município (caso base = lista vazia de
    municípios restantes) e concatena o resultado com a chamada recursiva
    para os municípios restantes — sumarização hierárquica.
    """
    if municipios is None:
        municipios = sorted({e["municipio"] for e in escolas})

    if not municipios:       # caso base
        return {}

    municipio_atual, *restantes = municipios
    notas = [e["proficiencia_matematica"] for e in escolas if e["municipio"] == municipio_atual]
    resultado_atual = {municipio_atual: soma_recursiva(notas) / len(notas)}

    return {**resultado_atual, **media_por_municipio_recursiva(escolas, restantes)}


def media_por_rede_recursiva(escolas: list[dict], redes: list[str] | None = None) -> dict:
    """Calcula, recursivamente, a média de proficiência por rede de ensino
    (estadual, municipal, privada) — mesmo padrão de sumarização
    hierárquica usado em media_por_municipio_recursiva.

    >>> escolas = [
    ...     {"rede": "estadual", "proficiencia_matematica": 250.0},
    ...     {"rede": "estadual", "proficiencia_matematica": 270.0},
    ...     {"rede": "privada", "proficiencia_matematica": 300.0},
    ... ]
    >>> media_por_rede_recursiva(escolas)
    {'estadual': 260.0, 'privada': 300.0}
    """
    if redes is None:
        redes = sorted({e["rede"] for e in escolas})

    if not redes:             # caso base
        return {}

    rede_atual, *restantes = redes
    notas = [e["proficiencia_matematica"] for e in escolas if e["rede"] == rede_atual]
    resultado_atual = {rede_atual: soma_recursiva(notas) / len(notas)}

    return {**resultado_atual, **media_por_rede_recursiva(escolas, restantes)}


def ranking_por_municipio_e_rede(escolas: list[dict]) -> dict:
    """Sumarização hierárquica de dois níveis: para cada município, o
    ranking de escolas por rede, usando recursão em ambos os níveis.
    Ilustra 'calcular rankings por município e rede' pedido no plano."""
    municipios = sorted({e["municipio"] for e in escolas})

    def _por_municipio(municipios_restantes: list[str]) -> dict:
        if not municipios_restantes:      # caso base
            return {}
        municipio_atual, *resto = municipios_restantes
        escolas_do_municipio = [e for e in escolas if e["municipio"] == municipio_atual]
        return {
            municipio_atual: media_por_rede_recursiva(escolas_do_municipio),
            **_por_municipio(resto),      # caso recursivo
        }

    return _por_municipio(municipios)


if __name__ == "__main__":
    escolas = carregar_escolas("../semana11/escolas_amostra.csv")

    print("Ranking por proficiência em matemática:")
    for i, e in enumerate(ranking_por_proficiencia(escolas), start=1):
        print(f"{i}. {e['escola']} — {e['proficiencia_matematica']}")

    print("\nMédia de proficiência por município (via recursão):")
    for municipio, media in media_por_municipio_recursiva(escolas).items():
        print(f"{municipio}: {media:.1f}")

    print("\nMédia de proficiência por rede (via recursão):")
    for rede, media in media_por_rede_recursiva(escolas).items():
        print(f"{rede}: {media:.1f}")

    print("\nRanking hierárquico por município e rede:")
    for municipio, redes in ranking_por_municipio_e_rede(escolas).items():
        print(f"{municipio}:")
        for rede, media in redes.items():
            print(f"  {rede}: {media:.1f}")
