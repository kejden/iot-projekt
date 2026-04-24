import paho.mqtt.client as mqtt
import projekt_protokol_pb2
import psycopg2
import os
import time

DB_PARAMS = {
    "host": os.getenv('DB_HOST', 'timescaledb'),
    "database": "iot_db",
    "user": "postgres",
    "password": "TwojeHaslo123"
}

def setup_database():
    """Tworzy tabelę readings i hypertable w TimescaleDB."""
    conn = None
    for i in range(5):
        try:
            conn = psycopg2.connect(**DB_PARAMS)
            break
        except Exception:
            print(f"Oczekiwanie na bazę... ({i+1}/5)")
            time.sleep(2)
    if not conn: return

    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS readings (
                    time           TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    station_id     INTEGER,
                    station_name   TEXT,
                    temperature    REAL,
                    humidity       REAL,
                    light_level    INTEGER
                );
                SELECT create_hypertable('readings', 'time', if_not_exists => TRUE);
            """)
            print("Baza danych gotowa (tabela: readings).")

def save_to_db(data):
    """Zapisuje SensorReport do tabeli readings."""
    try:
        with psycopg2.connect(**DB_PARAMS) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO readings 
                       (station_id, station_name, temperature, humidity, light_level) 
                       VALUES (%s, %s, %s, %s, %s)""",
                    (data.station.id, data.station.name, data.temperature, data.humidity, data.light_level)
                )
    except Exception as e:
        print(f"Błąd zapisu: {e}")

def on_message(client, userdata, msg):
    report = projekt_protokol_pb2.SensorReport()
    try:
        report.ParseFromString(msg.payload)
        print(f"Odebrano: {report.station.name} | T:{report.temperature} L:{report.light_level}")
        save_to_db(report)
    except Exception as e:
        print(f"Błąd dekodowania: {e}")

if __name__ == "__main__":
    setup_database()
    
    client = mqtt.Client()
    client.on_message = on_message
    
    try:
        client.connect("mosquitto", 1883)
        client.subscribe("esp32/sensors")
        print("Mostek MQTT -> DB uruchomiony...")
        client.loop_forever()
    except Exception as e:
        print(f"Błąd MQTT: {e}")
