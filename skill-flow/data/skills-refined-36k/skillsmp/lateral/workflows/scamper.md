# Workflow: SCAMPER

Systematic creative reframing using the SCAMPER methodology.

## What is SCAMPER?

A structured approach to generating new ideas by applying seven transformation operators to existing concepts.

**S**ubstitute | **C**ombine | **A**dapt | **M**odify | **P**ut to other use | **E**liminate | **R**everse

## When to Use

- Need alternative angles on your thesis
- Looking for The Turn
- Stuck with obvious framing
- Critic found conflicts that need creative resolution
- Want to differentiate from predictable takes

## The Seven Operators

### 1. SUBSTITUTE

**Question**: "What if we replaced [key component] with [something else]?"

**Applications**:
- Swap a core assumption for its opposite
- Replace one constraint with a different one
- Use different evidence for the same claim
- Trade one audience for another

**Example prompts**:
- "What if instead of adding friction, we removed speed?"
- "What if the user wasn't human but another AI?"
- "What if we substituted 'accuracy' for 'confidence'?"

**Exercise**: List the 3 most important components of your argument. For each, ask: "What if this was [something else]?"

---

### 2. COMBINE

**Question**: "What if we merged [idea A] with [seemingly unrelated idea B]?"

**Applications**:
- Cross-pollinate concepts from different domains
- Find unexpected parallels
- Build hybrid hypotheses
- Merge contradictory evidence into synthesis

**Example prompts**:
- "What if we combined cognitive friction with game design?"
- "What if we merged the adversarial approach with the archaeological one?"
- "What if deliberation + automation weren't either/or?"

**Exercise**: List 3 concepts from completely unrelated fields. Force a connection to your topic.

---

### 3. ADAPT

**Question**: "How does [different field] solve this problem?"

**Applications**:
- Borrow solutions from adjacent domains
- Apply old frameworks to new contexts
- Import metaphors that clarify
- Find analogies that explain

**Example prompts**:
- "How does aviation handle speed vs safety tradeoffs?"
- "How do immune systems create beneficial friction?"
- "How did medieval monasteries structure deliberation?"

**Exercise**: Name 3 fields that have nothing to do with your topic. Research how they handle similar challenges.

---

### 4. MODIFY

**Question**: "What if this was [bigger/smaller/faster/slower/more extreme]?"

**Applications**:
- Change scale (individual → organization → society)
- Adjust intensity (subtle friction → hard stop)
- Shift timeframe (milliseconds → years)
- Alter scope (narrow → comprehensive)

**Example prompts**:
- "What if friction was 100x more intense? 100x subtler?"
- "What if we designed for decade-long effects, not immediate?"
- "What if this applied to entire industries, not individual systems?"

**Exercise**: Take your core claim. Apply each modifier: bigger, smaller, faster, slower, more intense, less intense.

---

### 5. PUT TO OTHER USE

**Question**: "What if this idea served a [completely different purpose]?"

**Applications**:
- Repurpose the insight for different context
- Find unexpected applications
- Flip who benefits
- Change the problem being solved

**Example prompts**:
- "What if friction mechanisms were used for creativity, not safety?"
- "What if the adversarial process was the product, not quality control?"
- "What if the primary beneficiary was the AI, not the human?"

**Exercise**: Your conclusion serves purpose X. List 5 other purposes it could serve.

---

### 6. ELIMINATE

**Question**: "What if we removed [the most complex part]?"

**Applications**:
- Simplify radically
- Remove constraints you assumed were fixed
- Strip to absolute essentials
- "Simple subtraction"

**Example prompts**:
- "What if we eliminated the human from the loop entirely?"
- "What if there was no friction, only better defaults?"
- "What if we removed all the caveats and stated it plainly?"

**Exercise**: What's the most complex part of your argument? Remove it. Does the core still work?

---

### 7. REVERSE

**Question**: "What if [the opposite] were true?"

**Applications**:
- Invert core assumptions
- Argue the other side convincingly
- Flip cause and effect
- Reverse the sequence

**Example prompts**:
- "What if friction REDUCES decision quality?"
- "What if the problem isn't too little friction but too much?"
- "What if speed enables accuracy rather than trading off against it?"

**Exercise**: State your thesis. Now argue the exact opposite as convincingly as you can.

---

## SCAMPER Session Protocol

### 1. Identify the Target

What concept, claim, or framing are you applying SCAMPER to?

```
TARGET: "Structural friction improves AI decision quality"
```

### 2. Rapid-Fire Application

Apply ALL seven operators quickly (2-3 minutes each):

| Operator | Application | Result |
|----------|-------------|--------|
| Substitute | Replace "friction" with "delay" | Different mechanism—delay might work through different cognitive pathway |
| Combine | Friction + game mechanics | Gamified deliberation—friction as challenge, not obstacle |
| Adapt | From circuit breakers | Adaptive friction that triggers only under specific conditions |
| Modify | Microscale friction | Sub-second pauses that are imperceptible but effective |
| Put to other use | Friction for creativity | Same mechanisms might enhance creative divergence |
| Eliminate | Remove friction, improve defaults | Maybe the answer is smarter defaults, not added friction |
| Reverse | Friction reduces quality | In time-critical scenarios, friction causes harmful delay |

### 3. Evaluate Results

For each result:
- Is this genuinely novel? (Not just rewording)
- Does it open a new direction? (Research, framing, argument)
- Is it worth pursuing? (Potentially valuable vs. clever but useless)

### 4. Select Top 2-3

Pick the most promising for development.

### 5. Record Outputs

```json
{
  "id": "hyp_007",
  "statement": "Friction mechanisms should be adaptive—triggered by stakes and uncertainty, not constant",
  "type": "novel",
  "confidence": 0.5,
  "generative_method": "SCAMPER-Adapt: borrowed from circuit breaker design",
  "evidence_needed": "Research on adaptive/conditional friction mechanisms",
  "potential_value": "Resolves speed-vs-accuracy tension; could be The Turn"
}
```

---

## Tips

- **Go fast**: Don't evaluate while generating
- **Force it**: Even bad ideas unlock good ones
- **Be literal**: Sometimes the obvious application is the best
- **Combine operators**: Reverse + Modify, Eliminate + Substitute
- **Return later**: Ideas that seem weak now may mature
