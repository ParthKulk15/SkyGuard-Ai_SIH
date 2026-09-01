import pandas as pd

from src.data.fault_augmentation import TrainingFaultAugmenter


def test_fault_augmentation_adds_labeled_operational_faults():
    source = pd.DataFrame([
        {
            'station_id': 'AWS001', 'timestamp': '2026-01-01 00:00:00',
            'temperature': 25.0, 'pressure': 1005.0, 'humidity': 65.0,
            'temperature_roll_mean': 25.0, 'pressure_roll_mean': 1005.0,
            'is_anomaly': 0, 'fault_type': 'NORMAL',
        }
    ])
    augmented = TrainingFaultAugmenter(random_state=7).augment(
        source,
        counts={'COMMUNICATION_FAILURE': 1, 'DATA_CORRUPTION': 1, 'DUPLICATE_PACKET': 1, 'SIMULTANEOUS_SENSOR_FAILURE': 1},
    )
    assert len(augmented) == 5
    assert set(augmented['fault_type']) >= {
        'COMMUNICATION_FAILURE', 'DATA_CORRUPTION', 'DUPLICATE_PACKET', 'SIMULTANEOUS_SENSOR_FAILURE'
    }
    assert augmented.loc[augmented.fault_type.eq('COMMUNICATION_FAILURE'), 'temperature'].isna().all()
    assert (augmented.loc[augmented.fault_type.eq('DATA_CORRUPTION'), 'humidity'] > 100).all()
    assert (augmented.loc[augmented.fault_type.eq('DUPLICATE_PACKET'), 'raw_is_duplicate_packet'] == 1).all()


def test_fault_augmentation_adds_sensor_fault_signatures():
    source = pd.DataFrame([{
        'station_id': 'AWS001', 'timestamp': '2026-01-01 00:00:00',
        'temperature': 25.0, 'pressure': 1005.0, 'humidity': 65.0,
        'temperature_roll_mean': 25.0, 'pressure_roll_mean': 1005.0, 'humidity_roll_mean': 65.0,
        'is_anomaly': 0, 'fault_type': 'NORMAL',
    }])
    counts = {'TEMPERATURE_SPIKE': 1, 'PRESSURE_FROZEN': 1, 'HUMIDITY_BIAS': 1}
    augmented = TrainingFaultAugmenter(random_state=7).augment(source, counts=counts)
    assert len(augmented) == 4
    assert augmented.loc[augmented.fault_type.eq('TEMPERATURE_SPIKE'), 'temperature'].iloc[0] > 35.0
    assert augmented.loc[augmented.fault_type.eq('PRESSURE_FROZEN'), 'press_persistence'].iloc[0] == 8.0
    assert augmented.loc[augmented.fault_type.eq('HUMIDITY_BIAS'), 'humidity'].iloc[0] > 65.0
