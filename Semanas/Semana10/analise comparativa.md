# Semana 10 — Análise comparativa: OctoStudio vs Python

| Simulador | OctoStudio (semana) | Python (semana 10) | O que muda |
|---|---|---|---|
| Semáforo inteligente | Bloco `se estado = ...` acionado por toque | Função `proximo_estado()` chamada em um laço `for` | A lógica de mudança de estado passa a ser implementada em uma função reutilizável, facilitando testes e manutenção do código. |
| Contador automático | Bloco `repita N vezes` atualizando uma variável exibida na tela | `for _ in range(limite)` acumulando valores em uma lista | Em Python, os dados podem ser armazenados e reutilizados em outras partes do programa, em vez de apenas serem exibidos na interface. |

## Reflexão

No OctoStudio, o estado do semáforo era armazenado em uma variável utilizada apenas durante a execução do projeto visual. Já em Python, essa mesma lógica pode ser representada por uma função como `proximo_estado()`, que recebe um estado de entrada e retorna o próximo estado sem alterar outras partes do programa. Essa abordagem facilita a realização de testes, como os feitos com `doctest`, além de tornar o código mais organizado, reutilizável e fácil de compreender.

## Matriz 3×3 de LEDs (Tinkercad)

**Descrição:**  
Na simulação da matriz 3×3 de LEDs, foram utilizados laços aninhados para controlar as linhas e colunas da matriz. O primeiro laço percorre cada linha, enquanto o segundo percorre todas as colunas dessa linha, acendendo ou apagando os LEDs conforme o padrão desejado. Esse tipo de estrutura permite controlar vários LEDs de forma organizada e eficiente, evitando a necessidade de escrever comandos individuais para cada posição da matriz.
