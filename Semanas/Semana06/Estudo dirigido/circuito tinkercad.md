# Tinkercad Circuits — LED piscando (Semana 6)

**Conceito principal:** Loops, robótica virtual como analogia corporal a laços de repetição.

**Circuito:** Arduino Uno + 1 LED + resistor de 220 Ω conectado ao pino digital 13.

**Código (Arduino, estrutura equivalente a `while True`):**
```cpp
void setup() {
  pinMode(13, OUTPUT);
}

void loop() {                 // equivalente ao while True do Python
  digitalWrite(13, HIGH);
  delay(500);
  digitalWrite(13, LOW);
  delay(500);
}
```


**Reflexão breve:**  
A função `loop()` do Arduino é executada continuamente enquanto a placa estiver ligada, fazendo com que o programa repita suas instruções indefinidamente. Esse comportamento é semelhante ao de um `while True` em Python, pois ambos executam um bloco de código sem um número definido de repetições. A principal diferença é que, no Arduino, o `loop()` faz parte da estrutura padrão da linguagem e é chamado automaticamente pelo sistema, enquanto em Python o `while True` precisa ser escrito explicitamente pelo programador e normalmente exige uma condição de interrupção (`break`) para encerrar sua execução.
