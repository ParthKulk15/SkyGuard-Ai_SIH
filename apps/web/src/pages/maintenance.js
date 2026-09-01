import { icons } from '../components/icons.js';

export function renderMaintenance() {
  return `
    <div style="padding-bottom: 2rem;">
      <header class="page-header" style="margin-bottom: 1.5rem;">
        <div>
          <h1 class="page-title">Predictive Maintenance</h1>
          <p class="subtitle">AI-driven asset health and failure prediction</p>
        </div>
        <div class="page-header-right">
          <div style="position: relative; width: 160px; margin-right: 0.5rem;">
            <select style="width: 100%; padding: 0.6rem 1rem; border-radius: var(--radius-full); border: 1px solid var(--border-color); background-color: var(--bg-card); font-family: var(--font-sans); outline: none; appearance: none; cursor: pointer; font-size: 0.85rem; font-weight: 500;">
              <option>All Stations</option>
              <option>Delta Station 07</option>
            </select>
            <div style="position: absolute; right: 1rem; top: 50%; transform: translateY(-50%); color: var(--text-secondary); pointer-events: none; width: 14px; height: 14px;">
              ${icons.chevronDown}
            </div>
          </div>
          
          <button class="btn btn-outline" style="background-color: var(--bg-card); display: flex; align-items: center; gap: 0.5rem; padding: 0.6rem 1rem;">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <span style="font-size: 0.85rem;">Last 30 Days</span>
          </button>
        </div>
      </header>

      <!-- Stat Icons Row -->
      <div class="card" style="display: flex; justify-content: space-between; padding: 1.25rem 2rem; margin-bottom: 2rem;">
        <div style="display: flex; align-items: center; gap: 1rem;">
          <div style="width: 40px; height: 40px; border-radius: 50%; background-color: var(--color-accent-bg); color: var(--color-secondary); display: flex; align-items: center; justify-content: center;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
          </div>
          <div>
            <div class="micro-label" style="margin-bottom: 0;">Assets Monitored</div>
            <div style="font-size: 1.5rem; font-weight: 700;">128</div>
          </div>
        </div>
        
        <div style="width: 1px; background-color: var(--border-color);"></div>
        
        <div style="display: flex; align-items: center; gap: 1rem;">
          <div style="position: relative; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center;">
            <svg viewBox="0 0 36 36" style="position: absolute; width: 100%; height: 100%; transform: rotate(-90deg);">
              <path d="M18 2 a 16 16 0 0 1 0 32 a 16 16 0 0 1 0 -32" fill="none" stroke="rgba(220, 38, 38, 0.2)" stroke-width="4" />
              <path d="M18 2 a 16 16 0 0 1 0 32 a 16 16 0 0 1 0 -32" fill="none" stroke="var(--status-critical)" stroke-width="4" stroke-dasharray="8, 100" />
            </svg>
            <span style="font-weight: 700; color: var(--status-critical);">2</span>
          </div>
          <div>
            <div class="micro-label" style="margin-bottom: 0;">High Priority</div>
          </div>
        </div>

        <div style="width: 1px; background-color: var(--border-color);"></div>

        <div style="display: flex; align-items: center; gap: 1rem;">
          <div style="position: relative; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center;">
            <svg viewBox="0 0 36 36" style="position: absolute; width: 100%; height: 100%; transform: rotate(-90deg);">
              <path d="M18 2 a 16 16 0 0 1 0 32 a 16 16 0 0 1 0 -32" fill="none" stroke="rgba(245, 158, 11, 0.2)" stroke-width="4" />
              <path d="M18 2 a 16 16 0 0 1 0 32 a 16 16 0 0 1 0 -32" fill="none" stroke="var(--status-warning)" stroke-width="4" stroke-dasharray="25, 100" />
            </svg>
            <span style="font-weight: 700; color: var(--status-warning);">5</span>
          </div>
          <div>
            <div class="micro-label" style="margin-bottom: 0;">Medium Priority</div>
          </div>
        </div>

        <div style="width: 1px; background-color: var(--border-color);"></div>

        <div style="display: flex; align-items: center; gap: 1rem;">
          <div style="position: relative; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center;">
            <svg viewBox="0 0 36 36" style="position: absolute; width: 100%; height: 100%; transform: rotate(-90deg);">
              <path d="M18 2 a 16 16 0 0 1 0 32 a 16 16 0 0 1 0 -32" fill="none" stroke="rgba(34, 165, 94, 0.2)" stroke-width="4" />
              <path d="M18 2 a 16 16 0 0 1 0 32 a 16 16 0 0 1 0 -32" fill="none" stroke="var(--status-healthy)" stroke-width="4" stroke-dasharray="75, 100" />
            </svg>
            <span style="font-weight: 700; color: var(--status-healthy);">21</span>
          </div>
          <div>
            <div class="micro-label" style="margin-bottom: 0;">Low Priority</div>
          </div>
        </div>

        <div style="width: 1px; background-color: var(--border-color);"></div>

        <div style="display: flex; align-items: center; gap: 1rem;">
          <div style="width: 40px; height: 40px; border-radius: 50%; background-color: var(--status-healthy-bg); color: var(--status-healthy); display: flex; align-items: center; justify-content: center;">
            <div style="width: 20px; height: 20px;">${icons.shield}</div>
          </div>
          <div>
            <div class="micro-label" style="margin-bottom: 0;">Healthy</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: var(--status-healthy);">100</div>
          </div>
        </div>
      </div>

      <!-- Expandable Priority Alert Cards -->
      <div style="display: flex; flex-direction: column; gap: 1.5rem; margin-bottom: 2rem;">
        
        <!-- High Priority Alert -->
        <div class="card" style="border-left: 4px solid var(--status-critical); position: relative; overflow: hidden; padding: 0;">
          <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(90deg, rgba(254, 226, 226, 0.3) 0%, transparent 40%); pointer-events: none;"></div>
          
          <div style="padding: 1.5rem; display: flex; align-items: stretch; gap: 2rem; position: relative;">
            
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.5rem; width: 80px; border-right: 1px solid var(--border-color); padding-right: 2rem;">
              <div class="badge badge-critical" style="margin-bottom: 0.5rem;">HIGH PRIORITY</div>
              <div style="width: 48px; height: 48px; border-radius: 50%; background-color: var(--status-critical-bg); color: var(--status-critical); display: flex; align-items: center; justify-content: center;">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
              </div>
            </div>

            <div style="flex: 1; display: flex; flex-direction: column; justify-content: center;">
              <h3 style="font-size: 1.1rem; font-weight: 700; margin-bottom: 0.25rem;">Inverter Overheating Risk</h3>
              <div style="display: flex; align-items: center; gap: 0.5rem; color: var(--text-secondary); font-size: 0.9rem;">
                <span style="font-weight: 600; color: var(--text-primary);">Asset ID: INV-07-A</span>
                <span>•</span>
                Delta Station 07
                <span>•</span>
                Rajasthan
              </div>
            </div>

            <!-- Risk Gauge -->
            <div style="display: flex; align-items: center; gap: 1rem; border-left: 1px solid var(--border-color); padding-left: 2rem;">
              <div style="position: relative; width: 64px; height: 64px; display: flex; align-items: center; justify-content: center;">
                <svg viewBox="0 0 36 36" style="position: absolute; width: 100%; height: 100%; transform: rotate(-90deg);">
                  <path d="M18 2 a 16 16 0 0 1 0 32 a 16 16 0 0 1 0 -32" fill="none" stroke="rgba(220, 38, 38, 0.2)" stroke-width="4" />
                  <path d="M18 2 a 16 16 0 0 1 0 32 a 16 16 0 0 1 0 -32" fill="none" stroke="var(--status-critical)" stroke-width="4" stroke-dasharray="92, 100" />
                </svg>
                <span style="font-weight: 800; font-size: 1.25rem; color: var(--status-critical);">92</span>
              </div>
              <div>
                <div class="micro-label" style="color: var(--status-critical); margin-bottom: 0;">Risk Score</div>
                <div style="font-size: 0.85rem; font-weight: 500;">Severe Risk</div>
              </div>
            </div>

            <!-- Prediction -->
            <div style="display: flex; flex-direction: column; justify-content: center; border-left: 1px solid var(--border-color); padding-left: 2rem;">
              <div class="micro-label" style="margin-bottom: 0.25rem;">Predicted Failure</div>
              <div style="font-size: 1.1rem; font-weight: 700; color: var(--status-critical);">2 Days</div>
              <div style="font-size: 0.75rem; color: var(--text-secondary);">95% Confidence</div>
            </div>
            
            <!-- Trend -->
            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; border-left: 1px solid var(--border-color); padding-left: 2rem;">
              <div class="micro-label" style="margin-bottom: 0.5rem; text-align: left; width: 100%;">7-Day Trend</div>
              <svg width="80" height="30" viewBox="0 0 80 30" preserveAspectRatio="none">
                <path d="M0,25 L10,24 L20,22 L30,23 L40,18 L50,15 L60,10 L70,8 L80,2" fill="none" stroke="var(--status-critical)" stroke-width="2" />
              </svg>
            </div>

            <!-- Action -->
            <div style="display: flex; align-items: center; padding-left: 2rem;">
              <button class="btn btn-outline" style="border-color: var(--status-critical); color: var(--status-critical); white-space: nowrap;">
                Schedule Inspection
              </button>
            </div>

          </div>
        </div>

        <!-- Medium Priority Alert -->
        <div class="card" style="border-left: 4px solid var(--status-warning); position: relative; overflow: hidden; padding: 0;">
          <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(90deg, rgba(245, 158, 11, 0.15) 0%, transparent 40%); pointer-events: none;"></div>
          
          <div style="padding: 1.5rem; display: flex; align-items: stretch; gap: 2rem; position: relative;">
            
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.5rem; width: 80px; border-right: 1px solid var(--border-color); padding-right: 2rem;">
              <div class="badge badge-warning" style="margin-bottom: 0.5rem;">WARNING</div>
              <div style="width: 48px; height: 48px; border-radius: 50%; background-color: var(--status-warning-bg); color: var(--status-warning); display: flex; align-items: center; justify-content: center;">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
              </div>
            </div>

            <div style="flex: 1; display: flex; flex-direction: column; justify-content: center;">
              <h3 style="font-size: 1.1rem; font-weight: 700; margin-bottom: 0.25rem;">Cooling Fan Degradation</h3>
              <div style="display: flex; align-items: center; gap: 0.5rem; color: var(--text-secondary); font-size: 0.9rem;">
                <span style="font-weight: 600; color: var(--text-primary);">Asset ID: FAN-14-C</span>
                <span>•</span>
                Theta Station 14
                <span>•</span>
                Madhya Pradesh
              </div>
            </div>

            <!-- Risk Gauge -->
            <div style="display: flex; align-items: center; gap: 1rem; border-left: 1px solid var(--border-color); padding-left: 2rem;">
              <div style="position: relative; width: 64px; height: 64px; display: flex; align-items: center; justify-content: center;">
                <svg viewBox="0 0 36 36" style="position: absolute; width: 100%; height: 100%; transform: rotate(-90deg);">
                  <path d="M18 2 a 16 16 0 0 1 0 32 a 16 16 0 0 1 0 -32" fill="none" stroke="rgba(245, 158, 11, 0.2)" stroke-width="4" />
                  <path d="M18 2 a 16 16 0 0 1 0 32 a 16 16 0 0 1 0 -32" fill="none" stroke="var(--status-warning)" stroke-width="4" stroke-dasharray="68, 100" />
                </svg>
                <span style="font-weight: 800; font-size: 1.25rem; color: var(--status-warning);">68</span>
              </div>
              <div>
                <div class="micro-label" style="color: var(--status-warning); margin-bottom: 0;">Risk Score</div>
                <div style="font-size: 0.85rem; font-weight: 500;">Elevated Risk</div>
              </div>
            </div>

            <!-- Prediction -->
            <div style="display: flex; flex-direction: column; justify-content: center; border-left: 1px solid var(--border-color); padding-left: 2rem;">
              <div class="micro-label" style="margin-bottom: 0.25rem;">Predicted Failure</div>
              <div style="font-size: 1.1rem; font-weight: 700; color: var(--status-warning);">12 Days</div>
              <div style="font-size: 0.75rem; color: var(--text-secondary);">82% Confidence</div>
            </div>
            
            <!-- Trend -->
            <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; border-left: 1px solid var(--border-color); padding-left: 2rem;">
              <div class="micro-label" style="margin-bottom: 0.5rem; text-align: left; width: 100%;">7-Day Trend</div>
              <svg width="80" height="30" viewBox="0 0 80 30" preserveAspectRatio="none">
                <path d="M0,25 L10,25 L20,24 L30,22 L40,20 L50,18 L60,16 L70,13 L80,10" fill="none" stroke="var(--status-warning)" stroke-width="2" />
              </svg>
            </div>

            <!-- Action -->
            <div style="display: flex; align-items: center; padding-left: 2rem;">
              <button class="btn btn-outline" style="white-space: nowrap;">
                View Details
              </button>
            </div>

          </div>
        </div>
      </div>

      <!-- Full Data Table -->
      <div class="card" style="padding: 0; overflow: hidden;">
        <table style="width: 100%; border-collapse: collapse; text-align: left;">
          <thead>
            <tr style="background-color: var(--bg-card-alt); border-bottom: 1px solid var(--border-color);">
              <th style="padding: 1rem 1.5rem; font-size: 0.75rem; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em;">Priority</th>
              <th style="padding: 1rem 1.5rem; font-size: 0.75rem; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em;">Asset</th>
              <th style="padding: 1rem 1.5rem; font-size: 0.75rem; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em;">Station</th>
              <th style="padding: 1rem 1.5rem; font-size: 0.75rem; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em;">Component</th>
              <th style="padding: 1rem 1.5rem; font-size: 0.75rem; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em;">Risk Score</th>
              <th style="padding: 1rem 1.5rem; font-size: 0.75rem; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em;">Predicted Failure</th>
              <th style="padding: 1rem 1.5rem; font-size: 0.75rem; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em;">Trend</th>
              <th style="padding: 1rem 1.5rem; font-size: 0.75rem; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em;">Status</th>
              <th style="padding: 1rem 1.5rem;"></th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom: 1px solid var(--border-color);">
              <td style="padding: 1rem 1.5rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                  <div class="status-dot dot-critical"></div>
                  <span style="font-weight: 600; font-size: 0.9rem;">High</span>
                </div>
              </td>
              <td style="padding: 1rem 1.5rem; font-weight: 600; font-size: 0.9rem;">INV-07-A</td>
              <td style="padding: 1rem 1.5rem; color: var(--text-secondary); font-size: 0.9rem;">Delta Station 07</td>
              <td style="padding: 1rem 1.5rem; font-size: 0.9rem;">Inverter Board</td>
              <td style="padding: 1rem 1.5rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                  <div style="width: 24px; height: 24px; position: relative;">
                    <svg viewBox="0 0 36 36" style="width: 100%; height: 100%; transform: rotate(-90deg);">
                      <path d="M18 2 a 16 16 0 0 1 0 32 a 16 16 0 0 1 0 -32" fill="none" stroke="rgba(220,38,38,0.2)" stroke-width="4" />
                      <path d="M18 2 a 16 16 0 0 1 0 32 a 16 16 0 0 1 0 -32" fill="none" stroke="var(--status-critical)" stroke-width="4" stroke-dasharray="92, 100" />
                    </svg>
                  </div>
                  <span style="font-weight: 600; color: var(--status-critical);">92</span>
                </div>
              </td>
              <td style="padding: 1rem 1.5rem; font-weight: 600; color: var(--status-critical); font-size: 0.9rem;">2 Days</td>
              <td style="padding: 1rem 1.5rem;">
                <svg width="40" height="20" viewBox="0 0 40 20" preserveAspectRatio="none">
                  <path d="M0,15 L10,13 L20,10 L30,5 L40,2" fill="none" stroke="var(--status-critical)" stroke-width="2" />
                </svg>
              </td>
              <td style="padding: 1rem 1.5rem;">
                <div class="badge badge-live" style="background-color: var(--status-healthy-bg); color: var(--status-healthy); display: flex; align-items: center; gap: 0.25rem;">
                   <div class="status-dot dot-healthy" style="width: 6px; height: 6px;"></div> Active
                </div>
              </td>
              <td style="padding: 1rem 1.5rem; text-align: right;">
                <a href="#" style="color: var(--color-secondary); text-decoration: none; font-weight: 600; font-size: 0.85rem; display: inline-flex; align-items: center; gap: 0.25rem;">
                  Review <div style="width: 14px; height: 14px;">${icons.chevronRight}</div>
                </a>
              </td>
            </tr>

            <tr style="border-bottom: 1px solid var(--border-color);">
              <td style="padding: 1rem 1.5rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                  <div class="status-dot dot-warning"></div>
                  <span style="font-weight: 600; font-size: 0.9rem;">Medium</span>
                </div>
              </td>
              <td style="padding: 1rem 1.5rem; font-weight: 600; font-size: 0.9rem;">FAN-14-C</td>
              <td style="padding: 1rem 1.5rem; color: var(--text-secondary); font-size: 0.9rem;">Theta Station 14</td>
              <td style="padding: 1rem 1.5rem; font-size: 0.9rem;">Cooling System</td>
              <td style="padding: 1rem 1.5rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                  <div style="width: 24px; height: 24px; position: relative;">
                    <svg viewBox="0 0 36 36" style="width: 100%; height: 100%; transform: rotate(-90deg);">
                      <path d="M18 2 a 16 16 0 0 1 0 32 a 16 16 0 0 1 0 -32" fill="none" stroke="rgba(245,158,11,0.2)" stroke-width="4" />
                      <path d="M18 2 a 16 16 0 0 1 0 32 a 16 16 0 0 1 0 -32" fill="none" stroke="var(--status-warning)" stroke-width="4" stroke-dasharray="68, 100" />
                    </svg>
                  </div>
                  <span style="font-weight: 600; color: var(--status-warning);">68</span>
                </div>
              </td>
              <td style="padding: 1rem 1.5rem; font-weight: 600; color: var(--status-warning); font-size: 0.9rem;">12 Days</td>
              <td style="padding: 1rem 1.5rem;">
                <svg width="40" height="20" viewBox="0 0 40 20" preserveAspectRatio="none">
                  <path d="M0,18 L10,16 L20,15 L30,12 L40,8" fill="none" stroke="var(--status-warning)" stroke-width="2" />
                </svg>
              </td>
              <td style="padding: 1rem 1.5rem;">
                <div class="badge badge-live" style="background-color: var(--status-healthy-bg); color: var(--status-healthy); display: flex; align-items: center; gap: 0.25rem;">
                   <div class="status-dot dot-healthy" style="width: 6px; height: 6px;"></div> Active
                </div>
              </td>
              <td style="padding: 1rem 1.5rem; text-align: right;">
                <a href="#" style="color: var(--color-secondary); text-decoration: none; font-weight: 600; font-size: 0.85rem; display: inline-flex; align-items: center; gap: 0.25rem;">
                  Review <div style="width: 14px; height: 14px;">${icons.chevronRight}</div>
                </a>
              </td>
            </tr>

            <tr style="border-bottom: 1px solid var(--border-color);">
              <td style="padding: 1rem 1.5rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                  <div class="status-dot dot-healthy"></div>
                  <span style="font-weight: 600; font-size: 0.9rem;">Low</span>
                </div>
              </td>
              <td style="padding: 1rem 1.5rem; font-weight: 600; font-size: 0.9rem;">PNL-03-X</td>
              <td style="padding: 1rem 1.5rem; color: var(--text-secondary); font-size: 0.9rem;">Beta Station 03</td>
              <td style="padding: 1rem 1.5rem; font-size: 0.9rem;">Solar Array</td>
              <td style="padding: 1rem 1.5rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                  <div style="width: 24px; height: 24px; position: relative;">
                    <svg viewBox="0 0 36 36" style="width: 100%; height: 100%; transform: rotate(-90deg);">
                      <path d="M18 2 a 16 16 0 0 1 0 32 a 16 16 0 0 1 0 -32" fill="none" stroke="rgba(34,165,94,0.2)" stroke-width="4" />
                      <path d="M18 2 a 16 16 0 0 1 0 32 a 16 16 0 0 1 0 -32" fill="none" stroke="var(--status-healthy)" stroke-width="4" stroke-dasharray="24, 100" />
                    </svg>
                  </div>
                  <span style="font-weight: 600; color: var(--status-healthy);">24</span>
                </div>
              </td>
              <td style="padding: 1rem 1.5rem; font-weight: 500; color: var(--text-secondary); font-size: 0.9rem;">45+ Days</td>
              <td style="padding: 1rem 1.5rem;">
                <svg width="40" height="20" viewBox="0 0 40 20" preserveAspectRatio="none">
                  <path d="M0,15 L10,15 L20,14 L30,14 L40,12" fill="none" stroke="var(--status-healthy)" stroke-width="2" />
                </svg>
              </td>
              <td style="padding: 1rem 1.5rem;">
                <div class="badge badge-live" style="background-color: var(--status-healthy-bg); color: var(--status-healthy); display: flex; align-items: center; gap: 0.25rem;">
                   <div class="status-dot dot-healthy" style="width: 6px; height: 6px;"></div> Active
                </div>
              </td>
              <td style="padding: 1rem 1.5rem; text-align: right;">
                <a href="#" style="color: var(--color-secondary); text-decoration: none; font-weight: 600; font-size: 0.85rem; display: inline-flex; align-items: center; gap: 0.25rem;">
                  Review <div style="width: 14px; height: 14px;">${icons.chevronRight}</div>
                </a>
              </td>
            </tr>

          </tbody>
        </table>
        
        <div style="padding: 1rem; text-align: center; border-top: 1px solid var(--border-color); background-color: var(--bg-card-alt);">
          <button style="border: none; background: none; font-size: 0.85rem; font-weight: 600; color: var(--text-secondary); cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 0.5rem; width: 100%;">
            View all maintenance predictions <div style="width: 16px; height: 16px;">${icons.chevronDown}</div>
          </button>
        </div>
      </div>
    </div>
  `;
}
