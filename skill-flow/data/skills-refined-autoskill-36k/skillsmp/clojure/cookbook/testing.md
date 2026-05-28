# Clojure Testing Cookbook

Practical recipes for testing Clojure applications with clojure.test, Kaocha, and test.check.

---

## Write Basic Unit Tests

**Problem**: You need to write simple unit tests for your Clojure functions.

**Solution**:
```clojure
(ns myapp.core-test
  (:require [clojure.test :refer [deftest is testing are]]
            [myapp.core :as core]))

;; Simple test
(deftest test-add
  (is (= 3 (core/add 1 2))))

;; Grouped assertions
(deftest test-calculation
  (testing "addition"
    (is (= 3 (core/add 1 2)))
    (is (= 0 (core/add 0 0))))
  (testing "multiplication"
    (is (= 6 (core/multiply 2 3)))
    (is (= 0 (core/multiply 0 5)))))
```

**Tip**: Use `testing` blocks to group related assertions and provide better error messages when tests fail.

---

## Test Different Assertion Types

**Problem**: You need to test equality, truthiness, types, and exceptions.

**Solution**:
```clojure
;; Equality
(is (= expected actual))

;; Truthiness
(is (true? value))
(is (false? value))
(is (nil? value))
(is (some? value))

;; Type checking
(is (vector? value))
(is (instance? Exception value))

;; Exception testing
(is (thrown? ArithmeticException (/ 1 0)))
(is (thrown-with-msg? Exception #"not found" (find-missing)))

;; Custom message
(is (= 4 (+ 2 2)) "Math is broken!")
```

**Tip**: Add custom messages to assertions to make failures easier to understand, especially in complex test scenarios.

---

## Write Table-Driven Tests

**Problem**: You need to test the same function with multiple input/output pairs without duplicating test code.

**Solution**:
```clojure
(deftest test-fizzbuzz
  (are [n expected]
    (= expected (fizzbuzz n))
    1  "1"
    3  "Fizz"
    5  "Buzz"
    15 "FizzBuzz"
    30 "FizzBuzz"))
```

**Tip**: Use `are` for table-driven tests where you have many similar test cases. The first row defines the pattern, and subsequent rows provide the test data.

---

## Set Up Test Fixtures

**Problem**: You need to run setup and teardown code before and after tests.

**Solution**:
```clojure
;; Per-test fixture
(defn setup-fixture [f]
  (println "Setup")
  (f)  ; Run the test
  (println "Teardown"))

(use-fixtures :each setup-fixture)

;; Per-namespace fixture
(defn db-fixture [f]
  (with-open [conn (connect-db)]
    (binding [*db* conn]
      (f))))

(use-fixtures :once db-fixture)

;; Composing fixtures
(use-fixtures :each
  (compose-fixtures setup-fixture logging-fixture))
```

**Tip**: Use `:each` for fixtures that need to run before/after every test, and `:once` for expensive setup that can be shared across all tests in a namespace.

---

## Test Async Operations

**Problem**: You need to test asynchronous code with promises or core.async channels.

**Solution**:
```clojure
;; Test async with promises
(deftest test-async-operation
  (let [p (promise)]
    (async-fn #(deliver p %))
    (is (= :expected (deref p 1000 :timeout)))))

;; Test core.async
(require '[clojure.core.async :as a])

(deftest test-channel
  (let [ch (a/chan)
        result (a/go
                 (a/>! ch :value)
                 (a/<! ch))]
    (is (= :value (a/<!! result)))))
```

**Tip**: Always use timeouts when dereferencing promises or blocking on channels to prevent tests from hanging indefinitely.

---

## Configure Kaocha Test Runner

**Problem**: You need a modern test runner with watch mode and better output.

**Solution**:
```clojure
;; deps.edn
{:aliases
 {:test/run
  {:extra-paths ["test"]
   :extra-deps {lambdaisland/kaocha {:mvn/version "1.91.1392"}}
   :exec-fn kaocha.runner/exec-fn
   :exec-args {:fail-fast? true}}

  :test/watch
  {:extra-paths ["test"]
   :extra-deps {lambdaisland/kaocha {:mvn/version "1.91.1392"}}
   :exec-fn kaocha.runner/exec-fn
   :exec-args {:watch? true :fail-fast? true}}}}
```

```clojure
;; tests.edn
#kaocha/v1
{:tests [{:id :unit
          :test-paths ["test"]
          :source-paths ["src"]}]

 :plugins [:kaocha.plugin/capture-output
           :kaocha.plugin/profiling]

 :capture-output? true
 :fail-fast? true
 :color? true}
```

**Tip**: Use separate aliases for running tests once vs. in watch mode. Watch mode automatically re-runs tests when files change.

---

## Run Tests with Kaocha

**Problem**: You need to run tests with different options like focusing on specific tests or skipping slow ones.

**Solution**:
```bash
# Run all tests
clojure -X:test/run

# Watch mode
clojure -X:test/run :watch? true

# Specific namespace
clojure -X:test/run :focus '[:unit myapp.core-test]'

# Fail fast
clojure -X:test/run :fail-fast? true

# Skip slow tests
clojure -X:test/run :skip-meta :slow
```

**Tip**: Use `:fail-fast? true` during development to stop at the first failure and fix issues quickly.

---

## Filter Tests with Metadata

**Problem**: You want to mark and selectively run slow, integration, or database tests.

**Solution**:
```clojure
;; Mark slow tests
(deftest ^:slow test-integration
  (is (= :ok (slow-operation))))

;; Skip with --skip-meta :slow
;; Run only with --focus-meta :slow

;; Mark with multiple tags
(deftest ^:slow ^:integration ^:db test-db
  ...)
```

**Tip**: Tag slow tests with `^:slow` and skip them during regular development, but include them in CI pipelines.

---

## Build Test Data

**Problem**: You need to create test data with sensible defaults but allow customization.

**Solution**:
```clojure
(defn make-user
  ([] (make-user {}))
  ([overrides]
   (merge {:id (random-uuid)
           :name "Test User"
           :email "test@example.com"
           :created-at (java.util.Date.)}
          overrides)))

(deftest test-with-builder
  (let [admin (make-user {:role :admin})]
    (is (= :admin (:role admin)))))
```

**Tip**: Test data builders make tests more readable and maintainable. Override only the fields that matter for each specific test.

---

## Test Side Effects

**Problem**: You need to test code that performs side effects like logging or HTTP calls.

**Solution**:
```clojure
;; Capture side effects
(deftest test-logging
  (let [logs (atom [])]
    (with-redefs [log/info (fn [& args] (swap! logs conj args))]
      (do-something)
      (is (= [["Operation complete"]] @logs)))))

;; Mock external calls
(deftest test-api-call
  (with-redefs [http/get (fn [_] {:status 200 :body "{}"})]
    (is (= :ok (fetch-data)))))
```

**Tip**: Use `with-redefs` to temporarily replace functions during tests. Capture side effects in atoms or return fixed values for external dependencies.

---

## Test and Inspect Exceptions

**Problem**: You need to verify that code throws exceptions with specific types and messages.

**Solution**:
```clojure
(deftest test-validation-errors
  ;; Throws any exception
  (is (thrown? Exception (validate nil)))

  ;; Throws with message pattern
  (is (thrown-with-msg? IllegalArgumentException
                        #"must be positive"
                        (validate -1)))

  ;; Capture and inspect exception
  (let [ex (try
             (validate nil)
             (catch Exception e e))]
    (is (= ::validation-error (-> ex ex-data :type)))
    (is (contains? (ex-data ex) :field))))
```

**Tip**: For detailed exception testing, catch the exception and inspect its `ex-data` to verify error details beyond just the message.

---

## Test Private Functions

**Problem**: You need to test a private function directly.

**Solution**:
```clojure
;; Access private var
(deftest test-private
  (let [private-fn #'myapp.core/private-helper]
    (is (= :expected (private-fn :input)))))

;; Better: test through public API
```

**Tip**: While you can test private functions using `#'namespace/private-fn`, it's usually better to test them indirectly through the public API.

---

## Write Property-Based Tests

**Problem**: You want to test properties that should hold for many generated inputs, not just specific examples.

**Solution**:
```clojure
(require '[clojure.test.check :as tc]
         '[clojure.test.check.generators :as gen]
         '[clojure.test.check.properties :as prop]
         '[clojure.test.check.clojure-test :refer [defspec]])

(defspec test-reverse-idempotent 100
  (prop/for-all [v (gen/vector gen/int)]
    (= v (reverse (reverse v)))))

(defspec test-sort-idempotent 100
  (prop/for-all [v (gen/vector gen/int)]
    (= (sort v) (sort (sort v)))))
```

**Tip**: Property-based testing is great for testing invariants like idempotency, commutativity, or round-trip conversions. The number (100) specifies how many random inputs to test.

---

## Create Custom Generators

**Problem**: You need to generate complex domain-specific test data for property-based tests.

**Solution**:
```clojure
;; Composite generator
(def user-gen
  (gen/hash-map
    :id gen/uuid
    :name (gen/not-empty gen/string-alphanumeric)
    :age (gen/choose 0 120)))

(defspec test-user-processing 50
  (prop/for-all [user user-gen]
    (let [result (process-user user)]
      (and (contains? result :processed)
           (= (:id user) (:id result))))))
```

**Tip**: Compose generators from simpler ones using `gen/hash-map`, `gen/vector`, and other combinators. Add constraints with functions like `gen/not-empty` and `gen/choose`.

---

## Organize Test Code

**Problem**: You need a clear structure for organizing tests, fixtures, and helpers.

**Solution**:
```text
test/
├── myapp/
│   ├── core_test.clj
│   ├── db_test.clj
│   ├── api_test.clj
│   └── integration_test.clj
├── fixtures/
│   └── sample_data.clj
└── helpers/
    └── test_utils.clj
```

```clojure
;; Unit tests mirror source structure
;; src/myapp/core.clj -> test/myapp/core_test.clj

(ns myapp.core-test
  (:require [clojure.test :refer :all]
            [myapp.core :as core]
            [myapp.test-helpers :as h]))
```

**Tip**: Mirror your source directory structure in tests with `_test.clj` suffix. Keep shared fixtures and helpers in separate directories.

---

## Create Shared Test Utilities

**Problem**: You need to share common test setup code, fixtures, and macros across multiple test namespaces.

**Solution**:
```clojure
;; test/myapp/test_helpers.clj
(ns myapp.test-helpers
  (:require [clojure.test :refer :all]))

(defn with-test-db [f]
  (let [db (create-test-db)]
    (try
      (binding [*db* db]
        (f))
      (finally
        (destroy-test-db db)))))

(defmacro with-timeout [ms & body]
  `(let [f# (future ~@body)]
     (deref f# ~ms :timeout)))
```

**Tip**: Create a dedicated test helpers namespace for shared fixtures, test data builders, and testing macros. This reduces duplication and makes tests more maintainable.

---
