import { icons } from './icons.js';

export function renderSidebar(currentRoute) {
  const navItems = [
    { id: 'dashboard', label: 'Overview', icon: 'overview', href: '#/dashboard' },
    { id: 'monitoring', label: 'Live Monitoring', icon: 'monitoring', href: '#/monitoring' },
    { id: 'weather', label: 'Weather', icon: 'weather', href: '#/weather' },
    { id: 'diagnostics', label: 'Diagnostics', icon: 'diagnostics', href: '#/dashboard' },
    { id: 'analytics', label: 'Analytics', icon: 'analytics', href: '#/dashboard' },
    { id: 'maintenance', label: 'Maintenance', icon: 'maintenance', href: '#/maintenance' },
    { id: 'settings', label: 'Settings', icon: 'settings', href: '#/settings' }
  ];

  return `
    <aside class="sidebar">
      <a href="#/" class="sidebar-logo">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none">
          <path d="M32 4L56 18V46L32 60L8 46V18L32 4Z" stroke="#153226" stroke-width="3" fill="none"/>
          <path d="M32 4L56 18V46L32 60L8 46V18L32 4Z" stroke="#153226" stroke-width="2" fill="none" transform="scale(0.7) translate(13.7 13.7)"/>
          <circle cx="32" cy="32" r="6" fill="#2D6A4F"/>
          <path d="M32 22C32 22 26 27 26 32C26 37 32 42 32 42" stroke="#2D6A4F" stroke-width="2" fill="none"/>
          <path d="M32 22C32 22 38 27 38 32C38 37 32 42 32 42" stroke="#2D6A4F" stroke-width="2" fill="none"/>
        </svg>
        SKYGUARD AI
      </a>
      
      <nav class="sidebar-nav">
        ${navItems.map(item => `
          <a href="${item.href}" class="nav-item ${currentRoute === item.id ? 'active' : ''}">
            <div class="nav-icon">${icons[item.icon]}</div>
            ${item.label}
          </a>
        `).join('')}
      </nav>

      <div class="sidebar-footer">
        <div class="user-card">
          <div class="avatar">AD</div>
          <div class="user-info">
            <span class="user-name">Admin User</span>
            <span class="user-role">Administrator</span>
          </div>
          <div class="nav-icon" style="margin-left: auto;">${icons.chevronDown}</div>
        </div>
      </div>
    </aside>
  `;
}
