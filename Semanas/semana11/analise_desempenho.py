"""
Semana 11 - Aplicação com dados reais (microdados do SAEB/INEP)
Carrega o CSV, filtra por UF, calcula a média de proficiência por escola e
compara os resultados visualmente com matplotlib.

Os dados de escolas_amostra.csv são ILUSTRATIVOS, no mesmo formato dos
microdados oficiais do SAEB/INEP:
https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/saeb
Para usar dados reais, baixe o microdado do SAEB, extraia as colunas
equivalentes (código INEP, escola, município, UF, rede, proficiências) e
troque o CSV mantendo os mesmos nomes de coluna.

Requer matplotlib: pip install matplotlib --break-system-packages
"""

import csv

import matplotlib.pyplot as plt


def carregar_escolas(caminho_csv: str) -> list[dict]:
    with open(caminho_csv, encoding="utf-8") as f:
        registros = []
        for linha in csv.DictReader(f):
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


def media_por_escola(escolas: list[dict]) -> list[tuple[str, float]]:
    """Calcula a média entre matemática e português para cada escola.

    Retorna uma lista de tuplas (nome_escola, media) — comparando os
    resultados diretamente como listas, sem estruturas mais avançadas.

    >>> escolas = [{"escola": "A", "proficiencia_matematica": 6.0, "proficiencia_portugues": 8.0}]
    >>> media_por_escola(escolas)
    [('A', 7.0)]
    """
    resultado = []
    for e in escolas:
        media = (e["proficiencia_matematica"] + e["proficiencia_portugues"]) / 2
        resultado.append((e["escola"], media))
    return resultado


def gerar_grafico_comparativo(escolas: list[dict], caminho_saida: str = "grafico_desempenho_escolas.png") -> None:
    """Gera um gráfico de barras comparando a média de proficiência por escola."""
    dados = media_por_escola(escolas)
    dados.sort(key=lambda item: item[1], reverse=True)  # reaproveita sort() de listas

    nomes = [nome for nome, _ in dados]
    medias = [media for _, media in dados]

    plt.figure(figsize=(9, 5))
    plt.barh(nomes, medias, color="#2563eb")
    plt.xlabel("Média de proficiência (Matemática + Português) / 2")
    plt.title("Desempenho médio por escola — amostra SAEB (DF)")
    plt.gca().invert_yaxis()  # maior média no topo
    plt.tight_layout()
    plt.savefig(caminho_saida)
    print(f"Gráfico salvo em {caminho_saida}")


if __name__ == "__main__":
    escolas = carregar_escolas("escolas_amostra.csv")

    print("=== Filtragem por UF (DF) ===")
    escolas_df = filtrar_por_uf(escolas, "DF")
    print(f"{len(escolas_df)} escola(s) encontrada(s) no DF")

    print("\n=== Média de proficiência por escola ===")
    for nome, media in media_por_escola(escolas_df):
        print(f"{nome}: {media:.1f}")

    gerar_grafico_comparativo(escolas_df)
