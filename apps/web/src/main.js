import './style.css';
import { renderSidebar } from './components/sidebar.js';
import { renderFooter } from './components/footer.js';
import { showAnomalyToast } from './components/anomalyToast.js';

// Lazy load pages for better structure
const routes = {
  '/': () => import('./pages/landing.js').then(m => m.renderLanding()),
  '/login': () => import('./pages/login.js').then(m => m.renderLogin()),
  '/dashboard': () => import('./pages/overview.js').then(m => m.renderOverview()),
  '/monitoring': () => import('./pages/monitoring.js').then(m => m.renderMonitoring()),
  '/weather': () => import('./pages/weather.js').then(m => m.renderWeather()),
  '/maintenance': () => import('./pages/maintenance.js').then(m => m.renderMaintenance()),
  '/settings': () => import('./pages/settings.js').then(m => m.renderSettings()),
};

const app = document.getElementById('app');

async function router() {
  const path = window.location.hash.slice(1) || '/';
  
  // Clean up body classes
  document.body.className = '';
  
  try {
    const routeHandler = routes[path];
    if (!routeHandler) {
      window.location.hash = '/';
      return;
    }

    const content = await routeHandler();
    
    // Check if it's an app route (needs sidebar)
    const isAppRoute = ['/dashboard', '/monitoring', '/weather', '/maintenance', '/settings'].includes(path);
    
    if (isAppRoute) {
      // Extract route name for active state (e.g., /dashboard -> dashboard)
      const currentRoute = path.slice(1);
      app.innerHTML = `
        <div class="app-container">
          ${renderSidebar(currentRoute)}
          <main class="main-content">
            ${content}${renderFooter()}
          </main>
        </div>
      `;
    } else {
      // Landing and Login pages
      app.innerHTML = content;
    }
    
    // Re-bind any necessary events
    bindGlobalEvents();
    if (isAppRoute) showAnomalyToast();
    
  } catch (err) {
    console.error('Routing error:', err);
    app.innerHTML = `<div style="padding: 2rem; color: var(--status-critical);">Error loading page. Please try again.</div>`;
  }
}

function bindGlobalEvents() {
  // Simple global event delegation if needed
}

// Initial load
window.addEventListener('hashchange', router);
window.addEventListener('load', router);
