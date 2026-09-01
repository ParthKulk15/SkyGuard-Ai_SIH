from __future__ import annotations
import math

LIMITS = {"temperature": (-60.0, 65.0), "pressure": (850.0, 1100.0), "humidity": (0.0, 100.0)}
JUMP_LIMITS = {"temperature": 12.0, "pressure": 10.0, "humidity": 35.0}


def rule_checks(current: dict, previous: dict | None, identical_count: int) -> list[tuple[str, str, float]]:
    """Return (fault type, parameter, normalized severity) deterministic checks."""
    issues: list[tuple[str, str, float]] = []
    if not current.get("communication_ok", True) or any(current.get(p) is None for p in LIMITS):
        return [("COMMUNICATION_FAILURE", "all", 1.0)]
    for p, (lo, hi) in LIMITS.items():
        v = current[p]
        if not math.isfinite(v) or v < lo or v > hi:
            issues.append(("DATA_CORRUPTION", p, 1.0))
        if previous and previous.get(p) is not None:
            d = abs(v - previous[p])
            if d > JUMP_LIMITS[p]:
                issues.append((f"{p.upper()}_SPIKE", p, min(1.0, d / (JUMP_LIMITS[p] * 2))))
    if identical_count >= 12:
        issues.append(("SENSOR_FROZEN", "all", min(1.0, identical_count / 24)))
    # Very hot + saturated humidity is a useful physical sanity check, not an absolute rule.
    if current["temperature"] > 50 and current["humidity"] > 95:
        issues.append(("MULTIVARIATE_INCONSISTENCY", "temperature", 0.75))
    return issues
