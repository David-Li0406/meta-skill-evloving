# Dependencies Guidelines

Not every library belongs in our codebase. We must be very selective about adding dependencies. This guide helps decide whether a package should be added as a dependency (and if so, which version and source).

## Guiding Principles for Adding Dependencies

- **Necessity**: First ask, do we truly need this dependency? Can the problem be solved with the standard library or existing code? Every dependency comes with cost (maintenance, bundle size, security).
- **Maintainability**: Is the package well-maintained? This is the highest priority factor:
  - Check the repository for recent activity (commits in the last few months, recent releases).
  - Look at open issues and PRs: are they addressed promptly or stagnating?
  - Many downloads/stars don’t always mean well-maintained, but it’s a clue. A critical project with a lone maintainer might be a risk if they step away.
  - If a project hasn’t had any update or communication in > 1 year, treat it as potentially abandoned – prefer alternatives.
- **Compatibility**: Does it work well with our frameworks/tools (React, Express/Node, Next.js, Vite)? Avoid packages that require awkward workarounds to integrate.
- **Unique Value**: Does this library provide something we cannot easily build ourselves or combine from smaller utilities? If it’s a thin wrapper or something trivial, better to implement in-house for control. If it provides a complex algorithm or significant functionality (e.g., a proven state management library), that might justify inclusion.
- **Bundle/Performance Impact**: For frontend projects especially, consider bundle size. Is the library small or tree-shakeable? If it’s large (like a whole UI framework) and we need just one function, maybe find a smaller alternative or copy the needed code with attribution.
- **License**: Ensure the license is compatible with our project (e.g., MIT, Apache are fine; avoid copyleft like GPL in proprietary projects).
- **Security**: Does the library have known vulnerabilities? Check advisories (`npm audit` can help). Also, does it handle data safely (e.g., an HTML sanitizer lib should be robust)? We prefer dependencies that are battle-tested for security in their domain.
- **TypeScript Support**: It must have good TypeScript types. Ideally written in TS, or provides official `.d.ts`. We should not add a lib that forces us to write a lot of custom typings or use `@types/*` that are incomplete.
- **Community & Documentation**: A library with good documentation and community adoption is easier for devs to learn and use correctly. If docs are lacking, adding the dependency might lead to misuse or bugs.
- **Long-Term Outlook**: Is the library's approach aligned with our long-term tech stack? Avoid trendy libraries that solve a very narrow problem or use unconventional patterns that might not be supported in future (unless that problem is crucial and no standard solution exists).

## Red Flags (When Not to Add)

- **Unmaintained**: No commits for > 6-12 months, many unanswered issues. (Exception: if the library is very stable/mature and needs no changes, but be cautious).
- **Single Maintainer Burnout**: Project depends on one person and they show signs of burnout or disinterest (issues piling up). Bus factor is low.
- **Low Usage / Niche**: If it’s obscure and not used widely, it could vanish or lack community knowledge for help.
- **Overly Complex**: The library does a lot more than we need (kitchen-sink) – introducing complexity and potential conflicts. E.g., pulling in a heavy framework just for one small utility.
- **Polyfills for Old JS**: Avoid adding dependencies that polyfill or support older JS environments we don’t target (since we always use latest environment with our bundlers).
- **Frequent Breaking Changes**: If release notes show the library often introduces breaking changes, that’s a maintenance burden on us (unless we pin a version, but then we might not get fixes).
- **Size vs Benefit Mismatch**: If a library is huge (say 500KB) and we only need a 5KB function from it, that’s a bad trade-off especially for frontend. Maybe extract or find a smaller alternative.
- **Proprietary or No License**: If license is unclear or problematic, definitely no-go.
- **Security History**: A library with a history of multiple vulnerabilities (especially if unmaintained now) – avoid. E.g., some abandoned npm packages might have known vulns with no fixes.

## Green Flags (When to Consider Adding)

- The library is industry-standard for the problem (e.g., Zod for schema validation is widely adopted and maintained[13], or React Query for data fetching).
- It significantly reduces our development time/complexity for a feature, more than offsetting the cost of added dependency.
- The maintainers are trustworthy (e.g., library is by a reputable organization or author, or part of a known toolkit like The Guild’s libraries or Vercel’s Next.js ecosystem).
- It integrates directly with our stack with minimal fuss (e.g., an official plugin for a tool we use).
- The library has excellent documentation and type definitions, meaning we can use it with confidence and onboard new devs to it easily.
- The library is modular or tree-shakeable, so we can include just what we need.
- We’ve evaluated alternatives (including in-house) and this clearly stands out as the best option.

## Process for Introducing a New Dependency

- **Research & Prototype**: Before adding, do a quick spike. Include the library in a sandbox or branch, try using it for our use case. Ensure it works as expected.
- **Review by Peers**: Open a discussion or RFC. Describe why the dependency is needed, what alternatives were considered, maintenance stats (e.g., “Library X last release 1 month ago, ~100k weekly downloads, MIT licensed”), and impact (bundle size if front-end).
- **Version Selection**: We always install the latest stable version (pin exact version in `package.json` to avoid surprise upgrades). No alpha/beta versions for production code unless absolutely necessary.
- **Check for Tree Shaking**: If front-end, verify that unused parts of the library are not bundled. Sometimes this means using import paths to specific submodules.
- **Add Documentation**: Update our internal docs (maybe in a `packages-always-use.md` or relevant section) that we use this library for X purpose, so future devs don’t add a different library for the same purpose.
- **Monitor**: After adding, keep an eye on the library’s releases. Subscribe to notifications or dependabot alerts. If a breaking change is coming, plan the upgrade, or if maintainers disappear, start looking for alternatives proactively.

## Upgrading and Removing Dependencies

- **Stay Updated**: We update dependencies regularly (via `pnpm update` or dependabot PRs). Minor/patch updates should be applied unless there’s known issues. Major updates require planning and testing.
- **Deprecation**: If maintainers deprecate the library or project direction shifts incompatibly, plan to migrate off. It’s better to remove early than be stuck with abandonware.
- **Replacing**: If a better solution emerges (e.g., a new standard in the community), evaluate if switching is worth it. Consider the cost of migration vs benefits.
- **Removing Unused**: Periodically audit for dependencies that are no longer used. Remove them to reduce bloat (both in bundle and cognitive load in `package.json`).

In summary, treat adding a dependency as a last resort when the benefits strongly outweigh the costs. If added, treat that external code as part of our codebase in terms of diligence: we must understand how to use it, keep it updated, and have a fallback plan if it falters. By being strict with this process, we ensure our projects remain lean, secure, and maintainable.
