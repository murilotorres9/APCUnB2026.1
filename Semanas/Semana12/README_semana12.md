# Semana 12 — Estruturas de dados heterogêneas: agenda de contatos

**Conceito principal:** dicionários (chave-valor, hashing intuitivo, CRUD),
tuplas (imutabilidade, registros/structs), JSON como ponte entre programas.

## Arquivos

- **`dicionarios_crud.py`** — explica hashing intuitivo (por que `dict` é
  O(1) médio) e demonstra as 4 operações CRUD (Create, Read, Update, Delete)
  num dicionário.
- **`tuplas.py`** — demonstra imutabilidade de tuplas e seu uso como
  registro/struct (ex.: uma escola representada como `(codigo, nome, nota)`).
- **`agenda_contatos.py`** — Simulador 9: agenda de contatos com dicionários
  aninhados, busca por nome e exportação/leitura em JSON (`agenda.json`).
- **`catalogo_escolas_df.py`** — aplicação com dados reais: dicionário de
  escolas do DF (rede, localização, proficiência) consultável por código
  INEP, exportado em `escolas_df.json`. Usa o CSV da semana 11 como fonte.
- **`comparacao_linguagens.md`** — como Python, JavaScript, Java e C lidam
  com estruturas chave-valor, registros e serialização JSON.
- **`octostudio_banco_personagens.md`** — documentação do simulador
  OctoStudio (banco de personagens como analogia visual a dicionários).

## Como rodar

```bash
python3 dicionarios_crud.py
python3 tuplas.py
python3 agenda_contatos.py
python3 catalogo_escolas_df.py

python3 -m doctest tuplas.py -v
python3 -m doctest agenda_contatos.py -v
python3 -m doctest catalogo_escolas_df.py -v
```


