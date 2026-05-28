# Detector File Templates

Replace `{kind}` with lowercase name (e.g., "autocomplete") and `{Kind}` with PascalCase (e.g., "Autocomplete").

## types.ts

```typescript
import type { GatheredNode } from "../../types";

/**
 * Meta fields for {kind} components.
 */
export interface {Kind}Meta {
  /**
   * Selector for {description}.
   * State: {how to check state}
   */
  fieldName: string;
}

/**
 * A detected {kind} node with typed meta.
 */
export interface {Kind}Node extends GatheredNode {
  kind: "{kind}";
  meta: {Kind}Meta;
}
```

## validate.ts

```typescript
import type { CheerioAPI } from "cheerio";
import type { Element } from "domhandler";

/**
 * Strict validation of {kind} structure.
 * Returns true only if ALL structural checks pass.
 */
export function validate(el: Element, $: CheerioAPI): boolean {
  const $el = $(el);

  // 1. Check root element tag
  if (el.tagName !== "expectedTag") {
    return false;
  }

  // 2. Check identifying attributes (data-testid, class, etc.)
  if ($el.attr("data-testid") !== "expected-testid") {
    return false;
  }

  // 3. Check required class
  const className = $el.attr("class") || "";
  if (!className.includes("Mui{Component}-root")) {
    return false;
  }

  // 4. Validate nested structure exists
  const nestedElement = $el.find(".expected-selector");
  if (nestedElement.length !== 1) {
    return false;
  }

  // 5. Check unique identifier exists
  const fieldName = nestedElement.attr("name");
  if (!fieldName || fieldName.trim() === "") {
    return false;
  }

  return true;
}
```

## detector.ts

```typescript
import type { CheerioAPI } from "cheerio";
import type { Element } from "domhandler";
import type { DetectionResult, Detector } from "../../types";
import type { {Kind}Meta } from "./types";
import { validate } from "./validate";

export const {kind}Detector: Detector = {
  name: "{kind}",

  detect(el: Element, $: CheerioAPI): DetectionResult | null {
    if (!validate(el, $)) {
      return null;
    }

    // Extract data (validation confirmed structure exists)
    const $el = $(el);
    const nestedElement = $el.find(".expected-selector");
    const fieldName = nestedElement.attr("name") as string;

    const meta: {Kind}Meta = {
      fieldName: `selector[name="${fieldName}"]`,
    };

    return {
      node: {
        type: "field",
        kind: "{kind}",
        path: `rootSelector:has(selector[name="${fieldName}"])`,
        meta,
      },
      childContainers: [],
    };
  },
};
```

## index.ts

```typescript
export { {kind}Detector } from "./detector";
export type { {Kind}Meta, {Kind}Node } from "./types";
```

## doc.md

```markdown
# {Kind} Detector

Detects MUI {Kind} components.

## Example HTML

```html
<!-- Paste real HTML sample here -->
```

## Output

```json
{
  "type": "field",
  "kind": "{kind}",
  "path": "selector...",
  "meta": {
    "fieldName": "selector..."
  }
}
```

## Meta Fields

| Field | Type | Description |
|-------|------|-------------|
| `fieldName` | string | Selector for ... (relative to `path`) |

## Value Handling

- **Read**: {Exact instructions for reading state}
- **Write**: {Exact instructions for changing state}

### State examples (if applicable)

#### ON/Selected state
```html
<!-- HTML showing active state -->
```

#### OFF/Unselected state
```html
<!-- HTML showing inactive state -->
```
```

## test file (tests/detectors/{kind}.test.ts)

```typescript
import { describe, expect, it } from "vitest";
import { {kind}Detector } from "../../src/detectors/{kind}";
import type { {Kind}Meta } from "../../src/detectors/{kind}";
import { createContext } from "../helpers";

const VALID_{KIND} = `<!-- paste valid HTML -->`;

const INVALID_WRONG_TAG = `<!-- paste invalid HTML -->`;

describe("{kind} detector", () => {
  describe("valid detection", () => {
    it("detects valid {kind} and extracts data", () => {
      const { el, $ } = createContext(VALID_{KIND});
      const result = {kind}Detector.detect(el, $);

      const expectedMeta: {Kind}Meta = {
        fieldName: 'expected-selector',
      };

      expect(result).toEqual({
        node: {
          type: "field",
          kind: "{kind}",
          path: "expected-path-selector",
          meta: expectedMeta,
        },
        childContainers: [],
      });
    });
  });

  describe("strict validation rejects invalid structures", () => {
    it("rejects wrong tag", () => {
      const { el, $ } = createContext(INVALID_WRONG_TAG);
      expect({kind}Detector.detect(el, $)).toBeNull();
    });

    // Add more rejection tests...
  });
});
```

## Registering in src/detectors/index.ts

Add these lines:

```typescript
import { {kind}Detector } from "./{kind}";

export const detectors: Detector[] = [toggleDetector, {kind}Detector];

export type { {Kind}Meta, {Kind}Node } from "./{kind}";
```
