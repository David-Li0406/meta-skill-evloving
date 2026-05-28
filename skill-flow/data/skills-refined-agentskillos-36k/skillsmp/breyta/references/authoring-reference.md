# Authoring reference
## Flow file format
- A flow file is a single EDN map literal (Clojure data), not JSON.
- The server reads it with `*read-eval*` disabled.
- Slug format: `^[a-zA-Z][a-zA-Z0-9_-]{0,127}$`.

Core fields:

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `:slug` | keyword | Yes | Non-namespaced keyword (URL-safe) |
| `:name` | string | Yes | Display name |
| `:description` | string | No | Help text |
| `:icon` | keyword | No | UI icon (if supported) |
| `:tags` | vector | No | Tags for grouping |
| `:concurrency` | map | Yes | See below |
| `:requires` | vector | No | Connection slots and activation inputs |
| `:templates` | vector | No | Template payloads (see `./templates.md`) |
| `:functions` | vector | No | Function templates for `:function` steps |
| `:triggers` | vector | Yes | Include a `:manual` trigger for discoverability |
| `:flow` | form | Yes | The orchestration DSL |

## `:requires`
Use `:requires` to declare connection slots and activation form inputs. Flows with `:requires` must have bindings applied and be activated.

### `:kind :connection`
Core fields:

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `:slot` | keyword | Yes | Used as `:connection` in steps |
| `:type` | keyword | Yes | `:http-api`, `:llm-provider`, `:database`, `:blob-storage`, `:kv-store`, `:secret` |
| `:label` | string | Yes | UI label |
| `:optional` | boolean | No | Use `flow/slot-bound?` |
| `:base-url` | string | If `:http-api` | Base URL |
| `:auth` | map | If not `:secret` | `{:type :api-key|:bearer|:basic}` |
| `:oauth` | map | Optional | OAuth config |

Example:

```clojure
:requires [{:slot :crm
            :type :http-api
            :label "CRM API"
            :base-url "https://api.example.com"
            :auth {:type :bearer}}
           {:slot :ai
            :type :llm-provider
            :label "AI Provider"
            :auth {:type :api-key}
            :optional true}]
```

### `:kind :form`
Activation-only inputs (no connection created):

```clojure
{:kind :form
 :label "Activation inputs"
 :fields [{:key :region :label "Region" :field-type :select :options ["EU" "US"]}
          {:key :batch-size :label "Batch size" :field-type :number :default 500}]}
```

Form fields:

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `:key` | keyword | Yes | Input key under `:activation` |
| `:label` | string | Yes | UI label |
| `:field-type` | keyword | Yes | `:string`, `:text`, `:number`, `:boolean`, `:select`, `:date`, `:email`, `:textarea`, `:password`, `:secret` |
| `:required` | boolean | No | Default false |
| `:options` | vector | If `:select` | Options |

### `:type :secret`
Use `:type :secret` for single-value secrets (webhook signing, tokens used in flow logic). Avoid for HTTP APIs.

## `:concurrency`
Both `:type` and `:on-new-version` are required.

| Config | Description |
| --- | --- |
| `{:type :singleton :on-new-version :supersede}` | One instance at a time. New version cancels current |
| `{:type :singleton :on-new-version :drain}` | One instance at a time. Wait for current to finish |
| `{:type :singleton :on-new-version :coexist}` | One instance at a time. Both versions can run |
| `{:type :keyed :key-field :user-id :on-new-version :supersede}` | One instance per key |
| `{:type :keyed :key-field :user-id :on-new-version :drain}` | One instance per key, drain on new version |

## `:triggers`
Common types:
- `:manual` with `:label` and optional `:config`
- `:schedule` with `:config {:cron "..." :timezone "..."}`
- `:event` with `:config {:source :webhook ...}`

Notes:
- Keep at least one enabled `:manual` trigger so the flow is runnable from the UI.
- Webhook triggers use `:event` with `:source :webhook`; the webhook path is generated at activation.
- The payload arrives in `flow/input`.
- Webhook secrets are declared as `:requires` slots of `:type :secret` and bound via profiles.
- Webhook auth is required; `:auth {:type :none}` is not allowed for webhook triggers.

Example webhook trigger + secret slot:

```clojure
{:requires [{:slot :webhook-secret
             :type :secret
             :label "Webhook Secret"}]
 :triggers [{:type :event
             :label "Inbound webhook"
             :config {:source :webhook
                      :auth {:type :api-key
                             :secret-ref :webhook-secret}}}]}
```

Bindings snippet (profile EDN):

```edn
{:bindings {:webhook-secret {:secret :generate}}}
```

Webhook setup checklist:
1) Generate a bindings template and add the secret slot.
2) Apply bindings to generate/store the secret.
3) Copy the webhook URL from the trigger UI or API.
4) Send requests with the secret (header name depends on trigger auth config).

Webhook endpoints:
- Public (external senders): `POST /:workspace-id/events/<path>`
- Draft webhook endpoint (workspace-auth): `POST /:workspace-id/api/events/draft/<path>`
- Validate endpoint (workspace-auth): `POST /:workspace-id/api/events/validate/<path>`

CLI validation:
- `breyta webhooks send --validate-only --path <path> --json '{...}'`
- Add `--persist-resources` to store multipart file parts during validation.

Webhook auth schemes:

| Type | Config | How to send |
| --- | --- | --- |
| `:api-key` | `{:type :api-key :secret-ref :webhook-secret :header "X-API-Key"}` | `X-API-Key: <secret>` (default header is `X-API-Key`) |
| `:bearer` | `{:type :bearer :secret-ref :webhook-secret}` | `Authorization: Bearer <secret>` |
| `:basic` | `{:type :basic :username "user" :secret-ref :webhook-secret}` | `Authorization: Basic <base64(user:secret)>` |
| `:hmac-sha256` | `{:type :hmac-sha256 :secret-ref :webhook-secret :header "X-Signature"}` | `X-Signature: <base64(hmac)>` computed over raw request bytes |
| `:ip-allowlist` | `{:type :ip-allowlist :allow ["203.0.113.10"]}` | Must match `X-Forwarded-For`/`X-Real-IP` |

Notes:
- For HMAC, compute the signature over the exact raw request body (JSON bytes or multipart bytes).
- For multipart webhooks, use HMAC over the full multipart payload bytes.

Example curl (api-key header):

```bash
curl -X POST "https://flows.breyta.ai/<workspace-id>/events/webhooks/orders" \
  -H "X-API-Key: <webhook-secret>" \
  -H "Content-Type: application/json" \
  -d '{"orderId":"123"}'
```

## `:flow` rules and determinism
- Keep flow body code deterministic; avoid `rand`, current time, UUIDs, or external calls.
- Use `flow/step` for side effects; data transforms belong in `:function` steps.
- Control flow is plain Clojure (`let`, `if`, `cond`), but avoid `map`/`reduce` in the flow body.

Deterministic helpers:
- `flow/now-ms` for current workflow time.
- `flow/elapsed?` for elapsed time checks.
- `flow/backoff` for deterministic backoff intervals (accepts `"10s"`, `"5m"`, or ms).

## Polling with `flow/poll`
Use `flow/poll` to wrap a step in a deterministic loop with a sleep between attempts.
It expands to a loop + `:sleep`, so it satisfies loop safety requirements.

Required config:
- `:interval` (duration string or ms)
- `:timeout` or `:max-attempts`
- `:return-on` (function or predicate symbol)

Optional config:
- `:backoff` (`:type :exponential|:linear|:constant`, `:factor`, `:step`, `:max`)
- `:abort-on` (`:error?` defaults true, `:status` set)
- `:id` (custom step id for the sleep step)

Example:

```clojure
(flow/poll
  {:interval "10s"
   :timeout "10m"
   :backoff {:type :exponential :factor 2 :max "2m"}
   :abort-on {:status #{400 401 403} :error? true}
   :return-on (fn [result] (true? (get-in result [:data :ready])))}
  (flow/step :http :check
             {:connection :api
              :path "/jobs/123"}))
```

Notes:
- `:return-on` can be a function literal or a named predicate symbol.
- Use `:backoff {:type :linear :step "5s"}` for linear backoff.
- Hard limits: `:timeout` max is 1h; `:max-attempts` max is 100.

## Step-by-step: poll with error handling
Use this when an external job can fail and you want to abort early.

1) Start the job:
```clojure
(let [create (flow/step :http :create-job
                        {:connection :api
                         :path "/jobs"
                         :method :post
                         :json {:queued-ms 200 :processing-ms 900}
                         :response-as :json})
      job-id (get-in create [:body :id])]
  ...)
```

2) Poll until completed or error:
```clojure
(flow/poll
  {:interval "200ms"
   :timeout "5s"
   :return-on (fn [resp]
                (let [status (get-in resp [:body :status])]
                  (cond
                    (= status "completed") true
                    (= status "error") (throw (ex-info "job failed" {:error (get-in resp [:body :error])}))
                    :else false)))}
  (flow/step :http :job-status
             {:connection :api
              :path (str "/jobs/" job-id)
              :method :get
              :response-as :json}))
```

## Result handling
- Small results are returned inline; large results become refs.
- Use `:persist {:type :blob}` on `:http` steps when you expect large payloads.
- See `./persist.md` for how refs flow to downstream steps.

## Metadata labels for UI
Add labels to branches and loops to make the visual editor clearer.

```clojure
(if ^{:label "Has user"} (:user input)
  (flow/step :http :fetch {:connection :api :path "/users"})
  (flow/step :http :fallback {:connection :api :path "/users/guest"}))
```

## Functions (`:functions`)
Use `:function` steps for sandboxed transforms. For reuse, define flow-local functions.

Sandbox helpers (safe, no Java interop) are available under `breyta.sandbox`:
`base64-encode` `(string|bytes) -> string`, `base64-decode` `(string|bytes) -> string`,
`base64-decode-bytes` `(string|bytes) -> bytes`, `hex-encode` `(string|bytes) -> string`,
`hex-decode` `(string) -> string`, `hex-decode-bytes` `(string) -> bytes`,
`sha256-hex` `(string|bytes) -> string`, `hmac-sha256-hex` `(key,value) -> string`,
`uuid-from` `(string) -> uuid`, `uuid-from-bytes` `(string|bytes) -> uuid`,
`parse-instant` `(string) -> java.time.Instant`, `format-instant` `(Instant) -> string`,
`format-instant-pattern` `(Instant, pattern) -> string`, `url-encode` `(string) -> string`,
`url-decode` `(string) -> string`.

```clojure
:functions [{:id :summarize-user
             :language :clojure
             :code "(fn [input] {:ok true :input input})"}]

(flow/step :function :summarize-user
           {:input {:user user}
            :ref :summarize-user})
```

## Input keys from `--input`
Inputs provided via `--input '{...}'` arrive as strings, but the runtime normalizes so both string and keyword keys work.

## Limits (author-facing)
Common limits to plan around (see `breyta/libraries/flows/config/limits.clj` for full list):

### Flow definition and templates
- Flow definition size: 100 KB max.
- Templates are packed to blob storage on deploy; large prompts/SQL should live in templates.

### Runtime execution
- Step executions per run: 100
- HTTP requests per run: 50
- LLM tokens per run: 100,000
- Workflow duration: 7 days

### Per-step payloads
- Inline result threshold: 10 KB (larger results become refs)
- Max step result: 1 MB
- HTTP response size: 1 MB
- DB max rows: 10,000

Tips:
- Keep results small; return summaries and persist large payloads.
- Use `:persist {:type :blob}` on `:http` when you need large response bodies.
