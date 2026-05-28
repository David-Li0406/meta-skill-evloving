---
name: component-iterate
description: Iterate on hiccup components with live preview, CSS styling, and library commits. Use alias-first workflow where structure lives in the UI namespace and examples use lean config props. Keywords: component, preview, iterate, css, hiccup, design, ui, commit, datastar, signals, interactive, alias.
---

# Component Iteration Skill

Drive component development through an **alias-first** REPL-powered iteration loop. Component structure lives in a UI namespace as chassis aliases, while `components.edn` stores lean alias invocations with config props.

## Configuration

Read `tsain.edn` at project root for file locations:

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
  (let [{:my-component/keys [title subtitle icon]} attrs]
    [:div.my-component attrs  ;; namespaced keys auto-elided by chassis
     [:div.my-component-header
      [:span.my-component-icon icon]
      [:h3.my-component-title title]]
     [:p.my-component-subtitle subtitle]]))
```

After adding the alias, reload the namespace:

```bash
clj-nrepl-eval -p 7888 "(reload)"
```

### Step 2: Preview with Alias Invocation

Use the alias with config props. The namespace is from `:ui-namespace`:

```bash
clj-nrepl-eval -p 7888 "(dispatch [[::tsain/preview
  [:{{top/ns}}.views.components/my-component
   {:my-component/title \"Hello World\"
    :my-component/subtitle \"A simple example\"
    :my-component/icon \"🎉\"}]]])"
```

### Step 3: Iterate on Structure and CSS

1. **Modify the alias** in the UI namespace to adjust structure
2. **Reload**: `clj-nrepl-eval -p 7888 "(reload)"`
3. **Re-preview** to see changes
4. **Add CSS** to the stylesheet (from `:stylesheet`) - hot-reloads automatically

### Step 4: Commit the Lean Example

```bash
clj-nrepl-eval -p 7888 "(dispatch [[::tsain/commit :my-component
  {:description \"Card with icon and title\"
   :examples
   [{:label \"Dark\"
     :hiccup [:div {:style \"padding: 40px;\"}
              [:{{top/ns}}.views.components/my-component
               {:my-component/title \"Hello World\"
                :my-component/subtitle \"A simple example\"
                :my-component/icon \"🎉\"}]]}
    {:label \"Light\"
     :hiccup [:div.theme-light {:style \"padding: 40px; background: #f0f4f8;\"}
              [:{{top/ns}}.views.components/my-component
               {:my-component/title \"Hello World\"
                :my-component/subtitle \"A simple example\"
                :my-component/icon \"🎉\"}]]}]}]])"
```

**Result:** `components.edn` stores the lean alias form. Copying from the sandbox UI gives you clean, portable hiccup.

## Config Props vs HTML Attrs

```clojure
[:{{top/ns}}.views.components/game-card
 {;; Config props (namespaced) - elided from HTML output
  :game-card/title "Neural Phantom"
  :game-card/attack "3"

  ;; HTML/Datastar attrs (not namespaced) - pass through to HTML
  :data-signals:selected "false"
  :data-on:click "$selected = !$selected"
  :class "highlighted"}]
```

The alias handler receives both, but chassis automatically elides namespaced keys from the rendered HTML.

## Effect Reference

All sandbox functionality is available via dispatch effects. Use `(describe (dispatch))` to see the full list. Common effects:

| Effect | Purpose |
|--------|---------|
| `[::tsain/preview hiccup]` | Replace preview with new content |
| `[::tsain/preview-append hiccup]` | Append to existing preview |
| `[::tsain/preview-clear]` | Clear the preview area |
| `[::tsain/commit :name]` | Save preview to library |
| `[::tsain/commit :name "desc"]` | Save with description |
| `[::tsain/commit :name {:description "..." :examples [...]}]` | Save with multiple examples |
| `[::tsain/uncommit :name]` | Remove from library |
| `[::tsain/show-components :name]` | View component with sidebar |
| `[::tsain/show-preview]` | Return to preview view |
| `[::tsain/patch-signals {:key val}]` | Patch Datastar signals on all clients |

## Discovery Functions

Available in the dev namespace:

| Function | Purpose |
|----------|---------|
| `(describe (dispatch))` | List all registered effects |
| `(describe (dispatch) ::tsain/preview)` | Inspect specific effect |
| `(sample (dispatch) ::tsain/preview)` | Generate example invocation |
| `(grep (dispatch) "pattern")` | Search by pattern |
| `(reload)` | Reload changed namespaces (includes alias changes) |

## File Locations (from tsain.edn)

| Config Key | Purpose |
|------------|---------|
| `:ui-namespace` | Namespace for chassis aliases |
| `:stylesheet` | CSS file for component styles |
| `:components-file` | Library persistence file |

## Best Practices

1. **Alias-first** - Always define structure in UI namespace before committing
2. **Config by component name** - Use `:component-name/prop` for config props
3. **CSS classes over inline styles** - Extract to stylesheet before committing
4. **Use CSS custom properties** - Leverage theme variables (`--accent-cyan`, `--bg-primary`)
5. **BEM-like naming** - `.component-name`, `.component-name-element`, `.component-name--modifier`
6. **Discovery-first** - Use `describe`, `sample`, `grep` to explore the API

## Example: Creating a New Component

```bash
# 1. Read config to find file paths
cat tsain.edn

# 2. Add alias to UI namespace (using Edit tool)
# Structure: [:div.status-badge attrs [:span.status-badge-dot] [:span.status-badge-label label]]

# 3. Reload
clj-nrepl-eval -p 7888 "(reload)"

# 4. Preview with config
clj-nrepl-eval -p 7888 "(dispatch [[::tsain/preview
  [:{{top/ns}}.views.components/status-badge
   {:status-badge/label \"Online\"
    :status-badge/status :active}]]])"

# 5. Add CSS to stylesheet
# .status-badge { ... }
# .status-badge--active { ... }

# 6. Commit with dark/light variants
clj-nrepl-eval -p 7888 "(dispatch [[::tsain/commit :status-badge
  {:description \"Status indicator badge\"
   :examples
   [{:label \"Dark\"
     :hiccup [:div {:style \"padding: 20px;\"}
              [:{{top/ns}}.views.components/status-badge {:status-badge/label \"Online\" :status-badge/status :active}]]}
    {:label \"Light\"
     :hiccup [:div.theme-light {:style \"padding: 20px; background: #f0f4f8;\"}
              [:{{top/ns}}.views.components/status-badge {:status-badge/label \"Online\" :status-badge/status :active}]]}]}]])"
```

## Dynamic Components with Datastar

For interactive components, Datastar attrs pass through to HTML:

```clojure
;; Alias handles structure
(defmethod c/resolve-alias ::accordion
  [_ attrs content]
  (let [{:accordion/keys [title]} attrs]
    [:div.accordion attrs  ;; data-signals, data-on pass through
     [:button.accordion-header {:data-on:click "$open = !$open"} title]
     [:div.accordion-content {:data-class:open "$open"} content]]))

;; Usage with Datastar attrs
[:{{top/ns}}.views.components/accordion
 {:accordion/title "Click to expand"
  :data-signals:open "false"}
 [:p "Hidden content"]]
```

Test interactivity from REPL:

```bash
clj-nrepl-eval -p 7888 "(dispatch [[::tsain/patch-signals {:open true}]])"
```

## CSS Extraction (Required Before Commit)

All committed components must use CSS classes. The copy button returns the lean alias form from `components.edn`, so keeping examples clean ensures portable snippets.

### Extraction Process

1. **Define structure in alias** with semantic class names
2. **Add CSS** for those classes in stylesheet
3. **Use CSS custom properties** for colors that vary by theme
4. **Commit the lean alias invocation** with config props only

### Theme Variants

Use `.theme-light` wrapper class - CSS custom properties handle the rest:

```clojure
;; Dark (default)
[:{{top/ns}}.views.components/game-card {:game-card/title "Card" ...}]

;; Light
[:div.theme-light
 [:{{top/ns}}.views.components/game-card {:game-card/title "Card" ...}]]
```
