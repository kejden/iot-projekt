# System Monitorowania Środowiska (IoT)

Kompletny system do zdalnego śledzenia warunków otoczenia. Urządzenie (ESP32) mierzy temperaturę, wilgotność oraz natężenie światła, a następnie przesyła te dane do serwera, gdzie są zapisywane w bazie danych i wyświetlane na wykresach.

## 1. Jak to działa? (W skrócie)
1.  **ESP32** (mikrokontroler) odczytuje dane z czujników.
2.  Dane są zamieniane na wydajny format binarny (**Protobuf**).
3.  Wiadomość jest wysyłana przez WiFi do "pośrednika" (**MQTT Broker**).
4.  Skrypt na serwerze (**Python**) odbiera wiadomość i zapisuje ją w bazie danych (**TimescaleDB**).
5.  Użytkownik widzi gotowe wykresy w panelu **Grafana**.

## 2. Sprzęt i Połączenia

### Wykorzystane elementy:
*   **ESP32**: Główny "mózg" urządzenia z modułem WiFi.
*   **DHT11**: Czujnik mierzący temperaturę oraz wilgotność powietrza.
*   **TEMT6000**: Precyzyjny czujnik natężenia światła (działa podobnie do ludzkiego oka).

### Schemat podłączenia (Piny):
| Czujnik | Pin w ESP32 | Typ sygnału | Opis |
| :--- | :--- | :--- | :--- |
| **DHT11 (Data)** | **GPIO 4** | Cyfrowy | Odczyt temperatury i wilgotności |
| **TEMT6000 (Out)** | **GPIO 32** | Analogowy | Odczyt natężenia światła (0-4095) |
| **Zasilanie (VCC)** | **3.3V** | Zasilanie | Wspólne zasilanie dla obu czujników |
| **Masa (GND)** | **GND** | Masa | Wspólna masa układu |

---

## 3. Opis plików projektu

### Mikroprocesor (`/esp32/src`)
*   **main.cpp**: Główny program sterujący. Odpowiada za łączenie z WiFi, odpytywanie czujników co 5 sekund i wysyłanie danych.
*   **projekt-protokol.proto**: "Słownik" danych. Definiuje jak wyglądają przesyłane informacje, aby obie strony (ESP32 i Serwer) rozumiały się bez błędów.
*   **projekt-protokol.pb.c / .h**: Pliki pomocnicze wygenerowane automatycznie, które pozwalają mikroprocesorowi obsługiwać format Protobuf.

### Serwer / Raspberry Pi (`/rspi`)
*   **main.py**: Program "odbiorca". Czeka na dane z sieci, tłumaczy je z formatu binarnego na zrozumiały dla bazy danych i wykonuje zapis.
*   **docker-compose.yml**: Plik konfiguracyjny, który "stawia" całe środowisko serwerowe (bazę danych, brokera MQTT i wykresy) jednym poleceniem.
*   **init.sql**: Instrukcje dla bazy danych, jak przygotować tabele na przyjęcie pomiarów.
*   **mosquitto.conf**: Ustawienia "centrali" (Brokera), która zarządza ruchem wiadomości MQTT w sieci.

---

## 4. Architektura techniczna
*   **Protokół komunikacji**: MQTT (lekki protokół idealny dla urządzeń IoT).
*   **Format danych**: Protocol Buffers (Protobuf) - znacznie mniejszy i szybszy niż standardowy tekst (JSON).
*   **Baza danych**: TimescaleDB - specjalna odmiana PostgreSQL stworzona do błyskawicznego zapisywania milionów pomiarów w czasie.
*   **Konteneryzacja**: Docker - pozwala na uruchomienie całego serwera w identyczny sposób na każdym komputerze.

## 5. Technologie
*   **Języki**: C++ (urządzenie), Python (serwer), SQL (baza danych).
*   **Narzędzia**: Arduino/PlatformIO, Docker, Grafana, Mosquitto.
