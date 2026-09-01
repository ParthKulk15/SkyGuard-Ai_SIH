# SkyGuard frontend modules

The frontend can run entirely in demo mode. It should consume the same packet
shape as the ESP32 path, with `demo_mode: true` shown in the UI.

1. **App shell** — routing, navigation, theme, responsive layout.
2. **Demo mode controller** — start/stop simulation, speed, station selector,
   scenario selector, and connection indicator.
3. **Live dashboard** — current temperature, pressure, humidity, anomaly score,
   severity, online status, and latest event.
4. **Station detail** — time-series charts, packet timeline, edge versus PC
   decisions, health score, and explanations.
5. **Alerts center** — active/history lists, severity filters, acknowledge and
   resolve actions.
6. **Station/device management** — stations, coordinates, firmware and model
   versions, last-seen time.
7. **Model health** — edge/PC model versions, agreement rate, precision/recall
   cards, and data-quality counters.
8. **Telemetry client** — REST queries, WebSocket live updates, reconnect and
   demo fallback.
9. **Shared UI components** — cards, charts, badges, tables, modal, toast,
   loading/empty/error/offline states.
10. **Types and validation** — TypeScript packet, prediction, alert, station,
    and model-status types matching the backend schema.

## Demo-mode contract

The backend can call `DemoTelemetryGenerator` directly, or the frontend can
use the same JSON shape from a mock WebSocket. Demo mode must never be mixed
with production station data; display a visible `DEMO` badge and keep demo
alerts in a separate namespace.

Run a local stream with:

```bash
.venv/bin/python scratch/run_demo.py --count 30
```
