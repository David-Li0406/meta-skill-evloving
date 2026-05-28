describe('telemetry facade', () => {
  let Telemetry;

  beforeEach(() => {
    jest.resetModules();
    jest.isolateModules(() => {
      Telemetry = require('../../web/demo/js/telemetry.js');
    });
    Telemetry.enable();
  });

  afterEach(() => {
    if (global.fetch) {
      delete global.fetch;
    }
  });

  it('emits via console.log when enabled', () => {
    const spy = jest.spyOn(console, 'log').mockImplementation(() => {});

    Telemetry.emit('story_start');
    Telemetry.emit('choice_selected', { idx: 0 });

    expect(spy).toHaveBeenCalledWith('story_start');
    expect(spy).toHaveBeenCalledWith('choice_selected', { idx: 0 });

    spy.mockRestore();
  });

  it('does not emit when disabled', () => {
    const spy = jest.spyOn(console, 'log').mockImplementation(() => {});
    Telemetry.disable();

    Telemetry.emit('story_start');
    Telemetry.emit('choice_selected');

    expect(spy).not.toHaveBeenCalled();

    spy.mockRestore();
  });

  describe('webhook', () => {
    it('posts embeds for key events', async () => {
      const fetchSpy = jest.fn().mockResolvedValue({ ok: true });
      global.fetch = fetchSpy;
      Telemetry.backendUrl = 'https://discord.test/webhook';

      const events = [
        { name: 'story_start', payload: { storyId: 'demo' } },
        { name: 'choice_selected', payload: { idx: 1, text: 'A' } },
        { name: 'smoke_triggered', payload: { intensity: 5 } },
        { name: 'story_complete', payload: undefined },
      ];

      events.forEach(({ name, payload }) => Telemetry.emit(name, payload));

      expect(fetchSpy).toHaveBeenCalledTimes(4);

      events.forEach(({ name, payload }, idx) => {
        const [url, opts] = fetchSpy.mock.calls[idx];
        expect(url).toBe('https://discord.test/webhook');
        expect(opts.method).toBe('POST');
        expect(opts.headers['Content-Type']).toBe('application/json');
        const parsed = JSON.parse(opts.body);
        expect(Array.isArray(parsed.embeds)).toBe(true);
        const embed = parsed.embeds[0];
        expect(embed.title).toBe(`Telemetry: ${name}`);
        expect(embed.fields[0]).toEqual({ name: 'Event', value: name, inline: true });
        expect(embed.fields[1].name).toBe('Payload');
        if (payload === undefined) {
          expect(embed.fields[1].value).toBe('none');
        } else {
          expect(embed.fields[1].value).toContain('```json');
          Object.keys(payload).forEach((key) => {
            expect(embed.fields[1].value).toContain(key);
          });
        }
        expect(typeof embed.timestamp).toBe('string');
      });
    });

    it('does not post when disabled even if backendUrl is set', () => {
      const fetchSpy = jest.fn();
      global.fetch = fetchSpy;
      Telemetry.backendUrl = 'https://discord.test/webhook';
      Telemetry.disable();

      Telemetry.emit('story_start', { foo: 'bar' });

      expect(fetchSpy).not.toHaveBeenCalled();
    });

    it('swallows fetch errors', () => {
      const fetchSpy = jest.fn(() => {
        throw new Error('boom');
      });
      global.fetch = fetchSpy;
      Telemetry.backendUrl = 'https://discord.test/webhook';

      expect(() => Telemetry.emit('story_start')).not.toThrow();
      expect(fetchSpy).toHaveBeenCalled();
    });

    it('sends minimal embed when payload is unserializable', () => {
      const fetchSpy = jest.fn().mockResolvedValue({ ok: true });
      global.fetch = fetchSpy;
      Telemetry.backendUrl = 'https://discord.test/webhook';

      const circular = {};
      circular.self = circular;

      Telemetry.emit('story_start', circular);

      const [, opts] = fetchSpy.mock.calls[0];
      const parsed = JSON.parse(opts.body);
      const embed = parsed.embeds[0];
      expect(embed.fields[1].value).toBe('unserializable payload');
    });
  });
});
