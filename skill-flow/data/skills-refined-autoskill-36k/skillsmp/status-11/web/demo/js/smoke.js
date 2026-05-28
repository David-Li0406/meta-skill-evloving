(function() {
  function broadcastState(state) {
    try {
      window.dispatchEvent(new CustomEvent('smoke_state', { detail: state }));
    } catch (e) {
      /* ignore */
    }
  }

  const canvas = document.getElementById('smoke-layer');
  if (!canvas) {
    window.Smoke = {
      trigger() { broadcastState({ running: false, durationMs: 0, intensity: 0, remainingMs: 0 }); },
      getState() { return { running: false, durationMs: 0, intensity: 0, remainingMs: 0 }; },
      loadState() { broadcastState({ running: false, durationMs: 0, intensity: 0, remainingMs: 0 }); },
      resize() {},
    };
    broadcastState({ running: false, durationMs: 0, intensity: 0, remainingMs: 0 });
    return;
  }
  const ctx = canvas.getContext('2d');
  if (!ctx) {
    window.Smoke = {
      trigger() { broadcastState({ running: false, durationMs: 0, intensity: 0, remainingMs: 0 }); },
      getState() { return { running: false, durationMs: 0, intensity: 0, remainingMs: 0 }; },
      loadState() { broadcastState({ running: false, durationMs: 0, intensity: 0, remainingMs: 0 }); },
      resize() {},
    };
    broadcastState({ running: false, durationMs: 0, intensity: 0, remainingMs: 0 });
    return;
  }
  let particles = [];
  let running = false;
  let startTime = 0;
  let durationMs = 3000;
  let intensity = 5;

  function resize() {
    if (!canvas) return;
    const dpr = window.devicePixelRatio || 1;
    canvas.width = window.innerWidth * dpr;
    canvas.height = window.innerHeight * dpr;
    canvas.style.width = `${window.innerWidth}px`;
    canvas.style.height = `${window.innerHeight}px`;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  function reset() {
    particles = [];
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  }

  function spawnParticle() {
    const x = Math.random() * window.innerWidth;
    const y = window.innerHeight + Math.random() * 40;
    const size = 20 + Math.random() * 50;
    const life = durationMs * (0.4 + Math.random() * 0.6);
    const driftX = (Math.random() - 0.5) * 30;
    const driftY = -50 - Math.random() * 30;
    particles.push({ x, y, size, life, born: performance.now(), driftX, driftY });
  }

  function draw() {
    if (!running) return;
    const now = performance.now();
    const elapsed = now - startTime;
    const remaining = durationMs - elapsed;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // spawn based on intensity
    const spawnCount = Math.max(1, Math.floor(intensity / 2));
    for (let i = 0; i < spawnCount; i++) {
      spawnParticle();
    }

    particles = particles.filter(p => (now - p.born) < p.life);
    for (const p of particles) {
      const age = now - p.born;
      const t = age / p.life;
      const alpha = Math.max(0, 0.6 * (1 - t));
      const offsetX = p.driftX * t;
      const offsetY = p.driftY * t;
      const x = p.x + offsetX;
      const y = p.y + offsetY;
      const grad = ctx.createRadialGradient(x, y, 0, x, y, p.size);
      grad.addColorStop(0, `rgba(200, 200, 220, ${alpha})`);
      grad.addColorStop(1, `rgba(200, 200, 220, 0)`);
      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.arc(x, y, p.size, 0, Math.PI * 2);
      ctx.fill();
    }

    if (remaining > 0) {
      broadcastState({ running, durationMs, remainingMs: remaining, intensity });
      requestAnimationFrame(draw);
    } else {
      running = false;
      reset();
      broadcastState({ running, durationMs, remainingMs: 0, intensity });
    }
  }

  function triggerSmoke(options) {
    const { duration = 3, intensity: level = 5 } = options || {};
    durationMs = Math.max(0.5, duration) * 1000;
    intensity = Math.min(10, Math.max(1, level));
    startTime = performance.now();
    running = true;
    broadcastState({ running, durationMs, remainingMs: durationMs, intensity });
    draw();
  }

  function getState() {
    return { running, remainingMs: Math.max(0, durationMs - (performance.now() - startTime)), durationMs, intensity };
  }

  function loadState(state) {
    if (!state) return;
    durationMs = state.durationMs || durationMs;
    intensity = state.intensity || intensity;
    if (state.running) {
      triggerSmoke({ duration: durationMs / 1000, intensity });
    } else {
      broadcastState({ running: false, durationMs, remainingMs: durationMs, intensity });
    }
  }

  window.Smoke = {
    trigger: triggerSmoke,
    getState,
    loadState,
    resize,
  };

  broadcastState({ running: false, durationMs, remainingMs: durationMs, intensity });
  resize();
  window.addEventListener('resize', resize);
})();
