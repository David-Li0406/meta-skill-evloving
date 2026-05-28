---
name: component-iterate
description: Use this skill when you need to iterate on hiccup components with live previews, CSS styling, and library commits in a structured, alias-first workflow.
---

# Component Iteration Skill

Drive component development through an **alias-first** REPL-powered iteration loop. Component structure lives in a UI namespace as chassis aliases, while `components.edn` stores lean alias invocations with config props.

## Configuration

Read `tsain.edn` at the project root for file locations:

```clojure
;; tsain.edn
{:ui-namespace {{top/ns}}.views.components  ;; Where chassis aliases live
 :components-file "dev/resources/components.edn"  ;; Component library persistence
 :stylesheet "resources/public/styles.css"  ;; CSS for hot reload
 :port 3000}
```

## Prerequisites

1. **nREPL running** on port 7888 (use `clj-nrepl-eval --discover-ports` to verify)
2. **Sandbox started** - if not running, evaluate `(dev)` then `(start)` in the REPL
3. **Browser open** at `http://localhost:3000/sandbox`

## Discovering the API

Use sandestin discovery to explore available effects. This is the primary way to learn what's available:

```clojure
(require '[ascolais.tsain :as tsain])

;; List all tsain effects
(describe (dispatch))

;; See schema and docs for an effect
(describe (dispatch) ::tsain/preview)

;; Generate example invocation
(sample (dispatch) ::tsain/preview)

;; Search by keyword
(grep (dispatch) "component")
```

## Alias-First Workflow

### Step 0: Read Configuration

First, read `tsain.edn` to find the correct file paths:

```bash
cat tsain.edn
```

The `:ui-namespace` tells you where to add aliases. The `:stylesheet` tells you where to add CSS.

### Step 1: Define the Chassis Alias (Required First Step)

Before iterating on visuals, define the component structure in the components namespace (from `:ui-namespace`). This is a production namespace, so aliases you define here can be used directly in your application views.

**Key conventions:**
- **Namespaced attrs** (`:game-card/title`) = config props (elided from HTML output)
- **Regular attrs** (`:data-on:click`, `:class`) = pass through to HTML
- **Namespace by component name** for self-documenting code

```clojure
;; In views/components.clj
(defmethod c/resolve-alias ::my-component
  [_ attrs _]
  (let [{:my-component/keys [title subtitle ic
```