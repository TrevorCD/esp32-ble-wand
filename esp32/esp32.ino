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

int connected;

class ServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      connected = 1;
      #if DEBUG
      Serial.println("Connected");
      #endif
    }

    void onDisconnect(BLEServer* pServer) {
      BLEDevice::getAdvertising()->start();  // restart advertising
      #if DEBUG
      Serial.println("Disconnected");
      Serial.println("Starting advertising");
      #endif
    }
};

class CharacteristicCallbacks: public BLECharacteristicCallbacks {
  void onRead(BLECharacteristic* pCharacteristic) {
    #if DEBUG
    Serial.println("read callback");
    #endif
    // get new value from stme32

    // set new value
    /// for testing:
    pCharacteristic->setValue(1);
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
  pCharacteristic->setCallbacks(new CharacteristicCallbacks());
  pCharacteristic->setValue(1);
  pService->start();

  connected = 0; 

  pAdvertising = pServer->getAdvertising();
  pAdvertising->start();

  #if DEBUG
  Serial.println("Advertising started");
  #endif

}

void loop()
{

}
