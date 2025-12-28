#include <SPI.h>
#include <LoRa.h>
#include <U8g2lib.h> // Biblioteca para o display OLED

// --- Definição dos Pinos LoRa (Padrão Heltec) ---
#define LORA_SS_PIN    18
#define LORA_RST_PIN   14
#define LORA_DIO0_PIN  26

// --- Definição dos Pinos do OLED (Padrão Heltec) ---
#define OLED_SDA   4
#define OLED_SCL   15
#define OLED_RST   16 // Reset do OLED

// Inicializa o objeto do display U8g2
U8G2_SSD1306_128X64_NONAME_F_SW_I2C u8g2(U8G2_R0, /* clock=*/ OLED_SCL, /* data=*/ OLED_SDA, /* reset=*/ OLED_RST);

int counter = 0;

void setup() {
  Serial.begin(115200);
  
  // --- Inicializa o Display ---
  pinMode(OLED_RST, OUTPUT);
  digitalWrite(OLED_RST, LOW);    // Reseta o OLED
  delay(20);
  digitalWrite(OLED_RST, HIGH);   // Tira o OLED do reset
  
  u8g2.begin(); // Inicia o display
  u8g2.clearBuffer();
  u8g2.setFont(u8g2_font_ncenB10_tr); // Define uma fonte
  u8g2.drawStr(0, 20, "Cliente LoRa");
  u8g2.drawStr(0, 40, "Iniciando...");
  u8g2.sendBuffer(); // Envia o buffer para a tela
  
  // --- Inicializa o LoRa ---
  Serial.println("LoRa Sender (Cliente #1)");
  LoRa.setPins(LORA_SS_PIN, LORA_RST_PIN, LORA_DIO0_PIN);
  
  if (!LoRa.begin(915E6)) { // 915MHz (Brasil/Américas)
    Serial.println("Erro ao iniciar LoRa!");
    u8g2.clearBuffer();
    u8g2.drawStr(0, 20, "Erro LoRa!");
    u8g2.sendBuffer();
    while (1);
  }

  Serial.println("LoRa iniciado com sucesso!");
  u8g2.clearBuffer();
  u8g2.drawStr(0, 20, "LoRa OK!");
  u8g2.drawStr(0, 40, "Enviando...");
  u8g2.sendBuffer();
  delay(1000);
}

void loop() {
  String packetToSend = "Dados: " + String(counter);
  
  Serial.print("Enviando pacote: ");
  Serial.println(packetToSend);

  // Atualiza o display
  u8g2.clearBuffer();
  u8g2.setFont(u8g2_font_ncenB10_tr);
  u8g2.drawStr(0, 20, "Cliente LoRa");
  u8g2.setFont(u8g2_font_ncenB08_tr); // Fonte menor
  u8g2.drawStr(0, 40, "Enviando pacote:");
  u8g2.drawStr(0, 55, packetToSend.c_str()); // .c_str() é necessário
  u8g2.sendBuffer();

  // Envia o pacote LoRa
  LoRa.beginPacket();
  LoRa.print(packetToSend);
  LoRa.endPacket();

  counter++;
  delay(10000); // Envia a cada 10 segundos
}