"""Generate SkyGuard's six clearly labelled synthetic CSV datasets."""
from pathlib import Path
import numpy as np
import pandas as pd

OUT = Path(__file__).parent / "data"
RNG = np.random.default_rng(20260830)
STATIONS = [
    ("AWS001", 12.97, 77.59, 900, 0.0, 0.0),
    ("AWS002", 12.94, 77.63, 870, 0.8, 0.3),
    ("AWS003", 13.01, 77.55, 920, -0.6, -0.2),
    ("AWS004", 12.90, 77.50, 780, 1.2, -0.5),
    ("AWS005", 13.07, 77.67, 970, -1.0, 0.4),
    ("AWS006", 12.84, 77.70, 840, 0.4, -0.3),
]
PARAMS = ("temperature", "pressure", "humidity")


def normal_data(days: int = 32) -> pd.DataFrame:
    timestamps = pd.date_range("2026-05-01", periods=days * 288, freq="5min")
    frames = []
    for i, (station, lat, lon, altitude, temp_offset, humid_offset) in enumerate(STATIONS):
        n = len(timestamps); h = timestamps.hour.to_numpy() + timestamps.minute.to_numpy()/60
        day = np.arange(n) / 288
        # Shared weather makes nearby stations correlated; local noise/offset retains station character.
        synoptic = 1.8*np.sin(2*np.pi*day/8 + .4) + .8*np.sin(2*np.pi*day/3.2)
        temp = 27 + 5.5*np.sin(2*np.pi*(h-8)/24) + synoptic + temp_offset - .0065*(altitude-850) + RNG.normal(0,.22,n)
        pressure = 1010 - .105*(altitude-850) + 2.2*np.sin(2*np.pi*day/5.5 + .5) + .6*np.sin(2*np.pi*h/24) + RNG.normal(0,.12,n)
        humidity = 70 - .95*(temp-27) + 5*np.sin(2*np.pi*(h+3)/24) + humid_offset + RNG.normal(0,1.1,n)
        frames.append(pd.DataFrame({"timestamp": timestamps, "station_id": station, "latitude":lat, "longitude":lon,
            "altitude_m":altitude, "temperature":temp, "pressure":pressure, "humidity":np.clip(humidity, 12,99),
            "fault_type":"NORMAL", "fault_parameter":"none", "is_anomaly":0, "severity":"NONE",
            "event_type":"NONE", "is_genuine_event":0}))
    return pd.concat(frames, ignore_index=True)


def label_rows(df: pd.DataFrame, idx, fault: str, parameter: str, severity="HIGH") -> None:
    df.loc[idx, ["fault_type", "fault_parameter", "is_anomaly", "severity"]] = [fault, parameter, 1, severity]


def inject_faults(df: pd.DataFrame) -> pd.DataFrame:
    """Fault periods span the chronology; the last 15% is later held out unseen."""
    out = df.copy(); n_per = len(out) // len(STATIONS); usable = int(n_per*.82)
    kinds = [("TEMPERATURE_SPIKE", "temperature", 25), ("PRESSURE_SPIKE", "pressure", 30),
             ("HUMIDITY_SPIKE", "humidity", 45), ("TEMPERATURE_BIAS", "temperature", 36),
             ("PRESSURE_BIAS", "pressure", 20), ("HUMIDITY_BIAS", "humidity", 20),
             ("TEMPERATURE_DRIFT", "temperature", 48), ("PRESSURE_DRIFT", "pressure", 48),
             ("HUMIDITY_DRIFT", "humidity", 48), ("TEMPERATURE_FROZEN", "temperature", 18),
             ("PRESSURE_FROZEN", "pressure", 18), ("HUMIDITY_FROZEN", "humidity", 18)]
    usable = int(n_per*.98)
    for s_i, (station, *_rest) in enumerate(STATIONS):
        base = out.index[out.station_id.eq(station)].to_numpy()
        cursor = 80 + s_i*17
        for k, (fault, p, length) in enumerate(kinds):
            # Repeat each family once early for training and once later for
            # chronological validation. The later instance is never in fit data.
            for start in (cursor + k*300 + s_i*73, 5000 + cursor + k*210 + s_i*73):
                ix = base[start:start+length]
                if "SPIKE" in fault:
                    out.loc[ix[0], p] += {"temperature":25, "pressure":30, "humidity":45}[p]
                    label_rows(out, ix[:1], fault, p, "CRITICAL")
                elif "FROZEN" in fault:
                    out.loc[ix, p] = float(out.loc[ix[0], p]); label_rows(out, ix, fault, p)
                elif "DRIFT" in fault:
                    out.loc[ix, p] += np.linspace(0, {"temperature":8,"pressure":15,"humidity":28}[p], len(ix)); label_rows(out, ix, fault, p, "MEDIUM")
                else:
                    out.loc[ix, p] += {"temperature":5,"pressure":12,"humidity":18}[p]; label_rows(out, ix, fault, p, "MEDIUM")
        # Data corruption, missing packets, duplicates, and simultaneous/intermittent failure.
        ix = base[usable-180+s_i:usable-176+s_i]; out.loc[ix, "humidity"] = 135; label_rows(out, ix, "DATA_CORRUPTION", "humidity", "CRITICAL")
        ix = base[usable-135+s_i:usable-130+s_i]; out.loc[ix, list(PARAMS)] = np.nan; label_rows(out, ix, "COMMUNICATION_FAILURE", "all", "CRITICAL")
        ix = base[usable-100+s_i:usable-96+s_i]; out.loc[ix, list(PARAMS)] = out.loc[ix[0], list(PARAMS)].to_numpy(); label_rows(out, ix, "DUPLICATE_PACKET", "all", "MEDIUM")
        ix = base[usable-60+s_i:usable-56+s_i]; out.loc[ix, "temperature"] += 20; out.loc[ix, "pressure"] += 20; label_rows(out, ix, "SIMULTANEOUS_SENSOR_FAILURE", "multiple", "CRITICAL")
    return out


def add_events(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy(); block = len(out)//len(STATIONS)
    # Regional heatwave: all local stations respond, so it is not sensor fault data.
    for start, length, event, dt, dp, dh in [(1800, 96, "REGIONAL_HEATWAVE", 9, -2, -18), (4100,72,"RAPID_PRESSURE_SYSTEM",-2,-9,12), (6200,72,"COLD_WAVE",-8,3,16), (8200,72,"WIDESPREAD_HUMIDITY_SURGE",-1,-1,20)]:
        for station, *_ in STATIONS:
            ix = out.index[out.station_id.eq(station)].to_numpy()[start:start+length]
            out.loc[ix, "temperature"] += dt; out.loc[ix, "pressure"] += dp; out.loc[ix, "humidity"] += dh
            # Preserve genuine event, except pre-existing explicitly injected faults.
            normal = out.loc[ix, "is_anomaly"].eq(0)
            ni = ix[normal.to_numpy()]
            out.loc[ni, ["event_type", "is_genuine_event"]] = [event, 1]
    return out


def temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    x = df.sort_values(["station_id", "timestamp"]).copy(); ts = pd.to_datetime(x.timestamp)
    x["hour"] = ts.dt.hour; x["day_of_year"] = ts.dt.dayofyear
    x["hour_sin"] = np.sin(2*np.pi*x.hour/24); x["hour_cos"] = np.cos(2*np.pi*x.hour/24)
    x["doy_sin"] = np.sin(2*np.pi*x.day_of_year/366); x["doy_cos"] = np.cos(2*np.pi*x.day_of_year/366)
    for p in PARAMS:
        g=x.groupby("station_id")[p]
        x[f"{p}_delta"] = g.diff()
        x[f"{p}_roll_mean"] = g.transform(lambda q:q.shift().rolling(6,min_periods=2).mean())
        x[f"{p}_roll_std"] = g.transform(lambda q:q.shift().rolling(6,min_periods=2).std())
        x[f"{p}_roll_median"] = g.transform(lambda q:q.shift().rolling(6,min_periods=2).median())
        x[f"{p}_mad"] = g.transform(lambda q:q.shift().rolling(6,min_periods=2).apply(lambda z: np.median(np.abs(z-np.median(z))), raw=True))
        x[f"{p}_residual"] = x[p]-x[f"{p}_roll_mean"]
        x[f"{p}_missing"] = x[p].isna().astype(int)
    x["dew_point"] = 243.04*(np.log(np.maximum(x.humidity,1)/100)+(17.625*x.temperature)/(243.04+x.temperature))/(17.625-np.log(np.maximum(x.humidity,1)/100)-(17.625*x.temperature)/(243.04+x.temperature))
    x["temp_humidity_product"] = x.temperature*x.humidity; x["temp_pressure_product"] = x.temperature*x.pressure
    return x.replace([np.inf,-np.inf],np.nan)


def spatial_features(df: pd.DataFrame) -> pd.DataFrame:
    x=df.copy()
    for p in PARAMS:
        grp=x.groupby("timestamp")[p]
        x[f"neighbor_{p}_median"] = grp.transform("median")
        x[f"spatial_residual_{p}"] = x[p]-x[f"neighbor_{p}_median"]
        mad=grp.transform(lambda q: np.median(np.abs(q-np.nanmedian(q))))
        x[f"spatial_z_{p}"] = .6745*x[f"spatial_residual_{p}"]/mad.clip(lower=.1)
    x["spatial_anomaly_score"] = x[[f"spatial_z_{p}" for p in PARAMS]].abs().max(axis=1).clip(0,15)/15
    x["spatial_consensus_score"] = 1-x.spatial_anomaly_score
    x["event_likelihood"] = np.where(x.is_genuine_event.eq(1), x.spatial_consensus_score, 0)
    x["sensor_fault_likelihood"] = np.where(x.is_anomaly.eq(1), x.spatial_anomaly_score, 0)
    return x


def save_datasets() -> dict[str, int]:
    OUT.mkdir(exist_ok=True)
    raw=add_events(inject_faults(normal_data()))
    feat=spatial_features(temporal_features(raw))
    # Strict chronological held-out data: last 15% of time at all stations.
    cutoff=feat.timestamp.quantile(.85); train=feat[feat.timestamp<cutoff].copy(); test=feat[feat.timestamp>=cutoff].copy()
    edge_cols=["timestamp","station_id",*PARAMS,*[f"{p}_delta" for p in PARAMS],*[f"{p}_roll_mean" for p in PARAMS],*[f"{p}_roll_std" for p in PARAMS],*[f"{p}_missing" for p in PARAMS],"is_anomaly"]
    # E1 covers only faults detectable from six local observations. Slow bias and
    # drift remain positives for P1/P3, not a false promise for the ESP32 model.
    edge_detectable = train.fault_type.str.contains("SPIKE|FROZEN|DATA_CORRUPTION|COMMUNICATION_FAILURE|DUPLICATE_PACKET|SIMULTANEOUS_SENSOR_FAILURE", regex=True)
    edge = train[edge_cols].copy(); edge["label"] = edge_detectable.astype(int)
    edge.drop(columns="is_anomaly").to_csv(OUT/"edge_training.csv",index=False)
    train.to_csv(OUT/"pc_anomaly_training.csv",index=False)
    fault_cols=list(dict.fromkeys([*train.columns,"fault_type","fault_parameter","is_anomaly","severity"]))
    train[fault_cols].to_csv(OUT/"fault_classification.csv",index=False)
    spatial_cols=["timestamp","station_id","latitude","longitude",*PARAMS,*[f"neighbor_{p}_median" for p in PARAMS],*[f"spatial_residual_{p}" for p in PARAMS],"spatial_anomaly_score","spatial_consensus_score","event_likelihood","sensor_fault_likelihood","event_type","is_genuine_event","fault_type","is_anomaly"]
    train[spatial_cols].to_csv(OUT/"spatial_consistency.csv",index=False)
    # Per-station weekly windows for health/degradation modelling (estimated risk label, not true failure probability).
    d=train.copy(); d["window_start"]=pd.to_datetime(d.timestamp).dt.to_period("7D").dt.start_time
    agg=d.groupby(["station_id","window_start"]).agg(anomaly_frequency=("is_anomaly","mean"), anomaly_severity=("is_anomaly","sum"), missing_data_pct=("temperature_missing","mean"), communication_failure_frequency=("fault_type",lambda q:(q=="COMMUNICATION_FAILURE").mean()), station_disagreement=("spatial_anomaly_score","mean"), temperature_drift=("temperature_residual","mean"), pressure_drift=("pressure_residual","mean"), humidity_drift=("humidity_residual","mean"), rolling_variance=("temperature_roll_std","mean"), repeated_fault_count=("fault_type",lambda q:(q!="NORMAL").sum())).reset_index()
    max_faults = max(1, float(agg.repeated_fault_count.max()))
    risk=(100*(.35*agg.anomaly_frequency+.2*agg.missing_data_pct+.25*(agg.station_disagreement.clip(0,1))+.2*(agg.repeated_fault_count/max_faults))).clip(0,100)
    agg["estimated_health_risk_score"]=risk; agg["sensor_health_score"]=(100-risk).round(1)
    agg["degradation_level"]=pd.cut(risk,[-1,15,35,60,101],labels=["HEALTHY","WATCH","DEGRADING","CRITICAL"])
    agg["maintenance_priority"]=pd.cut(risk,[-1,15,35,60,101],labels=["LOW","MEDIUM","HIGH","URGENT"])
    agg.to_csv(OUT/"sensor_degradation.csv",index=False)
    test.to_csv(OUT/"test_dataset.csv",index=False)
    return {p.name:len(pd.read_csv(p)) for p in OUT.glob("*.csv")}


if __name__ == "__main__":
    print(save_datasets())
