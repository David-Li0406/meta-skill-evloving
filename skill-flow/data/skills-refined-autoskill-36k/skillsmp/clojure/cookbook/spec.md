# clojure.spec Cookbook

Data validation, generative testing, and runtime checking for Clojure.

---

## Setup clojure.spec

**Problem**: You need to import the clojure.spec libraries for validation and testing.

**Solution**:
```clojure
(require '[clojure.spec.alpha :as s]
         '[clojure.spec.gen.alpha :as gen]
         '[clojure.spec.test.alpha :as stest])
```

**Tip**: Use consistent aliases (`s`, `gen`, `stest`) for readability across your codebase.

---

## Validate with Predicates

**Problem**: You need to validate data against simple predicates like integers, strings, and custom constraints.

**Solution**:
```clojure
;; Define specs with predicates
(s/def ::age (s/and int? #(>= % 0) #(< % 150)))
(s/def ::name (s/and string? #(not (empty? %))))
(s/def ::email (s/and string? #(re-matches #".+@.+\..+" %)))

;; Using built-in predicates
(s/def ::id uuid?)
(s/def ::score double?)
(s/def ::active? boolean?)

;; Validate
(s/valid? ::age 25)     ; => true
(s/valid? ::age -5)     ; => false
(s/valid? ::age "25")   ; => false

;; Get explanation
(s/explain ::age -5)
; -5 - failed: (>= % 0) spec: :user/age

;; Get explanation data
(s/explain-data ::age -5)
; {:clojure.spec.alpha/problems [...] ...}
```

**Tip**: Use `s/explain` during development to understand validation failures, and `s/explain-data` in production for programmatic error handling.

---

## Validate Against a Set of Values

**Problem**: You need to restrict a value to a specific set of allowed options.

**Solution**:
```clojure
(s/def ::status #{:pending :active :done :cancelled})
(s/def ::color #{:red :green :blue})

(s/valid? ::status :active)  ; => true
(s/valid? ::status :unknown) ; => false
```

**Tip**: Sets are the simplest way to define enum-like specs in Clojure. They're clear and self-documenting.

---

## Allow Nil Values

**Problem**: You need to make a spec optional by allowing nil values.

**Solution**:
```clojure
(s/def ::optional-name (s/nilable string?))

(s/valid? ::optional-name nil)     ; => true
(s/valid? ::optional-name "Alice") ; => true
```

**Tip**: Use `s/nilable` when a field can be absent or explicitly nil. For optional map keys, use `:opt` in `s/keys` instead.

---

## Validate Maps with Required and Optional Keys

**Problem**: You need to validate maps with specific required and optional keys.

**Solution**:
```clojure
;; Required and optional keys (qualified)
(s/def ::user
  (s/keys :req [::id ::name ::email]
          :opt [::age ::phone]))

;; Unqualified keys (for external data like JSON)
(s/def ::api-user
  (s/keys :req-un [::id ::name ::email]
          :opt-un [::age]))

;; Validates both structure AND value specs
(s/valid? ::user
  {::id (random-uuid)
   ::name "Alice"
   ::email "alice@example.com"})
; => true

;; Missing required key
(s/explain ::user {::name "Alice"})
; ... missing required keys: [:user/id :user/email]
```

**Tip**: Use `:req-un` and `:opt-un` for unqualified keys when working with external APIs or JSON data.

---

## Validate Collections

**Problem**: You need to validate homogeneous collections with type and size constraints.

**Solution**:
```clojure
;; Homogeneous collection
(s/def ::numbers (s/coll-of int?))
(s/def ::user-ids (s/coll-of uuid? :kind set?))
(s/def ::scores (s/coll-of double? :min-count 1 :max-count 100))

;; Vector specifically
(s/def ::point (s/coll-of number? :kind vector? :count 3))

;; Map of specific key/value types
(s/def ::config (s/map-of keyword? string?))

;; Tuples (fixed-size heterogeneous)
(s/def ::name-age (s/tuple string? int?))
(s/valid? ::name-age ["Alice" 30]) ; => true
```

**Tip**: Use `:kind` to restrict collection type (vector?, set?, list?), and `:min-count`/`:max-count`/`:count` for size constraints.

---

## Match Sequences with Regex Operators

**Problem**: You need to validate sequences with complex patterns like optional parts and alternatives.

**Solution**:
```clojure
;; cat: concatenation (named parts)
(s/def ::http-request
  (s/cat :method #{:get :post :put :delete}
         :url string?
         :body (s/? map?)))  ; optional

(s/conform ::http-request [:get "/api/users"])
; => {:method :get :url "/api/users"}

(s/conform ::http-request [:post "/api/users" {:name "Alice"}])
; => {:method :post :url "/api/users" :body {:name "Alice"}}

;; alt: alternatives
(s/def ::id-or-name
  (s/alt :id int?
         :name string?))

(s/conform ::id-or-name [42])
; => [:id 42]

;; *: zero or more
(s/def ::args (s/* string?))

;; +: one or more
(s/def ::args+ (s/+ string?))

;; ?: zero or one
(s/def ::maybe-int (s/? int?))
```

**Tip**: Regex operators (`s/cat`, `s/alt`, `s/*`, `s/+`, `s/?`) work on sequences and return structured data via `s/conform`.

---

## Choose Between Alternatives with Or

**Problem**: You need to accept one of several types with labeled alternatives.

**Solution**:
```clojure
;; s/or: labeled alternatives
(s/def ::name-or-id
  (s/or :name string?
        :id int?))

(s/conform ::name-or-id "Alice")  ; => [:name "Alice"]
(s/conform ::name-or-id 42)       ; => [:id 42]

;; s/and: all must pass
(s/def ::big-even
  (s/and int?
         even?
         #(> % 1000)))
```

**Tip**: `s/or` returns a tagged tuple `[tag value]` so you can distinguish which alternative matched. Use `s/and` to combine multiple predicates.

---

## Specify Function Contracts

**Problem**: You need to define contracts for function arguments, return values, and relationships.

**Solution**:
```clojure
(defn calculate-discount [price percentage]
  (* price (- 1 (/ percentage 100.0))))

(s/fdef calculate-discount
  :args (s/cat :price (s/and number? pos?)
               :percentage (s/int-in 0 101))
  :ret (s/and number? #(>= % 0))
  :fn (fn [{:keys [args ret]}]
        (<= ret (:price args))))

;; Check function manually
(s/valid? (:args (s/get-spec `calculate-discount))
          [100 20])
; => true
```

**Tip**: The `:fn` spec validates relationships between args and return value, enabling powerful invariant checking.

---

## Enable Runtime Function Checking

**Problem**: You want to catch invalid function calls during development.

**Solution**:
```clojure
;; Turn on runtime checking (dev only!)
(stest/instrument `calculate-discount)

(calculate-discount 100 20)  ; Works
(calculate-discount -100 20) ; Throws spec error!

;; Turn off
(stest/unstrument `calculate-discount)

;; Instrument all
(stest/instrument)
```

**Tip**: Only use instrumentation in development—it adds runtime overhead. Never ship instrumented code to production.

---

## Generate Sample Data

**Problem**: You need to generate sample data that conforms to your specs for testing.

**Solution**:
```clojure
;; Generate sample values
(gen/sample (s/gen ::age) 5)
; => (0 1 0 2 4)

(gen/sample (s/gen ::status) 5)
; => (:pending :active :done :pending :cancelled)

(gen/sample (s/gen ::user) 3)
; => ({:user/id #uuid "..." :user/name "Fy" ...} ...)

;; Exercise: generate and conform
(s/exercise ::name-or-id 5)
; => ([("" "") [:name ""]] [("a") [:name "a"]] ...)
```

**Tip**: Specs automatically generate sample data. Use `gen/sample` for quick data, and `s/exercise` to see both generated and conformed values.

---

## Write Property-Based Tests

**Problem**: You want to test functions with many random inputs to find edge cases.

**Solution**:
```clojure
(require '[clojure.test.check.clojure-test :refer [defspec]]
         '[clojure.test.check.properties :as prop])

;; Test function against spec
(defspec test-calculate-discount 100
  (prop/for-all [price (s/gen (s/and number? pos?))
                 pct (s/gen (s/int-in 0 101))]
    (let [result (calculate-discount price pct)]
      (and (>= result 0)
           (<= result price)))))

;; Run spec check
(stest/check `calculate-discount)
```

**Tip**: Property-based testing with generated data can find bugs that example-based testing misses. Run `stest/check` to automatically test function specs.

---

## Create Custom Generators

**Problem**: The default generator doesn't create realistic data for your domain.

**Solution**:
```clojure
;; Override default generator
(s/def ::email
  (s/with-gen
    (s/and string? #(re-matches #".+@.+\..+" %))
    #(gen/fmap
       (fn [[user domain tld]]
         (str user "@" domain "." tld))
       (gen/tuple
         (gen/such-that not-empty gen/string-alphanumeric)
         (gen/such-that not-empty gen/string-alphanumeric)
         (gen/elements ["com" "org" "net"])))))

;; Generator from fn
(s/def ::timestamp
  (s/with-gen
    inst?
    #(gen/fmap
       (fn [ms] (java.util.Date. ms))
       (gen/choose 0 (System/currentTimeMillis)))))
```

**Tip**: Use `s/with-gen` to provide custom generators for domain-specific data. Combine `gen/fmap`, `gen/tuple`, and `gen/such-that` to build complex generators.

---

## Validate Polymorphic Data

**Problem**: You need different validation rules based on a discriminator field.

**Solution**:
```clojure
;; Dispatch on :type field
(defmulti event-type :type)

(defmethod event-type :login [_]
  (s/keys :req-un [::type ::user-id ::timestamp]))

(defmethod event-type :purchase [_]
  (s/keys :req-un [::type ::user-id ::item-id ::amount]))

(defmethod event-type :logout [_]
  (s/keys :req-un [::type ::user-id]))

(s/def ::event (s/multi-spec event-type :type))

;; Validates based on :type
(s/valid? ::event
  {:type :login
   :user-id "u123"
   :timestamp (java.util.Date.)})
; => true

(s/valid? ::event
  {:type :purchase
   :user-id "u123"
   :item-id "i456"
   :amount 99.99})
; => true
```

**Tip**: `s/multi-spec` with multimethods enables type-based validation for polymorphic data structures like events or commands.

---

## Transform Data with Conform

**Problem**: You need to validate and transform data into a structured format.

**Solution**:
```clojure
;; conform: validate and transform
(s/conform ::name-or-id "Alice")
; => [:name "Alice"]

;; Invalid returns :clojure.spec.alpha/invalid
(s/conform ::age "not-a-number")
; => :clojure.spec.alpha/invalid

;; Check conformity
(let [result (s/conform ::age 25)]
  (if (= result ::s/invalid)
    (println "Invalid!")
    (println "Valid:" result)))

;; unform: reverse conform
(s/unform ::name-or-id [:name "Alice"])
; => "Alice"
```

**Tip**: `s/conform` returns transformed/tagged data on success or `::s/invalid` on failure. Use it to parse and destructure validated data. `s/unform` reverses the transformation.

---

## Organize Specs in a Central Namespace

**Problem**: You need to organize domain specs in a maintainable way.

**Solution**:
```clojure
;; specs.clj - Central spec definitions
(ns myapp.specs
  (:require [clojure.spec.alpha :as s]))

;; Domain specs
(s/def ::user-id uuid?)
(s/def ::username (s/and string? #(re-matches #"[a-z0-9_]{3,20}" %)))
(s/def ::email (s/and string? #(re-matches #".+@.+\..+" %)))

;; Entity specs
(s/def ::user
  (s/keys :req [::user-id ::username ::email]
          :opt [::display-name ::avatar-url]))

;; API specs (unqualified for JSON)
(s/def ::api-user
  (s/keys :req-un [::user-id ::username ::email]
          :opt-un [::display-name ::avatar-url]))
```

**Tip**: Keep all specs in a dedicated namespace (e.g., `myapp.specs`). Define domain primitives first, then compose them into entity specs.

---

## Create Validation Helpers

**Problem**: You need reusable functions to validate and handle errors consistently.

**Solution**:
```clojure
(defn validate! [spec data]
  (if (s/valid? spec data)
    data
    (throw (ex-info "Validation failed"
                    {:spec spec
                     :problems (s/explain-data spec data)}))))

(defn validate [spec data]
  (if (s/valid? spec data)
    {:ok data}
    {:error (s/explain-str spec data)}))
```

**Tip**: Create helper functions for common patterns. `validate!` for throwing errors, `validate` for returning result maps.

---

## Assert Data Conforms to Spec

**Problem**: You want runtime assertions that data matches a spec within your functions.

**Solution**:
```clojure
;; Enable spec assertions
(s/check-asserts true)

;; Use in code
(defn process-user [user]
  (s/assert ::user user)
  ;; ... process ...
  )

;; Throws detailed error if invalid
```

**Tip**: Enable `s/check-asserts` in development for automatic validation. Disable in production for performance. `s/assert` throws with detailed spec errors.

---
