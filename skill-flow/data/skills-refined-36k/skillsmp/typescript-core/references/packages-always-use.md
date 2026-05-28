# Packages – Always Use (Our Standard Toolkit)

Some packages have proven their value across many projects and are effectively part of our “standard library.” We include these by default in new projects (ensuring latest versions) and encourage their use.

## 1. Effect (Functional Effect System)

We always use **Effect** for managing async and concurrent operations, instead of raw `Promise` or miscellaneous utility libs. Effect provides a comprehensive framework for:

- Concurrency (fiber-based) with high scalability[14].
- Typed effects that encode failure modes (no more unhandled promise rejections).
- Resource management (safely acquire/release resources).
- Great dev experience (structured logs, traces of computations).

All asynchronous business logic or complex sync logic should be done with Effect where possible. This yields more predictable, testable code.

**Why always**: Effect reduces the need for other libraries like Redux-saga, async utils, or task runners – one tool covers it all with better type safety[15]. It integrates with Node (see `@effect/platform` for FS, etc.) and with front-end (though primarily our use is backend/CLI).

👉 Use `effect-getting-started.md` for a quickstart, and refer to `effect-full-docs.md` for advanced usage. We keep these docs handy as Effect’s API is rich.

## 2. Zod (Schema Validation)

We use **Zod** everywhere for schema validation and type-safe parsing of external data:

- Validating inputs to APIs (e.g. request bodies, query params).
- Validating responses from external APIs or config files.
- Enforcing types at boundaries (e.g., parsing environment variables into correct types).

Zod v4 is fast and powerful, providing features like super refining, pipeline, and native coercion (e.g., transform strings to numbers)[16][17]. It’s our go-to instead of custom validation logic or legacy libraries like Joi or Yup.

We always install the latest Zod 4.x – it’s actively maintained by Colinhacks and community. Major improvements in v4 (performance 10x+ faster than v3[18], better error messages, smaller bundle via `zod-mini`[19]) mean we should stay up-to-date.

**Integration**: Zod works seamlessly with:

- React (for form validation, often with React Hook Form – we use RHF’s `zodResolver`).
- Express/Next API: parse `req.body` or `req.query` with zod schemas and immediately get typed data or throw a 400 with helpful message.
- Effect: can integrate via `Effect.tryCatch` to wrap Zod parsing in an Effect, or using Effect’s own `Schema` if needed (Effect’s Schema is Zod-like; our preference is Zod since we’re familiar).

## 3. TypeScript Target & Tools (Latest Always)

We always use the latest stable TypeScript. At time of writing (2026), that’s TS 5.x. This ensures we have modern syntax and features:

- We enable all strict flags as per `strict-configuration.md`.
- Use `tsdown` to bundle libraries/CLIs (discussed below).
- `pnpm` as our package manager – always updated to latest stable (pnpm has frequent improvements; e.g., better workspace handling).
- ESLint & Prettier latest versions with our strict config.

Essentially, our baseline stack (TypeScript + build tool + linter) is a “must use” set. It’s not optional to turn off strict mode or to not format code, etc.

## 4. LogTape (Structured Logging)

For logging, we always include **LogTape**. It gives us structured logging with pluggable sinks:

- Use `@logtape/pretty` in development for human-friendly colored logs.
- Use core `@logtape/logtape` with JSON output (or NDJSON) for production (so logs can be parsed by systems).
- Redaction and sensitive info handling via `@logtape/redaction` (prevents secrets from leaking in logs by pattern or field[20][21]).
- Integration with frameworks: `@logtape/express` to automatically log HTTP requests (with method, path, response time, etc.) and attach a request ID.
- Error reporting: `@logtape/sentry` to send error logs to Sentry seamlessly.
- Additional outputs: `@logtape/file` if we need to log to files, `@logtape/syslog` for server syslog integration.

We consider LogTape essential because it standardizes logging across projects – same JSON structure, same approach to context (categories, severity). It’s better than `console.log` or `winston` because of zero-config in libraries (if library code uses LogTape and no logger is configured by app, it outputs nothing – so libs don’t spam logs unless enabled by app)[22][23].

All new projects include a basic LogTape setup:

```ts
import { getLogger } from '@logtape/logtape';
import { pretty } from '@logtape/pretty';
const logger = getLogger(['my-app']);
if (process.env.NODE_ENV !== 'production') {
  logger.addSink(pretty());  // human-readable logs in dev
}
export { logger };
```

And then use `logger.info({userId}, 'User login')`, etc., throughout.

## 5. True Myth (Option/Result types)

We include **True Myth** to handle null/undefined and error results in a functional style:

- Use `Maybe` for optional values instead of `null`. E.g., a function that might not find a user returns `Maybe<User>` (`Just(user)` or `Nothing`) instead of `User | undefined`.
- Use `Result` for operations that can fail with an error. E.g., `Result<ParsedData, ParseError>` rather than throwing. True Myth’s `Result` is similar to `neverthrow`, and we prefer it to exceptions for many situations.
- True Myth’s API (with methods like `.map`, `.andThen`, `.unwrapOr`) helps avoid a lot of `if`-checks. It also makes intent clear – if I see a function returns `Result`, I know I must handle both `Ok` and `Err`.

Even though Effect also provides `Option` and `Either`, True Myth is lightweight and can be used in places where we might not use the full Effect runtime. For example, in React components or simple synchronous functions, True Myth is handy for avoiding null checks (which our linter would warn about if not handled).

We particularly like True Myth for its safety (no more forgetting a null check) and its integration with TS (the `Result.match` or using `.toJSON()` for debug). It’s well-maintained and simple.

Thus, we often have:

```ts
import Maybe from 'true-myth/maybe';
import Result from 'true-myth/result';
```

and use `Maybe.just(x)`/`Maybe.nothing()` and `Result.ok(x)`/`Result.err(e)` instead of raw `null` or throwing. This prevents “Cannot read property of undefined” errors and keeps our functions total (always returning something of the declared type).

**Note**: In an Effect-heavy codebase, we sometimes convert True Myth <-> Effect (Effect’s `Effect.option`, `Effect.either` can wrap/unwrap these). They complement each other.

## 6. Oclif (for CLIs) and Related Tools

When building a CLI application, our default choice is **Oclif** (by Salesforce). It provides a robust framework for multi-command CLI tools with minimal setup:

- Generators for a new CLI (`pnpm create oclif`).
- Handles parsing arguments, generating help text, and plugin architecture.
- We always use it with TypeScript (Oclif supports TS out of the box).

Alongside Oclif, a set of companion libraries are part of our standard CLI toolkit:

- **Ink**: For rich interactive CLI output using React-like components (use when building TUI elements beyond basic `console.log`). For example, render a dynamic UI with Ink’s `<Text>`, `<Box>` and even use hooks like `useInput`. It makes complex CLI UIs easier to manage.
- **Inquirer**: For simpler CLI prompts (Y/N, select from list, ask for input). Oclif doesn’t provide prompt out of the box, so Inquirer is our go-to for quick questionnaires.
- **Ora**: For spinners in CLI feedback. Use `ora()` to show a spinner during long operations (though Ink has components like `ink-spinner`[24]; we can use either).
- **cli-progress**: For progress bars in the console (e.g., showing download progress). It's well-maintained and flexible (support multiple bars, etc.).

We include these by default in CLI projects because almost every non-trivial CLI needs to prompt the user or show progress. Rather than custom-hacking a spinner or prompt, we use these reliable packages.

They play well together: e.g., Oclif command can use Inquirer to ask user something, then use Ora spinner while doing an Effect-based async task, then perhaps use Ink to render a fancy summary table.

All these are actively maintained:

- Ink v6 is latest (by Vadim Demedes) – lots of community contributions, works with React 18.
- Inquirer v9+ – still standard for node prompts.
- Ora – simple, and if needed we can swap it, but it’s fine.
- cli-progress – solid for progress.

## 7. Testing Libraries (Vitest & RTL)

We consider our testing stack as required dependencies:

- **Vitest** as test runner, with `@vitest/ui` sometimes for UI runner.
- **`@testing-library/react`** and **`@testing-library/dom`** for component testing.
- **`msw`** (Mock Service Worker) for API mocking in tests.

These are `devDependencies`, but they are part of every project’s setup. Always use the latest versions (we keep an eye on `testing-library` updates, etc.).

Vitest is chosen over Jest now because it’s faster with Vite and handles ESM well, plus we can share config with Vite easily. It’s very similar API to Jest, so easy adoption.

We also include types like `@types/jest` or rather use Vitest’s global types so that `describe`/`it`/`expect` are recognized.

## 8. Utility Libraries

Some utility libraries are broadly useful enough that we include them unless there’s a reason not to:

- **lodash** (selective): We avoid full lodash to keep bundles small, but sometimes we use `lodash-es` or specific lodash functions (via cherry-pick import) for things not easily done otherwise (deep clone, etc.). However, with utility alternatives (like `es-toolkit`, see utilities doc), lodash may eventually be replaced. If used, ensure tree-shaking or use `import cloneDeep from 'lodash/cloneDeep'` style.
- **date-fns**: For date/time manipulation we prefer `date-fns` (v3) because it’s tree-shakeable and pure. If a project deals with a lot of dates, `date-fns` is brought in (unless Luxon or Temporal API suffice, but Temporal is not finalized as of 2026).
- **axios**: We actually often avoid `axios` now in favor of `fetch` (especially in Node 18+ which has `fetch` built-in). But for some projects that require advanced HTTP features or a different API, `axios` is okay. Given `fetch` is standard, `axios` is not an “always include” – more optional. So perhaps not in this list strictly.
- **node-fetch** (for Node <18): If we need `fetch` in Node versions that didn’t have it, but since we’re on latest Node LTS, built-in `fetch` covers it.

In summary, our “Always Use” package set includes the ones above. When bootstrapping a new project, you’ll typically see these in the `package.json` from the start. They form a stable foundation that we know, trust, and have documentation for internally.

By consistently using this toolkit, we reduce the learning curve for new team members (they'll see familiar patterns across projects) and ensure high quality (these libraries have been vetted thoroughly).
