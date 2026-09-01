import { icons } from '../components/icons.js';

export function renderOverview() {
  return `
    <div style="padding-bottom: 2rem;">
      <header class="page-header">
        <div>
          <h1 class="page-title">Overview</h1>
          <p class="subtitle">Real-time network health and performance</p>
        </div>
        <div class="page-header-right">
          <div style="font-size: 0.85rem; color: var(--text-secondary); text-align: right;">
            <div>May 26, 2025 • 10:24:38 AM</div>
            <div style="display: flex; align-items: center; justify-content: flex-end; gap: 0.5rem; margin-top: 0.25rem;">
              Auto-refresh 
              <span style="font-weight: 600; color: var(--status-healthy); display: flex; align-items: center; gap: 0.25rem;">
                On <span class="status-dot dot-healthy"></span>
              </span>
            </div>
          </div>
          <button class="btn btn-outline" style="width: 40px; height: 40px; padding: 0; border-color: transparent;">
            <div style="width: 20px; height: 20px;">${icons.bell}</div>
          </button>
        </div>
      </header>

      <!-- Hero Health Panel -->
      <div class="card" style="background: linear-gradient(135deg, var(--bg-card) 0%, #E9F2EC 100%); border: none; margin-bottom: 1.5rem; position: relative; overflow: hidden; min-height: 320px; display: flex; flex-direction: column; justify-content: space-between;">
        
        <!-- Decorative Concentric Circles -->
        <div style="position: absolute; right: 5%; top: 50%; transform: translateY(-50%); width: 400px; height: 400px;">
          ${[...Array(8)].map((_, i) => `
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: ${100 + i*40}px; height: ${100 + i*40}px; border-radius: 50%; border: 1px dashed rgba(45, 106, 79, ${0.4 - i*0.05});"></div>
          `).join('')}
          <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 64px; height: 64px; background-color: var(--color-secondary); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; box-shadow: 0 0 0 10px rgba(45, 106, 79, 0.2);">
            <div style="width: 32px; height: 32px;">${icons.shield}</div>
          </div>
          
          <!-- Node Dots on Rings -->
          <div style="position: absolute; top: 20%; left: 30%; width: 6px; height: 6px; border-radius: 50%; background-color: var(--status-healthy);"></div>
          <div style="position: absolute; top: 70%; left: 20%; width: 6px; height: 6px; border-radius: 50%; background-color: var(--status-healthy);"></div>
          <div style="position: absolute; top: 40%; right: 20%; width: 6px; height: 6px; border-radius: 50%; background-color: var(--status-warning);"></div>
          <div style="position: absolute; bottom: 25%; right: 35%; width: 6px; height: 6px; border-radius: 50%; background-color: var(--status-healthy);"></div>
        </div>

        <div style="position: relative; z-index: 10;">
          <div class="micro-label" style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
            NETWORK HEALTH SCORE 
            <span style="display: inline-block; width: 14px; height: 14px; border: 1px solid currentColor; border-radius: 50%; text-align: center; line-height: 12px;">i</span>
          </div>
          
          <div style="font-size: 7rem; font-weight: 800; color: var(--color-primary); line-height: 0.9; letter-spacing: -0.04em;">
            98<span style="font-size: 2.5rem; font-weight: 500; color: var(--text-secondary); letter-spacing: 0;">/100</span>
          </div>
        </div>
        
        <div style="display: flex; align-items: center; gap: 1rem; position: relative; z-index: 10;">
          <div style="width: 48px; height: 48px; position: relative;">
            <svg viewBox="0 0 36 36" style="width: 100%; height: 100%; transform: rotate(-90deg);">
              <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="rgba(34,165,94,0.2)" stroke-width="3" />
              <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="var(--status-healthy)" stroke-width="3" stroke-dasharray="98, 100" />
            </svg>
          </div>
          <div>
            <div style="font-weight: 600; color: var(--color-primary); font-size: 1.1rem;">Excellent</div>
            <div style="color: var(--text-secondary); font-size: 0.9rem;">All systems operational</div>
          </div>
        </div>
      </div>

      <!-- Stats Row -->
      <div class="grid-3" style="margin-bottom: 1.5rem;">
        <div class="card" style="display: flex; align-items: center; gap: 1rem; padding: 1.25rem 1.5rem;">
          <div style="width: 48px; height: 48px;">
            <svg viewBox="0 0 36 36" style="width: 100%; height: 100%; transform: rotate(-90deg);">
              <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="rgba(34,165,94,0.2)" stroke-width="3" />
              <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="var(--status-healthy)" stroke-width="3" stroke-dasharray="97, 100" />
            </svg>
          </div>
          <div>
            <div class="micro-label" style="text-transform: none;">Healthy Nodes</div>
            <div class="stat-value" style="color: var(--status-healthy);">124<small>/127</small></div>
          </div>
        </div>
        
        <div class="card" style="display: flex; align-items: center; gap: 1rem; padding: 1.25rem 1.5rem;">
          <div style="width: 48px; height: 48px;">
            <svg viewBox="0 0 36 36" style="width: 100%; height: 100%; transform: rotate(-90deg);">
              <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="rgba(245,158,11,0.2)" stroke-width="3" />
              <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="var(--status-warning)" stroke-width="3" stroke-dasharray="3, 100" />
            </svg>
          </div>
          <div>
            <div class="micro-label" style="text-transform: none;">Warnings</div>
            <div class="stat-value" style="color: var(--status-warning);">3<small>/127</small></div>
          </div>
        </div>
        
        <div class="card" style="display: flex; align-items: center; gap: 1rem; padding: 1.25rem 1.5rem;">
          <div style="width: 48px; height: 48px;">
            <svg viewBox="0 0 36 36" style="width: 100%; height: 100%; transform: rotate(-90deg);">
              <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="rgba(107,114,128,0.2)" stroke-width="3" />
              <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="var(--text-secondary)" stroke-width="3" stroke-dasharray="100, 100" />
            </svg>
          </div>
          <div>
            <div class="micro-label" style="text-transform: none;">Total Nodes</div>
            <div class="stat-value">127</div>
          </div>
        </div>
      </div>

      <!-- Map & Alerts Row -->
      <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 1.5rem; margin-bottom: 1.5rem;">
        
        <!-- Live Network Map -->
        <div class="card" style="padding: 0; display: flex; flex-direction: column;">
          <div class="card-header" style="padding: 1.5rem 1.5rem 0; justify-content: space-between;">
            <div class="card-title">Live Network Map</div>
            <div class="badge badge-live">Live</div>
          </div>
          
          <div style="flex: 1; position: relative; min-height: 300px; padding: 1.5rem; display: flex; align-items: center; justify-content: center; overflow: hidden;">
            <div class="bg-topo" style="opacity: 0.3;"></div>
            
            <!-- Abstract Network Graph -->
            <div style="position: relative; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;">
              
              <!-- SVG Lines -->
              <svg style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1;">
                <path d="M 200 150 L 350 150 L 450 100 M 350 150 L 420 220 L 500 200 M 350 150 L 280 250 M 200 150 L 120 100 L 80 180 M 200 150 L 150 220" stroke="var(--border-color)" stroke-width="1" fill="none" />
                <path d="M 350 150 L 420 220" stroke="var(--status-warning)" stroke-width="1.5" fill="none" stroke-dasharray="4 4" />
              </svg>

              <!-- Central Node -->
              <div style="position: absolute; z-index: 2; width: 48px; height: 48px; border-radius: 50%; background-color: var(--color-accent-bg); display: flex; align-items: center; justify-content: center; color: var(--color-secondary); box-shadow: 0 0 0 10px rgba(231,240,233,0.5);">
                <div style="width: 24px; height: 24px;">${icons.shield}</div>
              </div>
              
              <!-- Other Nodes -->
              ${[
                { top: '35%', left: '20%', status: 'healthy' },
                { top: '60%', left: '28%', status: 'healthy' },
                { top: '25%', left: '42%', status: 'healthy' },
                { top: '75%', left: '48%', status: 'healthy' },
                { top: '30%', left: '70%', status: 'healthy' },
                { top: '55%', left: '75%', status: 'warning' },
                { top: '65%', left: '85%', status: 'healthy' },
              ].map(n => `
                <div style="position: absolute; top: ${n.top}; left: ${n.left}; z-index: 2; width: 24px; height: 24px; border-radius: 50%; background-color: white; border: 1px solid var(--border-color); display: flex; align-items: center; justify-content: center;">
                  <div style="width: 10px; height: 10px; border-radius: 50%; background-color: var(--status-${n.status}); box-shadow: 0 0 8px var(--status-${n.status});"></div>
                </div>
              `).join('')}
            </div>

            <!-- Zoom Controls -->
            <div style="position: absolute; bottom: 1.5rem; left: 1.5rem; background-color: var(--bg-card); border: 1px solid var(--border-color); border-radius: var(--radius-md); display: flex; flex-direction: column; z-index: 10;">
              <button style="width: 32px; height: 32px; border: none; background: none; font-size: 1.2rem; cursor: pointer; color: var(--text-secondary); border-bottom: 1px solid var(--border-color);">+</button>
              <button style="width: 32px; height: 32px; border: none; background: none; font-size: 1.2rem; cursor: pointer; color: var(--text-secondary); border-bottom: 1px solid var(--border-color);">-</button>
              <button style="width: 32px; height: 32px; border: none; background: none; display: flex; align-items: center; justify-content: center; cursor: pointer; color: var(--text-secondary);">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="3"/></svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Active Alerts -->
        <div class="card" style="display: flex; flex-direction: column;">
          <div class="card-header" style="justify-content: space-between; margin-bottom: 2rem;">
            <div class="card-title">Active Alerts</div>
            <div style="width: 20px; height: 20px; color: var(--text-secondary);">${icons.chevronRight}</div>
          </div>
          
          <div style="display: flex; justify-content: space-between; margin-bottom: 2.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid var(--border-color);">
            <div style="text-align: center;">
              <div style="font-size: 2.5rem; font-weight: 700; color: var(--status-critical); line-height: 1;">2</div>
              <div class="micro-label" style="color: var(--status-critical); margin-top: 0.25rem;">Critical</div>
            </div>
            <div style="text-align: center;">
              <div style="font-size: 2.5rem; font-weight: 700; color: var(--text-primary); line-height: 1;">3</div>
              <div class="micro-label" style="margin-top: 0.25rem;">High</div>
            </div>
            <div style="text-align: center;">
              <div style="font-size: 2.5rem; font-weight: 700; color: var(--text-primary); line-height: 1;">5</div>
              <div class="micro-label" style="margin-top: 0.25rem;">Medium</div>
            </div>
          </div>

          <div style="display: flex; flex-direction: column; gap: 1rem; flex: 1;">
            
            <div style="border: 1px solid var(--status-critical-bg); background-color: rgba(254,226,226,0.2); border-radius: var(--radius-md); padding: 1rem; display: flex; align-items: flex-start; gap: 1rem;">
              <div style="width: 16px; height: 16px; margin-top: 2px;">
                <svg viewBox="0 0 24 24" fill="none" stroke="var(--status-critical)" stroke-width="3"><circle cx="12" cy="12" r="10"/></svg>
              </div>
              <div style="flex: 1;">
                <div style="font-weight: 600; font-size: 0.95rem; margin-bottom: 0.25rem;">Inverter Timeout</div>
                <div style="font-size: 0.85rem; color: var(--text-secondary);">Site Alpha • Node 23</div>
              </div>
              <div style="font-size: 0.8rem; color: var(--status-critical); font-weight: 500;">2m ago</div>
            </div>

            <div style="border: 1px solid var(--status-critical-bg); background-color: rgba(254,226,226,0.2); border-radius: var(--radius-md); padding: 1rem; display: flex; align-items: flex-start; gap: 1rem;">
              <div style="width: 16px; height: 16px; margin-top: 2px;">
                <svg viewBox="0 0 24 24" fill="none" stroke="var(--status-critical)" stroke-width="3"><circle cx="12" cy="12" r="10"/></svg>
              </div>
              <div style="flex: 1;">
                <div style="font-weight: 600; font-size: 0.95rem; margin-bottom: 0.25rem;">Temperature Threshold</div>
                <div style="font-size: 0.85rem; color: var(--text-secondary);">Site Delta • Node 11</div>
              </div>
              <div style="font-size: 0.8rem; color: var(--status-critical); font-weight: 500;">5m ago</div>
            </div>
            
          </div>
          
          <a href="#/monitoring" style="display: inline-flex; align-items: center; gap: 0.5rem; margin-top: 1.5rem; text-decoration: none; font-weight: 600; font-size: 0.95rem; color: var(--color-secondary);">
            View all alerts
            <span style="width: 16px;">${icons.chevronRight}</span>
          </a>
        </div>
      </div>

      <!-- Bottom Row -->
      <div class="grid-3">
        
        <!-- AI System Status -->
        <div class="card">
          <div class="card-header">
            <div class="card-title">AI System Status</div>
            <span style="display: inline-block; width: 14px; height: 14px; border: 1px solid var(--text-secondary); border-radius: 50%; text-align: center; line-height: 12px; color: var(--text-secondary); font-size: 10px;">i</span>
          </div>
          
          <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 2rem;">
            <div class="icon-badge" style="width: 56px; height: 56px; background-color: var(--status-healthy-bg); color: var(--status-healthy);">
              <div style="width: 24px; height: 24px;">${icons.shield}</div>
            </div>
            <div>
              <div style="font-weight: 600; color: var(--color-primary); font-size: 1.1rem;">Operational</div>
              <div style="color: var(--text-secondary); font-size: 0.9rem;">All AI services running normally</div>
            </div>
          </div>
          
          <div style="display: flex; flex-direction: column; gap: 1rem;">
            ${['Anomaly Detection', 'Predictive Models', 'Self-Healing Engine', 'Data Ingestion'].map(svc => `
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 0.5rem; font-size: 0.9rem; color: var(--text-secondary);">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--status-healthy)" stroke-width="2"><path d="M20 6 9 17l-5-5"/></svg>
                  ${svc}
                </div>
                <div style="font-weight: 600; font-size: 0.85rem; color: var(--status-healthy);">Active</div>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- Performance Chart -->
        <div class="card" style="display: flex; flex-direction: column;">
          <div class="card-header" style="justify-content: space-between; margin-bottom: 1rem;">
            <div class="card-title">Performance <span style="color: var(--text-secondary); font-weight: normal;">(Today)</span></div>
            <div style="width: 20px; height: 20px; color: var(--text-secondary);">${icons.chevronRight}</div>
          </div>
          
          <div style="flex: 1; position: relative;">
            <svg viewBox="0 0 300 150" width="100%" height="150" preserveAspectRatio="none">
              <!-- Grid lines -->
              <line x1="0" y1="0" x2="300" y2="0" stroke="var(--border-color)" stroke-width="1" />
              <line x1="0" y1="37.5" x2="300" y2="37.5" stroke="var(--border-color)" stroke-width="1" />
              <line x1="0" y1="75" x2="300" y2="75" stroke="var(--border-color)" stroke-width="1" />
              <line x1="0" y1="112.5" x2="300" y2="112.5" stroke="var(--border-color)" stroke-width="1" />
              <line x1="0" y1="150" x2="300" y2="150" stroke="var(--border-color)" stroke-width="1" />
              
              <!-- Area fill -->
              <path d="M0,150 L0,30 Q20,25 40,35 T80,15 T120,20 T160,10 T200,30 T220,70 T240,40 T280,20 L300,15 L300,150 Z" fill="url(#perf-gradient)" />
              
              <!-- Line -->
              <path d="M0,30 Q20,25 40,35 T80,15 T120,20 T160,10 T200,30 T220,70 T240,40 T280,20 L300,15" fill="none" stroke="var(--color-secondary)" stroke-width="2" />
              
              <defs>
                <linearGradient id="perf-gradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stop-color="var(--color-secondary)" stop-opacity="0.2" />
                  <stop offset="100%" stop-color="var(--color-secondary)" stop-opacity="0" />
                </linearGradient>
              </defs>
              
              <!-- Data point -->
              <circle cx="300" cy="15" r="4" fill="white" stroke="var(--color-secondary)" stroke-width="2" />
            </svg>
            
            <div style="display: flex; justify-content: space-between; margin-top: 0.5rem; font-size: 0.75rem; color: var(--text-secondary);">
              <div>12 AM</div>
              <div>6 AM</div>
              <div>12 PM</div>
              <div>6 PM</div>
            </div>
            
            <div style="position: absolute; left: -25px; top: -5px; height: 160px; display: flex; flex-direction: column; justify-content: space-between; font-size: 0.75rem; color: var(--text-secondary);">
              <div>100</div>
              <div>75</div>
              <div>50</div>
              <div>25</div>
              <div>0</div>
            </div>
          </div>
          
          <div style="display: flex; justify-content: space-between; margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid var(--border-color);">
            <div>
              <div class="micro-label" style="text-transform: none;">Avg. Uptime</div>
              <div style="font-weight: 600; color: var(--color-primary); font-size: 1.1rem;">99.6%</div>
            </div>
            <div>
              <div class="micro-label" style="text-transform: none;">Data Quality</div>
              <div style="font-weight: 600; color: var(--color-primary); font-size: 1.1rem;">99.2%</div>
            </div>
            <div>
              <div class="micro-label" style="text-transform: none;">Response Time</div>
              <div style="font-weight: 600; color: var(--color-primary); font-size: 1.1rem;">120ms</div>
            </div>
          </div>
        </div>

        <!-- Last Update Card -->
        <div class="card" style="display: flex; flex-direction: column; position: relative; overflow: hidden;">
          <div class="bg-topo" style="opacity: 0.4;"></div>
          
          <div class="card-header">
            <div class="card-title">Last Update</div>
          </div>
          
          <div style="flex: 1; display: flex; flex-direction: column; justify-content: center; position: relative; z-index: 10;">
            <div style="font-size: 2.5rem; font-weight: 700; color: var(--color-primary); letter-spacing: -0.02em; line-height: 1; margin-bottom: 0.5rem;">
              10:24:38 AM
            </div>
            <div style="color: var(--text-secondary); font-size: 1.1rem;">
              May 26, 2025
            </div>
          </div>
          
          <div style="margin-top: auto; display: flex; align-items: center; gap: 0.75rem; font-size: 0.9rem; color: var(--text-secondary); position: relative; z-index: 10;">
            <div style="width: 16px; height: 16px; color: var(--text-secondary);">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="animation: spin 2s linear infinite;"><path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/><path d="M16 21v-5h5"/></svg>
            </div>
            Next update in 12s
          </div>
          
          <style>
            @keyframes spin { 100% { transform: rotate(360deg); } }
          </style>
        </div>
      </div>
    </div>
  `;
}
