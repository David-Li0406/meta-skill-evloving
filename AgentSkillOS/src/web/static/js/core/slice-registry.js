/**
 * Slice Registry — self-registration infrastructure for execute slices.
 *
 * Module JS files call registerExecuteSlice() at load time so that
 * app-shell.js can discover them without hardcoded checks.
 *
 * Load order: initial-state.js → ws-handlers.js → phase-hooks.js → slice-registry.js → module slices → app-shell.js
 */
const _executeSliceRegistry = {};

function registerExecuteSlice(engineId, sliceFn) {
    _executeSliceRegistry[engineId] = sliceFn();
}

window.registerExecuteSlice = registerExecuteSlice;
window._executeSliceRegistry = _executeSliceRegistry;
