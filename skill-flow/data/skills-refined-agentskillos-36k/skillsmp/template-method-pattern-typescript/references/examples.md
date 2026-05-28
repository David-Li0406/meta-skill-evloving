# Template Method Pattern Examples (TypeScript)

Each example is runnable in Node with ts-node.

## Example 1: Document import pipeline (CSV/PDF)

```ts
type ImportResult = { id: string; rows: number };

class ImportError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ImportError";
  }
}

abstract class ImportJob {
  private trace: string[] = [];

  run(input: string): ImportResult {
    this.trace = [];
    this.beforeLoad();
    const raw = this.load(input);
    const parsed = this.parse(raw);
    const normalized = this.normalize(parsed);
    this.validate(normalized);
    const result = this.persist(normalized);
    this.afterPersist(result);
    return result;
  }

  getTrace() {
    return [...this.trace];
  }

  protected record(step: string) {
    this.trace.push(step);
  }

  protected beforeLoad(): void {}
  protected afterPersist(_result: ImportResult): void {}

  protected abstract load(input: string): string;
  protected abstract parse(raw: string): Array<Record<string, string>>;

  protected normalize(rows: Array<Record<string, string>>): Array<Record<string, string>> {
    this.record("normalize");
    return rows.map((r) => {
      const out: Record<string, string> = {};
      for (const k of Object.keys(r)) out[k.trim().toLowerCase()] = r[k].trim();
      return out;
    });
  }

  protected validate(rows: Array<Record<string, string>>): void {
    this.record("validate");
    if (rows.length === 0) throw new ImportError("No rows");
  }

  protected persist(rows: Array<Record<string, string>>): ImportResult {
    this.record("persist");
    return { id: "import-1", rows: rows.length };
  }
}

class CsvImportJob extends ImportJob {
  protected load(input: string): string {
    this.record("load");
    return input;
  }

  protected parse(raw: string): Array<Record<string, string>> {
    this.record("parse");
    const [header, ...lines] = raw.split("\n");
    const keys = header.split(",");
    return lines.map((line) => {
      const values = line.split(",");
      return Object.fromEntries(keys.map((k, i) => [k, values[i] ?? ""]));
    });
  }
}

class PdfImportJob extends ImportJob {
  protected load(input: string): string {
    this.record("load");
    return `PDF:${input}`;
  }

  protected parse(raw: string): Array<Record<string, string>> {
    this.record("parse");
    if (!raw.startsWith("PDF:")) throw new ImportError("Invalid PDF");
    return [{ title: raw.replace("PDF:", "").trim() }];
  }
}

const csv = new CsvImportJob();
const result = csv.run("name,age\nAda,37");
console.log(result, csv.getTrace());

const pdf = new PdfImportJob();
const result2 = pdf.run("Report Title");
console.log(result2, pdf.getTrace());

const expected = ["load", "parse", "normalize", "validate", "persist"];
const trace = csv.getTrace().slice(0, expected.length);
if (trace.join("/") !== expected.join("/")) {
  throw new Error("Ordering mismatch");
}
```

## Example 2: Payment processing flow (Card/BankTransfer)

```ts
type Receipt = { id: string; amount: number; method: string };

type PaymentInput = { amount: number; account: string };

class PaymentError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "PaymentError";
  }
}

abstract class PaymentFlow {
  run(input: PaymentInput): Receipt {
    this.validate(input);
    this.beforeAuthorize(input);
    const authId = this.authorize(input);
    const receipt = this.capture(input, authId);
    this.afterCapture(receipt);
    return receipt;
  }

  protected validate(input: PaymentInput) {
    if (input.amount <= 0) throw new PaymentError("Invalid amount");
  }

  protected beforeAuthorize(_input: PaymentInput): void {}
  protected afterCapture(_receipt: Receipt): void {}

  protected abstract authorize(input: PaymentInput): string;
  protected abstract capture(input: PaymentInput, authId: string): Receipt;
}

class CardPayment extends PaymentFlow {
  protected authorize(input: PaymentInput): string {
    if (!input.account.startsWith("card_")) throw new PaymentError("Invalid card");
    return "auth-card-1";
  }

  protected capture(input: PaymentInput, authId: string): Receipt {
    return { id: authId, amount: input.amount, method: "card" };
  }
}

class BankTransferPayment extends PaymentFlow {
  protected authorize(input: PaymentInput): string {
    if (!input.account.startsWith("bank_")) throw new PaymentError("Invalid bank");
    return "auth-bank-1";
  }

  protected capture(input: PaymentInput, authId: string): Receipt {
    return { id: authId, amount: input.amount, method: "bank" };
  }
}

const card = new CardPayment();
try {
  card.run({ amount: 0, account: "card_123" });
} catch (e) {
  console.log((e as Error).message);
}

const bank = new BankTransferPayment();
console.log(bank.run({ amount: 50, account: "bank_abc" }));
```

## Example 3: Report generation (Summary/Detailed)

```ts
type Report = { name: string; content: string };

type RecordRow = { id: string; value: number };

abstract class ReportJob {
  run(rows: RecordRow[]): Report {
    const data = this.fetch(rows);
    const computed = this.compute(data);
    const formatted = this.format(computed);
    this.afterFormat(formatted);
    this.deliver(formatted);
    return formatted;
  }

  protected fetch(rows: RecordRow[]): RecordRow[] {
    return rows;
  }

  protected abstract compute(rows: RecordRow[]): RecordRow[];
  protected abstract format(rows: RecordRow[]): Report;

  protected afterFormat(_report: Report): void {}

  protected deliver(report: Report) {
    console.log("delivered", report.name);
  }
}

class SummaryReport extends ReportJob {
  protected compute(rows: RecordRow[]): RecordRow[] {
    const total = rows.reduce((sum, r) => sum + r.value, 0);
    return [{ id: "total", value: total }];
  }

  protected format(rows: RecordRow[]): Report {
    return { name: "summary", content: JSON.stringify(rows) };
  }
}

class DetailedReport extends ReportJob {
  protected compute(rows: RecordRow[]): RecordRow[] {
    return rows.filter((r) => r.value > 0);
  }

  protected format(rows: RecordRow[]): Report {
    return { name: "detailed", content: rows.map((r) => `${r.id}:${r.value}`).join("\n") };
  }

  protected afterFormat(report: Report): void {
    console.log("hook: formatted", report.name);
  }
}

const rows = [
  { id: "a", value: 1 },
  { id: "b", value: 0 },
];

const summary = new SummaryReport();
console.log(summary.run(rows));

const detailed = new DetailedReport();
console.log(detailed.run(rows));
```

## Disambiguation snippet

```ts
// Template Method vs Strategy: Template Method fixes the skeleton; Strategy swaps algorithms.
// Template Method vs State: Template Method varies steps; State varies behavior by lifecycle.
// Template Method vs Command: Template Method structures a workflow; Command encapsulates a request.
// Template Method vs shared util: Template Method enforces ordering and hooks.

type TemplateMethod = { run(input: unknown): unknown };

type Strategy = { execute(input: unknown): unknown };

type State = { handle(ctx: unknown): void };

type Command = { execute(): void };
```
