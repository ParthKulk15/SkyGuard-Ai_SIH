import pandas as pd
import numpy as np
from typing import Dict, Any, List


class RuleBaselineDetector:

    def __init__(self, config: Dict[str, Any] = None):
        self.config = {
            'temp_delta_threshold': 5.0,       # °C / 5min spike threshold
            'pressure_delta_threshold': 5.0,   # hPa / 5min spike threshold
            'humidity_delta_threshold': 25.0,  # % / 5min spike threshold
            'residual_z_threshold': 8.0,       # conservative single-sensor residual Z-score
            'simultaneous_residual_threshold': 8.0,
            'frozen_ticks_threshold': 6,       # 6 ticks = 30 minutes of unchanged reading
            'temp_min_bound': -10.0,
            'temp_max_bound': 55.0,
            'humidity_min_bound': 0.0,
            'humidity_max_bound': 100.0,
            'pressure_min_bound': 850.0,
            'pressure_max_bound': 1080.0
        }
        if config:
            self.config.update(config)

    def predict_observation(self, obs: Dict[str, Any]) -> Dict[str, Any]:
        flags = []
        types = []
        explanations = []

        temp = obs.get('temperature', None)
        press = obs.get('pressure', None)
        hum = obs.get('humidity', None)

        # 1. STREAM QUALITY CHECK: Missing observation (COMMUNICATION_FAILURE)
        is_missing_raw = (obs.get('raw_is_missing', 0) == 1.0) or (obs.get('temperature_missing', 0) == 1.0)
        is_missing_null = (temp is None or pd.isna(temp) or press is None or pd.isna(press) or hum is None or pd.isna(hum))

        if is_missing_raw or is_missing_null:
            return {
                'anomaly_flag': 1,
                'anomaly_score': 1.0,
                'severity': 'HIGH',
                'fault_type': 'COMMUNICATION_FAILURE',
                'explanation': "Missing sensor observation payload recorded on telemetry stream."
            }

        # 2. STREAM QUALITY CHECK: Duplicate packet signature (DUPLICATE_PACKET)
        if obs.get('raw_is_duplicate_packet', 0) == 1.0:
            return {
                'anomaly_flag': 1,
                'anomaly_score': 0.90,
                'severity': 'MEDIUM',
                'fault_type': 'DUPLICATE_PACKET',
                'explanation': "Identical sensor payload transmitted across consecutive timestamps (Duplicate Packet)."
            }

        # 3. Out-of-bounds / Data Corruption
        if temp < self.config['temp_min_bound'] or temp > self.config['temp_max_bound']:
            flags.append(True)
            types.append("DATA_CORRUPTION")
            explanations.append(f"Temperature {temp:.1f}°C is out of physical bounds [{self.config['temp_min_bound']}, {self.config['temp_max_bound']}].")

        if hum < self.config['humidity_min_bound'] or hum > self.config['humidity_max_bound']:
            flags.append(True)
            types.append("DATA_CORRUPTION")
            explanations.append(f"Relative humidity {hum:.1f}% exceeds physical limit [0-100%].")

        if press < self.config['pressure_min_bound'] or press > self.config['pressure_max_bound']:
            flags.append(True)
            types.append("DATA_CORRUPTION")
            explanations.append(f"Atmospheric pressure {press:.1f} hPa is out of physical bounds.")

        # Two independent sensors moving far above their own recent baselines
        # is a stronger failure signal than a single residual.  The signed
        # check intentionally does not flag the expected return-to-baseline
        # packet after a detected positive excursion.
        t_res_signed = float(obs.get('temperature_residual', 0.0) or 0.0)
        p_res_signed = float(obs.get('pressure_residual', 0.0) or 0.0)
        multi_threshold = self.config['simultaneous_residual_threshold']
        if t_res_signed >= multi_threshold and p_res_signed >= multi_threshold:
            return {
                'anomaly_flag': 1,
                'anomaly_score': 1.0,
                'severity': 'CRITICAL',
                'fault_type': 'SIMULTANEOUS_SENSOR_FAILURE',
                'explanation': 'Temperature and pressure both exceed their recent baselines by a large positive margin.'
            }

        # 4. Sudden Delta Spikes / Drops
        t_delta = abs(obs.get('temperature_delta', 0.0) or 0.0)
        p_delta = abs(obs.get('pressure_delta', 0.0) or 0.0)
        h_delta = abs(obs.get('humidity_delta', 0.0) or 0.0)

        if t_delta >= self.config['temp_delta_threshold']:
            flags.append(True)
            fault_name = "TEMPERATURE_SPIKE" if (obs.get('temperature_delta', 0) > 0) else "TEMPERATURE_DROP"
            types.append(fault_name)
            explanations.append(f"Sudden temperature change of {obs.get('temperature_delta', 0):.2f}°C within 5 minutes.")

        if p_delta >= self.config['pressure_delta_threshold']:
            flags.append(True)
            fault_name = "PRESSURE_SPIKE" if (obs.get('pressure_delta', 0) > 0) else "PRESSURE_DROP"
            types.append(fault_name)
            explanations.append(f"Sudden pressure change of {obs.get('pressure_delta', 0):.2f} hPa within 5 minutes.")

        if h_delta >= self.config['humidity_delta_threshold']:
            flags.append(True)
            fault_name = "HUMIDITY_SPIKE" if (obs.get('humidity_delta', 0) > 0) else "HUMIDITY_DROP"
            types.append(fault_name)
            explanations.append(f"Sudden humidity change of {obs.get('humidity_delta', 0):.2f}% within 5 minutes.")

        # 5. Conservative single-sensor residual deviation.  Broad weather
        # variation can create small rolling-window residuals, so this is not
        # used as an immediate hard override by the decision layer.
        t_res = abs(obs.get('temperature_residual', 0.0) or 0.0)
        t_std = obs.get('temperature_roll_std', 1.0) or 1.0
        if t_std > 0 and t_res >= 2.0 and (t_res / max(t_std, 1e-3)) >= self.config['residual_z_threshold']:
            flags.append(True)
            types.append("TEMPERATURE_BIAS")
            explanations.append(f"Temperature residual ({t_res:.2f}°C) significantly deviates from recent rolling mean.")

        # 6. Frozen Sensor Detection
        for param in ['temp', 'press', 'hum']:
            persistence_val = obs.get(f'{param}_persistence', 1)
            if persistence_val >= self.config['frozen_ticks_threshold']:
                flags.append(True)
                param_name = 'TEMPERATURE' if param == 'temp' else ('PRESSURE' if param == 'press' else 'HUMIDITY')
                types.append(f"{param_name}_FROZEN")
                explanations.append(f"{param_name.title()} sensor reading stuck/unchanged for {persistence_val} consecutive timestamps.")

        # Decision synthesis
        is_anom = 1 if len(flags) > 0 else 0
        primary_fault = types[0] if len(types) > 0 else "NORMAL"
        severity = 'NONE'
        if is_anom:
            if len(flags) >= 3 or "DATA_CORRUPTION" in types or "COMMUNICATION_FAILURE" in types:
                severity = 'CRITICAL'
            elif len(flags) == 2 or "SPIKE" in primary_fault:
                severity = 'HIGH'
            else:
                severity = 'MEDIUM'

        score = min(1.0, 0.4 * len(flags) + 0.3 * (t_delta / self.config['temp_delta_threshold'])) if is_anom else 0.05

        return {
            'anomaly_flag': is_anom,
            'anomaly_score': float(np.clip(score, 0.0, 1.0)),
            'severity': severity,
            'fault_type': primary_fault,
            'explanation': " | ".join(explanations) if explanations else "Normal observation within expected physical and statistical bounds."
        }

    def predict_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        results = []
        for _, row in df.iterrows():
            obs = row.to_dict()
            res = self.predict_observation(obs)
            results.append(res)
        return pd.DataFrame(results)
