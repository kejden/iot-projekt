# System Monitorowania Środowiska (IoT)

## 1. Przepływ danych
1. **ESP32**: Odczyt danych z sensorów -> Serializacja Protobuf -> Publikacja MQTT (`esp32/sensors`).
2. **Python Bridge**: Subskrypcja MQTT -> Deserializacja Protobuf -> Zapis do TimescaleDB.
3. **TimescaleDB**: Przechowywanie danych (hypertable).
4. **Grafana**: Wizualizacja danych z bazy SQL.

## 2. Specyfikacja sprzętowa i połączenia
| Komponent | Model | Pin ESP32 | Typ sygnału | Funkcja |
| :--- | :--- | :--- | :--- | :--- |
| **Mikrokontroler** | ESP32 | - | - | Jednostka sterująca, komunikacja WiFi |
| **Czujnik Temp/Wilg** | DHT11 | **GPIO 4** | Cyfrowy (1-Wire) | Pomiar temperatury i wilgotności |
| **Czujnik Światła** | TEMT6000 | **GPIO 32** | Analogowy (ADC) | Pomiar natężenia światła (0-4095) |
| **Zasilanie** | - | **3.3V** | DC | Zasilanie sensorów |
| **Masa** | - | **GND** | - | Wspólny punkt odniesienia |

## 3. Struktura Codebase

### /esp32/src (Firmware)
*   **main.cpp**: Logika odczytu sensorów, klient MQTT, obsługa stosu WiFi i NanoPB.
*   **projekt-protokol.proto**: Definicja struktury wiadomości w formacie Protocol Buffers.
*   **projekt-protokol.pb.c / .h**: Skompilowane pliki biblioteczne NanoPB dla języka C.
*   **projekt-protokol.options**: Parametry kompilacji pól wiadomości Protobuf.

### /rspi (Backend & Infrastructure)
*   **main.py**: Skrypt Python realizujący funkcję mostka między brokerem MQTT a bazą danych SQL.
*   **docker-compose.yml**: Konfiguracja kontenerów: `iot_app`, `mosquitto`, `timescaledb`, `grafana`.
*   **init.sql**: Definicja schematu bazy danych i inicjalizacja rozszerzenia TimescaleDB.
*   **Dockerfile**: Instrukcje budowania obrazu dla aplikacji Python.
*   **mosquitto/config/mosquitto.conf**: Konfiguracja brokera MQTT (nasłuch, porty).

## 4. Stos Technologiczny
*   **Języki**: C++, Python, SQL.
*   **Protokół komunikacji**: MQTT (Broker: Mosquitto).
*   **Serializacja**: Protocol Buffers (NanoPB na urządzeniu, protobuf w Pythonie).
*   **Baza danych**: TimescaleDB (PostgreSQL).
*   **Wizualizacja**: Grafana.
*   **Infrastruktura**: Docker / Docker Compose.
