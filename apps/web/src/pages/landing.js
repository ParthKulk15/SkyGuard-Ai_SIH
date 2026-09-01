import { icons } from '../components/icons.js';

export function renderLanding() {
  return `
    <div style="min-height: 100vh; background-color: var(--bg-base); position: relative; overflow-x: hidden;">
      <div class="bg-topo"></div>
      
      <!-- Navbar -->
      <header style="display: flex; justify-content: space-between; align-items: center; padding: 1.5rem 4rem; max-width: 1400px; margin: 0 auto; position: relative; z-index: 10;">
        <div style="display: flex; align-items: center; gap: 0.75rem; font-weight: 800; font-size: 1.25rem; color: var(--color-primary);">
          <svg width="28" height="28" viewBox="0 0 64 64" fill="none">
            <path d="M32 4L56 18V46L32 60L8 46V18L32 4Z" stroke="#153226" stroke-width="3" fill="none"/>
            <path d="M32 4L56 18V46L32 60L8 46V18L32 4Z" stroke="#153226" stroke-width="2" fill="none" transform="scale(0.7) translate(13.7 13.7)"/>
            <circle cx="32" cy="32" r="6" fill="#2D6A4F"/>
          </svg>
          SKYGUARD AI
        </div>
        
        <nav style="display: flex; gap: 2rem;">
          <a href="#" style="text-decoration: none; color: var(--text-secondary); font-weight: 500; font-size: 0.95rem;">Platform</a>
          <a href="#" style="text-decoration: none; color: var(--text-secondary); font-weight: 500; font-size: 0.95rem;">How It Works</a>
          <a href="#" style="text-decoration: none; color: var(--text-secondary); font-weight: 500; font-size: 0.95rem;">Solutions</a>
          <a href="#" style="text-decoration: none; color: var(--text-secondary); font-weight: 500; font-size: 0.95rem;">Resources</a>
          <a href="#" style="text-decoration: none; color: var(--text-secondary); font-weight: 500; font-size: 0.95rem;">Company</a>
        </nav>
        
        <a href="#/login" class="btn btn-primary" style="padding: 0.6rem 1.5rem;">
          Request Access
          <span style="width: 16px;">${icons.chevronRight}</span>
        </a>
      </header>

      <!-- Hero Section -->
      <section style="padding: 4rem 4rem 8rem; max-width: 1400px; margin: 0 auto; display: flex; position: relative; z-index: 10;">
        <div style="flex: 1; max-width: 600px;">
          <h1 class="hero-title" style="margin-bottom: 2rem;">
            SKYGUARD<br/>
            <span style="color: var(--color-secondary);">AI</span>
          </h1>
          
          <div class="eyebrow" style="margin-bottom: 2rem; letter-spacing: 0.2em; font-size: 0.85rem;">
            INTELLIGENCE THAT PROTECTS THE SKY
          </div>
          
          <p style="font-size: 1.25rem; color: var(--text-primary); margin-bottom: 2.5rem; line-height: 1.6;">
            From raw sensor signals<br/>
            to self-healing systems —<br/>
            SkyGuard AI <span style="color: var(--color-secondary); font-weight: 500;">watches</span>,<br/>
            <span style="color: var(--color-secondary); font-weight: 500;">understands</span> and <span style="color: var(--color-secondary); font-weight: 500;">acts</span>.
          </p>
          
          <a href="#/login" style="display: flex; align-items: center; gap: 1rem; text-decoration: none; color: var(--text-primary); font-weight: 600;">
            <div style="width: 48px; height: 48px; border-radius: 50%; background-color: var(--color-primary); color: white; display: flex; align-items: center; justify-content: center;">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
            </div>
            Watch Overview
          </a>
        </div>
        
        <div style="flex: 1; position: relative;">
          <!-- Decorative Particle/Network Graphic goes here in real app, using placeholder styling -->
          <div style="position: absolute; right: 0; top: 10%; width: 400px; height: 400px; border-radius: 50%; border: 1px dashed var(--color-secondary); opacity: 0.2;"></div>
          <div style="position: absolute; right: 50px; top: 20%; width: 300px; height: 300px; border-radius: 50%; border: 1px solid var(--color-secondary); opacity: 0.1;"></div>
          <div style="position: absolute; right: 150px; top: 30%; width: 10px; height: 10px; border-radius: 50%; background-color: var(--color-secondary);"></div>
          <div style="position: absolute; right: 80px; top: 60%; width: 8px; height: 8px; border-radius: 50%; background-color: var(--color-secondary);"></div>
          
          <div class="card" style="position: absolute; bottom: 0; right: 0; display: flex; align-items: center; gap: 2rem; padding: 1.25rem 2rem;">
            <div>
              <div class="micro-label">SYSTEM STATUS</div>
              <div style="color: var(--status-healthy); font-weight: 600;">All Systems Operational</div>
            </div>
            <div class="status-dot dot-healthy"></div>
          </div>
        </div>
      </section>

      <!-- Pipeline Section -->
      <section style="background-color: var(--bg-card-alt); border-top: 1px solid var(--border-color); border-bottom: 1px solid var(--border-color); padding: 5rem 0;">
        <div style="max-width: 1400px; margin: 0 auto; padding: 0 4rem;">
          <div class="eyebrow" style="margin-bottom: 1rem;">THE SKYGUARD AI PIPELINE</div>
          <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 4rem;">
            <h2 style="font-size: 2.5rem; max-width: 500px; line-height: 1.2;">
              End-to-end intelligence.<br/>
              Always learning. <span style="color: var(--color-secondary);">Always acting.</span>
            </h2>
            <p style="color: var(--text-secondary); max-width: 300px;">
              A continuous loop of perception, cognition and action — purpose-built for the skies.
            </p>
          </div>
          
          <!-- Pipeline steps -->
          <div style="display: flex; justify-content: space-between; position: relative;">
            <div style="position: absolute; top: 32px; left: 40px; right: 40px; height: 2px; background-color: var(--border-color); z-index: 1;"></div>
            
            ${[
              { num: '1', title: 'RAW DATA', icon: icons.monitoring },
              { num: '2', title: 'EDGE AI', icon: icons.cpu },
              { num: '3', title: 'ADVANCED AI', icon: icons.brain },
              { num: '4', title: 'SPATIAL VALIDATION', icon: icons.layers },
              { num: '5', title: 'DIAGNOSIS', icon: icons.diagnostics },
              { num: '6', title: 'EXPLAINABLE DECISION', icon: icons.reports },
              { num: '7', title: 'SELF-HEALING', icon: icons.refresh },
              { num: '8', title: 'MAINTENANCE', icon: icons.maintenance }
            ].map(step => `
              <div style="position: relative; z-index: 2; width: 120px; text-align: center;">
                <div style="width: 64px; height: 64px; border-radius: 50%; background-color: var(--bg-card); border: 2px solid var(--border-color); display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem; color: var(--color-primary);">
                  <div style="width: 28px; height: 28px;">${step.icon}</div>
                </div>
                <div style="font-weight: 700; font-size: 0.8rem; margin-bottom: 0.5rem; color: var(--text-primary);">${step.num}. ${step.title}</div>
              </div>
            `).join('')}
          </div>
        </div>
      </section>

      <!-- CTA Footer -->
      <footer style="background-color: var(--color-primary); color: white; padding: 6rem 4rem; text-align: center; position: relative; overflow: hidden;">
        <!-- Glowing effect -->
        <div style="position: absolute; bottom: -50%; left: 50%; transform: translateX(-50%); width: 800px; height: 800px; border-radius: 50%; background: radial-gradient(circle, rgba(45,106,79,0.4) 0%, rgba(21,50,38,0) 70%); pointer-events: none;"></div>
        
        <div style="position: relative; z-index: 10;">
          <h2 style="font-size: 3rem; margin-bottom: 1.5rem;">
            Protect the skies.<br/>
            <span style="color: var(--color-secondary-light);">Stay ahead.</span>
          </h2>
          <p style="color: rgba(255,255,255,0.7); max-width: 500px; margin: 0 auto 2.5rem; font-size: 1.1rem;">
            Join forward-thinking teams using SkyGuard AI to build safer, smarter and more resilient operations.
          </p>
          <a href="#/login" class="btn" style="background-color: var(--color-secondary); color: white; padding: 1rem 2rem; font-size: 1.1rem;">
            Request Access
            <span style="width: 20px;">${icons.chevronRight}</span>
          </a>
        </div>
      </footer>
    </div>
  `;
}
