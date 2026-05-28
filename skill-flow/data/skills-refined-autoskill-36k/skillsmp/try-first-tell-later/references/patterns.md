# Implementation Patterns for Try-First-Tell-Later

This document provides detailed implementation guidance for each of the seven prompt patterns, along with templates for different content formats.

## The Seven Prompt Patterns

### 1. Prediction Prompts

Ask students to predict outcomes, behaviors, or solutions before showing them.

**Pattern**: "What do you think will happen if...?" / "Vad tror du händer om...?"

**Examples from practice**:
- "Vad tror du händer om du försöker läsa ett fält som inte finns för en person?"
- "Hur tror du vi kan läsa information från en Person-instans?"
- "Vad tror du `__str__()`-metoden gör?"
- "What do you think happens when we call `print(person)`?"

**Implementation**:
```
Before introducing a concept:
1. Present a concrete scenario or code example
2. Ask students to predict the outcome or behavior
3. Encourage them to articulate their reasoning
4. THEN provide the explanation and actual answer
5. Explicitly contrast their prediction with the reality
```

**When to use**:
- Before demonstrating behavior of unfamiliar code
- Before showing the result of operations
- When there's a common misconception to surface
- When the actual behavior might surprise students

### 2. Design/Solution Prompts

Ask students to attempt designing a solution before showing the standard approach.

**Pattern**: "How would you...?" / "Hur skulle du...?" / "How could you implement...?"

**Examples from practice**:
- "Hur skulle du modifiera programmet ovan för att även lagra adresser? Tänk igenom strukturen innan du fortsätter läsa."
- "Om du skulle skapa en PersonNick-klass som är precis som Person men också har ett smeknamn, hur skulle du göra det?"
- "Hur kan vi implementera multiplikation av två bråk?"
- "How would you store both a phone number and an address for each person?"

**Implementation**:
```
Before showing a solution:
1. Describe the problem or requirement clearly
2. Ask students to think through their own approach
3. Optionally: Ask them to consider multiple approaches
4. Encourage "thinking through before continuing to read"
5. THEN present the standard/expert solution
6. Compare approaches, highlighting trade-offs
```

**When to use**:
- Before introducing a new programming technique
- When there are multiple valid approaches
- Before showing refactoring or improvement
- When students have enough knowledge to attempt a solution

### 3. Conceptual Definition Prompts

Ask students to formulate their own definitions before providing formal ones.

**Pattern**: "What is...?" / "Vad är...?" / "Try to formulate your own definition before..."

**Examples from practice**:
- "Vad är en klass och vad är ett objekt? Varför vi behöver två olika begrepp i överhuvudtaget? Försök att formulera dina egna definitioner innan du fortsätter läsa."
- "Vad är skillnaden mellan attribut och metoder i en klass? Försök att formulera dina egna definitioner innan du fortsätter läsa."
- "What is a class and what is an object? Try to formulate your own definitions before continuing."

**Implementation**:
```
Before defining a concept:
1. Ask students to formulate their own understanding
2. Explicitly request they do this "before continuing to read"
3. Optionally: Provide familiar examples to ground thinking
4. THEN provide the formal definition
5. Show how the formal definition captures (or extends) their intuition
```

**When to use**:
- Before introducing fundamental concepts
- When students have seen related ideas
- When connecting to familiar metaphors or analogies
- Before formalizing intuitive understanding

### 4. Reasoning Prompts

Ask students to reason about causes, implications, or connections.

**Pattern**: "Why do you think...?" / "Varför tror du...?"

**Examples from practice**:
- "Varför tror du att attributen börjar med dubbla understreck (`__`)? Vad betyder detta i Python?"
- "Varför tror du det är bra att inte kunna komma åt attributen direkt? Vad skulle kunna gå fel om vi tillät det?"
- "Varför tror du det är användbart att kunna jämföra objekt med operatorer som `<` och `==`? Ge ett exempel på när detta skulle vara praktiskt."
- "Why do you think methods have `self` as the first parameter?"

**Implementation**:
```
Before explaining rationale:
1. Present a design decision, convention, or pattern
2. Ask why it exists or what purpose it serves
3. Encourage connection to their experience
4. THEN explain the actual reasoning
5. Validate correct intuitions, correct misconceptions
```

**When to use**:
- Before explaining design patterns or conventions
- When there's underlying rationale worth discovering
- To connect language features to programming principles
- Before discussing trade-offs in design decisions

### 5. Comparison Prompts

Ask students to compare approaches, options, or examples before explaining differences.

**Pattern**: "Jämför..." / "Compare..." / "Vilka skillnader ser du...?" / "What differences do you see...?"

**Examples from practice**:
- "Jämför koden för att skapa personer i de två exemplen. Vilka skillnader ser du? Vilket sätt tycker du är tydligare och varför?"
- "Vilka problem kan du se med denna approach? Tänk på: [specific aspects]"
- "Compare the code for creating people in the two examples. Which approach is clearer and why?"

**Implementation**:
```
Before analyzing differences:
1. Present two or more alternatives side-by-side
2. Ask students to identify differences
3. Ask them to evaluate trade-offs
4. THEN provide expert analysis
5. Show critical aspects they might have missed
```

**When to use**:
- When showing evolution from naive to sophisticated approach
- Before introducing a new paradigm or technique
- When comparing multiple valid solutions
- To highlight critical aspects through contrast

### 6. Reflection Prompts

Ask students to reflect on broader implications, advantages, or applications.

**Pattern**: "Reflektera över..." / "Reflect on..." / "Vilka fördelar/nackdelar ser du...?" / "What advantages/disadvantages do you see...?"

**Examples from practice**:
- "Reflektera över fördelarna med arv: När skulle det vara lämpligt att använda arv? När skulle det vara bättre att skapa en helt ny klass istället?"
- "Vilka fördelar ser du med att använda klasser jämfört med uppslagslistor? Lista minst tre fördelar."
- "When would it be appropriate to use inheritance? When would it be better to create a new class instead?"

**Implementation**:
```
After introducing a concept:
1. Ask students to step back and consider implications
2. Prompt analysis of when/why to use the approach
3. Encourage connection to principles or patterns
4. THEN provide expert perspective
5. Synthesize their insights with broader framework
```

**When to use**:
- After teaching a new technique or pattern
- To encourage strategic thinking about tool selection
- When discussing software design principles
- To connect specific techniques to broader concepts

### 7. Experimentation Prompts

Encourage students to try something themselves before showing the result.

**Pattern**: "Prova!" / "Try it!" / "Skriv ett program som..." / "Write a program that..."

**Examples from practice**:
- Exercise blocks that ask students to write programs before showing solutions
- "(Prova!)" annotations encouraging hands-on experimentation
- Problems to solve before revealing implementations
- "Try running this code and observe what happens"

**Implementation**:
```
Before showing working code:
1. Present clear requirements or goal
2. Provide enough context but not full solution
3. Encourage actual implementation attempt
4. THEN show the complete solution
5. Compare their approach with shown solution
```

**When to use**:
- When students can implement with current knowledge
- Before showing complete working examples
- To encourage active problem-solving
- When hands-on experience aids understanding

## Structuring Educational Materials

### Typical Flow Pattern

```
1. Context/Scenario
   ↓
2. Prompt to Predict/Try/Reflect
   ↓
3. Space for student thinking
   ↓
4. Explanation/Answer
   ↓
5. Explicit contrast between prediction and reality
   ↓
6. Deeper explanation of critical aspects
```

This flow creates variation patterns:
- **Variant**: Student understanding → Expert understanding
- **Invariant**: The concept/problem being discussed
- **Discernment**: Critical aspects revealed through the contrast

### LaTeX/Beamer Implementation

When writing LaTeX slides or notes, use this structure:

```latex
% 1. Set context
Vi har sett hur... Nu ska vi...

% 2. Exercise/prediction prompt
\begin{exercise}
  Hur skulle du...? / Vad tror du...?
  Tänk igenom innan du fortsätter läsa.
\end{exercise}

% 3. Space (implicit - student pauses to think)

% 4. Answer/explanation
Svaret är att... / Vi kan göra detta genom att...

% 5. Contrast and deeper explanation
Notera att... / Detta skiljer sig från... /
Här ser vi att...
```

**Example with prediction**:
```latex
\subsection{Attribut som egenskaper}

\begin{exercise}
  Vad är skillnaden mellan att skriva
  \mintinline{python}{frac.get_nominator()} och
  \mintinline{python}{frac.nominator}?
  Vilket känns mer naturligt?
\end{exercise}

Egenskaper låter oss använda attribut-liknande syntax
medan vi fortfarande behåller kontrollen över hur data
läses och skrivs.

\begin{frame}[fragile]
  \inputminted[linenos]{python}{examples/properties.py}
\end{frame}
```

**Example with design challenge**:
```latex
\begin{exercise}
  Hur skulle du modifiera programmet ovan för att även
  lagra adresser? Tänk igenom strukturen innan du
  fortsätter läsa.
\end{exercise}

Ett första försök skulle kunna vara att använda en
nästlad uppslagslista, där varje person får en
uppslagslista med olika fält.

\begin{frame}[fragile]
  \inputminted[linenos]{python}{examples/nested_dict.py}
\end{frame}

Som du ser blev koden ganska omständlig...
```

### Markdown/Text Implementation

```markdown
## Topic Name

Brief context setting to activate relevant prior knowledge...

### Think About This First

**Before continuing**: How would you...? / What do you think happens when...?

Take a moment to consider this before reading on.

---

### The Answer

Here's how it actually works...

[Provide complete explanation]

**Comparing Approaches**: You might have thought X, but actually Y.
This is because [explain critical aspect]. The key difference is
[highlight what matters].
```

**Example**:
```markdown
## String Representation of Objects

We've created our `Person` class with attributes. But what happens
when we try to print a person object?

### Predict First

**Before trying it**: What do you think `print(person)` will output?
- The person's name?
- The object's memory address?
- An error?

Think about what you've seen when printing other objects in Python.

---

### What Actually Happens

When you print an object without defining special methods, Python
shows the object's memory address: `<__main__.Person object at 0x...>`

This isn't very useful! To control how our objects are displayed,
we use the `__str__()` dunder method:

```python
def __str__(self):
    return f"{self.first_name} {self.last_name}"
```

**The Key Insight**: Python automatically calls `__str__()` when
converting objects to strings. This lets us define human-readable
representations.
```

### Jupyter Notebook Implementation

```markdown
## Concept Introduction

[Context markdown cell]

### Exercise: Think First

Before running the code below, predict what will happen:
1. ...
2. ...

[Code cell - students can run to test prediction]

### Explanation

[Markdown cell with answer and contrast]
```

## Sequencing Multiple Prompts

When teaching complex topics, sequence prompts strategically:

### Progression Pattern

1. **Start with Prediction** - "What do you think X does?"
2. **Move to Design** - "How would you implement X?"
3. **Follow with Reasoning** - "Why do you think X works this way?"
4. **End with Reflection** - "When would you use X vs Y?"

### Example Sequence (Teaching Classes)

```
1. Prediction: "What happens when we print a Person object?"
   → Shows default object representation

2. Design: "How would you make the object print nicely?"
   → Attempts before showing __str__()

3. Reasoning: "Why use __str__() instead of just adding a print_person() function?"
   → Discusses integration with Python's print() and str()

4. Comparison: "Compare our dictionary approach vs. class approach"
   → Highlights encapsulation benefits

5. Reflection: "When would you use classes vs dictionaries?"
   → Strategic thinking about tool selection
```

## Pacing Considerations

**Don't overuse prompts**: Too many interruptions for thinking can create cognitive fatigue.

**Space them out**:
- Major concepts: Multiple prompts in sequence
- Minor details: Traditional explanation
- Complex topics: Prompt → Explanation → Prompt → Explanation

**Timing**:
- In lectures: Wait 10-30 seconds after posing question
- In written materials: Use clear visual separation
- In videos: Use editing to create pause

## Adapting for Different Formats

### Live Lectures
- Use think-pair-share after prompts
- Poll students for predictions before revealing
- Ask volunteers to share reasoning
- Use whiteboards to compare approaches

### Recorded Videos
- Pause video after prompt
- On-screen timer showing thinking time
- Multiple-choice overlay for predictions
- Resume with "Here's what actually happens..."

### Written Materials
- Use visual separation (horizontal rules, spacing)
- Explicit phrases: "Think about this before continuing"
- Present question on one page, answer on next (for print)
- Use collapsible sections (for digital)

### Interactive Platforms
- Required pause before showing answer
- Lock answer until student provides response
- Show student's attempt alongside correct answer
- Track which prompts students engage with

## Common Mistakes to Avoid

1. **Asking without answering**: Always provide the explanation after the prompt
2. **Trivial questions**: Ensure prompts are worth thinking about
3. **Impossible questions**: Build on accessible prior knowledge
4. **Skipping the contrast**: Explicitly compare prediction with reality
5. **Too much cognitive load**: Don't chain too many prompts together
6. **No follow-through**: Always explain why the answer matters
7. **Dismissing attempts**: Validate good thinking even if prediction is wrong
8. **Revealing critical aspects in the question**: Don't point out what students should discern (see Teacher's Paradox in SKILL.md)

## Diagnostic Use of Try-First Prompts

Try-first prompts double as diagnostic tools, revealing which critical aspects students can already discern. This section provides implementation guidance.

### Pre-Test Pattern

```latex
% Before teaching, pose open question that doesn't reveal critical aspects
\begin{exercise}[Diagnostic]
  [Present scenario without highlighting critical aspects]
  
  What would you do? / What do you think happens? / What could go wrong?
\end{exercise}

% Document expected response categories:
% - Response showing discernment of critical aspect X: [description]
% - Response missing critical aspect X: [description]  
% - Common misconception: [description]
```

### Analyzing Responses

Create a simple rubric for the critical aspects:

| Critical Aspect | Student Discerns | Student Misses |
|-----------------|------------------|----------------|
| Aspect A | Mentions X, Y | Focuses only on Z |
| Aspect B | Considers edge case | Assumes happy path |

### Example: File Resource Management

**Diagnostic prompt**:
```latex
\begin{exercise}
  Here's code that reads a file:
  \begin{minted}{python}
file = open("data.txt", "r")
content = file.read()
file.close()
  \end{minted}
  What could go wrong with this code?
\end{exercise}
```

**Response analysis**:

| Response Type | Critical Aspect Discerned? | Next Step |
|---------------|---------------------------|-----------|
| "Exception before close()" | Yes - resource safety | Ready for `with` statement |
| "File doesn't exist" | No - focuses on different aspect | Teach resource management first |
| "Wrong filename" | No - surface level | Need contrast: working vs failing code |

### Teaching Response Based on Diagnostic

**For students who discern the critical aspect**:
- Move directly to solution (`with` statement)
- Use generalization to show pattern applies to other resources

**For students who miss the critical aspect**:
- First create contrast to reveal it (show code that fails to close)
- Let them experience the problem before explaining the solution

### Post-Test Comparison

After teaching with appropriate variation patterns, re-pose the prompt (or similar). Students should now mention the critical aspects they previously missed.

**Documentation template**:
```latex
\ltnote{%
  \textbf{Diagnostic results}:
  
  Pre-test: X\% mentioned critical aspect (resource safety)
  
  Post-test: Y\% mentioned critical aspect
  
  \textbf{Implication}: Variation pattern (contrast between 
  exception-safe and unsafe code) was effective/needs revision.
}
```

### Connection to Variation Theory

The diagnostic results inform which variation patterns to use:

| Diagnostic Result | Variation Pattern Needed |
|-------------------|-------------------------|
| Students miss aspect entirely | Contrast (vary the critical aspect) |
| Students see aspect in one context | Generalization (show across contexts) |
| Students see aspects separately | Fusion (vary multiple aspects together) |

See the variation-theory skill for detailed guidance on each pattern.
