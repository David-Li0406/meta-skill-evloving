# Macros & Metaprogramming Cookbook

Transform code at compile time with macros, create DSLs, and master Clojure's metaprogramming capabilities.

---

## Choosing Between Macros and Functions

**Problem**: You need to decide whether to write a macro or a function for code transformation.

**Solution**:
```clojure
;; BAD: macro for simple transformation
(defmacro add-one [x] `(+ ~x 1))

;; GOOD: function instead
(defn add-one [x] (+ x 1))
```

**Tip**: Only use macros when you need: (1) new control flow, (2) compile-time code transformation, (3) DSLs with custom syntax, or (4) performance optimization by avoiding function call overhead. Functions are simpler, composable, and can be passed as values.

---

## Basic Syntax Quoting

**Problem**: You need to understand the difference between quote and syntax quote for writing macros.

**Solution**:
```clojure
;; Quote: literal list
'(a b c)         ; => (a b c)

;; Syntax quote: namespace-qualified + unquoting
`(a b c)         ; => (user/a user/b user/c)

;; Unquote: insert value
(let [x 1]
  `(a ~x c))     ; => (user/a 1 user/c)

;; Unquote-splicing: insert sequence elements
(let [xs [1 2 3]]
  `(a ~@xs b))   ; => (user/a 1 2 3 user/b)
```

**Tip**: Use syntax quote (`) for macros because it auto-qualifies symbols. Use unquote (~) to insert values and unquote-splicing (~@) to insert multiple elements from a sequence.

---

## Creating a Simple Control Flow Macro

**Problem**: You want to create a custom control flow that executes code when a condition is false.

**Solution**:
```clojure
(defmacro unless [pred & body]
  `(if (not ~pred)
     (do ~@body)))

;; Usage
(unless (empty? items)
  (process items)
  (notify))

;; Expands to
(if (not (empty? items))
  (do (process items)
      (notify)))
```

**Tip**: Use `~@` (unquote-splicing) with `body` to insert multiple expressions into the generated code.

---

## Avoiding Variable Name Collisions

**Problem**: Your macro introduces a local binding that could shadow a variable from the calling code.

**Solution**:
```clojure
;; BAD: name collision
(defmacro with-value [v & body]
  `(let [x ~v]     ; x might shadow user's x!
     ~@body))

;; GOOD: auto-gensym with #
(defmacro with-value [v & body]
  `(let [x# ~v]    ; x# generates unique name
     ~@body))

;; Or explicit gensym
(defmacro with-value [v & body]
  (let [sym (gensym "x")]
    `(let [~sym ~v]
       ~@body)))
```

**Tip**: Use the `#` suffix (auto-gensym) for generated symbols in syntax-quoted forms. This creates a unique symbol that won't conflict with user code.

---

## Timing Code Execution

**Problem**: You want to measure how long a block of code takes to execute.

**Solution**:
```clojure
(defmacro with-timing [& body]
  `(let [start# (System/currentTimeMillis)]
     (try
       ~@body
       (finally
         (println "Elapsed:"
           (- (System/currentTimeMillis) start#)
           "ms")))))

(with-timing
  (Thread/sleep 100)
  :done)
; Elapsed: 100 ms
; => :done
```

**Tip**: Use auto-gensym (`start#`) to avoid variable capture and `finally` to ensure timing is printed even if the body throws an exception.

---

## Debugging Macro Expansions

**Problem**: You need to see what code your macro generates to debug or understand its behavior.

**Solution**:
```clojure
;; Expand one level
(macroexpand '(unless true (println "hi")))
; => (if (clojure.core/not true) (do (println "hi")))

;; Expand all levels
(macroexpand-all '(unless true (println "hi")))

;; Pretty print
(clojure.pprint/pprint
  (macroexpand '(my-macro ...)))
```

**Tip**: Use `macroexpand` to expand one level of macros, `macroexpand-all` for complete expansion, and `clojure.pprint/pprint` for readable output.

---

## Preventing Double Evaluation

**Problem**: Your macro evaluates an expression multiple times, causing side effects or expensive computations to run repeatedly.

**Solution**:
```clojure
;; MISTAKE: Double evaluation
(defmacro square [x]
  `(* ~x ~x))

(square (expensive-fn))  ; Calls expensive-fn TWICE!

;; FIX: Bind once
(defmacro square [x]
  `(let [x# ~x]
     (* x# x#)))
```

**Tip**: When using an argument multiple times in generated code, bind it to a gensym'd variable first to ensure it's only evaluated once.

---

## Conditional Compilation

**Problem**: You want code to compile only when certain conditions are met (e.g., development mode).

**Solution**:
```clojure
(defmacro when-dev [& body]
  (when (= "dev" (System/getenv "ENV"))
    `(do ~@body)))

;; Only compiles in dev
(when-dev
  (println "Debug mode"))
```

**Tip**: Since macros run at compile time, you can check environment variables or other conditions to decide whether to include code in the compiled output.

---

## Resource Management Pattern

**Problem**: You need to ensure a resource is properly closed after use, similar to try-with-resources.

**Solution**:
```clojure
(defmacro with-resource [binding & body]
  `(let [~(first binding) ~(second binding)]
     (try
       ~@body
       (finally
         (close! ~(first binding))))))

;; Usage
(with-resource [conn (connect)]
  (query conn "SELECT ..."))
```

**Tip**: Use `finally` to guarantee cleanup code runs even if the body throws an exception. This pattern is useful for files, connections, and other resources.

---

## Nil-Safe Threading Macros

**Problem**: You want to thread values through functions but stop if any intermediate result is nil.

**Solution**:
```clojure
(defmacro ->? [expr & forms]
  "Thread if not nil"
  `(some-> ~expr ~@forms))

(defmacro ->>? [expr & forms]
  "Thread-last if not nil"
  `(some->> ~expr ~@forms))
```

**Tip**: These macros are actually just aliases for the built-in `some->` and `some->>` macros, which already provide this functionality.

---

## Context-Rich Assertions

**Problem**: You want assertions that provide meaningful error messages with relevant context when they fail.

**Solution**:
```clojure
(defmacro assert-with [test msg & ctx]
  `(when-not ~test
     (throw (ex-info ~msg
              (hash-map ~@ctx)))))

(assert-with (pos? x) "x must be positive"
  :x x
  :context "validation")
```

**Tip**: Use `ex-info` to create exceptions with structured data. The alternating key-value pairs in `ctx` become a map of context information.

---

## Accessing Call Site Information

**Problem**: You need to know about local bindings or the form being expanded at the macro call site.

**Solution**:
```clojure
;; &form: the actual form being expanded
;; &env: local bindings at expansion site

(defmacro debug [expr]
  `(let [result# ~expr]
     (println "Form:" '~expr)
     (println "Result:" result#)
     result#))

(defmacro locals []
  "Return map of local bindings"
  (into {}
    (for [k (keys &env)]
      [`'~k k])))

(let [x 1 y 2]
  (locals))
; => {x 1, y 2}
```

**Tip**: `&env` contains a map of local bindings at the macro expansion site, and `&form` contains the full form with metadata (like line numbers).

---

## Extracting Source Location

**Problem**: You want to include file and line number information in logged messages or errors.

**Solution**:
```clojure
(defmacro log-location [msg]
  (let [{:keys [line column]} (meta &form)]
    `(println ~(str "[" line ":" column "]") ~msg)))
```

**Tip**: The `&form` special variable includes metadata about where the macro was called, including `:line` and `:column` information.

---

## Anaphoric If Macro

**Problem**: You want to reuse the result of a test expression in the then clause without re-evaluating it.

**Solution**:
```clojure
;; 'it' bound to test result
(defmacro if-it [test then else]
  `(let [~'it ~test]
     (if ~'it ~then ~else)))

(if-it (find-user id)
  (process it)    ; 'it' is the found user
  (not-found))

;; 'aif' - anaphoric if
(defmacro aif [test then & [else]]
  `(let [~'it ~test]
     (if ~'it ~then ~else)))
```

**Tip**: Use `~'it` (unquote a plain symbol) to introduce an intentionally unhygienic binding that users can reference. This violates normal macro hygiene rules but is occasionally useful.

---

## Building a Simple Query DSL

**Problem**: You want to create a readable domain-specific language for database queries.

**Solution**:
```clojure
(defmacro query [table & clauses]
  (let [parsed (parse-clauses clauses)]
    `(execute-query
       {:table ~(keyword table)
        :where ~(:where parsed)
        :select ~(:select parsed)
        :order ~(:order parsed)})))

(defn- parse-clauses [clauses]
  (reduce
    (fn [acc [k & v]]
      (assoc acc k (vec v)))
    {}
    (partition-by keyword? clauses)))

;; Usage
(query users
  :where {:active true}
  :select [:name :email]
  :order [:created-at :desc])
```

**Tip**: Split complex macros into a macro part (handling code generation) and helper functions (handling parsing and data transformation). Helper functions are easier to test.

---

## Creating a Mini Test Framework

**Problem**: You want to define tests with a clean syntax and automatic pass/fail reporting.

**Solution**:
```clojure
(defmacro deftest+ [name & body]
  `(defn ~name []
     (try
       ~@body
       (println "PASS:" '~name)
       (catch Exception e#
         (println "FAIL:" '~name)
         (println "  " (.getMessage e#))))))

(defmacro expect [expr]
  `(when-not ~expr
     (throw (ex-info "Expectation failed"
              {:expr '~expr}))))

(deftest+ test-math
  (expect (= 4 (+ 2 2)))
  (expect (pos? 1)))
```

**Tip**: Use `'~name` to capture the test name as a quoted symbol for display, and combine multiple macros to create a cohesive DSL.

---

## Testing Macros

**Problem**: You need to verify that your macros both expand correctly and behave as expected.

**Solution**:
```clojure
(deftest test-my-macro
  ;; Test expansion
  (is (= '(if (not x) (do y))
         (macroexpand-1 '(unless x y))))

  ;; Test behavior
  (is (= :executed (unless false :executed)))
  (is (nil? (unless true :not-executed))))
```

**Tip**: Test both the expansion (what code the macro generates) and the runtime behavior (what happens when you run the generated code). Use `macroexpand-1` for expansion tests.

---
