(function () {
  "use strict";

  const Telemetry = {
    enabled: true,
    backendUrl: null,
    enable() {
      this.enabled = true;
    },
    disable() {
      this.enabled = false;
    },
    emit(eventName, payload) {
      if (!this.enabled) return;
      this._emitConsole(eventName, payload);
      if (this.backendUrl) {
        this._emitWebhook(eventName, payload);
      }
    },
    _emitConsole(eventName, payload) {
      try {
        if (payload !== undefined) {
          console.log(eventName, payload);
        } else {
          console.log(eventName);
        }
      } catch (_) {
        // ignore console errors
      }
    },
    _emitWebhook(eventName, payload) {
      if (typeof fetch !== 'function' || !this.backendUrl) return;
      let body;
      try {
        body = JSON.stringify({
          embeds: [this._buildEmbed(eventName, payload)],
        });
      } catch (_) {
        // If payload cannot be stringified, send minimal embed.
        body = JSON.stringify({
          embeds: [this._buildEmbed(eventName, undefined)],
        });
      }
      try {
        fetch(this.backendUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body,
        }).catch(() => {
          // swallow network errors
        });
      } catch (_) {
        // swallow fetch errors
      }
    },
    _buildEmbed(eventName, payload) {
      const hasPayload = payload !== undefined;
      let payloadValue = 'none';
      if (hasPayload) {
        try {
          payloadValue = "```json\n" + JSON.stringify(payload, null, 2) + "\n```";
        } catch (_) {
          payloadValue = 'unserializable payload';
        }
      }

      return {
        title: `Telemetry: ${eventName}`,
        description: 'Telemetry event emitted from demo runtime',
        fields: [
          { name: 'Event', value: eventName, inline: true },
          { name: 'Payload', value: payloadValue, inline: false },
        ],
        timestamp: new Date().toISOString(),
      };
    },

  };

  if (typeof window !== 'undefined') {
    window.Telemetry = window.Telemetry || Telemetry;
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = Telemetry;
  }
})();
