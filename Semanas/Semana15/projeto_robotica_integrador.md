# Tinkercad Circuits — Projeto integrador de robótica (Semana 15)

**Conceito principal:** simulador ambiental com múltiplos sensores, lógica
de alerta e log de dados — integrando tudo que foi visto nas semanas de
Tinkercad (LED piscando, matriz de LEDs, sensor ultrassônico).

**Circuito:** Arduino Uno + sensor de temperatura (ex.: TMP36) + sensor
ultrassônico HC-SR04 (simulando nível de água/distância) + LED vermelho
(alerta) + LED verde (normal).

**Lógica de alerta:**
```
ler temperatura
ler distância (nível)
se temperatura > limite_temperatura OU distância < limite_critico
    acender LED vermelho
    registrar leitura no log (Serial Monitor) com marcação "ALERTA"
senão
    acender LED verde
    registrar leitura no log com marcação "normal"
```

**Código (Arduino):**
```cpp
const int PINO_TEMP = A0;
const int TRIG = 9;
const int ECHO = 10;
const int LED_ALERTA = 12;
const int LED_NORMAL = 13;

const float LIMITE_TEMPERATURA = 30.0;  // graus Celsius
const long LIMITE_CRITICO = 10;         // cm

float lerTemperatura() {
  int leitura = analogRead(PINO_TEMP);
  float tensao = leitura * (5.0 / 1024.0);
  return (tensao - 0.5) * 100.0;  // conversão típica do TMP36
}

long medirDistancia() {
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  long duracao = pulseIn(ECHO, HIGH);
  return duracao * 0.034 / 2;
}

void setup() {
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
  pinMode(LED_ALERTA, OUTPUT);
  pinMode(LED_NORMAL, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  float temperatura = lerTemperatura();
  long distancia = medirDistancia();
  bool alerta = (temperatura > LIMITE_TEMPERATURA) || (distancia < LIMITE_CRITICO);

  digitalWrite(LED_ALERTA, alerta ? HIGH : LOW);
  digitalWrite(LED_NORMAL, alerta ? LOW : HIGH);

  Serial.print(temperatura);
  Serial.print(" C, ");
  Serial.print(distancia);
  Serial.print(" cm - ");
  Serial.println(alerta ? "ALERTA" : "normal");

  delay(1000);
}
```

**Conexão com Python:** a mesma lógica de alerta (`temperatura > limite OU
distancia < limite`) é a estrutura condicional composta vista desde a
semana 4 (`and`/`or`) — o Arduino só troca `print()` por `Serial.println()`
e a leitura de sensores físicos no lugar de `input()`.

**Print do circuito:** _(adicione `projeto_robotica_integrador.png`)_

**Reflexão breve:** _(qual conceito das 15 semanas você reconhece mais
claramente neste projeto final de robótica: condicionais, funções, ou
estruturas de dados do log?)_
