#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

#define DEBUG 1

BLECharacteristic *pCharacteristic;
BLEServer *pServer;
BLEService *pService;
BLEAdvertising * pAdvertising;

char * serviceUUID = "3cd00375-4415-4fe2-aa41-42bd35f1c526";
char * characteristicUUID = "cc84a98c-36be-4fe1-8345-be620545fd34";

class ServerCallbacks : public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
        #if DEBUG
        Serial.println("Connected");
        #endif
    }

    void onDisconnect(BLEServer* pServer) {
        BLEDevice::getAdvertising()->start();  // restart advertising
        #if DEBUG
        Serial.println("Disconnected. Advertising started");
        #endif
    }
};

void setup()
{
  #if DEBUG
  Serial.begin(9600);
  Serial.println("Setup started");
  #endif
  // pin setup

  // BLE setup
  BLEDevice::init("ESP32MagicWand");
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new ServerCallbacks());

  pService = pServer->createService(serviceUUID);
  
  pCharacteristic = pService->createCharacteristic(
    characteristicUUID,
    BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_NOTIFY
  );

  pCharacteristic->setValue("Hello world");
  pService->start();

  pAdvertising = pServer->getAdvertising();
  pAdvertising->start();

  #if DEBUG
  Serial.println("Advertising started");
  #endif
}

void loop()
{
  // Wait on connection

  // while connected:
  //   get data from stm32

  //   send data over bluetooth

}
