# Project and versions

Read this file before running the shadcn CLI.

## UI project location

- Target app: `apps/web`
- UI components: `apps/web/src/components/ui`
- Global styles: `apps/web/src/index.css`

## shadcn configuration (components.json)

- `style`: `base-lyra`
- `rsc`: `false`
- `tsx`: `true`
- `tailwind.css`: `src/index.css`
- `tailwind.baseColor`: `neutral`
- `tailwind.cssVariables`: `true`
- `tailwind.prefix`: `""`
- `iconLibrary`: `lucide`
- Aliases:
  - `components`: `@/components`
  - `utils`: `@/lib/utils`
  - `ui`: `@/components/ui`
  - `lib`: `@/lib`
  - `hooks`: `@/hooks`

## Registries

- Configured registries: `@shadcn`
- Add custom registries in `components.json` under `registries` if needed.

## Relevant versions (apps/web/package.json)

- `shadcn`: `^3.6.2`
- `next`: `^16.1.1`
- `react`: `^19.2.3`
- `react-dom`: `^19.2.3`
- `tailwindcss`: `^4.1.10`
- `lucide-react`: `^0.562.0`
- `class-variance-authority`: `^0.7.1`
- `tailwind-merge`: `^3.3.1`
- `tw-animate-css`: `^1.3.4`

## CLI execution

Always run from `apps/web` to use the correct `components.json`:

```
cd /home/ermian/workspace/fobos/apps/web
bun x shadcn add <component>
```

If versions change, update this file and re-check `components.json`.
