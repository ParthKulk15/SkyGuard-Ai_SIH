const API_BASE_URL = (import.meta.env?.VITE_API_BASE_URL || '').replace(/\/$/, '');
export async function apiGet(path) { const response = await fetch(`${API_BASE_URL}${path}`); if (!response.ok) throw Error(`API request failed (${response.status})`); return response.json(); }
export async function downloadReport() { const response = await fetch(`${API_BASE_URL}/v1/reports/live-monitor.pdf`); if (!response.ok) throw Error('Report download failed'); return response.blob(); }
export const getOverview = () => apiGet('/v1/overview');
export const getStations = () => apiGet('/v1/stations');
export const getStation = id => apiGet(`/v1/stations/${encodeURIComponent(id)}`);
export const getWeather = (id, range) => apiGet(`/v1/weather?station_id=${encodeURIComponent(id)}&range=${encodeURIComponent(range)}`);
export const getAnomalies = () => apiGet('/v1/anomalies');
