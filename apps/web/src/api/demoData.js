const now = new Date();
const minutesAgo = (minutes) => new Date(now.getTime() - minutes * 60_000).toISOString();

export const demoStations = [
  { id: 'AWS-PUNE-01', name: 'Pune Observatory', region: 'Maharashtra', health: 'Healthy', anomaly_status: 'None', last_updated: minutesAgo(2), latest: { temperature: 27.4, pressure: 1009.8, relative_humidity: 68, timestamp: minutesAgo(2) } },
  { id: 'AWS-MUM-02', name: 'Colaba Coast', region: 'Maharashtra', health: 'Warning', anomaly_status: 'High wind pattern', last_updated: minutesAgo(4), latest: { temperature: 29.1, pressure: 1007.2, relative_humidity: 79, timestamp: minutesAgo(4) } },
  { id: 'AWS-DEL-03', name: 'Safdarjung', region: 'Delhi', health: 'Healthy', anomaly_status: 'None', last_updated: minutesAgo(3), latest: { temperature: 31.8, pressure: 1004.6, relative_humidity: 46, timestamp: minutesAgo(3) } },
  { id: 'AWS-GUW-04', name: 'Guwahati Field', region: 'Assam', health: 'Critical', anomaly_status: 'Rainfall sensor drift', last_updated: minutesAgo(7), latest: { temperature: 25.6, pressure: 1006.1, relative_humidity: 91, timestamp: minutesAgo(7) } },
  { id: 'AWS-JPR-05', name: 'Jaipur Airport', region: 'Rajasthan', health: 'Healthy', anomaly_status: 'None', last_updated: minutesAgo(1), latest: { temperature: 34.2, pressure: 1002.9, relative_humidity: 32, timestamp: minutesAgo(1) } },
  { id: 'AWS-KOC-06', name: 'Kochi Harbour', region: 'Kerala', health: 'Healthy', anomaly_status: 'None', last_updated: minutesAgo(5), latest: { temperature: 28.3, pressure: 1008.5, relative_humidity: 84, timestamp: minutesAgo(5) } },
];

export const demoOverview = {
  last_updated: minutesAgo(1),
  stats: { network_health: 92, total_stations: 6, healthy_stations: 4, warning_stations: 1, critical_stations: 1, active_anomalies: 2, data_quality: '98.6%' },
  recent_anomalies: [
    { station_id: 'AWS-GUW-04', title: 'Rainfall sensor drift detected', severity: 'Critical' },
    { station_id: 'AWS-MUM-02', title: 'Wind-gust pattern exceeds baseline', severity: 'Warning' },
  ],
};

export function demoWeather(stationId) {
  const station = demoStations.find((item) => item.id === stationId) || demoStations[0];
  const base = station.latest;
  return Array.from({ length: 12 }, (_, index) => ({
    timestamp: minutesAgo((11 - index) * 10),
    temperature: Number((base.temperature + Math.sin(index * 0.8) * 1.4).toFixed(1)),
    pressure: Number((base.pressure + Math.cos(index * 0.55) * 1.8).toFixed(1)),
    relative_humidity: Math.round(base.relative_humidity + Math.sin(index * 0.65) * 5),
  }));
}

export function demoStation(stationId) {
  const station = demoStations.find((item) => item.id === stationId) || demoStations[0];
  return { ...station, observations: demoWeather(station.id) };
}
