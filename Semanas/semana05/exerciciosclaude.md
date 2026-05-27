
# Aprendendo C — Exercícios com PythonTutor

**Disciplina:** Algoritmo e Programação de Computadores  
**Aluno:** Murilo Torres  
**Professor:** Jorge Henrique Cabral Fernandes (JHCF)  
**Semestre:** 2026.1

---

Repositório com exercícios práticos de linguagem C, desenvolvidos para serem visualizados passo a passo no [PythonTutor (modo C)](https://pythontutor.com/c.html). Cada exercício foca em um conceito fundamental e pode ser acompanhado observando o estado das variáveis, da pilha de chamadas (*call stack*) e do heap em tempo real.

---

## O que aprendi

### 1. Estrutura de um programa C
Entendi que todo programa C começa por `main`, que aparece na **pilha de chamadas** e é desempilhado quando `return 0` é executado. O `#include <stdio.h>` é necessário para usar funções de entrada e saída como `printf`.

---

### 2. Tipos primitivos e tamanhos
Aprendi os tipos básicos da linguagem (`char`, `int`, `long`, `float`, `double`) e seus tamanhos típicos em bytes. Usei o operador `sizeof` para inspecionar esses valores em tempo de execução e entendi os modificadores `unsigned`, `signed`, `short` e `long`.

---

### 3. Declaração e inicialização de variáveis
Entendi a diferença entre **declarar** e **inicializar** uma variável. Variáveis não inicializadas contêm "lixo de memória". Aprendi também a usar `const` para criar constantes somente leitura — qualquer tentativa de modificação gera erro de compilação.

---

### 4. Operadores
Pratiquei os principais operadores da linguagem:
- **Aritméticos:** divisão inteira vs. real, módulo (`%`)
- **Incremento:** diferença entre pré-incremento (`++x`) e pós-incremento (`x++`)
- **Ternário:** `cond ? a : b` como atalho para `if/else`
- **Lógicos e relacionais:** usados em condicionais

---

### 5. Controle de fluxo
Exercitei as principais estruturas de controle:
- `if / else if / else` para ramificações condicionais
- `for` com `break` e `continue` para controle fino do laço
- `do-while`, onde o corpo executa **antes** do teste da condição
- `switch` com *fall-through* intencional para agrupar casos

---

### 6. Funções e pilha de chamadas
Aprendi a criar funções com protótipos, a passar argumentos por valor e por **referência** (via ponteiro). Visualizei no PythonTutor como os frames empilham e desempilham, especialmente em funções **recursivas** como o cálculo do fatorial.

---

### 7. Arrays
Entendi como declarar e acessar arrays unidimensionais e matrizes (`int m[2][3]`). C **não** verifica limites em tempo de execução, então acessar fora do array é um erro silencioso e perigoso.

---

### 8. Strings
Aprendi que strings em C são arrays de `char` terminados com `'\0'`. Usei funções da `<string.h>` como `strlen`, `strcpy` e `strcmp`. Entendi a diferença entre `char s[]` (array mutável) e `char *p` (ponteiro para literal imutável).

---

### 9. Ponteiros
Este foi um dos tópicos mais importantes. Aprendi:
- O que é um ponteiro e como declarar (`int *p = &x`)
- **Derreferência** (`*p`) para ler/escrever via ponteiro
- **Aritmética de ponteiros** e equivalência com índices de array
- **Ponteiro para ponteiro** (`int **pp`) e dois níveis de indireção

No PythonTutor, visualizei ponteiros como **setas** apontando para variáveis, o que tornou o conceito muito mais concreto.

---

### 10. Alocação dinâmica de memória
Aprendi a diferença entre **stack** (variáveis locais, automáticas) e **heap** (alocação manual). Usei `malloc` para alocar memória dinamicamente e `free` para liberá-la. Entendi que esquecer o `free` causa *memory leak* e que usar a memória após o `free` é comportamento indefinido.

---

### 11. Structs e Unions
Aprendi a criar tipos compostos com `struct` e a acessar membros com `.` (acesso direto) ou `->` (via ponteiro). Com `union`, entendi que todos os membros **compartilham o mesmo espaço de memória** — escrever em um campo sobrescreve os demais.

---

### 12. Enums
Aprendi a criar enumerações com `typedef enum`, que são tratadas internamente como `int`. Combinei `enum` com `switch` para criar código legível e seguro.

---

### 13. Entrada e Saída básica
Pratiquei os principais especificadores de formato do `printf` (`%d`, `%f`, `%c`, `%s`, `%x`, `%p`) e entendi por que o `scanf` exige o operador `&` — ele precisa do **endereço** da variável para escrever o valor lido.

---

### 14. Pré-processador
Aprendi a usar `#define` para criar constantes simbólicas e **macros com parâmetros**. Entendi a armadilha clássica de macros sem parênteses e como efeitos colaterais em argumentos (como `a++`) podem causar bugs sutis.

---

### 15. Escopo e duração de variáveis
Entendi as diferentes classes de armazenamento:
- **Automática:** existe apenas dentro do bloco `{}`
- **`static` local:** persiste entre chamadas da função, mas o escopo continua local
- **`static` global:** visível apenas no arquivo `.c` onde foi declarada

Visualizei no PythonTutor como variáveis `static` aparecem **fora** do frame da função, mesmo sendo declaradas dentro dela.

---

### 16. Boas práticas
Aprendi práticas essenciais para escrever C seguro:
- Sempre inicializar variáveis
- Preferir `strncpy` e `snprintf` para evitar estouro de buffer
- Verificar o retorno de `malloc` e `fopen`
- Parear todo `malloc` com um `free`
- Usar `const` quando um valor não deve ser modificado
- Compilar com `-Wall -Wextra -fsanitize=address`

---

## Como executar os exercícios

1. Acesse [pythontutor.com/c.html](https://pythontutor.com/c.html)
2. Cole o código do exercício desejado
3. Clique em **"Visualize Execution"**
4. Use os botões **Next** e **Prev** para avançar passo a passo
5. Observe o estado das variáveis, da stack e do heap em tempo real

> **Dica:** Ative **"Show all frames"** para ver funções recursivas empilhando. Use **"Generate permanent link"** para salvar e compartilhar exercícios.
