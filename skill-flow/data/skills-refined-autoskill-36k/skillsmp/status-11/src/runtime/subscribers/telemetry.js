// Telemetry subscriber for runtime HookManager
// Emits console-based telemetry events; in prod this should hook into telemetry module

const { defaultTelemetry } = require('../../telemetry/emitter');

// Map runtime hook names to telemetry event types
const HOOK_EVENT_MAP = {
  pre_inject: 'generation',
  post_inject: 'presentation',
  pre_checkpoint: 'validation',
  post_checkpoint: 'outcome'
};

module.exports = function createTelemetrySubscriber(telemetryBackend) {
  const telemetry = telemetryBackend || defaultTelemetry;
  return {
    name: 'runtime-telemetry-subscriber',
    async pre_inject(payload) {
      try { telemetry.emit(HOOK_EVENT_MAP.pre_inject, payload); } catch (err) { }
    },
    async post_inject(payload) {
      try { telemetry.emit(HOOK_EVENT_MAP.post_inject, payload); } catch (err) { }
    },
    async pre_checkpoint(payload) {
      try { telemetry.emit(HOOK_EVENT_MAP.pre_checkpoint, payload); } catch (err) { }
    },
    async post_checkpoint(payload) {
      try { telemetry.emit(HOOK_EVENT_MAP.post_checkpoint, payload); } catch (err) { }
    }
  };
};
