# Adapter Examples (TypeScript)

## Example 1: Object adapter wrapping a mismatched client

```ts
// Internal port
interface PaymentsPort {
  charge(amountCents: number, currency: "USD" | "EUR", sourceId: string): Promise<{ id: string; status: "ok" | "failed" }>;
}

// External SDK types
class PaymentSdkClient {
  async createCharge(input: { amount: number; currency_code: string; source: string }): Promise<{ charge_id: string; status: string }> {
    return { charge_id: "ch_123", status: "succeeded" };
  }
}

class PaymentsAdapter implements PaymentsPort {
  constructor(private readonly sdk: PaymentSdkClient) {}

  async charge(amountCents: number, currency: "USD" | "EUR", sourceId: string) {
    const result = await this.sdk.createCharge({
      amount: amountCents,
      currency_code: currency,
      source: sourceId,
    });
    return {
      id: result.charge_id,
      status: result.status === "succeeded" ? "ok" : "failed",
    };
  }
}

const payments: PaymentsPort = new PaymentsAdapter(new PaymentSdkClient());
payments.charge(500, "USD", "card_1").then(console.log);
```

## Example 2: Error translation with Result type

```ts
type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };

type ChargeError = "DECLINED" | "UPSTREAM";

class PaymentSdkError extends Error {
  constructor(public readonly code: string, message: string) {
    super(message);
  }
}

class PaymentSdkClient {
  async createCharge(): Promise<{ charge_id: string }> {
    throw new PaymentSdkError("CARD_DECLINED", "declined");
  }
}

async function chargeWithResult(sdk: PaymentSdkClient): Promise<Result<string, ChargeError>> {
  try {
    const res = await sdk.createCharge();
    return { ok: true, value: res.charge_id };
  } catch (err) {
    const e = err as PaymentSdkError;
    if (e.code === "CARD_DECLINED") return { ok: false, error: "DECLINED" };
    return { ok: false, error: "UPSTREAM" };
  }
}

chargeWithResult(new PaymentSdkClient()).then(console.log);
```

## Example 3: Callback API adapted to Promise API

```ts
type Callback<T> = (err: Error | null, value?: T) => void;

class LegacyCache {
  get(key: string, cb: Callback<string | null>): void {
    cb(null, key === "a" ? "1" : null);
  }
}

interface CachePort {
  get(key: string): Promise<string | null>;
}

class CacheAdapter implements CachePort {
  constructor(private readonly legacy: LegacyCache) {}

  get(key: string): Promise<string | null> {
    return new Promise((resolve, reject) => {
      this.legacy.get(key, (err, value) => {
        if (err) return reject(err);
        resolve(value ?? null);
      });
    });
  }
}

const cache: CachePort = new CacheAdapter(new LegacyCache());
cache.get("a").then(console.log);
```

## Pure mapping functions + unit-test style usage

```ts
const mapUser = (sdkUser: { user_id: string; email_address: string }) => ({
  id: sdkUser.user_id,
  email: sdkUser.email_address,
});

function assertEqual(a: unknown, b: unknown): void {
  const pass = JSON.stringify(a) === JSON.stringify(b);
  if (!pass) throw new Error(`assertEqual failed: ${JSON.stringify(a)} != ${JSON.stringify(b)}`);
}

assertEqual(mapUser({ user_id: "u1", email_address: "a@b.com" }), { id: "u1", email: "a@b.com" });
```
