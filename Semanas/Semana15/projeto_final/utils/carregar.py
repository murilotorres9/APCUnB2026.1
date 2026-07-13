"""
utils/carregar.py
Funções de leitura, limpeza e junção dos microdados do PDAD 2024 (dados reais).

Observações sobre o formato real dos arquivos (confirmadas nos dados
completos e no Dicionario_de_variaveis_PDAD_2024.xlsx):
  - moradores.csv usa ';' como separador de campos e vem com BOM (utf-8-sig)
  - localidade vem como CÓDIGO numérico (ex: 5301), não como nome de RA —
    o mapeamento código -> nome está no Anexo 1 do dicionário de variáveis
  - A01uf distingue DF (53) de municípios de Goiás amostrados (52); este
    sistema analisa apenas o Distrito Federal (A01uf == 53)
  - id_genero NÃO é "sexo" — é a "Composição entre a resposta de sexo de
    nascimento e identidade de gênero" (1=Cisgênero, 2=Transgênero,
    3=Outro, 99999=Não se aplica/sem classificação). O sentinela 99999 é
    usado sobretudo para crianças, que não respondem esse bloco — por
    isso NÃO usamos id_genero para a pirâmide etária (excluiria as
    crianças da pirâmide inteira); usamos E03 (Sexo: 1=Masculino,
    2=Feminino), que é perguntado para todas as idades. id_genero é usado
    à parte, como um recorte complementar sobre a população adulta.
  - E05 é "Cor ou raça" (1=Branca, 2=Preta, 3=Amarela, 4=Parda,
    5=Indígena), não uma variável de estado civil.
  - arranjos (na tabela de domicílios) é a variável derivada de "tipo de
    arranjo familiar" pedida no enunciado do recorte F.

Valores sentinela usados no PDAD:
    99999 -> "não se aplica" / "sem classificação"
    88888 -> "não declarado"
"""

import os

import pandas as pd

SENTINELAS = (99999, 88888)

CAMINHO_MORADORES = os.path.join("dados", "moradores_parcial.csv")
CAMINHO_DOMICILIOS = os.path.join("dados", "domicilios_parcial.xlsx")

# Anexo 1 do dicionário de variáveis: código da RA -> nome (apenas DF, A01uf=53)
MAPA_LOCALIDADES = {
    5301: "Plano Piloto", 5302: "Gama", 5303: "Taguatinga", 5304: "Brazlândia",
    5305: "Sobradinho", 5306: "Planaltina", 5307: "Paranoá", 5308: "Núcleo Bandeirante",
    5309: "Ceilândia", 5310: "Guará", 5311: "Cruzeiro", 5312: "Samambaia",
    5313: "Santa Maria", 5314: "São Sebastião", 5315: "Recanto Das Emas", 5316: "Lago Sul",
    5317: "Riacho Fundo", 5318: "Lago Norte", 5319: "Candangolândia", 5320: "Águas Claras",
    5321: "Riacho Fundo II", 5322: "Sudoeste e Octogonal", 5323: "Varjão", 5324: "Park Way",
    5325: "SCIA", 5326: "Sobradinho II", 5327: "Jardim Botânico", 5328: "Itapoã",
    5329: "SIA", 5330: "Vicente Pires", 5331: "Fercal", 5332: "Sol Nascente / Pôr do Sol",
    5333: "Arniqueira", 5334: "Arapoanga", 5335: "Água Quente", 5336: "Área Rural",
}

# Rótulos das variáveis derivadas de dicionário/categoria (evitam "1", "2", "3" crus na tela)
ROTULOS_SEXO = {1: "Masculino", 2: "Feminino"}
ROTULOS_ID_GENERO = {1: "Cisgênero", 2: "Transgênero", 3: "Outro"}
ROTULOS_COR_RACA = {1: "Branca", 2: "Preta", 3: "Amarela", 4: "Parda", 5: "Indígena"}
ROTULOS_ARRANJOS = {
    1: "Unipessoal", 2: "Monoparental feminino", 3: "Casal com 1 filho",
    4: "Casal com 2 filhos", 5: "Casal com 3 filhos ou mais",
    6: "Casal sem filhos", 7: "Outro perfil",
}


def carregar_dados(caminho_moradores: str = CAMINHO_MORADORES,
                    caminho_domicilios: str = CAMINHO_DOMICILIOS) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Lê os microdados de moradores (CSV ';') e domicílios (XLSX) do PDAD,
    filtra para o Distrito Federal e já limpa os valores sentinela usados
    pelo recorte F."""
    moradores = pd.read_csv(
        caminho_moradores, sep=";", encoding="utf-8-sig",
        usecols=["A01nficha", "A01uf", "idade_calculada", "E03", "id_genero", "E05"],
    )
    domicilios = pd.read_excel(
        caminho_domicilios,
        usecols=["A01nficha", "A01uf", "localidade", "A01npessoas", "A01ncriancas", "arranjos"],
    )

    # Requisito 6: apenas Distrito Federal (A01uf == 53) — a amostra PDAD
    # inclui também municípios do entorno em Goiás (A01uf == 52), fora do
    # escopo deste recorte.
    moradores = moradores[moradores["A01uf"] == 53].drop(columns="A01uf")
    domicilios = domicilios[domicilios["A01uf"] == 53].drop(columns="A01uf")

    # Requisito 6: remover sentinelas 99999/88888 antes de qualquer cálculo.
    # idade_calculada e E03 (sexo) não têm sentinela nos dados reais, mas
    # filtramos mesmo assim por segurança/robustez do sistema.
    moradores = limpar_sentinelas(moradores, colunas=["idade_calculada", "E03"])
    domicilios = limpar_sentinelas(domicilios, colunas=["A01npessoas", "A01ncriancas", "arranjos"])

    domicilios = domicilios.copy()
    domicilios["localidade"] = domicilios["localidade"].map(MAPA_LOCALIDADES)
    domicilios = domicilios.dropna(subset=["localidade"])

    return moradores, domicilios


def limpar_sentinelas(df: pd.DataFrame, colunas: list[str]) -> pd.DataFrame:
    """Remove linhas em que qualquer uma das `colunas` contém um valor
    sentinela (99999 = não se aplica, 88888 = não declarado)."""
    filtro = pd.Series(True, index=df.index)
    for coluna in colunas:
        filtro &= ~df[coluna].isin(SENTINELAS)
    return df[filtro].copy()


def montar_base_unificada(moradores: pd.DataFrame, domicilios: pd.DataFrame) -> pd.DataFrame:
    """Junta (merge) moradores e domicílios por A01nficha, trazendo a RA
    (localidade) e o tamanho do domicílio para cada morador.

    Implementa o Diferencial D3 (merge entre as duas tabelas) — necessário
    porque a localidade só existe na tabela de domicílios.
    """
    return pd.merge(moradores, domicilios, on="A01nficha", how="inner")


def listar_localidades(domicilios: pd.DataFrame) -> list[str]:
    """Retorna a lista de RAs (localidades) presentes nos dados, ordenada."""
    return sorted(domicilios["localidade"].dropna().unique().tolist())
