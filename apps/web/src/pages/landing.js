import { icons } from '../components/icons.js';
import { renderAntigravity } from '../components/antigravity.js';
import { renderLogin } from './login.js';

const pipeline = [
  ['1', 'Raw data', 'Ingest', icons.monitoring, 'Signals, feeds and logs.'],
  ['2', 'Edge AI', 'Infer', icons.cpu, 'Real-time intelligence at the edge.'],
  ['3', 'Advanced AI', 'Learn', icons.brain, 'Models uncover patterns and anomalies.'],
  ['4', 'Spatial validation', 'Validate', icons.layers, 'Context from location and time.'],
  ['5', 'Diagnosis', 'Diagnose', icons.diagnostics, 'Pinpoint root cause with confidence.'],
  ['6', 'Explainable decision', 'Decide', icons.reports, 'Clear reasons. Human trust.'],
  ['7', 'Self-healing', 'Act', icons.refresh, 'Autonomous actions restore health.'],
  ['8', 'Maintenance', 'Improve', icons.maintenance, 'Smarter schedules. Longer life.']
];

const capabilities = [
  ['capability-card capability-card-large', 'Real-time awareness', 'Live', 'Live insights across assets, environments and events.', 'radar'],
  ['capability-card', 'Explainable by design', '', 'Every decision is traceable, transparent and trustworthy.', 'layers'],
  ['capability-card', 'Edge to cloud', '', 'Seamless intelligence from the edge to the cloud.', 'cloud'],
  ['capability-card', 'Adaptive and autonomous', '', 'Continuously learning. Continuously improving.', 'target'],
  ['capability-card', 'Self-healing systems', '', 'Detect, decide and act automatically.', 'bolt']
];

function logo() {
  return `<a class="brand" href="#/"><span class="brand-mark">${icons.shield}</span><span>SKYGUARD AI</span></a>`;
}

function graphic(type) {
  if (type === 'radar' || type === 'target') return `<span class="mini-radar"><i></i><i></i><i></i></span>`;
  if (type === 'layers') return `<span class="mini-layers"><i></i><i></i><i></i></span>`;
  if (type === 'cloud') return `<span class="mini-cloud">${icons.weather}<b>${icons.analytics}</b></span>`;
  return `<span class="mini-bolt">${icons.alerts}</span>`;
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
          <div class="hero-particle-layer">${renderAntigravity({ count: 300, magnetRadius: 6, ringRadius: 7, waveSpeed: 0.4, waveAmplitude: 1, particleSize: 1.5, lerpSpeed: 0.05, color: '#3300ff', autoAnimate: true, particleVariance: 1 })}</div>
          <div class="hero-center">
            <p class="hero-kicker">Autonomous intelligence for resilient skies</p>
            <h1>SkyGuard-AI</h1>
            <p class="hero-slogan"><span data-typewriter="Intelligence that protects the sky"></span><span class="type-cursor" aria-hidden="true"></span></p>
            <button type="button" class="btn btn-primary hero-login" data-login-open>Login ${icons.chevronRight}</button>
          </div>
        </section>

        <section class="pipeline-section section-band" id="pipeline">
          <div class="shell">
            <div class="section-intro"><div><p class="eyebrow">The SkyGuard AI pipeline</p><h2>End-to-end intelligence.<br>Always learning. <span>Always acting.</span></h2></div><div class="intro-aside"><p>A continuous loop of perception, cognition and action - purpose-built for the skies.</p><a href="#pipeline" class="text-link">Scroll to explore <span>&#8595;</span></a></div></div>
            <div class="pipeline-grid">${pipeline.map(([num, title, verb, icon, desc], index) => `<div class="pipeline-step"><div class="step-visual"><span class="step-number">${num}</span><span class="step-icon">${icon}</span>${index < pipeline.length - 1 ? '<span class="step-connector">&#8594;</span>' : ''}</div><h3>${title}</h3><p><b>${verb}.</b> ${desc}</p></div>`).join('')}</div>
          </div>
        </section>

        <section class="impact-section" id="impact"><div class="shell impact-grid"><div class="impact-copy"><p class="eyebrow">Built for complexity</p><h2>See more.<br>Understand deeper.<br><span>Act earlier.</span></h2><p>SkyGuard AI unifies multi-source data, advanced models and domain expertise to deliver decisions that are accurate, explainable and actionable.</p><div class="stats"><div><strong>10x</strong><span>Faster detection</span></div><div><strong>92%</strong><span>Diagnostic accuracy</span></div><div><strong>35%</strong><span>Lower downtime</span></div></div></div><div class="radar-dome"><div class="dome-sky"><span class="dome-glow"></span><div class="dome-grid"></div><div class="dome-structure"><div class="dome-cap"></div><div class="dome-base"></div></div><span class="dome-label">REMOTE STATION / 04</span></div></div></div></section>

        <section class="capabilities-section section-band" id="capabilities"><div class="shell capabilities-grid"><div class="capability-intro"><p class="eyebrow">Designed for impact</p><h2>Powerful<br>capabilities.<br><span>Real-world<br>results.</span></h2><a href="#/dashboard" class="text-link">Explore platform <span>&#8594;</span></a></div><div class="capability-cards">${capabilities.map(([klass, title, badge, desc, type]) => `<article class="${klass}"><div class="cap-card-head"><h3>${title}</h3>${badge ? `<span class="live-badge"><i></i>${badge}</span>` : ''}</div><p>${desc}</p>${graphic(type)}</article>`).join('')}</div></div></section>

        <section class="final-cta"><div class="cta-contours"></div><div class="cta-content"><p class="eyebrow">Designed for what comes next</p><h2>Protect the skies.<br><span>Stay ahead.</span></h2><p>Join forward-thinking teams using SkyGuard AI to build safer, smarter and more resilient operations.</p><button type="button" class="btn btn-light" data-login-open>Login ${icons.chevronRight}</button></div></section>
      </main>
      ${renderLogin(true)}
    </div>
  `;
}
