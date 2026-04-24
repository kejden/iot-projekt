import paho.mqtt.client as mqtt
import iot_protokol_pb2 # Skompilowany protoc --python_out

def on_message(client, userdata, msg):
    dht_report = iot_protokol_pb2.DHTData()
    
    try:
        dht_report.ParseFromString(msg.payload)
        
        print(f"--- Dane od: {dht_report.station.name} (ID: {dht_report.station.id}) ---")
        print(f"Temp: {dht_report.temperature:.2f}°C, Hum: {dht_report.humidity:.2f}%")
        
    except Exception as e:
        print(f"Błąd dekodowania pakietu: {e}")

client = mqtt.Client()
client.on_message = on_message
client.connect("127.0.0.1", 1883)
client.subscribe("esp32/dht")
client.loop_forever()
