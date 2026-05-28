# LLM step (`:llm`)
Use for model calls via an `:llm-provider` connection.

Core fields:

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `:connection` | keyword/string | Yes | Slot or connection id |
| `:model` | string | No | Default from connection if omitted |
| `:messages` | vector | No | Explicit message array |
| `:prompt` | string | No | Simple prompt (mutually exclusive with `:messages`) |
| `:system` | string | No | System prompt (simple mode) |
| `:template` | keyword | No | Template id |
| `:data` | map | No | Template inputs |
| `:tools` | map | No | Agentic tool definitions |

Notes:
- Use either `:messages` or `:prompt`/`:system`.
- Prefer templates for long prompts.
- `:tools` belongs on the step config, not inside templates.

Example:

```clojure
;; In the flow definition:
;; :templates [{:id :summary
;;              :type :llm-prompt
;;              :system "You are concise."
;;              :prompt "Summarize in 3 bullets:\\n{{text}}"}]
(flow/step :llm :summarize
           {:connection :ai
            :model "gpt-4o-mini"
            :template :summary
            :data {:text (:text (flow/input))}
            :tools {:definitions [{:name "fetch-user"
                                   :description "Fetch a user by id"
                                   :params {:type "object"
                                            :properties {:id {:type "string"}}
                                            :required ["id"]}}]}})
```
