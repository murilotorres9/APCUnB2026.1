# Simulador OctoStudio — Contador Automático (Semana 6)

**Conceito principal:** Repetição / Loop.

**Descrição:** Um bloco `repita 10 vezes` incrementa uma variável `contador` em 1 a cada iteração, com um pequeno atraso entre as repetições. A cada incremento, o valor do contador é exibido na tela do sprite, criando uma animação de contagem. Ao final das dez repetições, é reproduzido um som e uma animação indicando o término da contagem.

**Pseudocódigo:**
```text
contador <- 0
repita 10 vezes
    contador <- contador + 1
    mostrar contador
    esperar 0.5 segundos
```

**Reflexão breve:**  
O bloco **`repita N vezes`** do OctoStudio corresponde, em Python, à estrutura **`for`** utilizando a função **`range()`**. Ambos executam um conjunto de instruções uma quantidade determinada de vezes, sendo muito úteis para automatizar tarefas repetitivas e evitar a repetição desnecessária de código.
