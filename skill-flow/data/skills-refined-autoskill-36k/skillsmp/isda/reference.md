# ISDA Reference Documentation

This file contains detailed methodology for complex analyses. Load on demand when deeper explanation is needed.

## Detailed Stratum Definitions

### Stratum 1: Structural Skeleton (S₁)

**Definition:** The formal architecture of the text independent of content.

**Includes:**
- Document type (essay, letter, proof, narrative, report)
- Section hierarchy and organization
- Rhetorical mode (expository, argumentative, descriptive, narrative)
- Template patterns that repeat
- Formatting conventions

**Measurement:** Describe the structure in minimal notation. Count bytes.

**Example:** "5-part essay with [Intro → Literature Review → Methods → Results → Discussion]" ≈ 75 bytes

---

### Stratum 2: Retrievable Knowledge (S₂)

**Definition:** Information that exists in standard reference sources and could be retrieved by a competent reader or language model with appropriate domain access.

**Includes:**
- Direct quotations from sources
- Definitions and translations
- Historical facts and dates
- Biographical data
- Statistical data from cited sources
- Standard interpretations within a field
- Established theories or frameworks

**Example Pointers:**
- Academic citation: `Smith.2019.p42` (14 bytes)
- Scripture: `Gen.2.9` (7 bytes)
- Dictionary entry: `OED.sublime.n.2` (15 bytes)
- Historical fact: `WWI.armistice.1918.11.11` (24 bytes)

---

### Stratum 3: Derived Inferences (S₃)

**Definition:** Claims that follow logically or conventionally from S₂ without requiring special insight.

**Includes:**
- Standard analytical moves in a discipline
- Predictable cross-references
- Conventional scholarly apparatus
- Logical deductions from stated premises
- Standard interpretive frameworks applied to data
- "Textbook" observations

**Example Encodings:**
- `statistical_test(data, t-test) → significance` (40 bytes)
- `etymology(word, PIE) → root_meaning` (35 bytes)
- `legal_precedent(case, doctrine) → application` (45 bytes)

---

### Stratum 4: Curatorial Decisions (S₄)

**Definition:** The author's choices about selection, arrangement, emphasis, and juxtaposition that are not mechanically derivable.

**Includes:**
- Which sources to cite (among many valid options)
- Which details to foreground vs. background
- Structural innovations or unusual organization
- Scope decisions (what to include/exclude)
- Sequencing and ordering choices
- Voice and register decisions
- Which examples to use
- Framing and angle of approach

**Calculation Examples:**
- "Select 5 examples from pool of 50" → log₂(C(50,5)) ≈ 22 bits
- "Choose argumentative frame from 8 options" → log₂(8) = 3 bits
- "Order 6 sections (non-obvious sequence)" → log₂(6!) ≈ 9.5 bits

---

### Stratum 5: Generative Novelty (S₅)

**Definition:** Content that cannot be derived from existing sources or standard methods—genuine intellectual creation.

**Includes:**
- Novel arguments or interpretations
- Original phrasings that carry meaning (aphorisms, memorable formulations)
- Unexpected connections between disparate domains
- Insights that would surprise domain experts
- New frameworks or taxonomies
- Creative coinages or reframings
- Rhetorical moves that could not be predicted from the material

**Rule:** Be rigorous—if it could be derived, it belongs in S₃. S₅ is the hard core.

---

## Applications

1. **Self-editing:** Identify S₂/S₃ (potentially cuttable) vs. S₅ (essential to preserve)

2. **Compression challenges:** Generate tweet/paragraph/abstract versions by retaining only S₅

3. **Quality assessment:** High ND suggests genuine intellectual work

4. **Plagiarism/originality analysis:** High S₂, near-zero S₅ suggests insufficient contribution

5. **AI-generated text heuristic:** AI often has high S₂/S₃ but low S₅

6. **Genre calibration:** Compare against expected profiles for the genre

7. **Editing feedback:** "Your S₅ is strong but buried under excessive S₂"

---

## Limitations

1. **Subjectivity:** S₄/S₅ boundary requires judgment
2. **Domain expertise required:** Accurate assessment needs field knowledge
3. **Rhetorical value not captured:** Measures semantic content, not persuasive effectiveness
4. **Assumes semantic reconstruction goal:** Not for exact reproduction needs
5. **Interdependencies:** S₄ decisions may not be independent
6. **Dynamic knowledge bases:** "Retrievable" depends on assumed access
