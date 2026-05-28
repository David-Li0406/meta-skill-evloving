const fs = require('fs');
const path = require('path');
const src = path.resolve(__dirname, '../src/runtime/hook-manager/index.js');
const out = path.resolve(__dirname, '../web/demo/js/hook-manager.bundled.js');
let srcText = fs.readFileSync(src, 'utf8');
// Remove module.exports line and wrap in IIFE that exposes HookManager constructor
srcText = srcText.replace(/module\.exports\s*=\s*HookManager\s*;?\s*$/m, 'return HookManager;');
const wrapped = `(function(){\n${srcText}\n})();\nif (typeof window !== 'undefined') {\n  try {\n    const HM = (function(){ ${srcText} })();\n    if (!window.RuntimeHooks) window.RuntimeHooks = new HM();\n  } catch (e) {\n    console.error('[build-hook-shim] failed to initialize HookManager', e);\n  }\n}\n`;
fs.writeFileSync(out, wrapped, 'utf8');
console.log('Wrote', out);
