from src.demo import DemoTelemetryGenerator
from datetime import datetime, timezone


def test_demo_generator_is_reproducible_and_injects_faults():
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    first = list(DemoTelemetryGenerator(seed=5, fault_every=2, start_time=start).stream(8))
    second = list(DemoTelemetryGenerator(seed=5, fault_every=2, start_time=start).stream(8))
    assert first == second
    assert any(packet["edge_fault_type"] != "NORMAL" for packet in first)
    assert all(packet["demo_mode"] is True for packet in first)


def test_demo_generator_supports_forced_scenario():
    packets = list(DemoTelemetryGenerator(fault_sequence=("DATA_CORRUPTION",)).stream(1))
    assert packets[0]["humidity"] == 130.0
    assert packets[0]["edge_fault_type"] == "DATA_CORRUPTION"
