import { icons } from '../components/icons.js';

export function renderWeather() {
  return `
    <div style="padding-bottom: 2rem;">
      <header class="page-header">
        <div>
          <h1 class="page-title">Real-Time Weather</h1>
          <p class="subtitle">Live environmental conditions from all monitoring stations</p>
        </div>
        <div class="page-header-right">
          <div style="font-size: 0.85rem; color: var(--text-secondary); display: flex; align-items: center; gap: 0.5rem;">
            <div style="width: 14px; height: 14px;">${icons.refresh}</div>
            Last updated • 10:24:38 AM
          </div>
          <button class="btn btn-outline" style="width: 40px; height: 40px; padding: 0; border-color: transparent;">
            <div style="width: 20px; height: 20px;">${icons.bell}</div>
          </button>
        </div>
      </header>

      <!-- Metrics Row -->
      <div style="display: flex; gap: 1rem; margin-bottom: 2rem; overflow-x: auto; padding-bottom: 0.5rem;">
        
        <!-- Metric Cards -->
        ${[
          { label: 'TEMPERATURE', value: '29.4', unit: '°C', trend: '+1.2°', dir: 'up', icon: '<path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z"/>' },
          { label: 'HUMIDITY', value: '45', unit: '%', trend: '-3%', dir: 'down', icon: '<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/>' },
          { label: 'WIND SPEED', value: '12.6', unit: 'km/h', trend: 'NW', dir: 'up', icon: '<path d="M9.59 4.59A2 2 0 1 1 11 8H2m10.59 11.41A2 2 0 1 0 14 16H2m15.73-8.27A2.5 2.5 0 1 1 19.5 12H2"/>' },
          { label: 'IRRADIANCE', value: '782', unit: 'W/m²', trend: '+4.8%', dir: 'up', icon: '<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>' },
          { label: 'PRESSURE', value: '1008', unit: 'hPa', trend: '-0.8 hPa', dir: 'down', icon: '<circle cx="12" cy="12" r="10"/><polyline points="12 16 16 12 10 8"/>' }
        ].map(m => `
          <div style="flex: 1; min-width: 160px; display: flex; align-items: center; gap: 1rem;">
            <div class="icon-badge" style="width: 48px; height: 48px; flex-shrink: 0; background-color: var(--color-accent-bg); color: var(--color-primary);">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">${m.icon}</svg>
            </div>
            <div>
              <div class="micro-label">${m.label}</div>
              <div style="display: flex; align-items: baseline; gap: 0.25rem;">
                <span style="font-size: 1.5rem; font-weight: 700; color: var(--text-primary); line-height: 1;">${m.value}</span>
                <span style="font-size: 0.9rem; font-weight: 500; color: var(--text-secondary);">${m.unit}</span>
              </div>
              <div style="font-size: 0.75rem; font-weight: 500; color: ${m.dir === 'up' ? 'var(--status-healthy)' : 'var(--status-warning)'}; display: flex; align-items: center; gap: 0.25rem; margin-top: 0.25rem;">
                <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" style="${m.dir === 'down' ? 'transform: rotate(180deg);' : ''}"><path d="m12 19V5"/><path d="m5 12 7-7 7 7"/></svg>
                ${m.trend} from 1h ago
              </div>
            </div>
          </div>
        `).join('')}

        <!-- Station Selector -->
        <div style="flex-shrink: 0; width: 220px; border-left: 1px solid var(--border-color); padding-left: 1rem; display: flex; align-items: center;">
          <div style="width: 100%; position: relative;">
            <div style="position: absolute; left: 1rem; top: 50%; transform: translateY(-50%); color: var(--text-secondary); width: 16px; height: 16px;">
              ${icons.monitoring}
            </div>
            <div style="position: absolute; left: 2.5rem; top: 0.5rem; font-size: 0.65rem; color: var(--text-secondary); font-weight: 600; text-transform: uppercase;">Station</div>
            <select style="width: 100%; padding: 1.5rem 1rem 0.5rem 2.5rem; border-radius: var(--radius-full); border: 1px solid var(--border-color); background-color: white; font-family: var(--font-sans); outline: none; appearance: none; cursor: pointer; font-weight: 600; font-size: 0.9rem;">
              <option>Delta Station 07</option>
              <option>Theta Station 14</option>
              <option>Beta Station 03</option>
            </select>
            <div style="position: absolute; right: 1rem; top: 50%; transform: translateY(-50%); color: var(--text-secondary); pointer-events: none; width: 16px; height: 16px;">
              ${icons.chevronDown}
            </div>
          </div>
        </div>
      </div>

      <!-- Chart Area -->
      <div class="card" style="position: relative; padding: 2rem 1.5rem;">
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
          <div style="display: flex; align-items: center; gap: 0.5rem; font-weight: 600; font-size: 1.1rem;">
            Temperature (°C)
            <div style="width: 16px; height: 16px; color: var(--text-secondary);">${icons.chevronDown}</div>
          </div>
          <div style="display: flex; gap: 0.5rem;">
            <button class="btn btn-outline" style="padding: 0.5rem 1rem; border-radius: var(--radius-md); font-size: 0.85rem;">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 0.25rem;"><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg>
              Compare
              <div style="width: 14px; height: 14px; display: inline-block; margin-left: 0.25rem;">${icons.chevronDown}</div>
            </button>
            <button class="btn btn-outline" style="width: 36px; padding: 0; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center;">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/></svg>
            </button>
          </div>
        </div>

        <!-- The Big Chart -->
        <div style="position: relative; height: 400px; width: 100%;">
          
          <svg viewBox="0 0 1000 400" preserveAspectRatio="none" style="width: 100%; height: 100%;">
            <!-- Grid Background -->
            <line x1="0" y1="50" x2="1000" y2="50" stroke="var(--border-light)" stroke-width="1" />
            <line x1="0" y1="125" x2="1000" y2="125" stroke="var(--border-light)" stroke-width="1" />
            <line x1="0" y1="200" x2="1000" y2="200" stroke="var(--border-light)" stroke-width="1" />
            <line x1="0" y1="275" x2="1000" y2="275" stroke="var(--border-light)" stroke-width="1" />
            <line x1="0" y1="350" x2="1000" y2="350" stroke="var(--border-color)" stroke-width="1" />
            
            <defs>
              <linearGradient id="chart-area" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="var(--color-primary)" stop-opacity="0.1" />
                <stop offset="100%" stop-color="var(--color-primary)" stop-opacity="0" />
              </linearGradient>
            </defs>

            <!-- Chart Path -->
            <path d="M0,250 Q20,245 40,260 T100,265 T150,250 T200,240 T250,260 T300,270 T350,270 T400,250 T430,230 L450,150 L470,80 T490,180 T520,260 T550,300 T600,320 T650,300 T700,280 L730,250 T770,270 T820,300 T850,290 T900,280 T950,270 L1000,260 L1000,350 L0,350 Z" fill="url(#chart-area)" />
            
            <path d="M0,250 Q20,245 40,260 T100,265 T150,250 T200,240 T250,260 T300,270 T350,270 T400,250 T430,230 L450,150 L470,80 T490,180 T520,260 T550,300 T600,320 T650,300 T700,280 L730,250 T770,270 T820,300 T850,290 T900,280 T950,270 L1000,260" fill="none" stroke="var(--color-primary)" stroke-width="2" />
            
            <!-- Anomaly 1: Critical (Red Spike) -->
            <line x1="470" y1="80" x2="470" y2="350" stroke="var(--status-critical)" stroke-width="1" stroke-dasharray="4 4" />
            <circle cx="470" cy="350" r="3" fill="var(--status-critical)" />
            <!-- Concentric rings for the spike -->
            <circle cx="470" cy="80" r="15" fill="none" stroke="var(--status-critical)" stroke-width="1" opacity="0.5" />
            <circle cx="470" cy="80" r="25" fill="none" stroke="var(--status-critical)" stroke-width="1" opacity="0.3" />
            <circle cx="470" cy="80" r="40" fill="none" stroke="var(--status-critical)" stroke-width="1" opacity="0.1" />
            
            <!-- Diamond Marker -->
            <g transform="translate(470, 80)">
              <polygon points="0,-12 12,0 0,12 -12,0" fill="white" stroke="var(--status-critical)" stroke-width="2" />
              <text x="0" y="3" font-size="10" fill="var(--status-critical)" text-anchor="middle" font-weight="bold">!</text>
            </g>

            <!-- Anomaly 2: Warning -->
            <line x1="730" y1="250" x2="730" y2="350" stroke="var(--status-warning)" stroke-width="1" stroke-dasharray="4 4" />
            <circle cx="730" cy="350" r="3" fill="var(--status-warning)" />
            <g transform="translate(730, 250)">
              <polygon points="0,-10 10,0 0,10 -10,0" fill="white" stroke="var(--status-warning)" stroke-width="2" />
              <circle cx="0" cy="0" r="2" fill="var(--status-warning)" />
            </g>

            <!-- Anomaly 3: Warning -->
            <line x1="850" y1="290" x2="850" y2="350" stroke="var(--status-warning)" stroke-width="1" stroke-dasharray="4 4" />
            <circle cx="850" cy="350" r="3" fill="var(--status-warning)" />
            <g transform="translate(850, 290)">
              <polygon points="0,-10 10,0 0,10 -10,0" fill="white" stroke="var(--status-warning)" stroke-width="2" />
              <circle cx="0" cy="0" r="2" fill="var(--status-warning)" />
            </g>
          </svg>

          <!-- Y Axis Labels -->
          <div style="position: absolute; left: -30px; top: -10px; height: 320px; display: flex; flex-direction: column; justify-content: space-between; font-size: 0.75rem; color: var(--text-secondary); text-align: right; width: 20px;">
            <div>60</div>
            <div>50</div>
            <div>40</div>
            <div>30</div>
            <div>20</div>
            <div>10</div>
            <div>0</div>
          </div>

          <!-- X Axis Labels -->
          <div style="position: absolute; left: 0; bottom: -30px; width: 100%; display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--text-secondary);">
            <div>12:00 AM</div>
            <div>03:00 AM</div>
            <div>06:00 AM</div>
            <div>09:00 AM</div>
            <div>12:00 PM</div>
            <div>03:00 PM</div>
            <div>06:00 PM</div>
            <div>09:00 PM</div>
            <div>12:00 AM</div>
          </div>

          <!-- The Tooltip / Popover for Critical Anomaly -->
          <div style="position: absolute; left: calc(47% + 20px); top: 80px; background-color: var(--bg-card); border: 1px solid var(--border-color); border-radius: var(--radius-lg); padding: 1.25rem; box-shadow: var(--shadow-lg); width: 240px; z-index: 20;">
            <div style="display: flex; align-items: center; gap: 0.5rem; color: var(--status-critical); font-size: 0.65rem; font-weight: 700; letter-spacing: 0.1em; margin-bottom: 0.75rem;">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              ANOMALY DETECTED
            </div>
            
            <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 1rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">
              <div style="font-weight: 700; font-size: 0.95rem;">08:42 AM</div>
              <div style="font-size: 0.8rem; color: var(--text-secondary);">May 26, 2025</div>
            </div>
            
            <div style="display: flex; flex-direction: column; gap: 0.5rem; font-size: 0.85rem; margin-bottom: 1rem;">
              <div style="display: flex; justify-content: space-between;">
                <span class="micro-label" style="margin: 0; color: var(--text-secondary);">TEMP</span>
                <span style="font-weight: 600; color: var(--status-critical);">58.7 °C</span>
              </div>
              <div style="display: flex; justify-content: space-between;">
                <span class="micro-label" style="margin: 0; color: var(--text-secondary);">HUMIDITY</span>
                <span style="font-weight: 600;">28 %</span>
              </div>
              <div style="display: flex; justify-content: space-between;">
                <span class="micro-label" style="margin: 0; color: var(--text-secondary);">WIND SPEED</span>
                <span style="font-weight: 600;">16.2 km/h</span>
              </div>
              <div style="display: flex; justify-content: space-between;">
                <span class="micro-label" style="margin: 0; color: var(--text-secondary);">IRRADIANCE</span>
                <span style="font-weight: 600;">912 W/m²</span>
              </div>
              <div style="display: flex; justify-content: space-between;">
                <span class="micro-label" style="margin: 0; color: var(--text-secondary);">PRESSURE</span>
                <span style="font-weight: 600;">1006 hPa</span>
              </div>
            </div>
            
            <div style="display: flex; align-items: center; gap: 0.5rem; background-color: var(--status-critical-bg); padding: 0.5rem; border-radius: var(--radius-sm);">
              <span class="micro-label" style="margin: 0; color: var(--status-critical);">SEVERITY</span>
              <span class="badge badge-critical" style="background-color: var(--status-critical); color: white;">CRITICAL</span>
            </div>
            
            <!-- Tooltip Arrow -->
            <div style="position: absolute; left: -6px; top: 20px; width: 12px; height: 12px; background-color: var(--bg-card); border-left: 1px solid var(--border-color); border-bottom: 1px solid var(--border-color); transform: rotate(45deg);"></div>
          </div>
          
        </div>
      </div>

      <!-- Time Range Selector Bottom -->
      <div style="display: flex; justify-content: center; margin-top: 3rem;">
        <div style="display: inline-flex; background-color: var(--bg-card); border: 1px solid var(--border-color); border-radius: var(--radius-full); padding: 0.25rem;">
          <button style="border: none; background: none; padding: 0.5rem 1rem; border-radius: var(--radius-full); font-size: 0.8rem; font-weight: 500; color: var(--text-secondary); cursor: pointer;">1H</button>
          <button style="border: none; background: none; padding: 0.5rem 1rem; border-radius: var(--radius-full); font-size: 0.8rem; font-weight: 500; color: var(--text-secondary); cursor: pointer;">6H</button>
          <button style="border: none; background: none; padding: 0.5rem 1rem; border-radius: var(--radius-full); font-size: 0.8rem; font-weight: 500; color: var(--text-secondary); cursor: pointer;">12H</button>
          <button style="border: none; background-color: var(--color-primary); padding: 0.5rem 1.25rem; border-radius: var(--radius-full); font-size: 0.8rem; font-weight: 600; color: white; cursor: pointer; box-shadow: var(--shadow-sm);">24H</button>
          <button style="border: none; background: none; padding: 0.5rem 1rem; border-radius: var(--radius-full); font-size: 0.8rem; font-weight: 500; color: var(--text-secondary); cursor: pointer;">7D</button>
          <button style="border: none; background: none; padding: 0.5rem 1rem; border-radius: var(--radius-full); font-size: 0.8rem; font-weight: 500; color: var(--text-secondary); cursor: pointer;">30D</button>
          <button style="border: none; background: none; padding: 0.5rem 1rem; border-radius: var(--radius-full); font-size: 0.8rem; font-weight: 500; color: var(--text-secondary); cursor: pointer; display: flex; align-items: center; gap: 0.5rem;">
            Custom
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
          </button>
        </div>
      </div>
    </div>
  `;
}
