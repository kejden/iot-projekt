# IoT Projekt - System Monitorowania Czujników

System zbierania, przesyłania i wizualizacji danych z czujników (Temperatura, Wilgotność, Światło) przy użyciu ESP32, MQTT i TimescaleDB.

## 1. Architektura Systemu
System typu IoT oparty na modelu **Edge -> Broker -> Cloud/Server**.
*   **Edge:** ESP32 zbierający dane z czujników.
*   **Message Broker:** Mosquitto (MQTT).
*   **Backend/Storage:** Python Bridge + TimescaleDB (PostgreSQL).
*   **Visualization:** Grafana.

## 2. Opis Codebase

### ESP32 (`/esp32/src`) - Firmware
*   **main.cpp**: Główna logika urządzenia. Obsługuje połączenie WiFi, klienta MQTT, odczyt z czujnika DHT11 oraz wejścia analogowego (fotorezystor). Wykorzystuje bibliotekę NanoPB do binarnej serializacji danych.
*   **projekt-protokol.proto**: Definicja struktury wiadomości Protobuf (`SensorReport` zawierający dane o stacji i odczytach).
*   **projekt-protokol.pb.c / .h**: Kod wygenerowany przez kompilator NanoPB, umożliwiający obsługę Protobuf w środowisku embedded.
*   **projekt-protokol.options**: Konfiguracja NanoPB (np. limity wielkości pól tekstowych).

### Server / Raspberry Pi (`/rspi`) - Infrastruktura i Backend
*   **main.py**: Serce backendu. Skrypt subskrybuje topic MQTT, deserializuje binarne dane przychodzące z ESP32 i zapisuje je do bazy TimescaleDB.
*   **docker-compose.yml**: Orkiestracja kontenerów:
    *   `iot_app`: Mostek Python.
    *   `mosquitto`: Broker MQTT.
    *   `timescaledb`: Baza danych SQL zoptymalizowana pod szeregi czasowe.
    *   `grafana`: Panel kontrolny do wykresów.
*   **init.sql**: Skrypt startowy bazy danych – tworzy tabelę `readings` i przekształca ją w `hypertable`.
*   **Dockerfile**: Definicja środowiska uruchomieniowego dla skryptu Python.
*   **mosquitto/config/mosquitto.conf**: Konfiguracja brokera (porty, uprawnienia).

## 3. Przepływ Danych
1.  **ESP32**: Odczyt czujników -> Serializacja Protobuf -> Publikacja MQTT (`esp32/sensors`).
2.  **Python Bridge**: Odbiór MQTT -> Deserializacja Protobuf -> SQL Insert do DB.
3.  **TimescaleDB**: Przechowywanie danych w strukturze zoptymalizowanej czasowo.
4.  **Grafana**: Query SQL -> Wizualizacja na dashboardach.

## 4. Technologie
*   **Języki**: C++ (ESP32), Python 3 (Backend), SQL.
*   **Komunikacja**: MQTT, Protocol Buffers (Protobuf).
*   **Baza**: TimescaleDB (PostgreSQL).
*   **Wirtualizacja**: Docker, Docker Compose.
