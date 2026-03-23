#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

BLECharacteristic *pCharacteristic;
BLEServer *pServer;
BLEService *pService;
BLEAdvertising * pAdvertising;

char * serviceUUID = "3cd00375-4415-4fe2-aa41-42bd35f1c526";
char * characteristicUUID = "cc84a98c-36be-4fe1-8345-be620545fd34";

void setup()
{
  // pin setup

  // BLE setup
  BLEDevice::init("ESP32MagicWand");
  pServer = BLEDevice::createServer();
  pService = pServer->createService(serviceUUID);
  
  pCharacteristic = pService->createCharacteristic(
    "characteristicUUID",
    BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_NOTIFY
  );

  pCharacteristic->setValue("Hello world");
  pService->start();

  pAdvertising = pServer->getAdvertising();
  pAdvertising->start();
}

void loop()
{
  // Wait on connection

  // while connected:
  //   get data from stm32

  //   send data over bluetooth

}
