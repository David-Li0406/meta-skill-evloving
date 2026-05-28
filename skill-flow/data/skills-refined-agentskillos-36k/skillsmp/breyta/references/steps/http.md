# HTTP step (`:http`)
Use for HTTP APIs. Prefer `:connection` with a `:http-api` slot.

Core fields:

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `:connection` | keyword/string | Yes (unless `:url`) | Slot or connection id |
| `:url` | string | Yes (unless `:connection`) | Full URL (bypasses `:path`) |
| `:path` | string | No | Appended to base URL |
| `:method` | keyword | No | `:get`, `:post`, `:put`, `:patch`, `:delete` |
| `:query` | map | No | Query params |
| `:headers` | map | No | Header map |
| `:json` | any | No | JSON body (sets content-type) |
| `:body` | any | No | Raw body |
| `:response-as` | keyword | No | `:auto`, `:json`, `:text`, `:bytes` (default `:auto`) |
| `:persist` | map | No | Store response as reference (`{:type :blob ...}`) |
| `:retry` | map | No | Retry policy (see flow limits) |

Notes:
- When both `:json` and `:body` are set, `:json` wins.
- `:response-as :auto` uses the response `Content-Type` to choose `:json`, `:text`, or `:bytes`.
- Binary responses are base64-encoded inline only for small payloads; larger bodies are truncated.
- If the response is truncated, the step fails unless `:persist {:type :blob ...}` is set.
- Use `:persist {:type :blob}` for large payloads; downstream steps can load refs.
- Templates only cover request shape; step-level keys like `:persist` stay on the step.
- Auth must use secret references. Inline tokens or API keys are rejected.
- Prefer connection auth (`:requires` with `:auth`), or set step-level auth with `:auth {:type :bearer|:api-key :secret-ref :my-secret}`.

Example:

```clojure
;; In the flow definition:
;; :templates [{:id :download-report
;;              :type :http-request
;;              :request {:path "/reports/latest" :method :get}}]

(flow/step :http :get-users
           {:connection :api
            :path "/users"
            :method :get
            :query {:limit 10}
            :headers {"X-Request-Id" (:request-id (flow/input))}
            :retry {:max-attempts 3
                    :backoff-ms 500}})

(flow/step :http :download-report
           {:connection :api
            :template :download-report
            :persist {:type :blob}})
```
