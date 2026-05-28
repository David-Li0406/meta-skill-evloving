## Secrets reference

This guide covers secret slots, secret refs, bindings, rotation, and how secrets
are consumed by triggers and steps.

### Core concepts
- A secret is stored under a `:secret-ref` key.
- A secret slot is declared in `:requires` with `:type :secret`.
- Bindings map a slot to its `:secret-ref`; the secret value is stored separately.
- Flow definitions should never embed secret values.

### Declare a secret slot
Always set an explicit `:secret-ref` on secret slots.

```clojure
{:requires [{:slot :webhook-secret
             :type :secret
             :secret-ref :webhook-secret
             :label "Webhook Secret"}]}
```

### Provide a secret value (bindings)
Create a bindings template, fill the secret value, and apply it.

```bash
breyta flows bindings template <slug> --out profile.edn
```

Edit `profile.edn`:
```edn
{:bindings {:webhook-secret {:secret "YOUR_SECRET_VALUE"}}}
```

Apply bindings:
```bash
breyta flows bindings apply <slug> @profile.edn
```

### Generate a new secret value
Use `:generate` to create a secret value server-side:

```edn
{:bindings {:webhook-secret {:secret :generate}}}
```

### Rotate a secret
1) Update the bindings file with the new secret value.
2) Re-apply bindings to store the new value under the same `:secret-ref`.
3) Update external systems to use the new secret.

```bash
breyta flows bindings apply <slug> @profile.edn
```

### Inspect bindings (no secret values)
```bash
breyta flows bindings show <slug>
```

### Using secrets in webhook auth
Auth configs reference secrets via `:secret-ref`:

```clojure
{:auth {:type :api-key
        :header "X-API-Key"
        :secret-ref :webhook-secret}}
```

```clojure
{:auth {:type :hmac-sha256
        :header "X-Signature"
        :secret-ref :webhook-secret}}
```

```clojure
{:auth {:type :basic
        :username "webhook-user"
        :secret-ref :webhook-basic-password}}
```

### Common mistakes
- Omitting `:secret-ref` on a secret slot.
- Putting secret values in flow definitions.
- Mismatching the trigger `:secret-ref` and the slot `:secret-ref`.
