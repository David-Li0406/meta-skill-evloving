// Fetches the generated director config JSON and sets window.DirectorConfig
(function(){
  if (typeof window === 'undefined') return;
  // Path is relative to demo root; dev script writes to web/demo/config/director-config.json
  const url = 'config/director-config.json';
  fetch(url, { cache: 'no-store' }).then(r => {
    if (!r.ok) throw new Error('Not found');
    return r.json();
  }).then(cfg => {
    window.DirectorConfig = cfg;
    console.info('[demo] DirectorConfig loaded', cfg);
  }).catch(() => {
    // silent fallback
  });
})();
