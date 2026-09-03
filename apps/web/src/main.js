import './style.css';
import { renderSidebar } from './components/sidebar.js';
import { renderFooter } from './components/footer.js';
import { showAnomalyToast } from './components/anomalyToast.js';
import { mountAntigravity } from './components/antigravity.js';

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
  const hash = window.location.hash.slice(1) || '/';
  const path = hash.split('?')[0];
  
  // Clean up body classes
  document.body.className = '';
  
  try {
    const routeHandler = routes[path];
    if (!routeHandler) {
      window.location.hash = '/';
      return;
    }

    const content = await routeHandler();

    document.querySelectorAll('[data-antigravity]').forEach((field) => field._antigravityCleanup?.());
    window.clearInterval(window.__skyguardTypewriter);
    
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
  document.querySelectorAll('[data-login-open]').forEach((button) => {
    button.addEventListener('click', () => {
      const modal = document.querySelector('[data-login-modal]');
      if (!modal) return;
      modal.hidden = false;
      document.body.classList.add('modal-open');
      modal.querySelector('input')?.focus();
    });
  });
  document.querySelectorAll('[data-login-close]').forEach((button) => button.addEventListener('click', closeLogin));
  document.querySelector('[data-login-modal]')?.addEventListener('click', (event) => {
    if (event.target === event.currentTarget) closeLogin();
  });
  document.querySelector('.login-form')?.addEventListener('submit', (event) => {
    event.preventDefault();
    closeLogin();
    window.location.hash = '/dashboard';
  });
  document.querySelectorAll('[data-logout]').forEach((button) => {
    button.addEventListener('click', () => {
      window.location.hash = '/';
    });
  });
  document.querySelectorAll('[data-antigravity]').forEach(mountAntigravity);
  const typewriter = document.querySelector('[data-typewriter]');
  if (typewriter) {
    let index = 0;
    window.clearInterval(window.__skyguardTypewriter);
    window.__skyguardTypewriter = window.setInterval(() => {
      typewriter.textContent = typewriter.dataset.typewriter.slice(0, index);
      index += 1;
      if (index > typewriter.dataset.typewriter.length) window.clearInterval(window.__skyguardTypewriter);
    }, 62);
  }
}

function closeLogin() {
  const modal = document.querySelector('[data-login-modal]');
  if (!modal) return;
  modal.hidden = true;
  document.body.classList.remove('modal-open');
}

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') closeLogin();
});

// Initial load
window.addEventListener('hashchange', router);
window.addEventListener('load', router);
