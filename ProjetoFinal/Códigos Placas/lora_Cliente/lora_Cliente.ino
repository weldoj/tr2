/**
 * @file cliente_tx_display.ino
 * @brief Cliente LoRa IOT com OLED + Deep Sleep (Heltec WiFi LoRa 32 V2).
 *
 * Exibe no display OLED os valores simulados de sensores, envia via LoRa,
 * e entra em deep sleep para economia de energia.
 */

#include <Arduino.h>
#include <SPI.h>
#include <LoRa.h>
#include <U8g2lib.h>
#include "esp_sleep.h"

// --- Pinos LoRa ---
#define LORA_SS   18
#define LORA_RST  14
#define LORA_DIO0 26

// Instância do display OLED
U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, U8X8_PIN_NONE);

// --- Configuração ---
#define INTERVALO_ENVIO 60   ///< intervalo em segundos

void mostrarDisplay(const String &l1, const String &l2 = "", const String &l3 = "") {
  u8g2.clearBuffer();
  u8g2.setFont(u8g2_font_6x12_tr);
  u8g2.drawStr(0, 12, l1.c_str());
  if (l2 != "") u8g2.drawStr(0, 28, l2.c_str());
  if (l3 != "") u8g2.drawStr(0, 44, l3.c_str());
  u8g2.sendBuffer();
}

void setup() {

  setCpuFrequencyMhz(80);   

  Serial.begin(115200);
  delay(200);

  // OLED
  u8g2.begin();
  mostrarDisplay("Cliente LoRa", "Acordou...");

  Serial.println("\n[CLIENTE] Acordou do Deep Sleep!");
  Serial.println("Inicializando LoRa...");

  // Inicialização LoRa
  LoRa.setPins(LORA_SS, LORA_RST, LORA_DIO0);
  if (!LoRa.begin(915E6)) {
    mostrarDisplay("ERRO:", "Falha no LoRa");
    delay(2000);
    esp_deep_sleep_start();
  }

  LoRa.setSpreadingFactor(9);
  LoRa.setSignalBandwidth(125E3);
  LoRa.setCodingRate4(5);
  LoRa.setTxPower(14);

  // --- Simula sensores ---
  float temperatura = random(2000, 3100) / 100.0;
  float umidade     = random(4000, 8100) / 100.0;

  // Payload JSON
  String payload = "{\"temperatura\": " + String(temperatura, 2) +
                   ", \"umidade\": " + String(umidade, 2) + "}";

  Serial.println("Enviando payload:");
  Serial.println(payload);

  mostrarDisplay("Enviando...", 
                 "Temp: " + String(temperatura, 2),
                 "Umid: " + String(umidade, 2));

  // Envia
  LoRa.beginPacket();
  LoRa.print(payload);
  LoRa.endPacket();

  mostrarDisplay("Pacote enviado!", "Dormindo...");

  Serial.println("Entrando em Deep Sleep por " + String(INTERVALO_ENVIO) + "s...");

  // Deep sleep
  esp_sleep_enable_timer_wakeup((uint64_t)INTERVALO_ENVIO * 1000000ULL);
  delay(800);
  esp_deep_sleep_start();
}

void loop() {}
