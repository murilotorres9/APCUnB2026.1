# Semana 07 — Abstração e modularização

**Refatoração dos simuladores anteriores:** os blocos repetidos do
semáforo (semana 5) e do contador (semana 6) no OctoStudio foram
reorganizados em **blocos customizados** (`mudar_estado()`, `incrementar()`),
evitando duplicação — o mesmo princípio DRY que motiva funções em Python.

**Comparação bloco customizado (OctoStudio) ↔ função (Python):**

| OctoStudio | Python |
|---|---|
| bloco customizado `mudar cor para (cor)` | `def mudar_cor(cor):` |
| parâmetro do bloco | parâmetro da função |
| "executar bloco" | chamar a função `mudar_cor("verde")` |

**Reflexão sobre abstração:** o OctoStudio já escondia a alocação de memória
das variáveis e o controle de fluxo interno do interpretador — o estudante só
via o bloco visual. Ao migrar para Python, expomos uma camada a mais de
abstração (a sintaxe textual), mas o conceito por trás — "empacotar um
comportamento reutilizável com um nome e parâmetros" — é o mesmo.
