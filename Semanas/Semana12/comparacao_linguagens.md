# Comparação — Estruturas de dados heterogêneas em outras linguagens

| Conceito | Python | JavaScript | Java | C |
|---|---|---|---|---|
| Chave-valor | `dict` — `{"nome": "Ana"}` | `Object` ou `Map` — `{nome: "Ana"}` | `HashMap<String, String>` | não tem nativo; usa-se struct + hash table manual |
| Registro fixo (struct) | `tuple` ou `dataclass` | objeto literal `{}` (sem imutabilidade nativa) | `record` (Java 16+) ou classe | `struct` |
| Imutabilidade | `tuple` é imutável; `dict`/`list` são mutáveis | `const` só impede reatribuição, não imutabilidade profunda | `final` em campos; `record` é imutável | `const` em campos do struct |
| Serialização (dados como ponte) | `json.dumps()` / `json.loads()` | `JSON.stringify()` / `JSON.parse()` (nativo da linguagem) | biblioteca externa (Jackson, Gson) | biblioteca externa (cJSON) |

**Reflexão:** o Python e o JavaScript têm a vantagem de já "pensar em JSON"
de forma quase nativa — um `dict` Python e um objeto JavaScript se
convertem quase 1:1 para JSON. Já em linguagens como Java e C, é preciso
uma etapa explícita de serialização com bibliotecas externas, porque essas
linguagens têm tipos mais rígidos (statically typed) e não têm uma
estrutura chave-valor "solta" como o `dict`.

**Por que usar tupla em vez de dicionário para um registro?** Quando os
campos são fixos e a ordem importa mais que o nome (ex.: coordenadas
`(x, y)`), a tupla é mais leve e comunica a intenção de "isso não deveria
mudar". Quando os campos têm nomes que precisam ser consultados (ex.:
`contato["telefone"]`), o dicionário é mais legível.
