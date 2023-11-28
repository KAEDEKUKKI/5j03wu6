// MyCrypto.h
#ifndef MyCrypto_h
#define MyCrypto_h

#include <Arduino.h>
#include <Crypto.h>
#include <SHA256.h>
#include <AES.h>
#include <ChaChaPoly.h>

class MyCrypto {
public:
  MyCrypto();

  void serverHello(uint8_t* receive, uint8_t* result) ;
  void certificate(uint8_t* receive);
  void createSession();
  bool verify(uint8_t* key);
  void encryptImage(const uint8_t* originalImage, uint8_t* encryptedImage, size_t imageSize);
  String getAllVariables();
  String byteArrayToString(const uint8_t *array, int length);
  
private:
  SHA256 shaLib;
  AES256 aesLib;
  const int HASH_SIZE = 32;

  uint8_t rr[3][32];  // Using a 2D array to store byte data
  uint8_t mm[32];
  uint8_t IDi[32];
  uint8_t yi[32];
  uint8_t x[32];
  uint8_t session_key[32];
  void hash(SHA256* shaLib, const uint8_t *data, uint8_t *hashResult, size_t dataSize);
  void encryptAES(AES256* aesLib, const uint8_t *input, uint8_t *output, uint8_t *key);
  void decryptAES(AES256* aesLib, const uint8_t *input, uint8_t *output, uint8_t *key);
  void generateRandomData(uint8_t *dataR);
};

#endif
