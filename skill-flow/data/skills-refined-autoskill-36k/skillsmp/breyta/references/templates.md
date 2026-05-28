# Templates
Templates keep large payloads out of step bodies and are referenced with `:template` + `:data`.

```clojure
:templates [{:id :get-user
             :type :http-request
             :request {:url "https://api.example.com/users/{{id}}"
                       :method :get}}
            {:id :welcome
             :type :llm-prompt
             :system "You are helpful."
             :prompt "Welcome {{user.name}}!"}]

(flow/step :http :get-user {:template :get-user :data {:id user-id}})
(flow/step :llm :welcome {:connection :ai :template :welcome :data {:user input}})
```

Notes:
- Prefer templates for long prompts, request bodies, or SQL.
- Keep template IDs stable and referenced via keywords.
- Templates are packed to blob storage on deploy; flow versions store small refs.
- Flow definition size limit is 100 KB; templates keep definitions under the limit.
