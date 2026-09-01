"""Print demo telemetry for frontend/backend development."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.demo import DemoTelemetryGenerator


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate SkyGuard demo telemetry JSON")
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument("--device-id", default="AWS-DEMO-001")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    generator = DemoTelemetryGenerator(device_id=args.device_id, seed=args.seed)
    for packet in generator.stream(args.count):
        print(json.dumps(packet), flush=True)


if __name__ == "__main__":
    main()
