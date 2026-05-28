# Classification Examples: MAJOR vs MINOR

Detailed examples to guide MAJOR/MINOR classification decisions.

---

## MAJOR Examples

### Example 1: Function Signature Mismatch (71.1 - ket)

**The Issue:**
```python
# Function defined with 1 parameter
def ket(dim):
    ...

# Tests call with 2 arguments
ket(2, 0)        # → TypeError!
ket(2, [1,1])    # → TypeError!
```

**Why MAJOR:**
- Code literally cannot execute
- Even a perfect implementation will crash
- This is a syntactic impossibility, not a domain knowledge gap

**The Fix:**
```python
# Just add the missing parameter
def ket(dim, j):  # ← minimal change
```

---

### Example 2: Method Ambiguity (63.3 - construct_matrix)

**The Issue:**
> "Write a function that produces a recursive matrix..."

But which numerical method?
- Explicit Euler: `V(n+1) = D × V(n)`
- Implicit Euler: `D × V(n+1) = V(n)`
- Crank-Nicolson: Average of both

Each produces a **different matrix D**.

**Why MAJOR:**
- Three experts could write three different (all correct) solutions
- Each would fail different test cases
- No way to determine which method tests expect

**The Fix:**
> "...Use the **explicit finite difference method** (Forward Euler / FTCS scheme)."

Just add one sentence specifying the method.

---

### Example 3: Formula Typo (63.3 - construct_matrix)

**The Issue:**
```
Original:  V(n+1,j) = a×V(n,j-1) + b×V(n,j) + c×V(n,j-1)
                                              ↑ WRONG! Should be j+1
```

**Why MAJOR:**
- Typo changes which diagonal coefficient `c` goes on
- Produces mathematically different matrix
- Even correct algorithm gives wrong output

**The Fix:**
```
Fixed:     V(n+1,j) = a×V(n,j-1) + b×V(n,j) + c×V(n,j+1)
```

---

## MINOR Examples

### Example 1: Missing Physical Constant (15.1 - Schrödinger)

**The Issue:**
> "ℏ = ×10⁻³⁴ Js" (missing mantissa "1.055")

**Why MINOR:**
- Planck's constant is universally known in physics
- Any physicist would use correct value: 1.055 × 10⁻³⁴
- Core algorithm (Crank-Nicolson) is fully specified

**No Fix Needed** - domain knowledge sufficient.

---

### Example 2: Standard Algorithm Implicit (74.1 - householder)

**The Issue:**
- Problem explains Householder reflector formula
- But doesn't explicitly state "iterate column by column"

**Why MINOR:**
- Householder QR is a standard algorithm in numerical linear algebra
- The notation $Q_k$ clearly implies iteration for k = 1, 2, ..., n
- Any expert in the field would know the procedure

**No Fix Needed** - standard algorithm knowledge sufficient.

---

### Example 3: Type Annotation Inconsistency

**The Issue:**
- Docstring says output is "float"
- But Schrödinger equation involves complex numbers

**Why MINOR:**
- The algorithm clearly produces complex values
- A physics-aware LLM would return complex numbers
- Tests would still pass with correct implementation

**No Fix Needed** - implementation logic is clear.

---

## Decision Comparison Table

| Aspect | MINOR | MAJOR |
|--------|-------|-------|
| **Core algorithm** | Clearly specified | Ambiguous/conflicting |
| **Missing info** | Well-known (constants, standard methods) | Fundamental definitions |
| **Multiple interpretations** | Lead to same answer | Lead to different answers |
| **Code execution** | Works | Crashes (TypeError, etc.) |
| **Fix complexity** | None needed | Requires rewriting specs |
| **LLM outcome** | Can produce correct code | Cannot determine correct code |

---

## Quick Tests for Classification

### Test 1: The Execution Test
```python
# Try to call the function as tests would
try:
    result = function(test_args)
except TypeError:
    # MAJOR - signature mismatch
```

### Test 2: The Interpretation Test
```python
# Implement with two different valid interpretations
result_A = method_A(inputs)
result_B = method_B(inputs)

if result_A != result_B:
    # MAJOR - ambiguity produces different answers
```

### Test 3: The Domain Knowledge Test
```python
# Implement with domain knowledge
our_result = our_implementation(inputs)
reference = numpy_or_scipy_reference(inputs)

if np.allclose(our_result, reference):
    # MINOR - domain knowledge sufficient
```

---

## Common Pitfalls

| Pitfall | Why It's Wrong | Correct Approach |
|---------|---------------|------------------|
| "Missing constant = MAJOR" | Well-known constants don't block solution | Check if constant is standard in field |
| "Any typo = MINOR" | Some typos change mathematical meaning | Check if typo affects output |
| "Algorithm implicit = MAJOR" | Standard algorithms don't need explicit steps | Check if algorithm is well-known |
| "Tests expect different format = MAJOR" | Format differences often don't matter | Check if core logic is correct |
