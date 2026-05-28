# Clojure

**Category**: languages
**Description**: Clojure programming language - dynamic, functional Lisp dialect for JVM with immutable data structures
**Homepage**: https://clojure.org

## Package Detection

### CLOJARS
- `org.clojure/clojure`
- `org.clojure/clojurescript`
- `ring/ring-core`
- `compojure`
- `reagent`

## Configuration Files

- `project.clj` (Leiningen)
- `deps.edn` (tools.deps)
- `build.clj`
- `shadow-cljs.edn`
- `figwheel-main.edn`
- `.lein-env`
- `profiles.clj`

## File Extensions

- `.clj`
- `.cljs` (ClojureScript)
- `.cljc` (cross-platform)
- `.edn`

## Import Detection

### Clojure
**Pattern**: `^\(ns\s+[\w.-]+`
- Namespace declaration
- Example: `(ns my-app.core`

**Pattern**: `\(:require\s+\[`
- Require directive
- Example: `(:require [clojure.string :as str])`

**Pattern**: `\(:import\s+`
- Import Java classes
- Example: `(:import [java.time Instant])`

**Pattern**: `^\(defn\s+\w+`
- Function definition
- Example: `(defn process-data [input]`

**Pattern**: `^\(def\s+\w+`
- Value definition
- Example: `(def config {:port 3000})`

## Environment Variables

- `CLJ_CONFIG`
- `LEIN_HOME`
- `CLOJURE_VERSION`

## Version Indicators

- Clojure 1.11 (current)
- Clojure 1.10 (widely used)
- ClojureScript 1.11

## Detection Notes

- Look for `.clj` files in repository
- project.clj indicates Leiningen
- deps.edn indicates tools.deps (modern)
- ClojureScript compiles to JavaScript
- Check for shadow-cljs.edn for CLJS builds

## Detection Confidence

- **File Extension Detection**: 95% (HIGH)
- **project.clj/deps.edn Detection**: 95% (HIGH)
- **Package Detection**: 90% (HIGH)
