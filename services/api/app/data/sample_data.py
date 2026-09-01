from __future__ import annotations


STATIONS = [
    {"station_id": "AWS-DL-01", "name": "Delhi AWS", "region": "Delhi", "latitude": 28.6139, "longitude": 77.2090, "base_temperature": 30.0, "base_pressure": 1007.0, "base_humidity": 48.0},
    {"station_id": "AWS-MH-01", "name": "Mumbai AWS", "region": "Maharashtra", "latitude": 19.0760, "longitude": 72.8777, "base_temperature": 29.0, "base_pressure": 1009.0, "base_humidity": 72.0},
    {"station_id": "AWS-RJ-01", "name": "Jaipur AWS", "region": "Rajasthan", "latitude": 26.9124, "longitude": 75.7873, "base_temperature": 34.0, "base_pressure": 1005.0, "base_humidity": 34.0},
    {"station_id": "AWS-GJ-01", "name": "Ahmedabad AWS", "region": "Gujarat", "latitude": 23.0225, "longitude": 72.5714, "base_temperature": 33.0, "base_pressure": 1006.0, "base_humidity": 42.0},
    {"station_id": "AWS-KA-01", "name": "Bengaluru AWS", "region": "Karnataka", "latitude": 12.9716, "longitude": 77.5946, "base_temperature": 25.0, "base_pressure": 1012.0, "base_humidity": 61.0},
    {"station_id": "AWS-TN-01", "name": "Chennai AWS", "region": "Tamil Nadu", "latitude": 13.0827, "longitude": 80.2707, "base_temperature": 31.0, "base_pressure": 1008.0, "base_humidity": 70.0},
    {"station_id": "AWS-WB-01", "name": "Kolkata AWS", "region": "West Bengal", "latitude": 22.5726, "longitude": 88.3639, "base_temperature": 30.0, "base_pressure": 1008.0, "base_humidity": 76.0},
    {"station_id": "AWS-AS-01", "name": "Guwahati AWS", "region": "Assam", "latitude": 26.1445, "longitude": 91.7362, "base_temperature": 27.0, "base_pressure": 1010.0, "base_humidity": 80.0},
]

SCENARIOS = {
    "normal",
    "temperature_spike",
    "temperature_drift",
    "frozen_sensor",
    "missing_data",
    "duplicate_packet",
    "data_corruption",
    "simultaneous_sensor_failure",
    "multivariate_inconsistency",
    "regional_weather_event",
}
