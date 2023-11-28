#include <WiFi.h>
#include <esp_camera.h>

#include "MyCrypto.h"
#include "config.h"
#include "camera_pins.h"

WiFiServer server(TCP_PORT);

//函式宣告
void connectWiFi();
void initCamera();
void handleClient(WiFiClient* client, uint8_t* data, MyCrypto* myCrypto);
void createSession(WiFiClient* client, uint8_t* data, MyCrypto* myCrypto);
void checkSession(WiFiClient* client, uint8_t* data, MyCrypto* myCrypto);
void streamCamera(WiFiClient* client, MyCrypto* myCrypto);

void setup() {
  Serial.begin(115200);
  initCamera();
  connectWiFi();
  server.begin();
}

void loop() {
  // Handle other tasks in the loop
  if (WiFi.status() != WL_CONNECTED) {
    connectWiFi();
  }
  WiFiClient client = server.available();   // listen for incoming clients
  if (client) {
    Serial.println("[INFO] Client Connected");
    unsigned long startTime = millis();
    MyCrypto myCrypto;

    while (client.connected()){
      if(client.available()){
        uint8_t rmsg[65];
        size_t bytesRead = client.readBytes(rmsg, sizeof(rmsg));
        if (bytesRead > 0){
          switch (rmsg[0]){
            case 'A':
              handleClient(&client, rmsg+1, &myCrypto);
              break;
            case 'C':
              createSession(&client, rmsg+1, &myCrypto);
              break;
            case 'V':
              checkSession(&client, rmsg+1, &myCrypto);
              break;
            default:
              Serial.println("[ERROR] Unregistered status.");
              client.stop();
              break;
          }
        }
        startTime = millis();
      }
      if (millis() - startTime > 5000) { //5s
        Serial.println("[INFO] Client Timeout");
        client.stop(); // Close the connection after a timeout
        break;
      }
    }
    Serial.println("[INFO] Client Disconneted");
  }
}

//WiFi連線
void connectWiFi() {
  Serial.print("Connecting to WiFi");
  WiFi.begin(SSID, PASSWORD);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected");
  Serial.print("IP Address:");
  Serial.println(WiFi.localIP());
}

void handleClient(WiFiClient* client, uint8_t* data, MyCrypto* myCrypto) {
  uint8_t smsg[65];
  smsg[0]='B';
  myCrypto->serverHello(data, smsg+1);
  client->write(smsg, sizeof(smsg));
}

void createSession(WiFiClient* client, uint8_t* data, MyCrypto* myCrypto) {
  myCrypto->certificate(data);
}

void checkSession(WiFiClient* client, uint8_t* data, MyCrypto* myCrypto) {
  if(myCrypto->verify(data)){
    Serial.println("[INFO] Session key verification Successful.");
    streamCamera(client, myCrypto);
  } else {
    Serial.println("[ERROR] Session key verification Failed.");
    Serial.println(myCrypto->getAllVariables());
    client->stop();
  }
}

void streamCamera(WiFiClient* client, MyCrypto* myCrypto) {
  camera_fb_t *fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("[WARING] Camera capture Failed");
  }
  // 加密（***ERROR*** A stack overflow in task loopTask has been detected.）
  //uint8_t encryptedImage[fb->len];
  //myCrypto->encryptImage(fb->buf, encryptedImage, fb->len);

  // Check for Authorization header and compare with valid session key
  if (client->connected()) {
    client->write((const uint8_t*)&fb->len, sizeof(fb->len));
    Serial.printf("[INFO] Sending frame, size: %u\n", fb->len);

    const int chunkSize = 512;
    uint8_t buffer[chunkSize];

    for (size_t i = 0; i < fb->len; i += chunkSize) {
      size_t chunkLen = min(static_cast<size_t>(chunkSize), fb->len - i);
      client->write(fb->buf + i, chunkLen);
    }
    // client->write(fb->buf, fb->len);
  } else {
    Serial.println("[WARNING] Client disconnected. Not sending frame.");
  }
  esp_camera_fb_return(fb);
}

void initCamera() {
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG; // for streaming
  //設定影像大小：UXGA(1600x1200),SXGA(1280x1024),XGA(1024x768),SVGA(800x600),VGA(640x480),CIF(400x296),QVGA(320x240),HQVGA(240x176),QQVGA(160x120)
  config.frame_size = FRAMESIZE_VGA;
  config.jpeg_quality = 12; //JPEG Quality
  config.fb_count = 2; //Frame Buffer Count

  // camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("[WARING] Camera init failed with error 0x%x", err);
  }
}