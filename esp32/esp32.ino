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
#include <BLE2902.h>

#define DEBUG 1

#define READ_TIMEOUT_MS 5000

/* Globals -------------------------------------------------------------------*/
/* Global BLE variables */

const char * serviceUUID = "3cd00375-4415-4fe2-aa41-42bd35f1c526";
const char * characteristicUUID = "cc84a98c-36be-4fe1-8345-be620545fd34";

/* Global connection state variables */
int connected;
int readingStarted; // init 0, set 1 on first read, set 0 on disconnect or timeout
unsigned long lastReadTime = 0;

#if DEBUG
int disconnected = 0;
#endif

/* BLE Callbacks -------------------------------------------------------------*/
class ServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      connected = 1;
      lastReadTime = millis(); // for initial read timeout time
      #if DEBUG
      Serial.println("Connected");
      #endif
    }

    void onDisconnect(BLEServer* pServer) {
      #if DEBUG
      disconnected = 1;
      Serial.println("Disconnected");
      Serial.println("Starting advertising");
      #endif
      connected = 0;
      readingStarted = 0;
      BLEAdvertising* pAdvertising = pServer->getAdvertising
      pAdvertising->start();  // restart advertising
    }
};

class CharacteristicCallbacks: public BLECharacteristicCallbacks {
  void onRead(BLECharacteristic* pCharacteristic) {
    #if DEBUG
    Serial.println("read callback");
    #endif
    if(readingStarted == 0)
    {
      readingStarted = 1;
    }
    // reset read timeout
    lastReadTime = millis();
    #if DEBUG
    Serial.print("lastReadTime: ");
    Serial.println(lastReadTime);
    #endif
    // get new value from stm32

    // set new value
    /// for testing:
    pCharacteristic->setValue(1);
  }
};

/* Helper functions ----------------------------------------------------------*/
void timeout()
{
  connected = 0;
  readingStarted = 0;
  pAdvertising->start();
  #if DEBUG
  Serial.println("Read timeout occured");
  Serial.println("Advertise start");
  #endif
}

/* Main ----------------------------------------------------------------------*/
void setup()
{
  #if DEBUG
  Serial.begin(9600);
  #endif
  // pin setup

  // state initialization
  connected = 0;
  readingStarted = 0;

  // BLE setup
  BLEDevice::init("ESP32MagicWand");
  BLEServer *pServer = BLEDevice::createServer();
  pServer->setCallbacks(new ServerCallbacks());

  BLEService *pService = pServer->createService(serviceUUID);
  
  BLECharacteristic *pCharacteristic = pService->createCharacteristic(
    characteristicUUID,
    BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_NOTIFY
  );
  pCharacteristic->setCallbacks(new CharacteristicCallbacks());
  pCharacteristic->setValue(1);
  pService->start();

  BLEAdvertising *pAdvertising = pServer->getAdvertising();
  pAdvertising->start();

  #if DEBUG
  Serial.println("Advertising started");
  #endif

}

void loop()
{
  Serial.print(disconnected);
  Serial.print(connected);
  Serial.println(readingStarted);
  if(connected == 1 && readingStarted == 1 && (lastReadTime + READ_TIMEOUT_MS < millis()))
  {
    #if DEBUG
    Serial.print("millis: ");
    Serial.print(millis());
    #endif
    Serial.print("connected: ");
    Serial.println(connected);
    Serial.print("ReadingStarted: ");
    Serial.println(readingStarted);
    timeout();
  }
}
