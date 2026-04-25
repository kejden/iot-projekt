#include <time.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include "pb_encode.h"
#include "projekt-protokol.pb.h"

#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

const char* ssid        = "S25u";
const char* password    = "9fnrb497";
const char* mqtt_server = "10.190.128.83";
const char* mqtt_topic  = "esp32/sensors";

WiFiClient espClient;
PubSubClient client(espClient);

const int LIGHT_PIN = 32;
int getLight() {
  long sum = 0;
  for(int i = 0; i < 10; i++) { sum += analogRead(LIGHT_PIN); delay(5); }
  return (int)(sum / 10);
}


SensorReport createReport() {
  SensorReport report = SensorReport_init_zero;
  
  report.temperature = dht.readTemperature();
  report.humidity = dht.readHumidity();
  report.light_level = getLight();
  
  report.station.id = 101;
  report.has_station = true;
  strncpy(report.station.name, "ESP32-Node-1", sizeof(report.station.name));
  
  return report;
}


void sendToBroker(SensorReport report) {
  uint8_t buffer[128];
  pb_ostream_t stream = pb_ostream_from_buffer(buffer, sizeof(buffer));

  if (pb_encode(&stream, SensorReport_fields, &report)) {
    client.publish(mqtt_topic, buffer, stream.bytes_written);
    
    Serial.printf("Data Sent | T:%.1f H:%.1f L:%d | Size: %db\r\n", 
                  report.temperature, report.humidity, report.light_level, stream.bytes_written);
  }
}

void setup() {
  Serial.begin(115200);
  dht.begin();
  analogReadResolution(12);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nPolaczono z WiFi!\r\n");
  Serial.print("Adres IP: ");
  Serial.println(WiFi.localIP());

  
  client.setServer(mqtt_server, 1883);
}

void loop() {
  if (!client.connected()) {
    if (client.connect("ESP32_Kejden")){
      Serial.println("MQTT OK\r\n");
      return;
    }else { 
      Serial.print("BLAD, rc=");
      Serial.print(client.state());
      Serial.println(" - ponowienie za 5 sekund\r\n");
      delay(5000);
     }
  }
  client.loop();

  static unsigned long lastUpdate = 0;
  if (millis() - lastUpdate > 5000) {
    lastUpdate = millis();
    
    SensorReport currentReport = createReport();
    
    if (!isnan(currentReport.temperature)) {
      sendToBroker(currentReport);
    }
  }
}