## Webhooks and event routing

This guide covers webhook triggers, event routing, multipart payloads, and wait-based
webhook completion.

### Overview
- Webhook triggers are `:event` triggers with `:config {:source :webhook ...}`.
- Webhook paths are generated at activation (prod profile) or when you run draft
  flows via the API.
- Payloads arrive in `flow/input`.
- Multipart webhooks preserve file parts and certain raw MIME fields as blob refs.
- Webhook secrets must use explicit `:secret-ref` + profile bindings.

### Webhook trigger setup
Minimal webhook trigger:

```clojure
{:triggers [{:type :event
             :label "Inbound webhook"
             :enabled true
             :config {:event-name "orders.created"
                      :source :webhook
                      :auth {:type :api-key
                             :secret-ref :webhook-secret}}}]}
```

Declare the secret slot and bind it:

```clojure
{:requires [{:slot :webhook-secret
             :type :secret
             :secret-ref :webhook-secret
             :label "Webhook Secret"}]}
```

Bindings template snippet:

```edn
{:bindings {:webhook-secret {:secret :generate}}}
```

Webhook setup checklist:
1) Generate a bindings template and add the secret slot.
2) Apply bindings to generate/store the secret.
3) Copy the webhook URL from the trigger UI or API.
4) Send requests with the secret (header name depends on auth config).

### Step-by-step: add a third-party webhook secret
Use this when a provider gives you a webhook secret and you must validate signatures.

1) Declare a secret slot in `:requires` (with explicit `:secret-ref`):
```clojure
{:requires [{:slot :webhook-secret
             :type :secret
             :secret-ref :webhook-secret
             :label "Webhook Secret"}]}
```

2) Configure the webhook trigger to reference the secret:
```clojure
{:triggers [{:type :event
             :label "Inbound webhook"
             :enabled true
             :config {:event-name "orders.created"
                      :source :webhook
                      :auth {:type :hmac-sha256
                             :header "X-Signature"
                             :secret-ref :webhook-secret}}}]}
```

3) Generate and fill a bindings file with the provider secret (stored under the
   explicit `:secret-ref` value):
```bash
breyta flows bindings template <slug> --out profile.edn
```
Edit `profile.edn`:
```edn
{:bindings {:webhook-secret {:secret "YOUR_PROVIDER_SECRET"}}}
```

4) Apply bindings and activate:
```bash
breyta flows bindings apply <slug> @profile.edn
breyta flows activate <slug> --version latest
```

5) Copy the webhook URL and configure the provider:
- Get URL from UI or via `breyta triggers <flow-slug>` (includes `webhookUrl` for webhook triggers)
- Set the provider to sign payloads and send `X-Signature`

### Step-by-step: webhook auth troubleshooting
Use this when requests hit your endpoint but the flow does not start or auth fails.

1) Confirm the trigger auth scheme matches the provider:
```clojure
{:auth {:type :hmac-sha256
        :header "X-Signature"
        :secret-ref :webhook-secret}}
```

2) Confirm the provider sends the exact header name (case-insensitive) and raw payload.
   For signature auth, the signature must be computed over the raw bytes (not parsed JSON).

3) Verify the secret binding is present:
```bash
breyta flows bindings show <slug>
```

4) Send a request that matches the provider:
```bash
curl -X POST "https://flows.breyta.ai/<workspace-id>/events/<path>" \
  -H "Content-Type: application/json" \
  -H "X-Signature: <computed-signature>" \
  -d '{"id":"evt_123","ok":true}'
```

5) If you use `:signature` auth:
- Check `:signed-message` (`:payload` vs `:timestamp-payload`).
- Check `:signature-format` (`:base64` vs `:hex`).
- Check `:signature-prefix` if the provider prepends `sha256=`.

### Webhook endpoints
- Public (external senders): `POST /:workspace-id/events/<path>`
- Draft webhook endpoint (workspace-auth): `POST /:workspace-id/api/events/draft/<path>`

Draft endpoint notes:
- Requires workspace auth (CLI token/session), not webhook auth.
- Useful for validating before deploying/activating a prod profile.

### Fetch webhook URLs (CLI)
Use the CLI to fetch webhook URLs for a flow:

```bash
breyta triggers <flow-slug>
```

If the webhook uses query-param auth, append the token:
`https://.../events/<path>?token=<secret>`

### Validate webhook payloads (CLI)
Use `webhooks send --validate-only` to preview how a payload becomes `flow/input`
without triggering a run.

JSON payload preview:
```bash
breyta webhooks send --path webhooks/orders/created \
  --json '{"id":"evt_123","ok":true}' \
  --validate-only
```

Multipart payload preview (no persistence):
```bash
breyta webhooks send --path webhooks/orders/inbound \
  --multipart-file "file=./receipt.pdf" \
  --form-field "from=sender@example.com" \
  --validate-only
```

Persist multipart resources during validation (so input includes resource refs):
```bash
breyta webhooks send --path webhooks/orders/inbound \
  --multipart-file "file=./receipt.pdf" \
  --validate-only \
  --persist-resources
```

Notes:
- Validation uses the workspace-auth endpoint; you need a CLI token/session.
- When `--persist-resources` is omitted, file parts are returned as previews.

### Auth schemes
Supported auth types:
- `:api-key`
- `:bearer`
- `:basic`
- `:hmac-sha256`
- `:signature` (generic signed payloads: HMAC or ECDSA)
- `:ip-allowlist`

Auth config examples:

API key (custom header):
```clojure
{:auth {:type :api-key
        :header "X-API-Key"
        :secret-ref :webhook-secret}}
```

API key (query param):
```clojure
{:auth {:type :api-key
        :location :query
        :param "token"
        :secret-ref :webhook-secret}}
```

Bearer token:
```clojure
{:auth {:type :bearer
        :secret-ref :webhook-token}}
```

HMAC (simple, Base64 signature):
```clojure
{:auth {:type :hmac-sha256
        :header "X-Signature"
        :secret-ref :webhook-secret}}
```

Signature (HMAC with timestamp + hex + prefix):
```clojure
{:auth {:type :signature
        :algo :hmac-sha256
        :signature-header "X-Signature"
        :timestamp-header "X-Timestamp"
        :signed-message :timestamp-payload
        :signature-format :hex
        :signature-prefix "sha256="
        :timestamp-max-skew-ms 300000
        :secret-ref :webhook-signing-secret}}
```

Signature (ECDSA, Base64):
```clojure
{:auth {:type :signature
        :algo :ecdsa-p256
        :signature-header "X-Signature"
        :signed-message :payload
        :signature-format :base64
        :public-key-ref :webhook-public-key}}
```

HMAC notes:
- Compute the HMAC over the exact raw request bytes.
- For JSON, sign the raw JSON bytes before any parsing.
- For multipart, sign the full multipart payload bytes.

Signature notes:
- `:signature` supports `:hmac-sha256` and `:ecdsa-p256` (SHA-256).
- Use `:signed-message :payload` to sign just the raw body bytes.
- Use `:signed-message :timestamp-payload` to sign `timestamp + raw body`.
- `:signature-format` defaults to `:base64`; set `:hex` if your provider uses hex.

### Multipart payloads (inbound email)
Inbound email providers often POST `multipart/form-data` containing fields like
`from`, `subject`, `text`, and attachments. Breyta normalizes these into the
flow input map. File parts are persisted and exposed as blob refs.

Raw MIME support:
- If a raw MIME field (default: `email`) is present, it is stored as a blob and
  the flow input includes a file ref map for `:email`.
- Storage tier is configurable (ephemeral by default).
- Raw MIME payloads share the same 50MB total payload limit as standard webhook
  payloads (limit applies across all attachments).
- Multipart payloads with `:hmac-sha256` or `:signature` auth have a stricter
  size cap; oversized requests return 413.

Example flow input (simplified):
```clojure
{:from "sender@example.com"
 :subject "Receipt"
 :email {:uri "resource://.../raw.eml"
         :content-type "message/rfc822"
         :size-bytes 845231
         :filename "raw.eml"}
 :attachment1 {:uri "resource://.../receipt.pdf"
               :content-type "application/pdf"
               :size-bytes 53210
               :filename "receipt.pdf"}}
```

### Keyed webhook routing (idempotency)
Use keyed concurrency so duplicate webhook deliveries collapse to the same workflow
based on a stable event identifier in the payload.

Example (keyed by `event-id`):
```clojure
{:slug :webhook-processor
 :concurrency {:type :keyed
               :key-field :event-id
               :on-new-version :supersede}
 :triggers [{:type :event
             :label "Incoming webhook"
             :enabled true
             :config {:event-name "orders.webhook"
                      :source :webhook
                      :auth {:type :hmac-sha256
                             :header "X-Signature"
                             :secret-ref :webhook-secret}}}]
 :flow
 '(let [input (flow/input)]
    {:ok true
     :event-id (:event-id input)
     :payload input})}
```

Notes:
- Ensure the webhook payload includes a stable `event-id` (or set `:key-field` to
  a nested path like `[:event :id]`).
- Duplicate deliveries return `deduped=true` and do not start a new workflow.

### Wait-based key correlation
Use a webhook trigger to start a flow and a wait step keyed by a correlation
identifier from the payload. The callback webhook completes the wait using the
same key.

Example (start webhook + wait for callback):
```clojure
{:slug :order-callback
 :concurrency {:type :keyed
               :key-field :order-id
               :on-new-version :supersede}
 :triggers [{:type :event
             :label "Order webhook"
             :enabled true
             :config {:event-name "orders.created"
                      :source :webhook
                      :auth {:type :api-key
                             :secret-ref :webhook-secret}}}]
 :flow
 '(let [input (flow/input)
        order-id (:order-id input)
        wait-result (flow/step :wait :callback
                               {:type :wait
                                :key order-id
                                :event {:name "orders.callback"
                                        :key {:path [:order-id]}}
                                :timeout 300})]
    {:ok true
     :order-id order-id
     :callback wait-result})}
```

Notes:
- The wait will only complete when the callback webhook includes the same
  `order-id` in its payload.
- For external callbacks, configure a webhook trigger for `orders.callback`.
- `:signature-prefix` strips a prefix like `sha256=` before decoding.
- If you set `:timestamp-header`, the timestamp is checked against
  `:timestamp-max-skew-ms` (default 5 minutes).

Example (api-key header):

```bash
curl -X POST "https://flows.breyta.ai/<workspace-id>/events/webhooks/orders" \
  -H "X-API-Key: <webhook-secret>" \
  -H "Content-Type: application/json" \
  -d '{"orderId":"123"}'
```

Example (api-key query):

```bash
curl -X POST "https://flows.breyta.ai/<workspace-id>/events/webhooks/orders?token=<webhook-secret>" \
  -H "Content-Type: application/json" \
  -d '{"orderId":"123"}'
```

### Event routing vs wait routing
There are two common patterns:

1) Webhook trigger (flow starts):
   - Use `:event` trigger with `:source :webhook`.
   - The webhook request starts the flow.

2) Wait completion (flow pauses and resumes):
   - Use a `:wait` step with `:webhook` config.
   - The flow pauses, and an external webhook completes the wait.

Wait example:

```clojure
(flow/step :wait :payment
  {:key order-id
   :webhook {:auth {:type :hmac-sha256 :secret-ref :webhook-secret}}
   :timeout 3600})
```

Event-key routing for waits:
- You can set `:event` on a wait to route by event name and a correlation key
  extracted from the payload.
- The `:event-key-path` (or `:event {:key {:path [...]}}`) identifies the field
  to extract from the payload.

Example:

```clojure
(flow/step :wait :transcript
  {:key transcript-id
   :event {:name "assemblyai.transcript"
           :key {:path [:transcript-id]}}
   :timeout 3600})
```

### Multipart payloads
If you send multipart payloads:
- Ensure the sender sets `Content-Type: multipart/form-data`.
- HMAC must be computed on the full multipart bytes.
- Use `:auth {:type :hmac-sha256 ...}` if you need integrity checks.

### Troubleshooting
- If the webhook is unauthorized, confirm the auth type and header.
- If HMAC fails, ensure you’re signing the exact raw bytes.
- If the flow never starts, verify the trigger is enabled and the profile is active.
- If a wait never completes, confirm the wait is registered and the webhook path is correct.
