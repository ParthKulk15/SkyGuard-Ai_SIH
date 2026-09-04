import { getStations, getWeather } from '../api/client.js';
import { demoStations, demoWeather } from '../api/demoData.js';
import { unwrap, value, state, mode } from './dataHelpers.js';

const chartColors = { temperature: '#e2673a', pressure: '#2563eb', humidity: '#16806a' };

function formatObservationTime(timestamp, index) {
  if (!timestamp) return `${index * 10}m`;
  return new Intl.DateTimeFormat('en-IN', { hour: '2-digit', minute: '2-digit' }).format(new Date(timestamp));
}

function smoothPath(points) {
  if (points.length < 2) return '';
  const start = `M ${points[0].x.toFixed(1)} ${points[0].y.toFixed(1)}`;
  return points.slice(0, -1).reduce((path, point, index) => {
    const previous = points[index - 1] || point;
    const next = points[index + 1];
    const following = points[index + 2] || next;
    const controlOne = { x: point.x + (next.x - previous.x) / 6, y: point.y + (next.y - previous.y) / 6 };
    const controlTwo = { x: next.x - (following.x - point.x) / 6, y: next.y - (following.y - point.y) / 6 };
    return `${path} C ${controlOne.x.toFixed(1)} ${controlOne.y.toFixed(1)}, ${controlTwo.x.toFixed(1)} ${controlTwo.y.toFixed(1)}, ${next.x.toFixed(1)} ${next.y.toFixed(1)}`;
  }, start);
}

function trendChart(label, keys, unit, rows, colorKey) {
  const samples = rows.map((row, index) => ({ value: Number(value(row, ...keys)), timestamp: row.timestamp, index })).filter((sample) => Number.isFinite(sample.value));
  if (!samples.length) return `<div class="card"><div class="card-title">${label}</div>${state('No observations returned.', 'empty')}</div>`;

  const width = 360, height = 164, padding = { top: 18, right: 12, bottom: 28, left: 38 };
  const values = samples.map((sample) => sample.value);
  const rawLow = Math.min(...values), rawHigh = Math.max(...values);
  const buffer = (rawHigh - rawLow || Math.max(Math.abs(rawHigh) * 0.04, 1)) * 0.22;
  const low = rawLow - buffer, high = rawHigh + buffer, span = high - low || 1;
  const point = (sample, index) => ({
    x: padding.left + (index / Math.max(samples.length - 1, 1)) * (width - padding.left - padding.right),
    y: padding.top + (1 - (sample.value - low) / span) * (height - padding.top - padding.bottom),
  });
  const points = samples.map(point);
  const line = smoothPath(points);
  const ticks = [0, 0.5, 1].map((step) => ({ value: high - span * step, y: padding.top + step * (height - padding.top - padding.bottom) }));
  const labels = [0, Math.floor((samples.length - 1) / 2), samples.length - 1].map((index) => ({ text: formatObservationTime(samples[index].timestamp, index), x: points[index].x }));
  const latest = samples.at(-1);
  const latestPoint = points.at(-1);
  const color = chartColors[colorKey];

  return `<section class="card weather-card" aria-labelledby="${colorKey}-chart-title">
    <div class="weather-card-header"><div><div class="card-title" id="${colorKey}-chart-title">${label}</div><div class="subtitle">Last 2 hours · simulated AWS feed</div></div><div class="weather-latest" style="--chart-color:${color}"><strong>${latest.value.toFixed(1)}</strong><span>${unit} now</span></div></div>
    <div class="weather-chart-shell">
      <svg class="weather-line-chart" viewBox="0 0 ${width} ${height}" role="img" aria-label="${label} trend over the last two hours">
        ${ticks.map((tick) => `<g><line x1="${padding.left}" y1="${tick.y.toFixed(1)}" x2="${width - padding.right}" y2="${tick.y.toFixed(1)}" class="chart-grid-line"/><text x="0" y="${(tick.y + 4).toFixed(1)}" class="chart-axis-label">${tick.value.toFixed(1)}</text></g>`).join('')}
        <path d="${line}" fill="none" stroke="${color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" />
        ${points.map((item, index) => `<circle cx="${item.x.toFixed(1)}" cy="${item.y.toFixed(1)}" r="4" fill="#fff" stroke="${color}" stroke-width="2.5"><title>${formatObservationTime(samples[index].timestamp, index)}: ${samples[index].value.toFixed(1)} ${unit}</title></circle>`).join('')}
        <circle cx="${latestPoint.x.toFixed(1)}" cy="${latestPoint.y.toFixed(1)}" r="6" fill="${color}" stroke="#fff" stroke-width="3" />
        ${labels.map((item) => `<text x="${item.x.toFixed(1)}" y="${height - 5}" text-anchor="middle" class="chart-axis-label">${item.text}</text>`).join('')}
      </svg>
    </div>
    <p class="subtitle weather-range">Range: ${rawLow.toFixed(1)}–${rawHigh.toFixed(1)} ${unit}</p>
  </section>`;
}

export async function renderWeather() {
  let stations, observations;
  try {
    stations = unwrap(await getStations(), 'stations');
    observations = unwrap(await getWeather(stations[0]?.id || stations[0]?.station_id || '', '24H'), 'observations');
  } catch {
    stations = demoStations;
    observations = demoWeather(stations[0].id);
  }
  if (!stations.length) return state('No stations are available.', 'empty');
  const rows = Array.isArray(observations) ? observations : [];

  return `<div><header class="page-header"><div><h1 class="page-title">Weather</h1><p class="subtitle">AWS observations</p></div>${mode()}</header><div class="card"><label class="input-label">Station</label><select class="input-field">${stations.map((station) => `<option>${station.name || station.station_name || station.id || station.station_id}</option>`).join('')}</select><div class="range-pills">${['1H', '6H', '12H', '24H', '7D'].map((range) => `<button class="btn btn-outline">${range}</button>`).join('')}</div></div><div class="grid-3 weather-chart-grid" style="margin-top:1.5rem">${trendChart('Temperature', ['temperature', 'temp'], '°C', rows, 'temperature')}${trendChart('Atmospheric pressure', ['pressure', 'atmospheric_pressure'], 'hPa', rows, 'pressure')}${trendChart('Relative humidity', ['relative_humidity', 'humidity'], '%', rows, 'humidity')}</div></div>`;
}
