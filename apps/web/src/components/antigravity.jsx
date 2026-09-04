/* eslint-disable react/no-unknown-property */
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import React, { useEffect, useMemo, useRef } from 'react';
import { createRoot } from 'react-dom/client';
import * as THREE from 'three';

const HALF_PI = Math.PI / 2;

const AntigravityInner = ({
  count = 300,
  magnetRadius = 6,
  ringRadius = 7,
  waveSpeed = 0.4,
  waveAmplitude = 1,
  particleSize = 1.0,
  lerpSpeed = 0.15,
  color = '#5227FF',
  autoAnimate = true,
  particleVariance = 1,
  rotationSpeed = 0,
  depthFactor = 1,
  pulseSpeed = 3,
  particleShape = 'capsule',
  fieldStrength = 10
}) => {
  const meshRef = useRef(null);
  const { viewport } = useThree();
  const dummy = useMemo(() => new THREE.Object3D(), []);

  const lastMousePos = useRef({ x: 0, y: 0 });
  const lastMouseMoveTime = useRef(0);
  const virtualMouse = useRef({ x: 0, y: 0 });

  // Pre-allocated object to eliminate per-frame garbage collection
  const targetPos = useRef({ x: 0, y: 0, z: 0 });

  // Global window pointer listener to ensure instantaneous cursor tracking across text/hero overlays
  useEffect(() => {
    const handlePointerMove = (e) => {
      const x = (e.clientX / window.innerWidth) * 2 - 1;
      const y = -(e.clientY / window.innerHeight) * 2 + 1;
      lastMousePos.current = { x, y };
      lastMouseMoveTime.current = Date.now();
    };

    window.addEventListener('pointermove', handlePointerMove, { passive: true });
    window.addEventListener('touchmove', handlePointerMove, { passive: true });
    window.addEventListener('touchstart', handlePointerMove, { passive: true });

    return () => {
      window.removeEventListener('pointermove', handlePointerMove);
      window.removeEventListener('touchmove', handlePointerMove);
      window.removeEventListener('touchstart', handlePointerMove);
    };
  }, []);

  const particles = useMemo(() => {
    const temp = [];
    for (let i = 0; i < count; i++) {
      const t = Math.random() * 100;
      const factor = 20 + Math.random() * 100;
      const speed = 0.01 + Math.random() / 200;
      const xFactor = -50 + Math.random() * 100;
      const yFactor = -50 + Math.random() * 100;
      const zFactor = -50 + Math.random() * 100;

      const normX = Math.random() - 0.5;
      const normY = Math.random() - 0.5;
      const mz = (Math.random() - 0.5) * 20;

      const randomRadiusOffset = (Math.random() - 0.5) * 2;

      temp.push({
        t,
        factor,
        speed,
        xFactor,
        yFactor,
        zFactor,
        normX,
        normY,
        mz,
        cx: 0,
        cy: 0,
        cz: mz,
        vx: 0,
        vy: 0,
        vz: 0,
        randomRadiusOffset,
        initialized: false
      });
    }
    return temp;
  }, [count]);

  useFrame((state, delta) => {
    const mesh = meshRef.current;
    if (!mesh) return;

    const { viewport: v } = state;
    const currentPointer = lastMousePos.current;

    let destX = (currentPointer.x * v.width) / 2;
    let destY = (currentPointer.y * v.height) / 2;

    if (autoAnimate && Date.now() - lastMouseMoveTime.current > 2000) {
      const time = state.clock.getElapsedTime();
      destX = Math.sin(time * 0.5) * (v.width / 4);
      destY = Math.cos(time * 0.5 * 2) * (v.height / 4);
    }

    const vpScale = Math.max(0.4, Math.min(1.0, v.width / 45));
    const responsiveMagnetRadius = magnetRadius * vpScale;
    const responsiveMagnetRadiusSq = responsiveMagnetRadius * responsiveMagnetRadius;
    const responsiveRingRadius = ringRadius * vpScale;

    const dt = Math.min(delta, 0.033);
    // Instantaneous smooth tracking for responsiveness without cursor lag
    const smoothFactor = 1 - Math.exp(-30 * dt);
    virtualMouse.current.x += (destX - virtualMouse.current.x) * smoothFactor;
    virtualMouse.current.y += (destY - virtualMouse.current.y) * smoothFactor;

    const targetX = virtualMouse.current.x;
    const targetY = virtualMouse.current.y;

    const globalRotation = state.clock.getElapsedTime() * rotationSpeed;
    const effectiveLerpSpeed = 1 - Math.exp(-lerpSpeed * 120 * dt);

    const tPos = targetPos.current;

    for (let i = 0; i < particles.length; i++) {
      const particle = particles[i];
      let { t, speed, normX, normY, mz, cz, randomRadiusOffset } = particle;

      const mx = normX * v.width * 1.1;
      const my = normY * v.height * 1.1;

      if (!particle.initialized) {
        particle.cx = mx;
        particle.cy = my;
        particle.cz = mz * depthFactor;
        particle.initialized = true;
      }

      t = particle.t += speed / 2;

      const projectionFactor = 1 - cz / 50;
      const projectedTargetX = targetX * projectionFactor;
      const projectedTargetY = targetY * projectionFactor;

      const dx = mx - projectedTargetX;
      const dy = my - projectedTargetY;
      const distSq = dx * dx + dy * dy;

      tPos.x = mx;
      tPos.y = my;
      tPos.z = mz * depthFactor;

      if (distSq < responsiveMagnetRadiusSq) {
        const angle = Math.atan2(dy, dx) + globalRotation;

        const wave = Math.sin(t * waveSpeed + angle) * (0.5 * waveAmplitude);
        const deviation = randomRadiusOffset * (5 / (fieldStrength + 0.1));

        const currentRingRadius = responsiveRingRadius + wave + deviation;

        tPos.x = projectedTargetX + currentRingRadius * Math.cos(angle);
        tPos.y = projectedTargetY + currentRingRadius * Math.sin(angle);
        tPos.z = mz * depthFactor + Math.sin(t) * (1 * waveAmplitude * depthFactor);
      }

      particle.cx += (tPos.x - particle.cx) * effectiveLerpSpeed;
      particle.cy += (tPos.y - particle.cy) * effectiveLerpSpeed;
      particle.cz += (tPos.z - particle.cz) * effectiveLerpSpeed;

      dummy.position.set(particle.cx, particle.cy, particle.cz);
      dummy.lookAt(projectedTargetX, projectedTargetY, particle.cz);
      dummy.rotateX(HALF_PI);

      const dxCur = particle.cx - projectedTargetX;
      const dyCur = particle.cy - projectedTargetY;
      const currentDistToMouse = Math.sqrt(dxCur * dxCur + dyCur * dyCur);

      const distFromRing = Math.abs(currentDistToMouse - responsiveRingRadius);
      let scaleFactor = 1 - distFromRing / (10 * vpScale);
      scaleFactor = Math.max(0, Math.min(1, scaleFactor));

      const finalScale = scaleFactor * (0.8 + Math.sin(t * pulseSpeed) * 0.2 * particleVariance) * particleSize * vpScale;
      dummy.scale.set(finalScale, finalScale, finalScale);

      dummy.updateMatrix();
      mesh.setMatrixAt(i, dummy.matrix);
    }

    mesh.instanceMatrix.needsUpdate = true;
  });

  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, count]}>
      {particleShape === 'capsule' && <capsuleGeometry args={[0.08, 0.32, 4, 8]} />}
      {particleShape === 'sphere' && <sphereGeometry args={[0.12, 10, 10]} />}
      {particleShape === 'box' && <boxGeometry args={[0.18, 0.18, 0.18]} />}
      {particleShape === 'tetrahedron' && <tetrahedronGeometry args={[0.18]} />}
      <meshBasicMaterial color={color} />
    </instancedMesh>
  );
};

const Antigravity = props => {
  return (
    <Canvas
      camera={{ position: [0, 0, 50], fov: 35 }}
      style={{ width: '100%', height: '100%', pointerEvents: 'auto' }}
      dpr={[1, 1.5]}
      gl={{ powerPreference: 'high-performance', antialias: true }}
    >
      <AntigravityInner {...props} />
    </Canvas>
  );
};

export default Antigravity;

const DEFAULTS = {
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
};

export function renderAntigravity(options = {}) {
  const config = { ...DEFAULTS, ...options };
  return `<div class="antigravity-field" data-antigravity='${JSON.stringify(config)}' aria-hidden="true" style="width: 100%; height: 100%; position: absolute; inset: 0;"></div>`;
}

export function mountAntigravity(field) {
  if (!field || field.dataset.mounted) return;
  field.dataset.mounted = 'true';

  const config = { ...DEFAULTS, ...JSON.parse(field.dataset.antigravity || '{}') };
  const root = createRoot(field);
  root.render(<Antigravity {...config} />);

  field._antigravityCleanup = () => {
    root.unmount();
  };
}
