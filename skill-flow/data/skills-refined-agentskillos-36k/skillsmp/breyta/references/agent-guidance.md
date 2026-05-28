# Agent guidance (flow authoring)
When you are authoring flows for a user:

- Stop and ask for bindings or activation inputs when required.
- Do not fabricate API keys, OAuth credentials, or webhook secrets.
- Offer the exact CLI commands or template file paths the user should fill.
- Use templates to collect inputs; keep API-provided `:redacted`/`:generate` placeholders and call out `--clean` when needed.
- Prefer tight loops: implement one step, run it in isolation (`breyta steps run`), then record docs/examples/tests for that step (or use `breyta steps record`, or `breyta steps run --record-example/--record-test`, to capture quickly).
- Treat step test cases as documentation: they preserve intent and expected behavior, and can be executed on demand via `breyta steps tests verify`.

Checklist:
1) If the flow has `:requires`, generate a template (`flows bindings template` or `flows draft bindings template`).
2) Ask the user to fill secrets/inputs and re-run `flows bindings apply` (or `draft bindings apply`).
3) If OAuth is required, direct the user to the activation URL printed by the template command.
4) Only activate once bindings are applied.

Example prompts to the user:
- "I need your API key for slot :api. Run `breyta flows bindings template <slug> --out profile.edn`, fill `:api :apikey`, then `breyta flows bindings apply <slug> @profile.edn`."
- "OAuth is required for :google. Run the template command and follow the activation URL printed to stderr."
- "You can keep existing `:conn` values if you don’t want to rebind. Use `--clean` for a fresh template."
