"""
utils/calcular.py
Funções de análise (estatísticas, pirâmide etária, arranjos, ordenação) —
sem nenhuma dependência de tkinter, para poderem ser testadas isoladamente.
"""

import pandas as pd

from utils.carregar import ROTULOS_SEXO, ROTULOS_ID_GENERO, ROTULOS_COR_RACA, ROTULOS_ARRANJOS

FAIXAS_ETARIAS = [0, 5, 12, 18, 25, 40, 60, 200]
ROTULOS_FAIXAS = ["0-4", "5-11", "12-17", "18-24", "25-39", "40-59", "60+"]


def filtrar_por_ra(base_unificada: pd.DataFrame, ra: str | None) -> pd.DataFrame:
    """Filtra a base unificada por Região Administrativa (ou retorna tudo se ra=None/'Todos')."""
    if ra is None or ra == "Todos":
        return base_unificada
    return base_unificada[base_unificada["localidade"] == ra]


def calcular_piramide_etaria(base_unificada: pd.DataFrame, ra: str | None = None) -> pd.DataFrame:
    """Calcula a contagem de moradores por faixa etária e sexo (E03), para
    a RA selecionada. Usamos E03 (Sexo) em vez de id_genero porque E03 é
    perguntado para todas as idades — id_genero tem sentinela para
    crianças, o que quebraria a pirâmide nas faixas mais jovens."""
    dados = filtrar_por_ra(base_unificada, ra).copy()
    dados["faixa_etaria"] = pd.cut(
        dados["idade_calculada"], bins=FAIXAS_ETARIAS, labels=ROTULOS_FAIXAS, right=False
    )
    piramide = dados.groupby(["faixa_etaria", "E03"], observed=True).size().unstack(fill_value=0)
    piramide = piramide.reindex(ROTULOS_FAIXAS, fill_value=0)
    return piramide


def calcular_distribuicao_tamanho_domicilio(domicilios: pd.DataFrame, ra: str | None = None) -> pd.Series:
    """Calcula quantos domicílios existem para cada tamanho (nº de pessoas), na RA selecionada."""
    dados = domicilios if (ra is None or ra == "Todos") else domicilios[domicilios["localidade"] == ra]
    return dados["A01npessoas"].value_counts().sort_index()


def calcular_distribuicao_arranjos(domicilios: pd.DataFrame, ra: str | None = None) -> pd.Series:
    """Calcula a distribuição de domicílios por tipo de arranjo familiar
    (variável derivada 'arranjos' do PDAD), na RA selecionada."""
    dados = domicilios if (ra is None or ra == "Todos") else domicilios[domicilios["localidade"] == ra]
    contagem = dados["arranjos"].map(ROTULOS_ARRANJOS).value_counts()
    return contagem.reindex(list(ROTULOS_ARRANJOS.values()), fill_value=0)


def calcular_perfil_complementar(base_unificada: pd.DataFrame, ra: str | None = None) -> dict:
    """Calcula a distribuição de id_genero (entre quem respondeu, ou seja,
    excluindo o sentinela 99999 predominantemente ligado a crianças) e de
    cor/raça (E05) para a RA selecionada — usa as duas variáveis
    'principais' do recorte F que não entram na pirâmide etária."""
    dados = filtrar_por_ra(base_unificada, ra)

    genero_valido = dados[dados["id_genero"] != 99999]
    dist_genero = genero_valido["id_genero"].map(ROTULOS_ID_GENERO).value_counts(normalize=True) * 100

    dist_cor_raca = dados["E05"].map(ROTULOS_COR_RACA).value_counts(normalize=True) * 100

    return {"id_genero_pct": dist_genero, "cor_raca_pct": dist_cor_raca}


def calcular_estatisticas(base_unificada: pd.DataFrame, domicilios: pd.DataFrame, ra: str | None = None) -> dict:
    """Calcula estatísticas descritivas para a RA selecionada: idade
    média, % de domicílios com crianças, tamanho médio do domicílio."""
    moradores_filtrados = filtrar_por_ra(base_unificada, ra)
    domicilios_filtrados = domicilios if (ra is None or ra == "Todos") else domicilios[domicilios["localidade"] == ra]

    idade_media = moradores_filtrados["idade_calculada"].mean()
    tamanho_medio = domicilios_filtrados["A01npessoas"].mean()
    pct_com_criancas = (domicilios_filtrados["A01ncriancas"] > 0).mean() * 100

    return {
        "n_moradores": len(moradores_filtrados),
        "n_domicilios": len(domicilios_filtrados),
        "idade_media": idade_media,
        "tamanho_medio_domicilio": tamanho_medio,
        "pct_domicilios_com_criancas": pct_com_criancas,
    }


def ordenar_ras_por_tamanho_medio(domicilios: pd.DataFrame) -> list[tuple[str, float]]:
    """Ranking de RAs por tamanho médio de domicílio, do maior para o menor.

    Implementa o Diferencial D4: ordenação feita manualmente com Selection
    Sort, em vez de usar .sort_values() do pandas.
    """
    medias_por_ra = domicilios.groupby("localidade")["A01npessoas"].mean()
    pares = list(medias_por_ra.items())  # [(ra, media), ...]

    n = len(pares)
    for i in range(n):
        indice_maior = i
        for j in range(i + 1, n):
            if pares[j][1] > pares[indice_maior][1]:
                indice_maior = j
        pares[i], pares[indice_maior] = pares[indice_maior], pares[i]

    return pares
