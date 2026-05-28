---
title: Never Use eval() or new Function()
impact: HIGH
impactDescription: Prevents code injection attacks and improves performance
tags: security, eval, injection, function
---

## Never Use eval() or new Function()

eval() and new Function() execute strings as code, enabling code injection attacks. They also prevent JavaScript engine optimizations.

**Incorrect (code injection vulnerability):**

```javascript
// User can inject malicious code
const userFormula = getUserInput(); // "1+1; stealData()"
const result = eval(userFormula); // Executes stealData()

// Dynamic property access with eval
const propName = getUserInput();
const value = eval(`obj.${propName}`); // Injection risk

// new Function has same risks
const fn = new Function('x', userCode);
```

**Correct (safe alternatives):**

```javascript
// For math expressions, use a safe parser
import { evaluate } from 'mathjs';
const result = evaluate(userFormula); // Safe math evaluation

// For dynamic property access, use bracket notation
const propName = getUserInput();
const value = obj[propName]; // Safe property access

// For JSON parsing
const data = JSON.parse(jsonString); // Safe JSON parsing

// For dynamic function selection
const handlers = {
  add: (a, b) => a + b,
  multiply: (a, b) => a * b
};
const result = handlers[operation]?.(x, y);
```

If you think you need eval(), you almost certainly don't. Use data-driven approaches instead.

Reference: [MDN eval() Security](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/eval#never_use_eval!)
