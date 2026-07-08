"""
Semana 12 - Aplicação com dados reais
Catálogo de escolas do DF: dicionário aninhado indexado por código INEP,
lido a partir de escolas.json (gerado a partir da amostra da semana 11).
Conceito principal: dicionários aninhados, consulta por chave, JSON como
ponte entre programas.
"""

import csv
import json


def csv_para_dicionario(caminho_csv: str) -> dict:
    """Converte o CSV de escolas em um dicionário indexado por codigo_inep."""
    catalogo = {}
    with open(caminho_csv, encoding="utf-8") as f:
        for linha in csv.DictReader(f):
            codigo = linha.pop("codigo_inep")
            catalogo[codigo] = linha
    return catalogo


def consultar_escola(catalogo: dict, codigo_inep: str) -> dict | None:
    """Consulta O(1) média de uma escola pelo código INEP.

    >>> catalogo = {"1": {"escola": "A"}}
    >>> consultar_escola(catalogo, "1")
    {'escola': 'A'}
    >>> consultar_escola(catalogo, "9") is None
    True
    """
    return catalogo.get(codigo_inep)


if __name__ == "__main__":
    catalogo = csv_para_dicionario("../semana11/escolas_amostra.csv")

    with open("escolas_df.json", "w", encoding="utf-8") as f:
        json.dump(catalogo, f, ensure_ascii=False, indent=2)

    exemplo = list(catalogo.keys())[0]
    print(f"Consulta ao código {exemplo}:", consultar_escola(catalogo, exemplo))
    print(f"Total de escolas no catálogo: {len(catalogo)}")
