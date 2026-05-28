# Phase 4: Root Cause Analysis with CoD^Σ

**Purpose**: Identify root cause using targeted file reads and complete CoD^Σ trace with file:line evidence.

---

## Targeted Read 1: Error Location

Read ONLY the lines identified by intel queries (from Phase 3):

```bash
sed -n '62,75p' src/pricing/calculator.ts
```

**Code:**
```typescript
// Line 62
export function calculateTotal(cart: Cart, discountCode?: string): number {
  const subtotal = cart.items.reduce((sum, item) => sum + item.price * item.quantity, 0)

  // Line 67 - ERROR LINE
  const discountAmount = discountCode
    ? getDiscount(discountCode).discount * subtotal  // ← BUG: no null check
    : 0

  const total = subtotal - discountAmount
  return formatPrice(total)
}
```

**Analysis**: Line 67 calls `getDiscount(discountCode).discount` without checking if getDiscount returns undefined.

---

## Targeted Read 2: Dependency Function

Read the suspicious dependency identified in Phase 3:

```bash
sed -n '12,25p' src/pricing/discountService.ts
```

**Code:**
```typescript
// Line 12
export function getDiscount(code: string): Discount | undefined {
  const discount = discounts.find(d => d.code === code && d.active)
  return discount  // ← Returns undefined when code not found
}
```

**Analysis**: getDiscount explicitly returns `Discount | undefined` - when no matching discount is found, it returns undefined.

---

## Complete CoD^Σ Trace

**Claim:** Error occurs because calculateTotal doesn't handle undefined from getDiscount

**Evidence Chain:**

```
Step 1: → ParseError
  ↳ Source: Error log
  ↳ Data: TypeError at src/pricing/calculator.ts:67

Step 2: ⇄ IntelQuery("locate calculateTotal")
  ↳ Query: project-intel.mjs --search "calculateTotal"
  ↳ Data: Found in src/pricing/calculator.ts at line 62

Step 3: ⇄ IntelQuery("analyze symbols")
  ↳ Query: project-intel.mjs --symbols calculator.ts
  ↳ Data: calculateTotal at line 62, error at line 67 (5 lines in)

Step 4: → TargetedRead(lines 62-75)
  ↳ Source: sed -n '62,75p' calculator.ts
  ↳ Data: Line 67 calls getDiscount(code).discount without null check

Step 5: ⇄ IntelQuery("check getDiscount")
  ↳ Query: project-intel.mjs --symbols discountService.ts
  ↳ Data: getDiscount returns Discount | undefined

Step 6: → TargetedRead(getDiscount function)
  ↳ Source: sed -n '12,25p' discountService.ts
  ↳ Data: Returns undefined when code not found/inactive

Step 7: ⊕ MCPVerify("TypeScript best practices")
  ↳ Tool: Ref MCP
  ↳ Query: "TypeScript optional chaining undefined handling"
  ↳ Data: Use ?. operator for potentially undefined values

Step 8: ∘ Conclusion
  ↳ Logic: getDiscount returns undefined → accessing .discount throws TypeError
  ↳ Root Cause: src/pricing/calculator.ts:67 - missing null check
  ↳ Fix: Use optional chaining: getDiscount(code)?.discount ?? 0
```

---

## Token Efficiency Analysis

Compare token usage:

| Approach | Token Count | Details |
|----------|-------------|---------|
| **Reading full files** | ~8600 tokens | Read calculator.ts (4200) + discountService.ts (3100) + related files |
| **Intel + targeted reads** | ~750 tokens | 4 intel queries (350) + 2 targeted reads (400) |
| **Savings** | **91%** | Intelligence-first saves ~7850 tokens |

**Why This Matters:**
- More tokens available for reasoning
- Faster analysis (less reading time)
- More context for MCP queries

---

## Enforcement Checklist

Before proceeding to Phase 5, verify:

- [ ] Root cause identified with specific file:line
- [ ] Complete CoD^Σ trace documented with all 8 steps
- [ ] MCP verification performed for best practices
- [ ] Fix approach validated with evidence
- [ ] Token efficiency analysis included

**Next Step**: Proceed to Phase 5 (Bug Report Generation) using template.
