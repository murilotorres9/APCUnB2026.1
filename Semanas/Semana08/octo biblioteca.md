# Simulador OctoStudio — Biblioteca de Blocos Reutilizáveis (Semana 8)

**Conceito principal:** Funções (blocos customizados com parâmetros).

**Descrição:** Foi criada uma biblioteca de blocos personalizados para reutilizar comportamentos desenvolvidos em simuladores anteriores. Entre os blocos implementados estão `alternar_estado()`, responsável por mudar o estado do semáforo; `incrementar(valor)`, que aumenta o valor de um contador; e `somar(a, b)`, utilizado para realizar a soma de dois valores. O objetivo foi reduzir a repetição de código e facilitar a reutilização das mesmas ações em diferentes partes do projeto.

**Correspondência com Python:**
```text
bloco customizado "somar (a) (b)"  →  def somar(a, b): return a + b
```


**Reflexão breve:**  
O bloco mais fácil de generalizar com parâmetros foi **`somar(a, b)`**, pois sua lógica é simples e pode ser utilizada em diferentes situações apenas alterando os valores de entrada. Isso mostrou como o uso de parâmetros torna uma função mais flexível e reutilizável, evitando a criação de vários blocos para executar praticamente a mesma tarefa.
