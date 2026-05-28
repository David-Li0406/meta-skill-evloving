// Custom Jest environment that strips Node's Web Storage accessors, which throw
// unless `--localstorage-file` is provided (Node 25+). We temporarily remove the
// accessors before loading `jest-environment-node` so Jest won't copy them into
// the test context, then restore them for the rest of the process.

const keys = ['localStorage', 'sessionStorage'];
const saved = [];

for (const key of keys) {
  const desc = Object.getOwnPropertyDescriptor(globalThis, key);
  if (desc && desc.configurable) {
    saved.push([key, desc]);
    try {
      delete globalThis[key];
    } catch (err) {
      // If delete fails, fall back to defining a harmless value.
      try {
        Object.defineProperty(globalThis, key, {
          value: undefined,
          writable: true,
          configurable: true,
          enumerable: desc.enumerable,
        });
      } catch (err2) {
        // ignore
      }
    }
  }
}

const NodeEnvironment = require('jest-environment-node').TestEnvironment || require('jest-environment-node');

for (const [key, desc] of saved) {
  try {
    Object.defineProperty(globalThis, key, desc);
  } catch (err) {
    // ignore
  }
}

module.exports = class NodeNoWebStorageEnvironment extends NodeEnvironment {};
