import { icons } from '../components/icons.js';

export function renderSettings() {
  return `
    <div style="padding-bottom: 2rem; max-width: 800px; margin: 0 auto;">
      <header class="page-header" style="margin-bottom: 2rem;">
        <div>
          <h1 class="page-title">Settings</h1>
          <p class="subtitle">Manage your account and system preferences</p>
        </div>
        <div class="page-header-right">
          <button class="btn btn-outline" style="width: 40px; height: 40px; padding: 0; border-color: transparent;">
            <div style="width: 20px; height: 20px;">${icons.bell}</div>
          </button>
        </div>
      </header>

      <!-- Profile Settings -->
      <div class="card" style="margin-bottom: 1.5rem;">
        <div class="card-header" style="margin-bottom: 2rem; border-bottom: 1px solid var(--border-color); padding-bottom: 1rem;">
          <div style="width: 20px; height: 20px; color: var(--color-primary);">${icons.user}</div>
          <div class="card-title">Profile Information</div>
        </div>

        <div style="display: flex; gap: 2rem; align-items: flex-start; margin-bottom: 2rem;">
          <div style="display: flex; flex-direction: column; align-items: center; gap: 1rem;">
            <div style="width: 80px; height: 80px; border-radius: 50%; background-color: var(--color-accent-bg); color: var(--color-primary); display: flex; align-items: center; justify-content: center; font-size: 2rem; font-weight: 700;">
              AD
            </div>
            <button class="btn btn-outline" style="font-size: 0.8rem; padding: 0.4rem 0.75rem;">Change Photo</button>
          </div>
          
          <div style="flex: 1; display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
            <div class="input-group">
              <label class="input-label">Full Name</label>
              <input type="text" class="input-field" value="Admin User" />
            </div>
            <div class="input-group">
              <label class="input-label">Email Address</label>
              <input type="email" class="input-field" value="admin@company.com" />
            </div>
            <div class="input-group">
              <label class="input-label">Role</label>
              <input type="text" class="input-field" value="Administrator" readonly style="color: var(--text-secondary);" />
            </div>
            <div class="input-group">
              <label class="input-label">Language</label>
              <div style="position: relative;">
                <select class="input-field" style="appearance: none; cursor: pointer; padding-right: 2rem;">
                  <option>English (US)</option>
                  <option>Hindi</option>
                  <option>Spanish</option>
                </select>
                <div style="position: absolute; right: 0; top: 50%; transform: translateY(-50%); width: 16px; height: 16px; color: var(--text-secondary); pointer-events: none;">
                  ${icons.chevronDown}
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div style="display: flex; justify-content: flex-end;">
          <button class="btn btn-primary">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 0.5rem;"><path d="M20 6 9 17l-5-5"/></svg>
            Save Changes
          </button>
        </div>
      </div>

      <!-- System Preferences -->
      <div class="card" style="margin-bottom: 1.5rem;">
        <div class="card-header" style="margin-bottom: 2rem; border-bottom: 1px solid var(--border-color); padding-bottom: 1rem;">
          <div style="width: 20px; height: 20px; color: var(--color-primary);">${icons.settings}</div>
          <div class="card-title">System Preferences</div>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 2rem;">
          <div class="input-group">
            <label class="input-label">Time Zone</label>
            <div style="position: relative;">
              <select class="input-field" style="appearance: none; cursor: pointer; padding-right: 2rem;">
                <option>Asia/Kolkata (IST)</option>
                <option>UTC</option>
              </select>
              <div style="position: absolute; right: 0; top: 50%; transform: translateY(-50%); width: 16px; height: 16px; color: var(--text-secondary); pointer-events: none;">
                ${icons.chevronDown}
              </div>
            </div>
          </div>
          
          <div class="input-group">
            <label class="input-label">Units</label>
            <div style="position: relative;">
              <select class="input-field" style="appearance: none; cursor: pointer; padding-right: 2rem;">
                <option>Metric (°C, km/h)</option>
                <option>Imperial (°F, mph)</option>
              </select>
              <div style="position: absolute; right: 0; top: 50%; transform: translateY(-50%); width: 16px; height: 16px; color: var(--text-secondary); pointer-events: none;">
                ${icons.chevronDown}
              </div>
            </div>
          </div>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; padding: 1rem; border: 1px solid var(--border-color); border-radius: var(--radius-md); background-color: var(--bg-card-alt);">
          <div>
            <div style="font-weight: 600; font-size: 0.95rem; margin-bottom: 0.25rem;">Auto refresh data</div>
            <div style="font-size: 0.85rem; color: var(--text-secondary);">Automatically update dashboards every 60 seconds</div>
          </div>
          <div class="toggle on" onclick="this.classList.toggle('on')">
            <div class="toggle-knob"></div>
          </div>
        </div>
      </div>

      <!-- Notifications -->
      <div class="card">
        <div class="card-header" style="margin-bottom: 2rem; border-bottom: 1px solid var(--border-color); padding-bottom: 1rem;">
          <div style="width: 20px; height: 20px; color: var(--color-primary);">${icons.bell}</div>
          <div class="card-title">Notifications</div>
        </div>

        <div style="display: flex; flex-direction: column; gap: 1rem;">
          <div style="display: flex; justify-content: space-between; align-items: center; padding: 1rem; border: 1px solid var(--border-color); border-radius: var(--radius-md); background-color: var(--bg-card-alt);">
            <div>
              <div style="font-weight: 600; font-size: 0.95rem; margin-bottom: 0.25rem;">Email alerts for critical events</div>
              <div style="font-size: 0.85rem; color: var(--text-secondary);">Receive immediate emails when a node goes offline</div>
            </div>
            <div class="toggle on" onclick="this.classList.toggle('on')">
              <div class="toggle-knob"></div>
            </div>
          </div>

          <div style="display: flex; justify-content: space-between; align-items: center; padding: 1rem; border: 1px solid var(--border-color); border-radius: var(--radius-md); background-color: var(--bg-card-alt);">
            <div>
              <div style="font-weight: 600; font-size: 0.95rem; margin-bottom: 0.25rem;">Maintenance reminders</div>
              <div style="font-size: 0.85rem; color: var(--text-secondary);">Weekly digest of upcoming predicted failures</div>
            </div>
            <div class="toggle" onclick="this.classList.toggle('on')">
              <div class="toggle-knob"></div>
            </div>
          </div>
        </div>
      </div>

    </div>
  `;
}
