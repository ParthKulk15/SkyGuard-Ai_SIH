import { icons } from '../components/icons.js';

export function renderMonitoring() {
  return `
    <div style="padding-bottom: 2rem;">
      <header class="page-header">
        <div>
          <h1 class="page-title">Live Monitoring</h1>
          <p class="subtitle">Real-time status of all monitoring stations</p>
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

      <!-- Stats Header Row -->
      <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 2rem;">
        
        <div>
          <div class="micro-label" style="text-transform: none; margin-bottom: 0.5rem;">Network Health Score</div>
          <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="font-size: 3rem; font-weight: 800; color: var(--color-primary); line-height: 1; letter-spacing: -0.04em;">
              98<span style="font-size: 1.25rem; font-weight: 500; color: var(--text-secondary); letter-spacing: 0;">/100</span>
            </div>
            
            <div>
              <div style="display: flex; gap: 4px; margin-bottom: 0.25rem;">
                ${[...Array(10)].map((_, i) => `
                  <div style="width: 16px; height: 6px; border-radius: 3px; background-color: ${i < 9 ? 'var(--status-healthy)' : 'var(--border-color)'};"></div>
                `).join('')}
              </div>
              <div style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem; font-weight: 600;">
                <div class="status-dot dot-healthy" style="width: 12px; height: 12px; border: 2px solid white; outline: 1px solid var(--status-healthy);"></div>
                <span style="color: var(--color-primary);">Excellent</span>
              </div>
            </div>
          </div>
        </div>

        <div style="display: flex; gap: 3rem;">
          <div style="text-align: center;">
            <div class="micro-label" style="text-transform: none; margin-bottom: 0.25rem;">Total Stations</div>
            <div style="font-size: 1.5rem; font-weight: 700;">24</div>
          </div>
          <div style="text-align: center; display: flex; flex-direction: column; align-items: center;">
            <div class="micro-label" style="text-transform: none; margin-bottom: 0.25rem;">Healthy</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: var(--status-healthy); display: flex; align-items: center; gap: 0.5rem;">
              18
              <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/></svg>
            </div>
          </div>
          <div style="text-align: center; display: flex; flex-direction: column; align-items: center;">
            <div class="micro-label" style="text-transform: none; margin-bottom: 0.25rem;">Warnings</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: var(--status-warning); display: flex; align-items: center; gap: 0.5rem;">
              4
              <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/></svg>
            </div>
          </div>
          <div style="text-align: center; display: flex; flex-direction: column; align-items: center;">
            <div class="micro-label" style="text-transform: none; margin-bottom: 0.25rem;">Critical</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: var(--status-critical); display: flex; align-items: center; gap: 0.5rem;">
              2
              <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/></svg>
            </div>
          </div>
        </div>

      </div>

      <!-- Main Layout -->
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; height: calc(100vh - 220px); min-height: 600px;">
        
        <!-- Map Column -->
        <div class="card" style="padding: 0; position: relative; overflow: hidden; display: flex; flex-direction: column;">
          
          <div style="flex: 1; position: relative; background-color: #F0F2EE; overflow: hidden;">
            <div class="bg-topo" style="opacity: 0.6;"></div>
            
            <style>
              .map-node:hover .node-tooltip {
                opacity: 1 !important;
                z-index: 100;
              }
              .node-tooltip {
                transition: opacity 0.2s ease-in-out;
              }
            </style>
            
            <!-- Real India Map Graphic -->
            <svg viewBox="0 0 500 600" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 90%; height: 90%; overflow: visible;">
              <image href="/india-map.svg" x="-20" y="-10" width="540" height="640" preserveAspectRatio="xMidYMid meet" opacity="0.4" />
              
              <!-- Map Labels (Hidden for cleaner look, but can be added back if needed) -->
              
              <!-- Node Plotting -->
              ${[
                { id: 'Delta-07', name: 'Delta Station 07', loc: 'Rajasthan', temp: 78.6, power: 2.1, x: 140, y: 220, status: 'critical', ping: true },
                { id: 'Theta-14', name: 'Theta Station 14', loc: 'Madhya Pradesh', temp: 81.2, power: 1.3, x: 230, y: 320, status: 'critical', ping: true },
                { id: 'Beta-03', name: 'Beta Station 03', loc: 'Uttar Pradesh', temp: 29.4, power: 15.7, x: 250, y: 240, status: 'healthy' },
                { id: 'Iota-04', name: 'Iota Station 04', loc: 'Maharashtra', temp: 30.2, power: 14.9, x: 170, y: 390, status: 'healthy' },
                { id: 'Gamma-05', name: 'Gamma Station 05', loc: 'Gujarat', temp: 46.8, power: 8.6, x: 80, y: 300, status: 'warning' },
                { id: 'Zeta-09', name: 'Zeta Station 09', loc: 'Bihar', temp: 51.3, power: 6.4, x: 340, y: 260, status: 'warning' },
                { id: 'Kappa-11', name: 'Kappa Station 11', loc: 'Karnataka', temp: 28.9, power: 10.3, x: 190, y: 470, status: 'healthy' },
                { id: 'Lambda-12', name: 'Lambda Station 12', loc: 'Tamil Nadu', temp: 29.7, power: 9.7, x: 230, y: 540, status: 'healthy' },
                { id: 'Alpha-01', name: 'Alpha Station 01', loc: 'J&K', temp: 15.2, power: 12.1, x: 170, y: 80, status: 'healthy' },
                { id: 'Sigma-22', name: 'Sigma Station 22', loc: 'Assam', temp: 25.1, power: 11.4, x: 440, y: 250, status: 'healthy' },
                { id: 'Omicron-19', name: 'Omicron Station 19', loc: 'Odisha', temp: 33.4, power: 13.2, x: 310, y: 370, status: 'healthy' },
              ].map(n => `
                <g transform="translate(${n.x}, ${n.y})" class="map-node" style="cursor: pointer;">
                  ${n.ping ? `<circle cx="0" cy="0" r="15" fill="var(--status-${n.status})" opacity="0.2"><animate attributeName="r" values="5; 20; 5" dur="2s" repeatCount="indefinite"/></circle>` : ''}
                  <circle cx="0" cy="0" r="8" fill="white" stroke="rgba(0,0,0,0.1)" stroke-width="1" />
                  <circle cx="0" cy="0" r="5" fill="var(--status-${n.status})" />
                  
                  <!-- Tooltip (ForeignObject) -->
                  <foreignObject x="-80" y="-120" width="160" height="110" class="node-tooltip" style="opacity: 0; pointer-events: none; overflow: visible;">
                    <div xmlns="http://www.w3.org/1999/xhtml" style="position: relative; background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 8px; padding: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 100%; height: 100%; box-sizing: border-box; display: flex; flex-direction: column;">
                      <div style="font-weight: 700; font-size: 13px; color: var(--text-primary); margin-bottom: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${n.name}</div>
                      <div style="font-size: 10px; color: var(--text-secondary); margin-bottom: 8px;">${n.loc}</div>
                      <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                        <span style="font-size: 9px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase;">Temp</span>
                        <span style="font-size: 11px; font-weight: 700; color: var(--status-${n.status});">${n.temp} °C</span>
                      </div>
                      <div style="display: flex; justify-content: space-between;">
                        <span style="font-size: 9px; font-weight: 600; color: var(--text-secondary); text-transform: uppercase;">Power</span>
                        <span style="font-size: 11px; font-weight: 700; color: var(--text-primary);">${n.power} kW</span>
                      </div>
                      <!-- Tooltip Arrow -->
                      <div style="position: absolute; bottom: -5px; left: 50%; transform: translateX(-50%) rotate(45deg); width: 10px; height: 10px; background: var(--bg-card); border-right: 1px solid var(--border-color); border-bottom: 1px solid var(--border-color);"></div>
                    </div>
                  </foreignObject>
                </g>
              `).join('')}
            </svg>

            <!-- Map Controls -->
            <div style="position: absolute; bottom: 1.5rem; left: 1.5rem; background-color: var(--bg-card); border: 1px solid var(--border-color); border-radius: var(--radius-md); display: flex; flex-direction: column; box-shadow: var(--shadow-sm);">
              <button style="width: 36px; height: 36px; border: none; background: none; font-size: 1.2rem; cursor: pointer; color: var(--text-secondary); border-bottom: 1px solid var(--border-color);">+</button>
              <button style="width: 36px; height: 36px; border: none; background: none; font-size: 1.2rem; cursor: pointer; color: var(--text-secondary); border-bottom: 1px solid var(--border-color);">-</button>
              <button style="width: 36px; height: 36px; border: none; background: none; display: flex; align-items: center; justify-content: center; cursor: pointer; color: var(--text-secondary);">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="3"/></svg>
              </button>
            </div>

            <!-- Legend -->
            <div style="position: absolute; bottom: 1.5rem; left: 5rem; background-color: var(--bg-card); border: 1px solid var(--border-color); border-radius: var(--radius-full); padding: 0.5rem 1rem; display: flex; gap: 1rem; box-shadow: var(--shadow-sm);">
              <div style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.8rem; font-weight: 500;">
                <div class="status-dot dot-healthy" style="width: 12px; height: 12px; border: 2px solid white; outline: 1px solid var(--status-healthy);"></div> Healthy
              </div>
              <div style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.8rem; font-weight: 500;">
                <div class="status-dot dot-warning" style="width: 12px; height: 12px; border: 2px solid white; outline: 1px solid var(--status-warning);"></div> Warning
              </div>
              <div style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.8rem; font-weight: 500;">
                <div class="status-dot dot-critical" style="width: 12px; height: 12px; border: 2px solid white; outline: 1px solid var(--status-critical);"></div> Critical
              </div>
            </div>
          </div>
        </div>

        <!-- List Column -->
        <div style="display: flex; flex-direction: column; overflow: hidden;">
          
          <!-- Controls -->
          <div style="display: flex; gap: 1rem; margin-bottom: 1.5rem;">
            <div style="flex: 1; position: relative;">
              <div style="position: absolute; left: 1rem; top: 50%; transform: translateY(-50%); color: var(--text-secondary); width: 16px; height: 16px;">
                ${icons.search}
              </div>
              <input type="text" placeholder="Search stations..." style="width: 100%; padding: 0.75rem 1rem 0.75rem 2.5rem; border-radius: var(--radius-md); border: 1px solid var(--border-color); background-color: var(--bg-card); font-family: var(--font-sans); outline: none;" />
            </div>
            
            <div style="position: relative; width: 140px;">
              <select style="width: 100%; padding: 0.75rem 1rem; border-radius: var(--radius-md); border: 1px solid var(--border-color); background-color: var(--bg-card); font-family: var(--font-sans); outline: none; appearance: none; cursor: pointer;">
                <option>All Status</option>
                <option>Critical</option>
                <option>Warning</option>
                <option>Healthy</option>
              </select>
              <div style="position: absolute; right: 1rem; top: 50%; transform: translateY(-50%); color: var(--text-secondary); pointer-events: none; width: 16px; height: 16px;">
                ${icons.chevronDown}
              </div>
            </div>
            
            <div style="display: flex; border: 1px solid var(--border-color); border-radius: var(--radius-md); background-color: var(--bg-card); overflow: hidden;">
              <button style="padding: 0.75rem; border: none; background-color: var(--color-primary); color: white; cursor: pointer; display: flex; align-items: center; justify-content: center;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
              </button>
              <button style="padding: 0.75rem; border: none; background: none; color: var(--text-secondary); cursor: pointer; border-left: 1px solid var(--border-color); display: flex; align-items: center; justify-content: center;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>
              </button>
            </div>
          </div>

          <!-- Cards Grid -->
          <div style="flex: 1; overflow-y: auto; display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; padding-right: 0.5rem; align-content: flex-start;">
            
            <!-- Critical Card 1 -->
            <a href="#/weather" class="card" style="text-decoration: none; border-color: var(--status-critical-bg); box-shadow: 0 4px 12px rgba(220, 38, 38, 0.08);">
              <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                <div>
                  <div style="font-weight: 600; color: var(--text-primary);">Delta Station 07</div>
                  <div style="font-size: 0.8rem; color: var(--text-secondary);">Rajasthan</div>
                </div>
                <div class="badge badge-critical">Critical</div>
              </div>
              
              <div style="display: flex; gap: 4px; margin-bottom: 1rem;">
                ${[...Array(6)].map((_, i) => `
                  <div style="flex: 1; height: 4px; border-radius: 2px; background-color: ${i < 3 ? 'var(--status-critical)' : 'var(--status-critical-bg)'};"></div>
                `).join('')}
              </div>
              
              <div style="display: flex; justify-content: space-between; margin-bottom: 1.5rem;">
                <div>
                  <div class="micro-label" style="text-transform: none;">Temp</div>
                  <div style="font-size: 1.25rem; font-weight: 600; color: var(--status-critical);">78.6 <span style="font-size: 0.9rem; font-weight: 500;">°C</span></div>
                </div>
                <div>
                  <div class="micro-label" style="text-transform: none;">Power</div>
                  <div style="font-size: 1.25rem; font-weight: 600; color: var(--text-primary);">2.1 <span style="font-size: 0.9rem; font-weight: 500;">kW</span></div>
                </div>
              </div>
              
              <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-color); padding-top: 0.75rem; margin-top: auto;">
                <div style="font-size: 0.75rem; color: var(--text-secondary);">Updated 10:24 AM</div>
                <div style="width: 16px; height: 16px; color: var(--text-secondary);">${icons.chevronRight}</div>
              </div>
            </a>

            <!-- Critical Card 2 -->
            <a href="#/weather" class="card" style="text-decoration: none; border-color: var(--status-critical-bg); box-shadow: 0 4px 12px rgba(220, 38, 38, 0.08);">
              <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                <div>
                  <div style="font-weight: 600; color: var(--text-primary);">Theta Station 14</div>
                  <div style="font-size: 0.8rem; color: var(--text-secondary);">Madhya Pradesh</div>
                </div>
                <div class="badge badge-critical">Critical</div>
              </div>
              
              <div style="display: flex; gap: 4px; margin-bottom: 1rem;">
                ${[...Array(6)].map((_, i) => `
                  <div style="flex: 1; height: 4px; border-radius: 2px; background-color: ${i < 2 ? 'var(--status-critical)' : 'var(--status-critical-bg)'};"></div>
                `).join('')}
              </div>
              
              <div style="display: flex; justify-content: space-between; margin-bottom: 1.5rem;">
                <div>
                  <div class="micro-label" style="text-transform: none;">Temp</div>
                  <div style="font-size: 1.25rem; font-weight: 600; color: var(--status-critical);">81.2 <span style="font-size: 0.9rem; font-weight: 500;">°C</span></div>
                </div>
                <div>
                  <div class="micro-label" style="text-transform: none;">Power</div>
                  <div style="font-size: 1.25rem; font-weight: 600; color: var(--text-primary);">1.3 <span style="font-size: 0.9rem; font-weight: 500;">kW</span></div>
                </div>
              </div>
              
              <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-color); padding-top: 0.75rem; margin-top: auto;">
                <div style="font-size: 0.75rem; color: var(--text-secondary);">Updated 10:24 AM</div>
                <div style="width: 16px; height: 16px; color: var(--text-secondary);">${icons.chevronRight}</div>
              </div>
            </a>
            
            <!-- Healthy Card 1 -->
            <a href="#/weather" class="card" style="text-decoration: none;">
              <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                <div>
                  <div style="font-weight: 600; color: var(--text-primary);">Beta Station 03</div>
                  <div style="font-size: 0.8rem; color: var(--text-secondary);">Uttar Pradesh</div>
                </div>
                <div class="badge badge-healthy">Healthy</div>
              </div>
              
              <div style="display: flex; gap: 4px; margin-bottom: 1rem;">
                ${[...Array(6)].map((_, i) => `
                  <div style="flex: 1; height: 4px; border-radius: 2px; background-color: var(--status-healthy);"></div>
                `).join('')}
              </div>
              
              <div style="display: flex; justify-content: space-between; margin-bottom: 1.5rem;">
                <div>
                  <div class="micro-label" style="text-transform: none;">Temp</div>
                  <div style="font-size: 1.25rem; font-weight: 600; color: var(--text-primary);">29.4 <span style="font-size: 0.9rem; font-weight: 500;">°C</span></div>
                </div>
                <div>
                  <div class="micro-label" style="text-transform: none;">Power</div>
                  <div style="font-size: 1.25rem; font-weight: 600; color: var(--text-primary);">15.7 <span style="font-size: 0.9rem; font-weight: 500;">kW</span></div>
                </div>
              </div>
              
              <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-color); padding-top: 0.75rem; margin-top: auto;">
                <div style="font-size: 0.75rem; color: var(--text-secondary);">Updated 10:24 AM</div>
                <div style="width: 16px; height: 16px; color: var(--text-secondary);">${icons.chevronRight}</div>
              </div>
            </a>
            
            <!-- Healthy Card 2 -->
            <a href="#/weather" class="card" style="text-decoration: none;">
              <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                <div>
                  <div style="font-weight: 600; color: var(--text-primary);">Iota Station 04</div>
                  <div style="font-size: 0.8rem; color: var(--text-secondary);">Maharashtra</div>
                </div>
                <div class="badge badge-healthy">Healthy</div>
              </div>
              
              <div style="display: flex; gap: 4px; margin-bottom: 1rem;">
                ${[...Array(6)].map((_, i) => `
                  <div style="flex: 1; height: 4px; border-radius: 2px; background-color: ${i < 5 ? 'var(--status-healthy)' : 'var(--status-healthy-bg)'};"></div>
                `).join('')}
              </div>
              
              <div style="display: flex; justify-content: space-between; margin-bottom: 1.5rem;">
                <div>
                  <div class="micro-label" style="text-transform: none;">Temp</div>
                  <div style="font-size: 1.25rem; font-weight: 600; color: var(--text-primary);">30.2 <span style="font-size: 0.9rem; font-weight: 500;">°C</span></div>
                </div>
                <div>
                  <div class="micro-label" style="text-transform: none;">Power</div>
                  <div style="font-size: 1.25rem; font-weight: 600; color: var(--text-primary);">14.9 <span style="font-size: 0.9rem; font-weight: 500;">kW</span></div>
                </div>
              </div>
              
              <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-color); padding-top: 0.75rem; margin-top: auto;">
                <div style="font-size: 0.75rem; color: var(--text-secondary);">Updated 10:24 AM</div>
                <div style="width: 16px; height: 16px; color: var(--text-secondary);">${icons.chevronRight}</div>
              </div>
            </a>
            
            <!-- Warning Card 1 -->
            <a href="#/weather" class="card" style="text-decoration: none;">
              <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                <div>
                  <div style="font-weight: 600; color: var(--text-primary);">Gamma Station 05</div>
                  <div style="font-size: 0.8rem; color: var(--text-secondary);">Gujarat</div>
                </div>
                <div class="badge badge-warning">Warning</div>
              </div>
              
              <div style="display: flex; gap: 4px; margin-bottom: 1rem;">
                ${[...Array(6)].map((_, i) => `
                  <div style="flex: 1; height: 4px; border-radius: 2px; background-color: ${i < 4 ? 'var(--status-warning)' : 'var(--status-warning-bg)'};"></div>
                `).join('')}
              </div>
              
              <div style="display: flex; justify-content: space-between; margin-bottom: 1.5rem;">
                <div>
                  <div class="micro-label" style="text-transform: none;">Temp</div>
                  <div style="font-size: 1.25rem; font-weight: 600; color: var(--status-warning);">46.8 <span style="font-size: 0.9rem; font-weight: 500;">°C</span></div>
                </div>
                <div>
                  <div class="micro-label" style="text-transform: none;">Power</div>
                  <div style="font-size: 1.25rem; font-weight: 600; color: var(--text-primary);">8.6 <span style="font-size: 0.9rem; font-weight: 500;">kW</span></div>
                </div>
              </div>
              
              <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-color); padding-top: 0.75rem; margin-top: auto;">
                <div style="font-size: 0.75rem; color: var(--text-secondary);">Updated 10:24 AM</div>
                <div style="width: 16px; height: 16px; color: var(--text-secondary);">${icons.chevronRight}</div>
              </div>
            </a>

            <!-- Warning Card 2 -->
            <a href="#/weather" class="card" style="text-decoration: none;">
              <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                <div>
                  <div style="font-weight: 600; color: var(--text-primary);">Zeta Station 09</div>
                  <div style="font-size: 0.8rem; color: var(--text-secondary);">Bihar</div>
                </div>
                <div class="badge badge-warning">Warning</div>
              </div>
              
              <div style="display: flex; gap: 4px; margin-bottom: 1rem;">
                ${[...Array(6)].map((_, i) => `
                  <div style="flex: 1; height: 4px; border-radius: 2px; background-color: ${i < 4 ? 'var(--status-warning)' : 'var(--status-warning-bg)'};"></div>
                `).join('')}
              </div>
              
              <div style="display: flex; justify-content: space-between; margin-bottom: 1.5rem;">
                <div>
                  <div class="micro-label" style="text-transform: none;">Temp</div>
                  <div style="font-size: 1.25rem; font-weight: 600; color: var(--status-warning);">51.3 <span style="font-size: 0.9rem; font-weight: 500;">°C</span></div>
                </div>
                <div>
                  <div class="micro-label" style="text-transform: none;">Power</div>
                  <div style="font-size: 1.25rem; font-weight: 600; color: var(--text-primary);">6.4 <span style="font-size: 0.9rem; font-weight: 500;">kW</span></div>
                </div>
              </div>
              
              <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-color); padding-top: 0.75rem; margin-top: auto;">
                <div style="font-size: 0.75rem; color: var(--text-secondary);">Updated 10:24 AM</div>
                <div style="width: 16px; height: 16px; color: var(--text-secondary);">${icons.chevronRight}</div>
              </div>
            </a>
            
            <!-- Healthy Card 3 -->
            <a href="#/weather" class="card" style="text-decoration: none;">
              <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                <div>
                  <div style="font-weight: 600; color: var(--text-primary);">Kappa Station 11</div>
                  <div style="font-size: 0.8rem; color: var(--text-secondary);">Karnataka</div>
                </div>
                <div class="badge badge-healthy">Healthy</div>
              </div>
              
              <div style="display: flex; gap: 4px; margin-bottom: 1rem;">
                ${[...Array(6)].map((_, i) => `
                  <div style="flex: 1; height: 4px; border-radius: 2px; background-color: var(--status-healthy);"></div>
                `).join('')}
              </div>
              
              <div style="display: flex; justify-content: space-between; margin-bottom: 1.5rem;">
                <div>
                  <div class="micro-label" style="text-transform: none;">Temp</div>
                  <div style="font-size: 1.25rem; font-weight: 600; color: var(--text-primary);">28.9 <span style="font-size: 0.9rem; font-weight: 500;">°C</span></div>
                </div>
                <div>
                  <div class="micro-label" style="text-transform: none;">Power</div>
                  <div style="font-size: 1.25rem; font-weight: 600; color: var(--text-primary);">10.3 <span style="font-size: 0.9rem; font-weight: 500;">kW</span></div>
                </div>
              </div>
              
              <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-color); padding-top: 0.75rem; margin-top: auto;">
                <div style="font-size: 0.75rem; color: var(--text-secondary);">Updated 10:24 AM</div>
                <div style="width: 16px; height: 16px; color: var(--text-secondary);">${icons.chevronRight}</div>
              </div>
            </a>

            <!-- Healthy Card 4 -->
            <a href="#/weather" class="card" style="text-decoration: none;">
              <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
                <div>
                  <div style="font-weight: 600; color: var(--text-primary);">Lambda Station 12</div>
                  <div style="font-size: 0.8rem; color: var(--text-secondary);">Tamil Nadu</div>
                </div>
                <div class="badge badge-healthy">Healthy</div>
              </div>
              
              <div style="display: flex; gap: 4px; margin-bottom: 1rem;">
                ${[...Array(6)].map((_, i) => `
                  <div style="flex: 1; height: 4px; border-radius: 2px; background-color: var(--status-healthy);"></div>
                `).join('')}
              </div>
              
              <div style="display: flex; justify-content: space-between; margin-bottom: 1.5rem;">
                <div>
                  <div class="micro-label" style="text-transform: none;">Temp</div>
                  <div style="font-size: 1.25rem; font-weight: 600; color: var(--text-primary);">29.7 <span style="font-size: 0.9rem; font-weight: 500;">°C</span></div>
                </div>
                <div>
                  <div class="micro-label" style="text-transform: none;">Power</div>
                  <div style="font-size: 1.25rem; font-weight: 600; color: var(--text-primary);">9.7 <span style="font-size: 0.9rem; font-weight: 500;">kW</span></div>
                </div>
              </div>
              
              <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-color); padding-top: 0.75rem; margin-top: auto;">
                <div style="font-size: 0.75rem; color: var(--text-secondary);">Updated 10:24 AM</div>
                <div style="width: 16px; height: 16px; color: var(--text-secondary);">${icons.chevronRight}</div>
              </div>
            </a>
            
          </div>
          
          <div style="text-align: center; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border-color);">
            <button style="border: none; background: none; color: var(--text-secondary); font-size: 0.85rem; font-weight: 500; cursor: pointer; display: inline-flex; align-items: center; gap: 0.5rem;">
              View all stations <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m6 9 6 6 6-6"/></svg>
            </button>
          </div>
          
        </div>

      </div>
    </div>
  `;
}
