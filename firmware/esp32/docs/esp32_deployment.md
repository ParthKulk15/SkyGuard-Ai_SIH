# ESP32 DevKit deployment guide

## Hardware

Use an ESP32 DevKit (ESP32-WROOM-32) and a BME280 I²C breakout. The BME280 is
used only for temperature, pressure, and relative humidity.

| BME280 pin | ESP32 DevKit pin |
|---|---|
| VIN / 3V3 | 3V3 |
| GND | GND |
| SDA | GPIO 21 |
| SCL | GPIO 22 |

Use 3.3 V I²C logic. The firmware tries the common BME280 addresses `0x76` and
`0x77`.

## One-time Arduino IDE setup

1. Install Arduino IDE 2.x.
2. Open **File → Preferences** and add this Boards Manager URL:

   ```text
   https://espressif.github.io/arduino-esp32/package_esp32_index.json
   ```

3. Open **Tools → Board → Boards Manager**, find **esp32 by Espressif Systems**,
   and install it.
4. In **Sketch → Include Library → Manage Libraries**, install:
   `Adafruit BME280 Library`, `Adafruit Unified Sensor`, `PubSubClient`, and
   `ArduinoJson`.

## Prepare the sketch

1. Create `Documents/Arduino/skyguard_devkit/`.
2. Copy both `edge/esp32/skyguard_devkit.ino` and
   `edge/esp32/edge_model.h` into that directory. They must be together because
   the sketch includes the generated model header at compile time.
3. Edit `skyguard_devkit.ino` and replace `WIFI_SSID`, `WIFI_PASSWORD`,
   `MQTT_HOST`, and `STATION_ID`. Do not commit real passwords to GitHub.

## Compile and upload

1. Connect the board with a data-capable USB cable.
2. Select **Tools → Board → ESP32 Arduino → ESP32 Dev Module**.
3. Select the correct **Tools → Port** entry and set upload speed to `115200`.
4. Click **Verify**. Arduino will display final flash and RAM usage.
5. Click **Upload**.
6. If the IDE is stuck at `Connecting...`, hold **BOOT**, click Upload, and
   release BOOT as soon as writing begins.
7. Open Serial Monitor at `115200` baud. A `BME280 not found` message means
   the power, wiring, or I²C address must be checked.

## What runs on the DevKit

Every five minutes the board reads the BME280, computes local features using a
six-sample ring buffer, applies hard safety checks and the generated E1 tree,
then publishes telemetry and the edge result over MQTT. The model is compiled
into firmware; there is no runtime Python, TensorFlow, or model download.

The generated E1 header is approximately 1.9 KB source and has a 37-node tree.
Inference needs about 124 bytes of explicit feature/model workspace plus the
Arduino networking and sensor-library overhead. This is well within a classic
ESP32’s data RAM, but the final compiler report remains the authoritative
memory measurement for the particular library versions and build flags.

When Wi‑Fi or the server fails, local detection continues. The reference sketch
does not yet persist packets during an outage; add a small NVS-backed queue
before a field deployment if delayed telemetry upload is required.

## Security and field-readiness

* Use MQTT over TLS and device-specific credentials in production.
* Provision credentials outside source control.
* Sync time using NTP and send UTC ISO-8601 timestamps rather than uptime.
* Calibrate the BME280 and re-train/evaluate with labelled field data before
  using alert thresholds for operational decisions.
