# Tinkercad Circuits — Sensor ultrassônico + Arduino (Semana 13)

**Conceito principal:** função `medir()` reutilizável com teste automatizado
(ponte entre robótica virtual e testes de software).

**Circuito:** Arduino Uno + sensor ultrassônico HC-SR04 (pinos trigger/echo).

**Código (Arduino):**
```cpp
const int TRIG = 9;
const int ECHO = 10;

long medir() {                     // equivalente a def medir(): ... return
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);
  long duracao = pulseIn(ECHO, HIGH);
  return duracao * 0.034 / 2;      // distância em cm
}

void setup() {
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
  Serial.begin(9600);
}

void loop() {
  long distancia = medir();
  Serial.println(distancia);
  delay(500);
}
```

**"Teste automatizado":** no Tinkercad, simule aproximando/afastando o
sensor de um objeto e registre se o valor impresso no Serial Monitor
condiz com a distância esperada (equivalente manual a um doctest).

**Print do circuito:** _(adicione `sensor_ultrassonico.png`)_
