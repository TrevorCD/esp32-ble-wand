/* esp32.ino
 *
 * device side program for magic wand project
 * implements BLE server for communication between stm32 and host
 *
 *-----------------------------------------------------------------------------
 *   Copyright 2026 Trevor B. Calderwood
 *
 *   Licensed under the Apache License, Version 2.0 (the "License");
 *   you may not use this file except in compliance with the License.
 *   You may obtain a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 *   Unless required by applicable law or agreed to in writing, software
 *   distributed under the License is distributed on an "AS IS" BASIS,
 *   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *   See the License for the specific language governing permissions and
 *   limitations under the License.
 *----------------------------------------------------------------------------*/

#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>

#define DEBUG_BLE 1
#define DEBUG_UART1 1

#define READ_TIMEOUT_MS 1000
#define CONNECT_TIMEOUT_MS 5000

#define UART1_MSG_LEN (sizeof(float) * 3)
#define UART1_RX_PIN 13
#define UART1_TX_PIN 12

/* Globals -------------------------------------------------------------------*/
/* Global BLE variables */
BLEServer* g_pServer;

const char* serviceUUID = "3cd00375-4415-4fe2-aa41-42bd35f1c526";
const char* characteristicUUID = "cc84a98c-36be-4fe1-8345-be620545fd34";

/* Global connection state variables */
enum BLEState {
  INIT,         // 0
  ADVERTISING,  // 1
  CONNECTED,    // 2
  READING,      // 3
  DISCONNECTED  // 4
};

BLEState g_state;
unsigned long lastReadTime;
unsigned long lastConnectTime;

/* Global UART variables */
uint8_t UART1_rx_buf[UART1_MSG_LEN];

/* TEST */
float TEST_UART1_rx_buf[3] = { 0.1f, 0.2f, 0.3f };
/* Helper functions ----------------------------------------------------------*/
void timeout() {
  g_state = DISCONNECTED;
}

/* BLE Callbacks -------------------------------------------------------------*/
class ServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      if(g_state != ADVERTISING) {
        #if DEBUG_BLE
        Serial.println("ERROR: Connection while state not advertising");
        Serial.print("State: ");
        Serial.println(g_state);
        #endif
      }
      g_state = CONNECTED;
      lastConnectTime = millis();
      #if DEBUG_BLE
      Serial.println("Connected");
      #endif
    }

    void onDisconnect(BLEServer* pServer) {
      #if DEBUG_BLE
      Serial.println("Disconnected");
      #endif
      g_state = DISCONNECTED;
    }
};

class CharacteristicCallbacks: public BLECharacteristicCallbacks {
  void onRead(BLECharacteristic* pCharacteristic) {
    #if DEBUG_BLE
    Serial.println("read callback");
    #endif
    if(g_state == CONNECTED) {
      g_state = READING;
    }
    else if(g_state != READING) {
      #if DEBUG_BLE
      Serial.print("ERROR: Read during state: ");
      Serial.println(g_state);
      for(;;){}
      #endif
    }
    // reset read timeout
    lastReadTime = millis();
    #if DEBUG_BLE
    Serial.print("lastReadTime: ");
    Serial.println(lastReadTime);
    #endif

    // set new value
    //pCharacteristic->setValue(UART1_rx_buf, UART1_MSG_LEN);
    pCharacteristic->setValue((uint8_t*)TEST_UART1_rx_buf, UART1_MSG_LEN);
  }
};

/* Main ----------------------------------------------------------------------*/
void setup() {
  #if DEBUG_BLE
  Serial.begin(115200);
  #endif
  // UART setup
  // rx = D13, tx = D12
  Serial1.begin(115200, SERIAL_8N1, UART1_RX_PIN, UART1_TX_PIN);

  // state initialization
  g_state = INIT;

  // BLE setup
  BLEDevice::init("ESP32MagicWand");
  BLEServer *pServer = BLEDevice::createServer();
  pServer->setCallbacks(new ServerCallbacks());
  g_pServer = pServer;
  BLEService *pService = pServer->createService(serviceUUID);
  
  BLECharacteristic *pCharacteristic = pService->createCharacteristic(
    characteristicUUID,
    BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_NOTIFY
  );
  pCharacteristic->setCallbacks(new CharacteristicCallbacks());
  pCharacteristic->setValue(0);
  pService->start();
}

void loop() {
  BLEAdvertising *pAdvertising = g_pServer->getAdvertising();

  #if DEBUG_BLE
  Serial.print("state: ");
  Serial.println(g_state);
  #endif

  // if buffer has full position vector, read into msg buffer
  /*
  if (Serial1.available() >= UART1_MSG_LEN) {
        Serial1.readBytes((uint8_t*)UART1_msg_buf, UART1_MSG_LEN);
  }
  */
  switch(g_state) {
    case INIT:
      pAdvertising->start();
      g_state = ADVERTISING;
      #if DEBUG_BLE
      Serial.println("Advertising started");
      #endif
      break;
    case ADVERTISING:

      break;
    case CONNECTED:
      if(lastConnectTime + CONNECT_TIMEOUT_MS < millis()) {
        #if DEBUG_BLE
        Serial.println("Connection timeout");
        #endif
        timeout();
      }
      break;
    case READING:
      if(lastReadTime + READ_TIMEOUT_MS < millis()) {
          #if DEBUG_BLE
          Serial.println("Reading timeout");
          #endif
          timeout();
        }
      break;
    case DISCONNECTED:
      pAdvertising->start();
      g_state = ADVERTISING;
      #if DEBUG_BLE
      Serial.println("Started advertising");
      #endif
      break;
  }
}