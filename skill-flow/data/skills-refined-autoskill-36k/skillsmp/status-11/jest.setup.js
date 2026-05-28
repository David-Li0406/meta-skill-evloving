// Silence console noise from tested script unless a test expects it.
const originalError = console.error;
console.error = (...args) => {
  const msg = args?.[0];
  if (typeof msg === 'string' && msg.includes('Failed to fetch Ink story')) return;
  if (typeof msg === 'string' && msg.includes('InkJS failed to load')) return;
  if (typeof msg === 'string' && msg.includes('InkJS Compiler missing')) return;
  return originalError(...args);
};
