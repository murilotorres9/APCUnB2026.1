# PDAD Explorer — Perfil demográfico e composição domiciliar (Recorte F)

## Descrição

Sistema com interface gráfica (tkinter) para explorar o perfil demográfico
e a composição domiciliar do Distrito Federal a partir dos microdados da
PDAD 2024. O sistema junta (merge) a tabela de moradores com a de
domicílios por `A01nficha`, permitindo visualizar a **pirâmide etária por
sexo**, a **distribuição de domicílios por tamanho e tipo de arranjo
familiar**, e um perfil complementar de **identidade de gênero** e
**cor/raça**, tudo filtrável por Região Administrativa. O usuário pode
exportar as estatísticas filtradas para `.csv` ou `.txt`.

## Integrantes

- Murilo Torres

## Como executar

```bash
pip install -r requirements.txt
python sistema.py
```

O sistema já vem com uma **amostra real** de 1.200 domicílios (e os
moradores correspondentes) extraída dos microdados completos, apenas do
Distrito Federal, em `dados/`. Para rodar com a base completa, baixe os
arquivos oficiais em https://pdad.ipe.df.gov.br e substitua:

- `PDAD_2024-Moradores.csv` → `dados/moradores_parcial.csv`
- `PDAD_2024-Domicilios.xlsx` → `dados/domicilios_parcial.xlsx`

(mantendo o CSV com separador `;` e o Excel com as mesmas colunas).

## Dependências

```
pip install pandas matplotlib openpyxl
```

## Arquivos de dados necessários e colunas usadas

- `dados/moradores_parcial.csv` (separador `;`): `A01nficha`, `A01uf`,
  `idade_calculada`, `E03` (sexo), `id_genero`, `E05` (cor/raça)
- `dados/domicilios_parcial.xlsx`: `A01nficha`, `A01uf`, `localidade`
  (código da RA), `A01npessoas`, `A01ncriancas`, `arranjos` (tipo de
  arranjo familiar)

> Os arquivos incluídos neste repositório são uma **amostra real** (não
> sintética) de 1.200 domicílios do DF, extraída dos microdados completos
> fornecidos em sala, para manter o repositório leve. Os arquivos
> completos devem ser baixados separadamente em
> https://pdad.ipe.df.gov.br.

## Decisões de análise importantes

- **`localidade` vem como código numérico** nos microdados (ex: 5301),
  não como nome de RA. O sistema mapeia o código para o nome usando a
  tabela do Anexo 1 do dicionário de variáveis (`utils/carregar.py::MAPA_LOCALIDADES`).
- **Filtramos `A01uf == 53`** (Distrito Federal): a amostra do PDAD
  também inclui municípios do entorno em Goiás (`A01uf == 52`), fora do
  escopo deste recorte.
- **A pirâmide etária usa `E03` (Sexo), não `id_genero`.** `id_genero` é
  a variável derivada "Composição entre a resposta de sexo de nascimento
  e identidade de gênero" e tem o sentinela 99999 ("não se
  aplica/sem classificação") concentrado em crianças, que não respondem
  esse bloco do questionário. Usar `id_genero` na pirâmide etária
  excluiria as faixas mais jovens quase por completo. Por isso, `id_genero`
  é analisado separadamente, como um recorte complementar sobre a
  população que respondeu a pergunta (aba "Arranjo familiar e perfil").
- **`E05` é "Cor ou raça"**, não estado civil — usada na mesma aba
  complementar.
- **`arranjos`** é a variável derivada de "tipo de arranjo familiar"
  pedida no enunciado do recorte F (Unipessoal, Casal com filhos, etc.),
  calculada pelo próprio PDAD a partir da composição do domicílio.

## Tratamento de valores sentinela

`utils/carregar.py::limpar_sentinelas()` remove explicitamente as linhas
em que `idade_calculada`, `E03`, `A01npessoas`, `A01ncriancas` ou
`arranjos` contêm 99999 ("não se aplica") ou 88888 ("não declarado"),
antes de qualquer cálculo estatístico. `id_genero` tem seu sentinela
tratado separadamente em `calcular_perfil_complementar()`, já que ali o
sentinela é informativo (indica quem não respondeu) em vez de ser
simplesmente descartado da base toda.

## Diferenciais implementados

- **D1 — Mais de um gráfico de tipo diferente:** pirâmide etária (barras
  horizontais divergentes), distribuição de domicílios por tamanho
  (barras verticais) e distribuição por arranjo familiar (barras
  horizontais).
- **D3 — Merge entre as duas tabelas:** `utils/carregar.py::montar_base_unificada()`
  cruza moradores e domicílios por `A01nficha` para trazer a RA (que só
  existe na tabela de domicílios) para cada morador.
- **D4 — Ordenação implementada à mão:** `utils/calcular.py::ordenar_ras_por_tamanho_medio()`
  usa Selection Sort implementado manualmente para o ranking de RAs,
  em vez de `.sort_values()` do pandas.

## Estrutura do repositório

```
pdad-explorer-dupla/
├── sistema.py              ← arquivo principal (python sistema.py)
├── utils/
│   ├── carregar.py         ← leitura, mapeamento de RA, limpeza de sentinelas e merge
│   ├── calcular.py         ← estatísticas, pirâmide etária, arranjos, ordenação manual
│   └── exportar.py         ← exportação para .csv/.txt
├── dados/
│   ├── moradores_parcial.csv     ← amostra real (DF), 1.200 domicílios
│   └── domicilios_parcial.xlsx   ← amostra real (DF), 1.200 domicílios
├── README.md
└── requirements.txt
```
