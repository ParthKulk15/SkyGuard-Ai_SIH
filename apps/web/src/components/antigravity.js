const DEFAULTS = {
  count: 300,
  magnetRadius: 6,
  ringRadius: 7,
  waveSpeed: 0.4,
  waveAmplitude: 1,
  particleSize: 1.5,
  lerpSpeed: 0.05,
  color: '#3300ff',
  autoAnimate: true,
  particleVariance: 1
};

export function renderAntigravity(options = {}) {
  const config = { ...DEFAULTS, ...options };
  return `<div class="antigravity-field" data-antigravity='${JSON.stringify(config)}' aria-hidden="true"><canvas></canvas></div>`;
}

export function mountAntigravity(field) {
  if (!field || field.dataset.mounted) return;
  field.dataset.mounted = 'true';

  const config = { ...DEFAULTS, ...JSON.parse(field.dataset.antigravity || '{}') };
  const canvas = field.querySelector('canvas');
  const context = canvas.getContext('2d');
  const virtualPointer = { x: 0, y: 0 };
  const particles = [];
  let width = 0;
  let height = 0;
  let scale = 1;
  let frameId;
  let lastFrameTime = 0;

  function resize() {
    const bounds = field.getBoundingClientRect();
    width = Math.max(1, bounds.width);
    height = Math.max(1, bounds.height);
    scale = Math.min(width, height) / 400;
    canvas.width = Math.round(width * window.devicePixelRatio);
    canvas.height = Math.round(height * window.devicePixelRatio);
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    context.setTransform(window.devicePixelRatio, 0, 0, window.devicePixelRatio, 0, 0);
    if (!virtualPointer.x && !virtualPointer.y) {
      virtualPointer.x = width * 0.5;
      virtualPointer.y = height * 0.48;
    }
  }

  function seed() {
    particles.length = 0;
    for (let i = 0; i < config.count; i += 1) {
      const x = Math.random() * width;
      const y = Math.random() * height;
      particles.push({
        x, y, homeX: x, homeY: y, z: Math.random(), angle: Math.random() * Math.PI * 2,
        speed: 0.35 + Math.random() * 0.8, radius: Math.random() * 1.8 + 0.5
      });
    }
  }

  function animate(time) {
    const deltaSeconds = lastFrameTime ? Math.min((time - lastFrameTime) / 1000, 0.05) : 1 / 60;
    lastFrameTime = time;
    const autoX = width * 0.5 + Math.sin(time * 0.00045) * width * 0.18;
    const autoY = height * 0.48 + Math.cos(time * 0.0008) * height * 0.18;
    const desiredX = config.autoAnimate ? autoX : width * 0.5;
    const desiredY = config.autoAnimate ? autoY : height * 0.48;
    virtualPointer.x += (desiredX - virtualPointer.x) * (1 - Math.exp(-8 * deltaSeconds));
    virtualPointer.y += (desiredY - virtualPointer.y) * (1 - Math.exp(-8 * deltaSeconds));
    const targetX = virtualPointer.x;
    const targetY = virtualPointer.y;
    const magnetRadius = Math.max(52, config.magnetRadius * 18 * scale);
    const ringRadius = Math.max(32, config.ringRadius * 11 * scale);

    context.clearRect(0, 0, width, height);
    particles.forEach((particle) => {
      particle.angle += 0.004 * config.waveSpeed * deltaSeconds * 60;
      const dx = particle.x - targetX;
      const dy = particle.y - targetY;
      const distance = Math.hypot(dx, dy);
      let destinationX = particle.homeX + Math.sin(time * 0.0005 * particle.speed + particle.angle) * 4;
      let destinationY = particle.homeY + Math.cos(time * 0.0006 * particle.speed + particle.angle) * 4;

      if (distance < magnetRadius) {
        const angle = Math.atan2(dy, dx);
        const wave = Math.sin(time * 0.001 * config.waveSpeed + angle) * config.waveAmplitude * 5;
        const radius = ringRadius + wave + (particle.z - 0.5) * 10 * config.particleVariance;
        destinationX = targetX + Math.cos(angle) * radius;
        destinationY = targetY + Math.sin(angle) * radius;
      }

      const particleEase = 1 - Math.exp(-config.lerpSpeed * 60 * deltaSeconds);
      particle.x += (destinationX - particle.x) * particleEase;
      particle.y += (destinationY - particle.y) * particleEase;
      const ringDistance = Math.abs(Math.hypot(particle.x - targetX, particle.y - targetY) - ringRadius);
      const opacity = Math.max(0.16, 1 - ringDistance / 100) * (0.45 + particle.z * 0.55);
      const size = Math.max(0.8, config.particleSize * (0.65 + particle.z * 0.8));
      const length = size * (2.4 + particle.z * 2);
      const angle = Math.atan2(particle.y - targetY, particle.x - targetX) + Math.PI / 2;

      context.save();
      context.translate(particle.x, particle.y);
      context.rotate(angle);
      context.strokeStyle = config.color;
      context.globalAlpha = opacity;
      context.lineWidth = size;
      context.lineCap = 'round';
      context.beginPath();
      context.moveTo(0, -length / 2);
      context.lineTo(0, length / 2);
      context.stroke();
      context.restore();
    });

    frameId = requestAnimationFrame(animate);
  }

  resize();
  seed();
  const observer = new ResizeObserver(() => { resize(); seed(); });
  observer.observe(field);
  frameId = requestAnimationFrame(animate);
  field._antigravityCleanup = () => { cancelAnimationFrame(frameId); observer.disconnect(); };
}
