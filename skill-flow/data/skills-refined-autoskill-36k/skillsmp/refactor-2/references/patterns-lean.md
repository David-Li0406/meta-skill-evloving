# Lean 4 Refactoring Patterns

Lean 4 specific refactoring patterns for functional programming and theorem proving.

## Definition Extraction

### Extract to Where Clause

Use `where` for helper definitions that are only used in one place.

Before:
```lean
def processItems (items : List α) (f : α → β) : List β :=
  let helper := fun x => f x
  items.map helper
```

After:
```lean
def processItems (items : List α) (f : α → β) : List β :=
  items.map helper
where
  helper x := f x
```

### Extract to Top-Level Definition

Extract when the helper is reusable or complex enough to warrant its own documentation.

Before:
```lean
def compute (n : Nat) : Nat :=
  let rec aux acc k :=
    if k == 0 then acc else aux (acc + k) (k - 1)
  aux 0 n
```

After:
```lean
def sumUpTo (acc k : Nat) : Nat :=
  if k == 0 then acc else sumUpTo (acc + k) (k - 1)

def compute (n : Nat) : Nat := sumUpTo 0 n
```

## Pattern Matching Refinements

### Consolidate Match Arms

Before:
```lean
def eval : Expr → Nat
  | .lit n => n
  | .add e1 e2 => eval e1 + eval e2
  | .sub e1 e2 => eval e1 - eval e2
  | .mul e1 e2 => eval e1 * eval e2
  | .div e1 e2 => eval e1 / eval e2
```

After (when operations can be generalized):
```lean
def eval : Expr → Nat
  | .lit n => n
  | .binOp op e1 e2 => op.apply (eval e1) (eval e2)
```

### Use Match Guards

Before:
```lean
def classify (n : Int) : String :=
  if n < 0 then "negative"
  else if n == 0 then "zero"
  else "positive"
```

After:
```lean
def classify : Int → String
  | n if n < 0 => "negative"
  | 0 => "zero"
  | _ => "positive"
```

## Tactic Refactoring

### Extract Common Tactic Sequence to Macro

Before:
```lean
theorem foo : P := by
  intro h
  cases h
  · simp [*]
  · simp [*]

theorem bar : Q := by
  intro h
  cases h
  · simp [*]
  · simp [*]
```

After:
```lean
macro "intro_cases_simp" : tactic =>
  `(tactic| intro h; cases h <;> simp [*])

theorem foo : P := by intro_cases_simp
theorem bar : Q := by intro_cases_simp
```

### Convert Term Mode to Tactic Mode

Use when proofs become complex and benefit from step-by-step reasoning.

Before:
```lean
theorem trans_symm (h1 : a = b) (h2 : b = c) : c = a :=
  (h1.trans h2).symm
```

After:
```lean
theorem trans_symm (h1 : a = b) (h2 : b = c) : c = a := by
  rw [← h1, ← h2]
```

### Convert Tactic Mode to Term Mode

Use for simple proofs that become clearer as terms.

Before:
```lean
theorem add_comm_example : a + b = b + a := by
  exact Nat.add_comm a b
```

After:
```lean
theorem add_comm_example : a + b = b + a := Nat.add_comm a b
```

## Structure Refactoring

### Extract Fields to Separate Structure

Before:
```lean
structure Person where
  name : String
  age : Nat
  street : String
  city : String
  postalCode : String
```

After:
```lean
structure Address where
  street : String
  city : String
  postalCode : String

structure Person where
  name : String
  age : Nat
  address : Address
```

### Use Extends for Inheritance

Before:
```lean
structure Point2D where
  x : Float
  y : Float

structure Point3D where
  x : Float
  y : Float
  z : Float
```

After:
```lean
structure Point2D where
  x : Float
  y : Float

structure Point3D extends Point2D where
  z : Float
```

## Type Class Refactoring

### Extract Type Class

Before:
```lean
def serialize (x : α) [ToString α] : String := toString x
def deserialize (s : String) [Inhabited α] [DecidableEq α] : Option α := ...
```

After:
```lean
class Serializable (α : Type) where
  serialize : α → String
  deserialize : String → Option α

def serialize [Serializable α] (x : α) : String := Serializable.serialize x
def deserialize [Serializable α] (s : String) : Option α := Serializable.deserialize s
```

### Use Default Implementations

Before:
```lean
class Monoid (α : Type) where
  empty : α
  append : α → α → α

instance : Monoid (List α) where
  empty := []
  append := List.append
```

After:
```lean
class Monoid (α : Type) where
  empty : α
  append : α → α → α
  appendEmpty (x : α) : append x empty = x := by rfl  -- default proof if possible
```

## Monad Refactoring

### Extract Do-Notation Steps

Before:
```lean
def processFile (path : String) : IO Unit := do
  let contents ← IO.FS.readFile path
  let lines := contents.splitOn "\n"
  let filtered := lines.filter (·.length > 0)
  let processed := filtered.map String.trim
  for line in processed do
    IO.println line
```

After:
```lean
def readNonEmptyLines (path : String) : IO (List String) := do
  let contents ← IO.FS.readFile path
  return contents.splitOn "\n" |>.filter (·.length > 0) |>.map String.trim

def processFile (path : String) : IO Unit := do
  let lines ← readNonEmptyLines path
  for line in lines do
    IO.println line
```

### Use Applicative Style

Before:
```lean
def combine : Option α → Option β → Option (α × β)
  | some a, some b => some (a, b)
  | _, _ => none
```

After:
```lean
def combine (oa : Option α) (ob : Option β) : Option (α × β) :=
  (·, ·) <$> oa <*> ob
```

## Namespace Organization

### Move Definitions to Appropriate Namespace

Before:
```lean
def listMap (f : α → β) (xs : List α) : List β := xs.map f
def listFilter (p : α → Bool) (xs : List α) : List α := xs.filter p
```

After:
```lean
namespace List
  def map' (f : α → β) (xs : List α) : List β := xs.map f
  def filter' (p : α → Bool) (xs : List α) : List α := xs.filter p
end List
```

### Use Section for Local Variables

Before:
```lean
def foo (α : Type) [Inhabited α] : α := default
def bar (α : Type) [Inhabited α] : List α := [default, default]
def baz (α : Type) [Inhabited α] : Option α := some default
```

After:
```lean
section
variable (α : Type) [Inhabited α]

def foo : α := default
def bar : List α := [default, default]
def baz : Option α := some default

end
```

## Attribute Refactoring

### Add Simp Lemmas

Identify frequently used rewrite lemmas and mark them.

```lean
@[simp]
theorem list_map_empty : ([] : List α).map f = [] := rfl

@[simp]
theorem list_map_cons : (x :: xs).map f = f x :: xs.map f := rfl
```

### Use Inline for Performance

```lean
@[inline]
def fastHelper (x : Nat) : Nat := x + 1
```

## Common Lean-Specific Smells

| Smell | Solution |
|-------|----------|
| Repeated `have` statements | Extract to lemma |
| Long tactic proofs | Split into smaller lemmas |
| Duplicated pattern matches | Use helper function with pattern |
| Nested `Option`/`Except` handling | Use monad transformers or `<|>` |
| Manual recursion | Use `List.foldl`, `List.map`, etc. |
| Hardcoded types | Use type class constraints |
| Long `do` blocks | Extract pure computations |
