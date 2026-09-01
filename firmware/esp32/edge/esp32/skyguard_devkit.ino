/* SkyGuard E1 on ESP32 DevKit + BME280 (temperature, pressure, humidity).
   Arduino libraries: Adafruit BME280, PubSubClient, ArduinoJson.
   Set Wi-Fi, MQTT, and station identity before flashing. */
#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <Adafruit_BME280.h>
#include <ArduinoJson.h>
#include "edge_model.h"

constexpr char WIFI_SSID[] = "REPLACE_WIFI_SSID";
constexpr char WIFI_PASSWORD[] = "REPLACE_WIFI_PASSWORD";
constexpr char MQTT_HOST[] = "192.168.1.10";
constexpr uint16_t MQTT_PORT = 1883;
constexpr char STATION_ID[] = "AWS001";
constexpr uint32_t SAMPLE_INTERVAL_MS = 300000UL; // five minutes

struct Sample { float t, p, h; };
Sample history[6]; uint8_t sampleCount=0, writeAt=0, repeated=0;
WiFiClient wifi; PubSubClient mqtt(wifi); Adafruit_BME280 bme;

void connectMqtt() {
  while (!mqtt.connected() && WiFi.status() == WL_CONNECTED) {
    mqtt.connect(STATION_ID); // Production: use authenticated TLS MQTT.
    if (!mqtt.connected()) delay(3000);
  }
}

float meanFeature(uint8_t parameter) {
  float sum=0; for (uint8_t i=0;i<sampleCount;i++) sum += parameter==0?history[i].t:(parameter==1?history[i].p:history[i].h);
  return sampleCount ? sum/sampleCount : NAN;
}
float stdFeature(uint8_t parameter, float mean) {
  if (sampleCount<2) return NAN; float sum=0;
  for (uint8_t i=0;i<sampleCount;i++) { float v=parameter==0?history[i].t:(parameter==1?history[i].p:history[i].h); sum+=(v-mean)*(v-mean); }
  return sqrtf(sum/(sampleCount-1));
}
void publishReading(const Sample& now, const Sample& previous, float score, uint8_t anomaly) {
  StaticJsonDocument<512> doc;
  doc["timestamp_ms"] = (uint32_t)(millis()/1000); // Use NTP UTC ISO-8601 in production.
  doc["station_id"] = STATION_ID; doc["temperature"] = now.t; doc["pressure"] = now.p; doc["humidity"] = now.h;
  doc["edge_anomaly_score"] = score; doc["edge_status"] = anomaly ? "ANOMALY" : "NORMAL";
  doc["model_name"] = "SkyGuard-E1"; doc["model_version"] = "E1-1.0.0";
  char topic[96], payload[512]; snprintf(topic,sizeof(topic),"skyguard/station/%s/telemetry",STATION_ID);
  size_t n=serializeJson(doc,payload,sizeof(payload)); mqtt.publish(topic,payload,n);
}
void takeSample() {
  Sample now={bme.readTemperature(), bme.readPressure()/100.0f, bme.readHumidity()};
  Sample prev = sampleCount ? history[(writeAt+5)%6] : now;
  bool same = sampleCount && now.t==prev.t && now.p==prev.p && now.h==prev.h;
  repeated = same ? repeated+1 : 0;
  float mt=meanFeature(0), mp=meanFeature(1), mh=meanFeature(2);
  float f[SKYG_E1_FEATURES] = {now.t,now.p,now.h,now.t-prev.t,now.p-prev.p,now.h-prev.h,
    mt,mp,mh,stdFeature(0,mt),stdFeature(1,mp),stdFeature(2,mh),0,0,0};
  uint8_t modelAnomaly=skyguard_e1_predict(f);
  bool ruleAnomaly = now.t<-60 || now.t>65 || now.p<850 || now.p>1100 || now.h<0 || now.h>100 || repeated>=12;
  float score=ruleAnomaly ? 1.0f : (modelAnomaly ? 0.80f : 0.05f);
  history[writeAt]=now; writeAt=(writeAt+1)%6; if(sampleCount<6) sampleCount++;
  if (WiFi.status()==WL_CONNECTED) { connectMqtt(); mqtt.loop(); if(mqtt.connected()) publishReading(now,prev,score,modelAnomaly||ruleAnomaly); }
  // Add a small NVS queue here to retain payloads during outage and replay after reconnect.
}
void setup() {
  Serial.begin(115200); Wire.begin();
  if (!bme.begin(0x76) && !bme.begin(0x77)) { Serial.println("BME280 not found"); while(true) delay(1000); }
  WiFi.begin(WIFI_SSID,WIFI_PASSWORD); mqtt.setServer(MQTT_HOST,MQTT_PORT);
}
void loop() { static uint32_t last=0; if(millis()-last>=SAMPLE_INTERVAL_MS || last==0) { last=millis(); takeSample(); } delay(20); }
