//MyCrypto.cpp
#include "MyCrypto.h"

MyCrypto::MyCrypto() {
  // 初始化
  for (int i = 0; i < 3; i++) {
    memset(rr[i], 0, HASH_SIZE);
  }

  const char *xString = "5j03wu6";
  hash(&shaLib, (const uint8_t *)xString, x, 7); 
}

void MyCrypto::serverHello(uint8_t* receive, uint8_t* result) {
  //Decrypt(IDi, R0)
  for (size_t i = 0; i < HASH_SIZE*2; i+=16) {
    decryptAES(&aesLib, receive+i, receive+i, x);
  }
  memcpy(IDi, receive, HASH_SIZE);
  memcpy(rr[0], receive + HASH_SIZE, HASH_SIZE);

  uint8_t temp1[HASH_SIZE*2];
  uint8_t temp2[HASH_SIZE*3];
  
  // Hash(IDi + x) and store the result in yi
  memcpy(temp1, IDi, HASH_SIZE);
  memcpy(temp1 + HASH_SIZE, x, HASH_SIZE);
  hash(&shaLib, temp1, yi, sizeof(temp1));

  // Generate random data for R1
  generateRandomData(rr[1]);

  // Combine Hash(R1 + yi + R0) the result
  memcpy(temp2, rr[1], HASH_SIZE);
  memcpy(temp2 + HASH_SIZE, yi, HASH_SIZE);
  memcpy(temp2 + HASH_SIZE*2, rr[0], HASH_SIZE);
  hash(&shaLib, temp2, mm, sizeof(temp2));

  // Copy the result to the output array
  memcpy(result, mm, HASH_SIZE);
  memcpy(result + HASH_SIZE, rr[1], HASH_SIZE);

  //Encrypt
  for (size_t i = 0; i < HASH_SIZE*2; i+=16) {
    encryptAES(&aesLib, result+i, result+i, x);
  }

  Serial.println("[INFO] Server Hello Done.");
}

void MyCrypto::certificate(uint8_t* receive) {
  for (size_t i = 0; i < HASH_SIZE*2; i+=16) {
    decryptAES(&aesLib, receive + i, receive + i, mm);
  }
  memcpy(mm, receive, HASH_SIZE);
  memcpy(rr[2], receive + HASH_SIZE, HASH_SIZE);

  uint8_t temp1[HASH_SIZE*3];
  uint8_t temp2[HASH_SIZE];
  memcpy(temp1, rr[2], HASH_SIZE);
  memcpy(temp1 + HASH_SIZE, rr[1], HASH_SIZE);
  memcpy(temp1 + HASH_SIZE*2, yi, HASH_SIZE);
  hash(&shaLib, temp1, temp2, sizeof(temp1));

  if (memcmp(mm, temp2, HASH_SIZE) != 0) {
    Serial.println("[ERROR] M2 verification Failed.");
    Serial.println(getAllVariables());
    memset(rr[2], 0, HASH_SIZE);
    return;
  }

  createSession();
}

void MyCrypto::createSession() {
  uint8_t temp1[HASH_SIZE*4];
  memcpy(temp1, rr[0], HASH_SIZE);
  memcpy(temp1 + HASH_SIZE, rr[1], HASH_SIZE);
  memcpy(temp1 + HASH_SIZE*2, rr[2], HASH_SIZE);
  memcpy(temp1 + HASH_SIZE*3, yi, HASH_SIZE);
  hash(&shaLib, temp1, session_key, sizeof(temp1));
  Serial.println("[INFO] Session key create Successful.");
}

bool MyCrypto::verify(uint8_t* key) {
  uint8_t tempKey[HASH_SIZE];  // Create a temporary array for decrypted key

  for (size_t i = 0; i < HASH_SIZE; i += 16) {
    decryptAES(&aesLib, key + i, tempKey + i, mm);
  }

  // Compare the content of tempKey and session_key
  return memcmp(tempKey, session_key, HASH_SIZE) == 0;
}

void MyCrypto::encryptImage(const uint8_t* originalImage, uint8_t* encryptedImage, size_t imageSize) {
  // 計算圖像中區塊的數量
  size_t blockCount = imageSize / 16;

  for (size_t i = 0; i < blockCount; ++i) {
    // 計算當前區塊在圖像中的偏移
    size_t offset = i * HASH_SIZE;

    // 對每個區塊進行AES加密
    encryptAES(&aesLib, originalImage + offset, encryptedImage + offset, session_key);
  }
}

String MyCrypto::getAllVariables() {
  String allVariables = "IDi=" + byteArrayToString(IDi, HASH_SIZE) + "\n";
  allVariables += "yi=" + byteArrayToString(yi, HASH_SIZE) + "\n";
  allVariables += "x=" + byteArrayToString(x, HASH_SIZE) + "\n";
  for (int i = 0; i < 3; i++) {
    allVariables += "rr[" + String(i) + "]=" + byteArrayToString(rr[i], HASH_SIZE) + "\n";
  }
  allVariables += "m=" + byteArrayToString(mm, HASH_SIZE) + "\n";
  allVariables += "session_key=" + byteArrayToString(session_key, HASH_SIZE) + "\n";
  return allVariables;
}

void MyCrypto::hash(SHA256* shaLib, const uint8_t *data, uint8_t *hashResult, size_t dataSize) {
  // Initialize the hash
  shaLib->reset();
  
  // 添加要進行加密的數據
  shaLib->update(data, dataSize);
  
  // 添加要進行加密的數據
  shaLib->finalize(hashResult, HASH_SIZE);
}

void MyCrypto::encryptAES(AES256* aesLib, const uint8_t *input, uint8_t *output, uint8_t *key) {
  aesLib->setKey(key, HASH_SIZE);
  aesLib->encryptBlock(output, input);
}

void MyCrypto::decryptAES(AES256* aesLib, const uint8_t *input, uint8_t *output, uint8_t *key) {
  aesLib->setKey(key, HASH_SIZE);
  aesLib->decryptBlock(output, input);
}

void MyCrypto::generateRandomData(uint8_t *dataR) {
  for (int i = 0; i < HASH_SIZE; i++) {
    dataR[i] = random(256);
  }
}

String MyCrypto::byteArrayToString(const uint8_t *array, int length) {
  String result = "";
  for (int i = 0; i < length; i++) {
    char hex[3];
    sprintf(hex, "%02X", array[i]);
    result += hex;
  }
  return result;
}
