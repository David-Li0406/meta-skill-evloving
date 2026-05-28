---
name: pedagogy
description: Core pedagogical principles for mathematical explanation
metadata:
  tags: pedagogy, teaching, explanation, intuition
priority: highest
---

# Pedagogical Principles

The goal is not to animate math, but to **build understanding**. Animation is just the medium.

## The 3b1b Teaching Philosophy

### 1. Intuition Before Formalism

**ALWAYS** build visual/conceptual intuition before showing formulas.

```
❌ BAD: "The eigenvalue equation is Av = λv. Let me show you..."
✅ GOOD: "What vectors, when transformed, only get stretched (not rotated)?
         Those special vectors are eigenvectors. The stretch factor is the eigenvalue."
```

### 2. The "Why" Before the "What"

Before explaining WHAT something is, explain WHY we need it.

```
❌ BAD: "GCD is the greatest common divisor of two numbers."
✅ GOOD: "Imagine you have 48 cookies and 18 kids. You want to divide them
         into identical groups with no leftovers. What's the largest group size possible?"
```

### 3. Concrete → Abstract

Start with specific numbers/examples, then generalize.

```
❌ BAD: "For any matrix A, the determinant represents..."
✅ GOOD: "Let's take this specific 2×2 matrix [2,1;0,1].
         Watch what happens to a unit square...
         The area changes by exactly 2. This factor IS the determinant."
```

## Explanation Structure Templates

### Template 1: Concept Introduction

```
1. HOOK: Pose an interesting question or problem
2. INTUITION: Build visual understanding (NO formulas yet)
3. PATTERN: Show the pattern emerging from examples
4. FORMALIZATION: NOW introduce the formula as a summary of the pattern
5. VERIFICATION: Show the formula working on examples
6. EXTENSION: "What if...?" - edge cases, generalizations
```

### Template 2: Algorithm Explanation

```
1. PROBLEM: What problem are we solving? Why do we care?
2. NAIVE APPROACH: Show the obvious (possibly inefficient) way
3. KEY INSIGHT: The "aha!" moment that makes the algorithm clever
4. STEP-BY-STEP: Walk through with concrete numbers
5. CORRECTNESS: Why does this always work?
6. SUMMARY: Crystallize into pseudocode/formula
```

### Template 3: Theorem/Proof

```
1. STATEMENT: State the theorem in plain language
2. MOTIVATION: Why would anyone believe this? Show examples.
3. KEY IDEA: The essential insight of the proof
4. VISUAL PROOF: Animate the proof visually
5. FORMAL SUMMARY: Show the formal statement
6. IMPLICATIONS: What does this let us do?
```

## Visual Storytelling Techniques

### Build-Up Pacing

```python
# ❌ BAD: Show everything at once
self.play(Create(complex_diagram))

# ✅ GOOD: Build up piece by piece
self.play(Create(simple_part))
self.wait(0.5)  # Let it sink in
explanation_text = Text("This represents...")
self.play(Write(explanation_text))
self.wait(1)    # Comprehension time
self.play(Create(next_part))
```

### The Pause Principle

**Key insight moments need PAUSES**, not speed.

```python
# After revealing something important:
self.wait(2)  # Give viewer time to think

# Before a transformation:
self.wait(0.5)  # Anticipation

# After a transformation:
self.wait(1)  # Let them see the result
```

### Visual Emphasis Hierarchy

1. **Color**: Most important elements get bright, distinct colors
2. **Size**: Key elements are larger
3. **Motion**: Moving elements draw attention
4. **Isolation**: Remove distractions when focusing on one thing

## Common Explanation Patterns

### "What Happens When..." Pattern

Great for transformations, functions, operations.

```python
# Show input
self.play(Create(input_visual))
self.play(Write(Text("What happens when we apply f?")))
self.wait(1)

# Show transformation
self.play(Transform(input_visual, output_visual), run_time=2)
self.wait(1)

# Highlight the key change
self.play(Indicate(changed_part))
```

### "Let's Count Both Ways" Pattern

Great for combinatorics, bijections, identities.

```python
# Method 1
self.play(Write(Text("Counting method 1:")))
# ... show first counting approach

# Method 2
self.play(Write(Text("Counting method 2:")))
# ... show second counting approach

# They must be equal!
self.play(Write(Text("Same thing, so they're equal!")))
```

### "Continuous Transformation" Pattern

Great for showing relationships, limits, generalizations.

```python
# Use ValueTracker for smooth transitions
param = ValueTracker(initial_value)

dynamic_object = always_redraw(
    lambda: create_object(param.get_value())
)

# Smoothly vary the parameter
self.play(param.animate.set_value(final_value), run_time=3)
```

## Language Guidelines

### Avoid Jargon Initially

```
❌ "The kernel of the linear transformation..."
✅ "The set of vectors that get sent to zero..."
```

### Use Active, Visual Language

```
❌ "The determinant is computed by..."
✅ "Watch how the area changes as we transform..."
```

### Anthropomorphize When Helpful

```
❌ "Vector v is mapped to Av"
✅ "Vector v gets pushed and stretched into a new position"
```

## Cognitive Load Management

### One Concept at a Time

Never introduce two new ideas simultaneously. If explaining A requires B, explain B first completely.

### Scaffolding

Build on what the viewer already knows:
- "Remember how we saw that..."
- "This is just like [familiar concept], but..."
- "We're going to use the same trick as before"

### Signposting

Tell viewers where you're going:
- "We need three ingredients for this proof..."
- "There are two key insights here..."
- "The punchline is coming..."

## Forbidden Anti-Patterns

### DO NOT:

1. **Rush the "aha" moment** - The key insight needs TIME
2. **Assume prerequisites** - Briefly recall what viewers need
3. **Skip the "why"** - Always motivate before defining
4. **Front-load formulas** - Build intuition first
5. **Use notation without explanation** - Introduce symbols gradually
6. **Animate without purpose** - Every animation should clarify, not decorate
7. **Overwhelm visually** - Keep scenes clean and focused

### DO:

1. **Pause after key points** - Let ideas sink in
2. **Connect to familiar concepts** - Analogies are powerful
3. **Show before telling** - Visual first, then formalize
4. **Verify with examples** - "Let's check this works..."
5. **Summarize periodically** - "So far we've seen..."
