/**
 * Phase lifecycle hooks.
 * Modules register onEnter/onExit callbacks for specific phases.
 */

const _phaseEnterHooks = {};
const _phaseExitHooks = {};

/**
 * Register a callback to run when entering a phase.
 * @param {string} phase - Phase name (e.g. 'searching', 'executing')
 * @param {function(app)} fn - Callback receiving the Alpine.js app instance
 */
function onPhaseEnter(phase, fn) {
    if (!_phaseEnterHooks[phase]) {
        _phaseEnterHooks[phase] = [];
    }
    _phaseEnterHooks[phase].push(fn);
}

/**
 * Register a callback to run when exiting a phase.
 * @param {string} phase - Phase name
 * @param {function(app)} fn - Callback
 */
function onPhaseExit(phase, fn) {
    if (!_phaseExitHooks[phase]) {
        _phaseExitHooks[phase] = [];
    }
    _phaseExitHooks[phase].push(fn);
}

/**
 * Fire phase transition hooks.
 * Called by the app when phase changes.
 * @param {object} app - Alpine.js app instance
 * @param {string} oldPhase - Previous phase
 * @param {string} newPhase - New phase
 */
function firePhaseTransition(app, oldPhase, newPhase) {
    if (oldPhase === newPhase) return;

    // Fire exit hooks for old phase
    const exitHooks = _phaseExitHooks[oldPhase];
    if (exitHooks) {
        for (const fn of exitHooks) {
            fn(app);
        }
    }

    // Fire enter hooks for new phase
    const enterHooks = _phaseEnterHooks[newPhase];
    if (enterHooks) {
        for (const fn of enterHooks) {
            fn(app);
        }
    }
}

// ── Built-in hooks: completion modal ────────────────────────────
onPhaseEnter('complete', function(app) {
    app.completionTriggeredLive = true;
    app.completionModalDismissed = false;
});
onPhaseEnter('error', function(app) {
    app.completionTriggeredLive = true;
    app.completionModalDismissed = false;
});

// Export
if (typeof window !== 'undefined') {
    window.onPhaseEnter = onPhaseEnter;
    window.onPhaseExit = onPhaseExit;
    window.firePhaseTransition = firePhaseTransition;
}
