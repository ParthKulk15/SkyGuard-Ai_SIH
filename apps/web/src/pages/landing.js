import { icons } from '../components/icons.js';
import { renderAntigravity } from '../components/antigravity.js';
import { renderLogin } from './login.js';

function logo() {
  return `<a class="brand" href="#/"><span class="brand-mark">${icons.shield}</span><span>SKYGUARD AI</span></a>`;
}

export function renderLanding() {
  return `
    <div class="landing-page">
      <header class="landing-nav shell">
        ${logo()}
        <button type="button" class="btn btn-primary nav-cta" data-login-open>Login ${icons.chevronRight}</button>
      </header>

      <main>
        <section class="hero hero-minimal">
          <div class="hero-particle-layer">${renderAntigravity({
            count: 300,
            magnetRadius: 6,
            ringRadius: 7,
            waveSpeed: 0.4,
            waveAmplitude: 1,
            particleSize: 1.0,
            lerpSpeed: 0.15,
            color: '#5227FF',
            autoAnimate: true,
            particleVariance: 1,
            rotationSpeed: 0,
            depthFactor: 1,
            pulseSpeed: 3,
            particleShape: 'capsule',
            fieldStrength: 10
          })}</div>
          <div class="hero-center">
            <p class="hero-kicker">Autonomous intelligence for resilient skies</p>
            <h1>SkyGuard-AI</h1>
            <p class="hero-slogan"><span data-typewriter="Intelligence that protects the sky"></span><span class="type-cursor" aria-hidden="true"></span></p>
            <button type="button" class="btn btn-primary hero-login" data-login-open>Login ${icons.chevronRight}</button>
          </div>
        </section>
      </main>
      ${renderLogin(true)}
    </div>
  `;
}
