# Detector Templates

Use these templates as starting points and adjust to match the HTML and existing detector patterns.

## Folder Structure

```
src/detectors/{kind}/
├── detector.ts
├── validate.ts
├── types.ts
├── index.ts
└── doc/
    ├── about.md
    ├── html.md
    ├── output.md
    └── usage.md
```

## types.ts

```typescript
import type { GatheredNode } from "../../types";

/**
 * Meta fields for {kind} components.
 */
export interface {Kind}Meta {
  /**
   * Selector for {description} (relative to path).
   * State: {how to check state}
   */
  fieldName: string;
}

/**
 * A detected {kind} node with typed meta.
 */
export interface {Kind}Node extends GatheredNode<{Kind}Meta> {
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

  // 1. Must be a <tag> element
  if (el.tagName !== "tag") {
    return false;
  }

  // 2. Must have required class/testid
  const className = $el.attr("class") || "";
  if (!className.includes("MuiComponent-root")) {
    return false;
  }

  // 3. Must contain required child elements
  const requiredChild = $el.find(".required-selector");
  if (requiredChild.length !== 1) {
    return false;
  }

  // 4. Must include unique identifier
  const fieldName = requiredChild.attr("name");
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

    const $el = $(el);
    const uniqueElement = $el.find(".required-selector");
    const fieldName = uniqueElement.attr("name") as string;

    const meta: {Kind}Meta = {
      fieldName: `input[name="${fieldName}"]`,
    };

    return {
      node: {
        type: "field",
        kind: "{kind}",
        path: `[data-testid="{kind}"]:has(input[name="${fieldName}"])`,
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

## doc/about.md

```markdown
# {Kind} Detector

Detects {Kind} components.

## Documentation

- [Output Schema](./output.md) - JSON structure and field descriptions
- [Playright Usage](./usage.md) - Locator snippets
- [HTML Example](./html.md) - Sample HTML that this detector recognizes
```

## doc/html.md

```markdown
# Example HTML

```html
<!-- Paste real HTML sample here -->
```
```

## doc/output.md

```markdown
# Output

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
```

## doc/usage.md

```markdown
# Playright Usage

```typescript
// HOW TO LOCATE
const container = stage.locateBy('{path}'); // from page
const container = element.locateBy('{path}'); // from parent element

// HOW TO ASSERT VALUE
// TODO: fill with real assertions

// HOW TO SET VALUE
// TODO: fill with real actions
```
```

## tests/detectors/{kind}.test.ts

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
        fieldName: "expected-selector",
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
  });
});
```
