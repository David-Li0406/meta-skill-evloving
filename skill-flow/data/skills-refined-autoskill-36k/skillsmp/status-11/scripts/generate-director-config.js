// Generates web/demo/config/director-config.json from src/runtime/director-config.js
// Run from repo root: node scripts/generate-director-config.js

const fs = require('fs');
const path = require('path');

(function main() {
  try {
    const cfg = require(path.join('..', 'src', 'runtime', 'director-config.js'));
    const outDir = path.join(process.cwd(), 'web', 'demo', 'config');
    fs.mkdirSync(outDir, { recursive: true });
    const outPath = path.join(outDir, 'director-config.json');
    fs.writeFileSync(outPath, JSON.stringify(cfg, null, 2), 'utf8');
    console.log('Wrote', outPath);
  } catch (err) {
    console.error('Failed to generate director config JSON:', err && err.stack || err);
    process.exitCode = 2;
  }
})();
