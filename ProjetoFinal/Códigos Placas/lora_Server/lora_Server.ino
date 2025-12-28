/**
 * @file servidor_rx_display.ino
 * @brief Servidor/Gateway LoRa com OLED (Heltec WiFi LoRa 32 V2).
 *
 * Recebe pacotes LoRa, imprime no Serial e mostra no display OLED
 * por um curto período para economizar energia.
 */

#include <SPI.h>
#include <LoRa.h>
#include <U8g2lib.h>

// --- Pinos LoRa ---
#define LORA_SS   18
#define LORA_RST  14
#define LORA_DIO0 26

// OLED
U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, U8X8_PIN_NONE);

#define OLED_TIMEOUT 1500  ///< tempo em ms para desligar display
unsigned long lastPacketTime = 0;
bool displayOn = false;

void mostrarDisplay(const String &l1, const String &l2 = "", const String &l3 = "") {
  u8g2.clearBuffer();
  u8g2.setFont(u8g2_font_6x12_tr);
  u8g2.drawStr(0, 12, l1.c_str());
  if (l2 != "") u8g2.drawStr(0, 28, l2.c_str());
  if (l3 != "") u8g2.drawStr(0, 44, l3.c_str());
  u8g2.sendBuffer();
}

void setup() {

  setCpuFrequencyMhz(40);   // economia máxima

  Serial.begin(9600);
  while (!Serial);

  // Inicia OLED desligado
  u8g2.begin();
  u8g2.setPowerSave(1);

  // Inicia LoRa
  LoRa.setPins(LORA_SS, LORA_RST, LORA_DIO0);
  if (!LoRa.begin(915E6)) {
    u8g2.setPowerSave(0);
    mostrarDisplay("ERRO:", "Falha LoRa");
    while (1);
  }

  LoRa.setSpreadingFactor(9);
  LoRa.setSignalBandwidth(125E3);
  LoRa.setCodingRate4(5);
  LoRa.enableCrc();

  Serial.println("Gateway LoRa pronto.");
}

void loop() {

  int packetSize = LoRa.parsePacket();
  if (packetSize) {

    String msg = "";
    while (LoRa.available()) {
      msg += (char)LoRa.read();
    }

    int rssi = LoRa.packetRssi();

    Serial.println(msg);

    // Liga OLED
    u8g2.setPowerSave(0);
    displayOn = true;
    lastPacketTime = millis();

    mostrarDisplay("Recebido:", msg, "RSSI: " + String(rssi));
  }

  // Desliga OLED após timeout
  if (displayOn && millis() - lastPacketTime > OLED_TIMEOUT) {
    u8g2.setPowerSave(1);
    displayOn = false;
  }

  delay(5);
}
