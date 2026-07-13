"""
utils/exportar.py
Função de exportação dos dados/estatísticas filtrados para um arquivo
.txt ou .csv legível fora do programa (Requisito 5).
"""

import pandas as pd


def exportar_dados(estatisticas: dict, ra_selecionada: str, caminho: str) -> None:
    """Exporta as estatísticas descritivas e o cabeçalho da RA selecionada
    para um arquivo .txt ou .csv, dependendo da extensão de `caminho`."""
    if caminho.lower().endswith(".csv"):
        df = pd.DataFrame([estatisticas])
        df.insert(0, "regiao_administrativa", ra_selecionada)
        df.to_csv(caminho, index=False, encoding="utf-8")
    else:
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(f"PDAD Explorer — Perfil demográfico e composição domiciliar\n")
            f.write(f"Região Administrativa: {ra_selecionada}\n")
            f.write("-" * 50 + "\n")
            f.write(f"Moradores considerados: {estatisticas['n_moradores']}\n")
            f.write(f"Domicílios considerados: {estatisticas['n_domicilios']}\n")
            f.write(f"Idade média: {estatisticas['idade_media']:.1f} anos\n")
            f.write(f"Tamanho médio do domicílio: {estatisticas['tamanho_medio_domicilio']:.1f} pessoas\n")
            f.write(f"Domicílios com crianças: {estatisticas['pct_domicilios_com_criancas']:.1f}%\n")
