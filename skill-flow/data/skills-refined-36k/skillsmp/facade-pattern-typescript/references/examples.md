# Facade Examples (TypeScript)

## Example 1: VideoConverter-like facade

```ts
type Video = { path: string; format: "mp4" | "webm" };

type ConvertOptions = { format: "mp4" | "webm"; bitrateKbps: number };

class Decoder {
  decode(input: Video): string {
    return `raw:${input.path}`;
  }
}

class Encoder {
  encode(raw: string, options: ConvertOptions): Video {
    return { path: `${raw}.${options.format}`, format: options.format };
  }
}

class Optimizer {
  optimize(raw: string): string {
    return `${raw}:optimized`;
  }
}

class MediaConverterFacade {
  constructor(
    private readonly decoder: Decoder,
    private readonly optimizer: Optimizer,
    private readonly encoder: Encoder
  ) {}

  convert(input: Video, options: ConvertOptions): Video {
    const raw = this.decoder.decode(input);
    const optimized = this.optimizer.optimize(raw);
    return this.encoder.encode(optimized, options);
  }
}

const facade = new MediaConverterFacade(new Decoder(), new Optimizer(), new Encoder());
const out = facade.convert({ path: "in", format: "mp4" }, { format: "webm", bitrateKbps: 800 });
console.log(out);
```

## Example 2: Data ingestion facade (Parser -> Validator -> Writer)

```ts
type RecordRow = { id: string; value: number };

type IngestResult = { ok: true; count: number } | { ok: false; error: string };

class Parser {
  parse(raw: string): RecordRow[] {
    return raw.split("\n").filter(Boolean).map((line) => {
      const [id, v] = line.split(",");
      return { id, value: Number(v) };
    });
  }
}

class Validator {
  validate(rows: RecordRow[]): RecordRow[] {
    return rows.filter((r) => Number.isFinite(r.value));
  }
}

class Writer {
  async write(rows: RecordRow[]): Promise<number> {
    return rows.length;
  }
}

class IngestionFacade {
  constructor(
    private readonly parser: Parser,
    private readonly validator: Validator,
    private readonly writer: Writer
  ) {}

  async ingest(raw: string): Promise<IngestResult> {
    const parsed = this.parser.parse(raw);
    const valid = this.validator.validate(parsed);
    const count = await this.writer.write(valid);
    return { ok: true, count };
  }
}

const facade = new IngestionFacade(new Parser(), new Validator(), new Writer());
const result = await facade.ingest("a,1\nb,2\nc,notanumber");
console.log(result);
```

## Facade vs Adapter vs Mediator vs Proxy (tiny sketches)

```ts
// Facade: simplified entrypoint to subsystem
class SubsystemFacade { run(): void { /* call multiple internals */ } }

// Adapter: translate interface to target
interface Target { execute(): void; }
class Adapter implements Target { constructor(private adaptee: { doThing(): void }) {} execute() { this.adaptee.doThing(); } }

// Mediator: coordinate peer interactions
class Mediator { notify(sender: object, event: string): void { /* route */ } }

// Proxy: same API, control access/lifecycle
class ProxySvc { constructor(private inner: { run(): void }) {} run() { /* auth/lazy */ this.inner.run(); } }
```
