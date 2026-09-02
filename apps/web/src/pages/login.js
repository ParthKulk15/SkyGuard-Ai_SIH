import { icons } from '../components/icons.js';

export function renderLogin(isModal = false) {
  if (isModal) return `
    <div class="login-backdrop" data-login-modal hidden>
      <section class="login-modal" role="dialog" aria-modal="true" aria-labelledby="login-title">
        <button class="modal-close" type="button" data-login-close aria-label="Close login">&times;</button>
        <div class="login-modal-header"><span class="login-symbol">${icons.shield}</span><p class="eyebrow">SkyGuard-AI access</p><h2 id="login-title">Welcome back</h2><p>Sign in to continue monitoring your systems.</p></div>
        <form class="login-form">
          <label>Email<input type="email" placeholder="you@company.com" required></label>
          <label>Password<input type="password" placeholder="Enter your password" required></label>
          <div class="login-options"><label class="remember"><input type="checkbox"> Remember me</label><a href="#">Forgot password?</a></div>
          <button type="submit" class="btn btn-primary login-submit">Sign in ${icons.chevronRight}</button>
        </form>
      </section>
    </div>`;

  return `
    <div style="min-height: 100vh; background-color: var(--bg-base); display: flex; flex-direction: column; align-items: center; position: relative; overflow: hidden;">
      <div class="bg-topo"></div>
      
      <!-- Gradient overlay at bottom -->
      <div style="position: absolute; bottom: 0; left: 0; width: 100%; height: 40vh; background: linear-gradient(to top, rgba(231, 240, 233, 0.8), transparent); z-index: 1;"></div>

      <div style="width: 100%; max-width: 420px; padding: 4rem 2rem; position: relative; z-index: 10; margin-top: 10vh;">
        
        <!-- Logo -->
        <div style="text-align: center; margin-bottom: 3rem;">
          <div style="display: inline-block; padding: 1rem; border-radius: var(--radius-lg); background-color: var(--bg-card); border: 1px solid var(--border-color); margin-bottom: 1.5rem; box-shadow: var(--shadow-sm);">
            <svg width="40" height="40" viewBox="0 0 64 64" fill="none">
              <path d="M32 4L56 18V46L32 60L8 46V18L32 4Z" stroke="#153226" stroke-width="3" fill="none"/>
              <path d="M32 4L56 18V46L32 60L8 46V18L32 4Z" stroke="#153226" stroke-width="2" fill="none" transform="scale(0.7) translate(13.7 13.7)"/>
              <circle cx="32" cy="32" r="6" fill="#2D6A4F"/>
            </svg>
          </div>
          <h1 style="font-size: 2.5rem; font-weight: 800; color: var(--color-primary); letter-spacing: -0.02em; margin-bottom: 1rem;">
            SKYGUARD <span style="color: var(--color-secondary); font-weight: 600;">AI</span>
          </h1>
          <div class="eyebrow" style="letter-spacing: 0.3em; font-size: 0.65rem;">
            INTELLIGENCE THAT PROTECTS THE SKY
          </div>
        </div>

        <!-- Form -->
        <form style="background: transparent;">
          <div style="position: relative; margin-bottom: 2rem;">
            <div style="position: absolute; left: 0; top: 12px; color: var(--text-secondary); width: 20px;">
              ${icons.user}
            </div>
            <label style="display: block; margin-left: 36px; font-size: 0.85rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">Email</label>
            <input type="email" placeholder="you@company.com" class="input-field" style="padding-left: 36px;" />
          </div>

          <div style="position: relative; margin-bottom: 1.5rem;">
            <div style="position: absolute; left: 0; top: 12px; color: var(--text-secondary); width: 20px;">
              ${icons.lock}
            </div>
            <label style="display: block; margin-left: 36px; font-size: 0.85rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">Password</label>
            <input type="password" value="••••••••••••" class="input-field" style="padding-left: 36px;" />
          </div>

          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 3rem; font-size: 0.85rem;">
            <label style="display: flex; align-items: center; gap: 0.5rem; cursor: pointer; color: var(--text-secondary);">
              <div style="width: 16px; height: 16px; border-radius: 4px; background-color: var(--color-secondary); display: flex; align-items: center; justify-content: center; color: white;">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>
              </div>
              Remember me
            </label>
            <a href="#" style="color: var(--color-secondary); text-decoration: none; font-weight: 500;">Forgot password?</a>
          </div>

          <!-- Changed link to a button-styled anchor for routing to dashboard -->
          <a href="#/dashboard" class="btn btn-primary" style="width: 100%; padding: 1rem; font-size: 1rem; justify-content: center; border-radius: var(--radius-full); box-shadow: 0 10px 20px rgba(21, 50, 38, 0.15);">
            Sign In
            <span style="width: 20px; margin-left: 0.5rem;">${icons.chevronRight}</span>
          </a>
        </form>

        <div style="text-align: center; margin-top: 2.5rem; position: relative;">
          <div style="position: absolute; top: 50%; left: 0; width: 100%; height: 1px; background-color: var(--border-color); z-index: 1;"></div>
          <span style="position: relative; z-index: 2; background-color: var(--bg-base); padding: 0 1rem; color: var(--text-secondary); font-size: 0.85rem;">or</span>
        </div>

        <div style="text-align: center; margin-top: 2rem; font-size: 0.9rem; color: var(--text-secondary);">
          Don't have an account? <a href="#" style="color: var(--color-secondary); text-decoration: none; font-weight: 600;">Sign up</a>
        </div>
      </div>
    </div>
  `;
}
