---
name: docstring-standards
description: Use this skill when documenting code in JavaScript or TypeScript, following the appropriate conventions for each language.
---

# Skill body

## Overview
This skill provides guidelines for writing documentation comments in JavaScript and TypeScript using JSDoc and TSDoc standards, respectively.

## When to Use
- **JavaScript**: Use JSDoc for documenting functions, classes, and modules, and for generating API documentation.
- **TypeScript**: Use TSDoc for documenting functions, classes, interfaces, and types, and for generating documentation with TypeDoc.

## When Not to Use
- Do not use for TypeScript code if you are documenting JavaScript (use `js-docstring`).
- Do not use for JavaScript code if you are documenting TypeScript (use `ts-docstring`).
- Avoid using for runtime logic that does not require documentation.

## Steps for Writing Documentation

### For JavaScript (JSDoc)
1. Start with a comment block using `/**` to begin.
2. Use `@param` to describe function parameters.
3. Use `@returns` to describe the return value.
4. Include `@example` for usage examples if applicable.
5. Close the comment block with `*/`.

### For TypeScript (TSDoc)
1. Begin with a comment block using `/**`.
2. Use `@param` for parameters, similar to JSDoc.
3. Use `@returns` for the return type.
4. Include `@example` for examples.
5. Close the comment block with `*/`.

## Additional Resources
- [JSDoc Documentation](https://jsdoc.app/)
- [TSDoc Documentation](https://tsdoc.org/)