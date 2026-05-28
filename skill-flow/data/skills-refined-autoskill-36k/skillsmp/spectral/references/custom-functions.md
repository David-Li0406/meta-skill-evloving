# Spectral Custom Functions

## Basic Custom Function

```javascript
// functions/ensureNoSecrets.js
export default function(input, options, context) {
  const secretPatterns = [
    /api[_-]?key/i,
    /password/i,
    /secret/i,
    /token/i
  ];

  const results = [];

  for (const pattern of secretPatterns) {
    if (pattern.test(input)) {
      results.push({
        message: `Potential secret in value: "${input}"`
      });
    }
  }

  return results;
}
```

## Using in Ruleset

```yaml
# .spectral.yaml
extends: spectral:oas
functions:
  - ensureNoSecrets

rules:
  no-hardcoded-secrets:
    given: $.paths[*][*].parameters[*].example
    then:
      function: ensureNoSecrets
```

## Function Parameters

```javascript
// functions/maxLength.js
export default function(input, options, context) {
  const { max, min = 0 } = options;

  if (typeof input !== 'string') {
    return [];
  }

  const results = [];

  if (input.length > max) {
    results.push({
      message: `Length ${input.length} exceeds max of ${max}`
    });
  }

  if (input.length < min) {
    results.push({
      message: `Length ${input.length} is below min of ${min}`
    });
  }

  return results;
}
```

```yaml
rules:
  description-length:
    given: $.info.description
    then:
      function: maxLength
      functionOptions:
        max: 500
        min: 10
```

## Context Object

```javascript
export default function(input, options, context) {
  const {
    path,          // JSONPath to current location
    document,      // Full document
    documentInventory,  // All documents
    rule          // Current rule definition
  } = context;

  // Access the path
  console.log('Checking:', path.join('.'));

  // Access parent values
  const parentPath = path.slice(0, -1);

  return [];
}
```

## Async Functions

```javascript
// functions/validateExternalRef.js
export default async function(input, options, context) {
  if (!input.startsWith('http')) {
    return [];
  }

  try {
    const response = await fetch(input, { method: 'HEAD' });
    if (!response.ok) {
      return [{
        message: `External reference returns ${response.status}`
      }];
    }
  } catch (error) {
    return [{
      message: `Cannot reach external reference: ${error.message}`
    }];
  }

  return [];
}
```

## TypeScript Functions

```typescript
// functions/ensureVersion.ts
import type { IFunction, IFunctionResult } from '@stoplight/spectral-core';

interface Options {
  minVersion: string;
}

const ensureVersion: IFunction<string, Options> = (
  input,
  options
): IFunctionResult[] => {
  const { minVersion } = options;

  if (compareVersions(input, minVersion) < 0) {
    return [{
      message: `Version ${input} is below minimum ${minVersion}`
    }];
  }

  return [];
};

export default ensureVersion;
```

## Error Messages with Paths

```javascript
export default function(input, options, context) {
  const results = [];

  if (typeof input === 'object') {
    for (const [key, value] of Object.entries(input)) {
      if (isInvalid(value)) {
        results.push({
          message: `Invalid value for "${key}"`,
          path: [...context.path, key]  // Specific path
        });
      }
    }
  }

  return results;
}
```

## Bundling Functions

```yaml
# .spectral.yaml with local functions
extends: spectral:oas
functions:
  - ./functions/custom1
  - ./functions/custom2
functionsDir: ./spectral-functions
```

Or create an npm package:

```javascript
// spectral-my-functions/index.js
export { default as myFunction1 } from './myFunction1.js';
export { default as myFunction2 } from './myFunction2.js';
```
