# Reference Guide

## Data Structure Selection

| Need | Data Structure |
|------|----------------|
| Indexed access, append at end | Vector `[]` |
| Sequential prepend | List `'()` |
| Key-value lookup | Map `{}` |
| Membership testing, uniqueness | Set `#{}` |
| FIFO queue | `clojure.lang.PersistentQueue/EMPTY` |
| Ordered by key | Sorted map `(sorted-map)` |
| Coordinate storage | Vector/tuple as map key |

### When to Use What

- **Vector**: Default choice for sequences. O(~1) indexed access and append.
- **List**: When prepending is the primary operation (stacks, recursion).
- **Map**: Key-value associations. Keywords as keys for named fields.
- **Set**: Membership testing, deduplication, filtering.

## Naming Conventions

```clojure
;; kebab-case for vars and functions
(def max-retry-attempts 3)
(defn calculate-total-price [items] ...)

;; Predicates end with ?
(defn valid-email? [email] ...)

;; Side-effecting functions end with !
(defn save-user! [user] ...)
(defn reset-counter! [] ...)

;; Dynamic vars use earmuffs
(def ^:dynamic *config* {...})

;; CamelCase for protocols and records
(defprotocol Storage ...)
(defrecord DatabaseStorage [conn] ...)

;; Private functions use defn-
(defn- parse [input] ...)      ; Internal helper
(defn process [data] ...)      ; Public API
```

## Best Practices

### Do

- **Prefer pure functions**: Same input, same output, no side effects
- **Use immutable data**: Let Clojure's persistent data structures work for you
- **Leverage threading macros**: `->` and `->>` for readable pipelines
- **Destructure liberally**: Makes code self-documenting
- **Use keywords as functions**: `(:name user)` instead of `(get user :name)`
- **Keep functions small**: Single responsibility, testable in isolation
- **Use the REPL**: Develop incrementally, test immediately
- **Spec your data**: Define specs for critical domain entities

### Don't

- **Avoid mutable state**: Use atoms/refs only when necessary
- **Avoid deep nesting**: Threading macros and small functions
- **Don't reinvent the wheel**: Check clojure.core and standard library first
- **Don't overuse macros**: Functions are simpler, composable, testable
- **Avoid global state**: Pass dependencies explicitly or use dynamic vars
- **Don't ignore laziness**: Be aware when sequences are lazy vs realized

## REPL Workflow

```clojure
;; Reload namespace
(require '[myapp.core :as core] :reload)

;; Reload all dependencies
(require '[myapp.core :as core] :reload-all)

;; Inspect var metadata
(meta #'core/my-fn)

;; Find docs
(doc map)
(source map)
(apropos "str")

;; Pretty print
(clojure.pprint/pprint (complex-data))

;; Time execution
(time (expensive-operation))
```

## Performance Tips

### Avoid

- **Reflection**: Use type hints `^String` for hot paths
- **Realizing lazy seqs unnecessarily**: Use `first`, `take` when possible
- **Repeated hash lookups**: Destructure once, use locals
- **Boxing in tight loops**: Use primitive type hints

### Prefer

- **Transducers**: For multi-step transformations on large data
- **Reducers**: For parallel fold operations
- **Persistent vectors over lists**: For random access
- **`into` over repeated `conj`**: Batches efficiently
- **`mapv`/`filterv`**: When you need vectors, avoid intermediate lazy seqs

## Code Organization

```
src/
├── myapp/
│   ├── core.clj         ; Entry point, -main
│   ├── config.clj       ; Configuration loading
│   ├── domain/          ; Domain entities, specs
│   │   ├── user.clj
│   │   └── order.clj
│   ├── db/              ; Database access
│   │   └── queries.clj
│   └── api/             ; HTTP handlers
│       └── routes.clj
test/
├── myapp/
│   └── domain/
│       └── user_test.clj
```

## Common Idioms

```clojure
;; Safe navigation (nil-punning)
(some-> user :address :city str/upper-case)

;; Default values
(or (:name user) "Anonymous")
(:name user "Anonymous")  ; Same with get

;; Update multiple keys
(-> user
    (assoc :updated-at (java.util.Date.))
    (update :version inc))

;; Conditional update
(cond-> user
  admin? (assoc :role :admin)
  verified? (assoc :verified true))

;; Juxt for extracting multiple values
((juxt :name :email) user)  ; => ["Alice" "alice@ex.com"]

;; Frequencies for counting
(frequencies ["a" "b" "a" "c" "a"])
; => {"a" 3, "b" 1, "c" 1}

;; Group and transform
(->> items
     (group-by :category)
     (map-vals #(map :name %)))
```

## Error Handling

```clojure
;; Use ex-info for exceptions with data
(throw (ex-info "User not found" {:user-id id}))

;; Catch and extract data
(try
  (find-user id)
  (catch Exception e
    (let [{:keys [user-id]} (ex-data e)]
      (log/error "Failed for user:" user-id))))

;; Return result maps instead of exceptions
{:ok result}
{:error {:type :not-found :message "..."}}
```

## Project Structure

```
myapp/
├── deps.edn
├── build.clj               # tools.build script
├── src/
│   └── myapp/
│       ├── core.clj
│       └── db.clj
├── test/
│   └── myapp/
│       └── core_test.clj
└── resources/
```

## deps.edn Configuration

```clojure
{:paths ["src" "resources"]

 :deps
 {org.clojure/clojure {:mvn/version "1.12.0"}
  org.clojure/core.async {:mvn/version "1.6.681"}
  metosin/malli {:mvn/version "0.16.4"}}

 :aliases
 {;; Run application
  :run
  {:main-opts ["-m" "myapp.core"]}

  ;; REPL with rebel-readline
  :repl/rebel
  {:extra-deps {com.bhauman/rebel-readline {:mvn/version "0.1.4"}}
   :main-opts ["-m" "rebel-readline.main"]}

  ;; Testing with Kaocha
  :test/run
  {:extra-paths ["test"]
   :extra-deps {lambdaisland/kaocha {:mvn/version "1.91.1392"}}
   :exec-fn kaocha.runner/exec-fn
   :exec-args {:fail-fast? true}}

  ;; Build
  :build
  {:replace-paths ["."]
   :replace-deps {io.github.clojure/tools.build
                  {:git/tag "v0.10.5" :git/sha "2a21b7a"}}
   :ns-default build}

  ;; Linting
  :lint
  {:extra-deps {clj-kondo/clj-kondo {:mvn/version "2024.08.01"}}
   :main-opts ["-m" "clj-kondo.main" "--lint" "src" "test"]}

  ;; Outdated deps
  :search/outdated
  {:extra-deps {com.github.liquidz/antq {:mvn/version "2.8.1201"}}
   :main-opts ["-m" "antq.core"]}}}
```

## Dependency Types

```clojure
;; Maven (most common)
{org.clojure/data.json {:mvn/version "2.5.0"}}

;; Git (latest or specific commit)
{io.github.user/lib {:git/tag "v1.0.0" :git/sha "abc1234"}}
{io.github.user/lib {:git/sha "abc1234def5678"}}

;; Local development
{mylib {:local/root "../mylib"}}
```

## Core Patterns

### Pure Functions + Immutability

```clojure
;; Immutable by default
(defn update-user [user new-email]
  (assoc user :email new-email))  ; Returns new map

;; Transform, don't mutate
(update {:count 0} :count inc)    ; => {:count 1}
(update-in m [:user :age] inc)    ; Nested update
```

### Threading Macros

```clojure
;; Thread-first: subject flows through
(-> user
    (assoc :updated-at (now))
    (update :login-count inc)
    validate
    save)

;; Thread-last: collection flows through
(->> numbers
     (filter even?)
     (map inc)
     (reduce +))

;; Conditional threading
(cond-> user
  admin? (assoc :role :admin)
  verified? (assoc :verified true))
```

### Destructuring

```clojure
;; Maps
(let [{:keys [name email]} user] ...)
(let [{:keys [name] :or {name "anon"}} user] ...)
(let [{:keys [name] :as user} data] ...)

;; Vectors
(let [[x y & rest] coords] ...)
(let [[_ second third] items] ...)

;; Function parameters
(defn greet [{:keys [name email]}]
  (format "Hello %s (%s)" name email))
```

### Higher-Order Functions

```clojure
;; Composition
(def process (comp str/upper-case str/trim))
(process "  hello  ")  ; => "HELLO"

;; Partial application
(def add-five (partial + 5))
(add-five 10)  ; => 15

;; Multiple transforms
((juxt :name :age) {:name "Alice" :age 30})
; => ["Alice" 30]
```

### Control Flow

```clojure
;; when: single truthy branch
(when (valid? user)
  (save user))

;; if-let: bind and branch
(if-let [user (find-user id)]
  (process user)
  (handle-not-found))

;; case: compile-time constants (fast)
(case status
  :pending (handle-pending)
  :active (handle-active)
  (handle-unknown))

;; cond: complex conditions
(cond
  (neg? n) "negative"
  (pos? n) "positive"
  :else "zero")
```

## Naming Conventions

```clojure
;; kebab-case for vars and functions
(def max-retry-attempts 3)
(defn calculate-total-price [items] ...)

;; Predicates end with ?
(defn valid-email? [email] ...)

;; Side-effecting functions end with !
(defn save-user! [user] ...)
(defn reset-counter! [] ...)

;; Dynamic vars use earmuffs
(def ^:dynamic *config* {...})

;; CamelCase for protocols and records
(defprotocol Storage ...)
(defrecord DatabaseStorage [conn] ...)

;; Private functions use defn-
(defn- parse [input] ...)      ; Internal helper
(defn process [data] ...)      ; Public API
```

## Anti-Patterns

| Avoid | Do Instead |
|-------|------------|
| Mutable state everywhere | Use atoms sparingly, prefer pure functions |
| `(if (not x) ...)` | `(if-not x ...)` or `(when-not x ...)` |
| `(not (= a b))` | `(not= a b)` |
| `(first (filter pred coll))` | `(some pred coll)` |
| Deep nesting | Threading macros `->`, `->>` |
| `(into [] (map f coll))` | `(mapv f coll)` |
| String concatenation | `(str a b c)` or `(format ...)` |
| `(nth coll 0)` | `(first coll)` |
| Manual recursion | `reduce`, `iterate`, `loop/recur` |
| `def` inside functions | `let` bindings |

