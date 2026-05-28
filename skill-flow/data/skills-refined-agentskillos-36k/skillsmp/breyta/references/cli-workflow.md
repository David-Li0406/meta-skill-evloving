# CLI workflow
This workflow splits into authoring (draft) and live operations.

## Authoring a flow (draft)
1) List flows
2) Pull a flow to a `.clj` file
3) Edit the file
4) Push a new draft version
5) Run draft with draft bindings

Core commands:
- `breyta flows list`
- `breyta flows pull <slug> --out ./tmp/flows/<slug>.clj`
- `breyta flows push --file ./tmp/flows/<slug>.clj`
- `breyta flows validate <slug>`
- `breyta flows compile <slug>`
- `breyta flows draft bindings template <slug> --out draft.edn`
- `breyta flows draft bindings apply <slug> @draft.edn`
- `breyta flows draft bindings show <slug>`
- `breyta flows draft run <slug> --input '{"n":41}' --wait`

Notes:
- Draft runs use draft bindings and the draft flow definition.
- `flows push` updates the draft; `flows deploy` publishes a version for prod.
- For long-running external jobs, prefer `flow/poll` to avoid manual wait loops.

## Fast loop: iterate per step
When authoring flows with an agent, prefer tight feedback loops:
1) Add or change exactly one `flow/step`
2) Run that step in isolation (API mode, no flow deploy needed):
   - `breyta steps run --type <type> --id <id> --params '<json-object>'`
   - Optionally record the observed output as sidecars (requires `--flow`):
     - `breyta steps record --flow <flow-slug> --type <type> --id <id> --params '<json-object>' --note '...' --test-name '...'`
     - (or) `breyta steps run --flow <flow-slug> --type <type> --id <id> --params '<json-object>' --record-example --record-test --record-note '...' --record-test-name '...'`
3) Store sidecars for the step (updatable without publishing a new flow version):
   - Docs: `breyta steps docs set <flow-slug> <step-id> --markdown '...'`
   - Examples: `breyta steps examples add <flow-slug> <step-id> --input '<json>' --output '<json>' --note '...'`
   - Tests (as documentation, runnable on demand): `breyta steps tests add <flow-slug> <step-id> --type <type> --name '...' --input '<json>' --expected '<json>'`
4) Inspect step context quickly: `breyta steps show <flow-slug> <step-id>` (prints a short "Next actions" helper to stderr in interactive terminals)
5) Verify stored tests: `breyta steps tests verify <flow-slug> <step-id> --type <type>`
6) Push + validate/compile, then run the draft flow end-to-end

### Templates during authoring
When iterating on draft bindings, templates reflect what is already bound:
- `breyta flows draft bindings template <slug> --out draft.edn`
- Add `--clean` to emit a requirements-only template without existing bindings.

Use the non-clean template when you want to tweak current bindings; use `--clean` for a fresh, shareable template.

## After deploy (live)
1) Deploy the draft (publish a version)
2) Apply prod bindings + activation inputs
3) Activate the prod profile (enable and pin a version)
4) Start runs or rely on triggers

Core commands:
- `breyta flows deploy <slug>`
- `breyta flows bindings template <slug> --out profile.edn`
- `breyta flows bindings apply <slug> @profile.edn`
- `breyta flows bindings apply <slug> --from-draft`
- `breyta flows bindings show <slug>`
- `breyta flows activate <slug> --version latest`
- `breyta runs start --flow <slug> --input '{"n":41}' --wait`
- `breyta runs cancel <workflow-id> --reason "..."` (use `--force` to terminate)

## End-user flows (installations)
End-user-facing flows are marked with the `:end-user` tag.

An installation is a per-user instance of the flow, backed by a prod profile (you can have multiple installations per flow).

Core commands:
- `breyta flows installations create <flow-slug> --name "My installation"`
- `breyta flows installations set-inputs <profile-id> --input '{"region":"EU"}'`
- `breyta flows installations enable <profile-id>` / `breyta flows installations disable <profile-id>`
- `breyta runs start --flow <flow-slug> --profile-id <profile-id> --input '{"x":1}' --wait`

Docs shortcuts:
- `breyta docs`
- `breyta docs flows`
- `breyta docs flows pull` / `push` / `deploy`

Local files:
- Default path is `./tmp/flows/<slug>.clj` when pulling.
- Keep each flow in a single file; use `flows pull` and `flows push` to round-trip changes.
- Use `flows validate` and `flows compile` after pushing to catch server-side errors.

Bindings and activation:
- See `./bindings-activation.md` for templates, profile files, and inline bindings.

## Clojure delimiter repair
If you hit delimiter errors while editing flow files:
- `breyta flows push` attempts delimiter repair by default (`--repair-delimiters=true`).
- It writes repaired content back to your file; opt out with `--no-repair-writeback`.

Local check:

```bash
breyta flows paren-check ./tmp/flows/<slug>.clj
```

Local repair:

```bash
breyta flows paren-repair ./tmp/flows/<slug>.clj
```
