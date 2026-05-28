# Templating (Handlebars)

Breyta Flows templates use Handlebars (`{{...}}`) via the Java implementation (`handlebars-java`).

## Basics

- **Variables**: `{{id}}`, nested: `{{user.name}}`
- **Conditionals**: `{{#if condition}}...{{/if}}`, `{{#unless condition}}...{{/unless}}`
- **Loops**: `{{#each items}}...{{/each}}`
- **Context switch**: `{{#with obj}}...{{/with}}`

## Custom helpers available

These helpers are available in the Flows runtime:

- `{{truncate text length=100 suffix="..."}}`
- `{{json data}}` or `{{json data pretty=true}}`
- `{{length items}}`
- `{{join items separator=", "}}`
- `{{first items}}`
- `{{last items}}`
- `{{default value fallback}}` (if `value` is missing/empty, returns `fallback`)

## Practical examples

### LLM prompt template

```clojure
{:id :findings
 :type :llm-prompt
 :system "Today is {{current-date}}."
 :prompt "Analyze: {{text}}"}
```

Called as:

```clojure
(flow/step :llm :findings {:connection :ai
                           :template :findings
                           :data {:current-date "2026-01-16"
                                  :text "..."}})
```

### Choosing between templates

When conditional logic gets messy, prefer two templates and select one in code:

```clojure
(let [tpl (if (:include-timestamps? ctx) :findings-with-ts :findings-no-ts)]
  (flow/step :llm :findings {:connection :ai :template tpl :data ctx}))
```
