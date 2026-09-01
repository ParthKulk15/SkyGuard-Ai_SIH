// SkyGuard Edge reference: deterministic, offline and allocation-free.
// Run training/train_edge.py before compiling so edge_model.h is generated.
#include "edge_model.h"
// Transport intentionally omitted: publish telemetry to skyguard/station/<id>/telemetry.
struct Reading { float t, p, h; bool communicationOk; };
float edgeScore(const Reading& now, const Reading& prev, uint8_t repeated) {
  if (!now.communicationOk || isnan(now.t) || isnan(now.p) || isnan(now.h)) return 1.0f;
  if (now.t < -60 || now.t > 65 || now.p < 850 || now.p > 1100 || now.h < 0 || now.h > 100) return 1.0f;
  float score = .035f * fabs(now.t-prev.t) + .025f * fabs(now.p-prev.p) + .012f * fabs(now.h-prev.h) + .03f * repeated;
  return min(1.0f, score);
}
uint8_t classify(const Reading& now, const Reading& prev, uint8_t repeated) {
  float f[SKYG_E1_FEATURES] = {now.t, now.p, now.h, now.t-prev.t, now.p-prev.p,
    now.h-prev.h, NAN, NAN, NAN, NAN, NAN, NAN, 0, 0, 0};
  // Replace NAN rolling statistics with the trained median; production firmware
  // should calculate them from a six-reading ring buffer before this call.
  return skyguard_e1_predict(f);
}
// Keep a ring buffer of 12 JSON payloads in NVS when MQTT disconnects; replay on reconnect.
