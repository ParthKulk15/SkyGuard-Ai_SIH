from __future__ import annotations
from collections import defaultdict, deque
from dataclasses import dataclass, field
import numpy as np
from edge.rules import rule_checks


@dataclass
class EdgeState:
    history: deque = field(default_factory=lambda: deque(maxlen=6))
    identical_count: int = 0


class EdgeDetector:
    """Tiny deterministic detector: suitable for quantized C/C++ implementation."""
    def __init__(self) -> None:
        self.states: dict[str, EdgeState] = defaultdict(EdgeState)

    def process(self, reading: dict) -> dict:
        state = self.states[reading["station_id"]]
        previous = state.history[-1] if state.history else None
        same = previous and all(reading.get(p) == previous.get(p) for p in ("temperature", "pressure", "humidity"))
        state.identical_count = state.identical_count + 1 if same else 0
        issues = rule_checks(reading, previous, state.identical_count)
        # Linear residual score can be represented as integer weights after scale x100.
        deltas = [abs(reading.get(p, 0) - previous.get(p, 0)) if previous and reading.get(p) is not None and previous.get(p) is not None else 0 for p in ("temperature", "pressure", "humidity")]
        linear_score = min(1.0, 0.035*deltas[0] + 0.025*deltas[1] + 0.012*deltas[2] + 0.03*state.identical_count)
        rule_score = max((x[2] for x in issues), default=0.0)
        score = round(max(linear_score, rule_score), 3)
        if score >= .85: status = "CRITICAL"
        elif score >= .55: status = "ANOMALY"
        elif score >= .25: status = "WARNING"
        else: status = "NORMAL"
        fault, parameter = (issues[0][0], issues[0][1]) if issues else ("NORMAL", None)
        state.history.append(dict(reading))
        return {"timestamp": reading["timestamp"], "station_id": reading["station_id"], "edge_anomaly_score": score,
                "edge_status": status, "suspected_parameter": parameter, "edge_fault_type": fault,
                "confidence": round(min(.99, .5 + score*.48), 3)}
