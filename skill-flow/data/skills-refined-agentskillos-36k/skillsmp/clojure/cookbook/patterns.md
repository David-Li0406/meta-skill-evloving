# Functional Patterns & Data Structures Cookbook

Essential patterns for working with Clojure's data structures, sequences, and functional programming idioms.

---

## Choosing the Right Collection

**Problem**: You need to select the appropriate data structure for your use case.

**Solution**:
```clojure
;; Vectors: indexed access, append at end
(def users ["Alice" "Bob" "Charlie"])
(get users 0)       ; => "Alice"
(conj users "Dave") ; => ["Alice" "Bob" "Charlie" "Dave"]
(nth users 1)       ; => "Bob"

;; Lists: prepend efficient, sequential access
(def queue '(1 2 3))
(cons 0 queue)      ; => (0 1 2 3)
(conj queue 0)      ; => (0 1 2 3) - prepends!

;; Maps: key-value lookup
(def user {:id 1 :name "Alice" :email "a@ex.com"})
(:name user)        ; => "Alice" (keyword as fn)
(get user :missing "default") ; => "default"

;; Sets: membership testing, uniqueness
(def tags #{"clojure" "functional" "jvm"})
(contains? tags "clojure") ; => true
(tags "clojure")           ; => "clojure" (set as fn)
```

**Tip**: Use vectors for indexed access, lists for sequential processing, maps for lookups, and sets for membership testing.

---

## Basic Collection Operations

**Problem**: You need to add, remove, or combine collection elements.

**Solution**:
```clojure
;; Adding
(conj [1 2] 3)           ; => [1 2 3]
(conj #{1 2} 3)          ; => #{1 2 3}
(assoc {:a 1} :b 2)      ; => {:a 1 :b 2}

;; Removing
(disj #{1 2 3} 2)        ; => #{1 3}
(dissoc {:a 1 :b 2} :a)  ; => {:b 2}
(pop [1 2 3])            ; => [1 2]

;; Combining
(concat [1 2] [3 4])     ; => (1 2 3 4)
(merge {:a 1} {:b 2})    ; => {:a 1 :b 2}
(merge-with + {:a 1} {:a 2}) ; => {:a 3}

;; Transforming
(mapv inc [1 2 3])       ; => [2 3 4] (eager vector)
(filterv even? [1 2 3 4]); => [2 4]
(reduce + [1 2 3 4])     ; => 10
```

**Tip**: Use `conj` for collection-appropriate addition, `assoc` for maps, and `merge-with` for merging maps with conflict resolution.

---

## Keywords as Functions

**Problem**: You need to extract values from maps or use sets as filters.

**Solution**:
```clojure
;; Keywords extract from maps
(:name {:name "Alice" :age 30}) ; => "Alice"
(:missing {:name "Alice"})      ; => nil
(:missing {:name "Alice"} "?")  ; => "?"

;; Sets as predicates
(filter #{:a :b} [:a :b :c :d]) ; => (:a :b)
(remove #{:skip :ignore} items)
```

**Tip**: Keywords and sets implement IFn, making them excellent for map extraction and filtering operations.

---

## Core Sequence Transformations

**Problem**: You need to transform, filter, or reduce sequences.

**Solution**:
```clojure
;; map: transform each element
(map inc [1 2 3])          ; => (2 3 4)
(map :name users)          ; => ("Alice" "Bob")
(map vector [:a :b] [1 2]) ; => ([:a 1] [:b 2])

;; filter/remove: select elements
(filter even? [1 2 3 4])   ; => (2 4)
(remove nil? [1 nil 2])    ; => (1 2)
(filter :active users)     ; truthy :active

;; reduce: fold to single value
(reduce + [1 2 3 4])       ; => 10
(reduce + 100 [1 2 3])     ; => 106 (with init)
(reduce conj [] [1 2 3])   ; => [1 2 3]

;; take/drop: subsequences
(take 3 (range 10))        ; => (0 1 2)
(drop 3 (range 10))        ; => (3 4 5 6 7 8 9)
(take-while pos? [2 1 0 -1]) ; => (2 1)
```

**Tip**: Use `map` for element-wise transforms, `filter` for selection, `reduce` for aggregation, and `take`/`drop` for subsequences.

---

## Grouping and Partitioning

**Problem**: You need to organize sequences into groups or chunks.

**Solution**:
```clojure
;; group-by: map of key -> items
(group-by :type [{:type :a :n 1} {:type :b :n 2} {:type :a :n 3}])
; => {:a [{:type :a :n 1} {:type :a :n 3}]
;     :b [{:type :b :n 2}]}

;; partition: fixed-size chunks
(partition 2 [1 2 3 4 5])     ; => ((1 2) (3 4))
(partition 2 1 [1 2 3 4])     ; => ((1 2) (2 3) (3 4)) step=1
(partition-all 2 [1 2 3 4 5]) ; => ((1 2) (3 4) (5))

;; partition-by: chunk by fn
(partition-by even? [1 3 2 4 5])
; => ((1 3) (2 4) (5))
```

**Tip**: Use `group-by` to categorize items by a key function, `partition` for fixed-size chunks, and `partition-by` to split when a function's return value changes.

---

## Finding and Testing Elements

**Problem**: You need to check if elements exist or meet certain conditions.

**Solution**:
```clojure
;; some: find first truthy
(some even? [1 3 5 6])       ; => true
(some #{:a :b} [:c :a :d])   ; => :a
(some #(when (> % 5) %) [1 3 7 9]) ; => 7

;; every?/not-every?
(every? even? [2 4 6])       ; => true
(not-every? even? [2 3 4])   ; => true

;; not-any?
(not-any? even? [1 3 5])     ; => true
```

**Tip**: `some` returns the first truthy result, not just true/false. Combine with sets or predicates for flexible searching.

---

## Creating Lazy Sequences

**Problem**: You need to work with infinite or large sequences without realizing them all at once.

**Solution**:
```clojure
;; range: lazy infinite or bounded
(range)           ; infinite: 0, 1, 2, ...
(range 5)         ; => (0 1 2 3 4)
(range 1 10 2)    ; => (1 3 5 7 9)

;; repeat/cycle
(take 3 (repeat :x))      ; => (:x :x :x)
(take 5 (cycle [:a :b]))  ; => (:a :b :a :b :a)

;; iterate: f(x), f(f(x)), ...
(take 5 (iterate inc 0))  ; => (0 1 2 3 4)
(take 5 (iterate #(* 2 %) 1)) ; => (1 2 4 8 16)

;; lazy-seq: custom lazy
(defn fibs
  ([] (fibs 0 1))
  ([a b] (lazy-seq (cons a (fibs b (+ a b))))))
(take 10 (fibs)) ; => (0 1 1 2 3 5 8 13 21 34)
```

**Tip**: Lazy sequences are only computed when needed. Always use `take` or similar to limit infinite sequences.

---

## Realizing Lazy Sequences

**Problem**: You need to force evaluation of a lazy sequence for side effects or to cache results.

**Solution**:
```clojure
;; Force evaluation
(doall (map println [1 2 3])) ; Realizes, returns seq
(dorun (map println [1 2 3])) ; Realizes, returns nil
(vec lazy-seq)                ; Realizes into vector
(into [] lazy-seq)            ; Same

;; Chunked sequences (32 elements at a time)
;; Most lazy seqs are chunked for performance
```

**Tip**: Use `doall` when you need the sequence back, `dorun` for side effects only, and `vec`/`into` to convert to concrete collections.

---

## Composable Transducers

**Problem**: You want to compose transformations that work across different contexts without intermediate collections.

**Solution**:
```clojure
;; Transducers separate transformation from data source
(def xf
  (comp
    (filter even?)
    (map inc)
    (take 5)))

;; Apply to different contexts
(into [] xf (range 100))           ; => [1 3 5 7 9]
(transduce xf + (range 100))       ; => 25
(sequence xf (range 100))          ; lazy seq

;; With core.async channels
(require '[clojure.core.async :as a])
(def ch (a/chan 10 xf))
```

**Tip**: Transducers eliminate intermediate sequences and work with collections, channels, and reducers. Compose with `comp`.

---

## Common Transducer Operations

**Problem**: You need to know which sequence operations are available as transducers.

**Solution**:
```clojure
(map f)           ; Transform
(filter pred)     ; Keep matching
(remove pred)     ; Remove matching
(take n)          ; First n
(drop n)          ; Skip first n
(take-while pred) ; Until pred false
(drop-while pred) ; Skip until pred false
(dedupe)          ; Remove consecutive dups
(distinct)        ; Remove all dups
(partition-all n) ; Chunk into vectors
(cat)             ; Flatten one level
(mapcat f)        ; map + flatten
```

**Tip**: Most core sequence functions have transducer arities when called with just their parameters (no collection).

---

## Parallel Reducers

**Problem**: You need to process large collections in parallel.

**Solution**:
```clojure
(require '[clojure.core.reducers :as r])

;; Parallel fold (for large collections)
(r/fold + (r/map inc (r/filter even? large-vec)))

;; fold with combiner
(r/fold
  (fn ([] {})              ; init
      ([a b] (merge a b))) ; combine
  (fn [acc x]              ; reduce
    (assoc acc x true))
  large-coll)
```

**Tip**: Reducers use Java's fork/join for parallel processing. Only beneficial for large collections due to overhead.

---

## For Comprehensions

**Problem**: You need to generate sequences with nested iteration, filtering, and bindings.

**Solution**:
```clojure
;; List comprehension
(for [x [1 2 3]
      y [:a :b]]
  [x y])
; => ([1 :a] [1 :b] [2 :a] [2 :b] [3 :a] [3 :b])

;; With :when filter
(for [x (range 10)
      :when (even? x)]
  (* x x))
; => (0 4 16 36 64)

;; With :let binding
(for [x [1 2 3]
      :let [y (* x x)]
      :when (> y 1)]
  y)
; => (4 9)

;; With :while early termination
(for [x (range 10)
      :while (< x 5)]
  x)
; => (0 1 2 3 4)
```

**Tip**: Use `:when` for filtering, `:let` for intermediate bindings, and `:while` for early termination. `for` is lazy.

---

## Transforming Maps

**Problem**: You need to update keys or values across an entire map.

**Solution**:
```clojure
;; Update values
(update-vals {:a 1 :b 2} inc)     ; => {:a 2 :b 3}
(update-keys {:a 1 :b 2} name)    ; => {"a" 1 "b" 2}

;; Select/rename keys
(select-keys {:a 1 :b 2 :c 3} [:a :b]) ; => {:a 1 :b 2}
(clojure.set/rename-keys {:a 1} {:a :alpha}) ; => {:alpha 1}

;; Deep merge
(defn deep-merge [& maps]
  (apply merge-with
    (fn [a b] (if (map? a) (deep-merge a b) b))
    maps))
```

**Tip**: Use `update-vals` and `update-keys` for bulk transformations, `select-keys` for projection, and custom merge functions for nested structures.

---

## Efficient Map Iteration

**Problem**: You need to iterate over map entries efficiently.

**Solution**:
```clojure
;; Iterate entries
(for [[k v] {:a 1 :b 2}]
  (str k "=" v))
; => (":a=1" ":b=2")

;; reduce-kv (more efficient)
(reduce-kv
  (fn [acc k v] (assoc acc k (inc v)))
  {}
  {:a 1 :b 2})
; => {:a 2 :b 3}
```

**Tip**: `reduce-kv` is more efficient than destructuring with `reduce` or `for` when working with maps, as it avoids creating MapEntry objects.

---

## Tree Navigation with Zippers

**Problem**: You need to navigate and edit nested tree structures functionally.

**Solution**:
```clojure
(require '[clojure.zip :as z])

(def tree [1 [2 3] [4 [5 6]]])
(def loc (z/vector-zip tree))

;; Navigate
(-> loc z/down z/right z/down z/node) ; => 2

;; Edit
(-> loc
    z/down
    z/right
    (z/replace [:new])
    z/root)
; => [1 [:new] [4 [5 6]]]
```

**Tip**: Zippers provide a functional way to navigate and edit trees. Use `z/root` to get the modified tree back after edits.

---
