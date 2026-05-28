---
name: lambdakit-ts
description: A TypeScript (TS) toolkit for bootstrapping AWS Lambda functions with production-ready best practices.
---

# LambdaKit TS

Bootstrap a new TypeScript AWS Lambda using the instructions below.

If the desired event source is not specified, create a Lambda with API Gateway as the event source.

Start with:

1. If a name is not specified, generate an interactive prompt and ask the user what `what should the lambda be called?`, and pre-populate it with the name of the current directory in kebab-case.
2. Before proceeding further, present the user with an interactive prompt: `The Lambda will be created at ${path}. Please confirm`
   Then give the user 2 options:
   - Yes — proceed with creating the Lambda at this path
   - Enter a directory name — a new subdirectory with this name will be created in the current directory
     If a new directory name is entered, use this value in kebab-case, and create the lambda in the new directory.
3. create package.json with `npm init -y`
4. install dev dependencies `npm install -D @types/aws-lambda @types/node esbuild typescript prettier eslint eslint-plugin-prettier eslint-plugin-check-file eslint-config-prettier @typescript-eslint/parser @typescript-eslint/eslint-plugin`
5. install runtime dependencies `npm install @aws-lambda-powertools/logger @middy/core`
6. run `mkdir -p src/functions src/interfaces` to create the directories
7. copy the provided `assets/tsconfig.json` file
8. copy the provided `assets/eslint.config.mjs` file
9. copy the provided `assets/index.ts` file and change the `serviceName` value according to the provided name or directory name
10. copy the provided `assets/local-invoke.ts` file and change the `functionName` value according to the provided name or directory name
11. copy the provided `assets/greet.ts` file and copy it to the `src/functions/` directory
12. copy the provided `build.sh` file and run `chmod + x` to assign execute permissions
13. copy the provided `.prettierrc` file
14. copy the provided `.gitignore` file
15. add scripts to `package.json` from the section `add package.json scripts` below
16. when done, add instructions to the output as per the `Final Instructions` section below

## Code Organization Principles

### add package.json scripts

add the following scripts in `package.json`:

```json
{
  "scripts": {
    "typecheck": "tsc --noEmit",
    "build": "bash build.sh",
    "invoke:local": "npx tsx src/local-invoke.ts",
    "prettier": "prettier --check '**/*.{ts,json}'",
    "prettier:fix": "prettier --write '**/*.{ts,json}'",
    "lint": "eslint . --ext .ts",
    "lint:fix": "eslint . --ext .ts --fix"
  }
}
```

### Final Instructions

- To build the project, run `npm run build`
- To autoformat using prettier, run `npm run prettier:fix`
- To autofix lint issues, run `npm run lint:fix`

## Best Practices

1. Use async/await syntax instead of promises
2. Use import statements instead of require where possible
3. Use aliased imports as defined in `tsconfig.json`
4. Use Middy middleware for cross-cutting concerns
5. Use AWS Lambda Powertools for structured logging
6. Always include proper error handling with appropriate logging
7. When creating other functions, pass the instance of the logger to those functions so that the context and properties can be persisted across logs
8. Use the Single Responsibility Principle (SRP) to rnsure good separation of concerns.
9. SRP: Ensure a single export per file
10. SRP: Always create separate files for functions and store functions in `src/functions`
11. SRP: Prefer interfaces over types and store interfaces in `src/interfaces`
