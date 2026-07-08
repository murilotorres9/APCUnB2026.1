# Simulador OctoStudio — Banco de personagens (Semana 12)

**Conceito principal:** analogia visual a dicionários (chave-valor).

**Descrição:** cada personagem (sprite) do projeto representa uma "chave"
(o nome do personagem), e seus atributos — cor, tamanho, mensagem — são os
"valores" associados a ele. Tocar em um personagem "consulta" seus
atributos, da mesma forma que `banco[nome]` consulta um valor num
dicionário Python.

**Correspondência com Python:**
```
sprite "Ana" com atributos (cor=azul, mensagem="Oi!")
    ↕
banco = {"Ana": {"cor": "azul", "mensagem": "Oi!"}}
```

**Pseudocódigo:**
```
banco_personagens <- {}
para cada sprite criado
    banco_personagens[nome_do_sprite] <- {cor, mensagem}
ao tocar em um sprite
    mostrar banco_personagens[nome_do_sprite]
```

**Print do projeto:** _(adicione `banco_personagens.png` exportado do OctoStudio)_

**Reflexão breve:** _(em que momento ficou mais claro que "procurar pelo
nome" no Scratch é a mesma ideia de `dicionario[chave]` em Python?)_
