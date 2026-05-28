# Bindings and activation
Draft workflow (safe preview):
- Generate a draft template: `breyta flows draft bindings template <slug> --out draft.edn`
- Set draft bindings: `breyta flows draft bindings apply <slug> @draft.edn`
- Show draft bindings status: `breyta flows draft bindings show <slug>`
- Show draft: `breyta flows draft show <slug>`
- Run draft: `breyta flows draft run <slug> --input '{"n":41}' --wait`

Inline bindings (no file):
- Prod: `breyta flows bindings apply <slug> --set api.conn=conn-123 --set activation.region=EU`
- Draft: `breyta flows draft bindings apply <slug> --set api.apikey=...`

Bindings (required for `:requires`):
- Generate a template: `breyta flows bindings template <slug> --out profile.edn`
- Apply bindings: `breyta flows bindings apply <slug> @profile.edn`
- Or promote draft bindings: `breyta flows bindings apply <slug> --from-draft`
- Show bindings status: `breyta flows bindings show <slug>`
- Enable prod profile: `breyta flows activate <slug> --version latest`

Templates prefill current `:conn` bindings by default; add `--clean` for a requirements-only template.

Profile file example (EDN):

```edn
{:profile {:type :prod
           :autoUpgrade false}

 :bindings {:api {:name "Users API"
                  :url "https://api.example.com"
                  :apikey :redacted}
            :ai {:conn "conn-openai-123"}}

 :activation {:region "EU"
              :batch-size 500}}
```

Notes:
- `:redacted` values are ignored when sending the profile to the server (use for API keys).
- `:generate` values are ignored when sending the profile to the server (use for secrets).
- Templates include comments that list OAuth and secret slots.
- Template commands print the activation URL to stderr for OAuth flows.
- `:profile :autoUpgrade` controls pinning: `false` pins to the activated version, `true` auto-upgrades to latest.

## Step-by-step: promote draft bindings to prod
Use this when a draft profile is already working and you want to reuse it in prod.

1) Apply draft bindings:
```bash
breyta flows draft bindings apply <slug> @draft.edn
```

2) Promote the current user's draft bindings:
```bash
breyta flows bindings apply <slug> --from-draft
```

3) Verify prod bindings:
```bash
breyta flows bindings show <slug>
```

4) Activate prod:
```bash
breyta flows activate <slug> --version latest
```

## Template commands and `--clean`
Template commands reflect current bindings by default:
- `breyta flows bindings template <slug> --out profile.edn`
- `breyta flows draft bindings template <slug> --out draft.edn`

Default behavior (no `--clean`):
- Existing connection bindings are prefilled as `:conn` values.
- Missing slots are emitted with placeholders (e.g., `:redacted`, `:generate`).
- Use this when you want to edit current bindings in place.

`--clean` behavior:
- Emits a requirements-only template without existing bindings.
- Use this when you want a fresh template or to share a minimal example.

Notes:
- Placeholders like `:redacted` and `:generate` are ignored when sent back in.
- If a slot is already bound to a connection, you can keep `:conn` as-is to avoid rebinding.
