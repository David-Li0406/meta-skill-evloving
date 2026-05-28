---
name: brand-voice-extraction
description: |
  Systematic methodology for capturing a client's authentic brand voice from writing samples, existing content, questionnaire responses, and stakeholder preferences.
  
  USE THIS SKILL WHEN:
  - Analyzing writing samples to document voice
  - Creating voice guidelines for a new client
  - Auditing existing content for voice consistency
  - User mentions "brand voice", "tone", "writing style", "voice extraction"
  - Preparing to write copy that needs to match client's voice
  - Building voice profile as part of client discovery
  
  OUTPUTS: Brand Voice Profile JSON with evidence-backed attributes
allowed-tools: Read, Grep, Glob
---

# Brand Voice Extraction Skill

## Overview

Brand voice is the consistent personality expressed through words. This skill provides a rigorous, evidence-based methodology for extracting voice attributes from client materials—not inventing them, not assuming them, but documenting what's actually there.

## The Voice Extraction Framework

### The Six Core Voice Dimensions

Every brand voice can be mapped across six dimensions. Each is a spectrum, not a binary:

```
DIMENSION 1: FORMALITY
├─ 1-2: Very Casual ("Hey! Let's chat about...")
├─ 3-4: Casual ("Here's the deal...")
├─ 5-6: Balanced ("We're happy to help you...")
├─ 7-8: Professional ("We are pleased to assist...")
└─ 9-10: Very Formal ("It is our privilege to serve...")

DIMENSION 2: ENTHUSIASM  
├─ 1-2: Reserved ("The product works well.")
├─ 3-4: Measured ("We're confident you'll see results.")
├─ 5-6: Engaged ("We love helping clients succeed!")
├─ 7-8: Energetic ("This is AMAZING and you'll love it!")
└─ 9-10: Exuberant ("OMG this will literally change your LIFE!!!")

DIMENSION 3: HUMOR
├─ 1-2: Serious (No humor, all business)
├─ 3-4: Occasional wit (Light touches, subtle)
├─ 5-6: Playful (Regular humor, approachable)
├─ 7-8: Witty (Clever wordplay, personality-forward)
└─ 9-10: Comedy-forward (Humor is the brand)

DIMENSION 4: DIRECTNESS
├─ 1-2: Soft/Indirect ("You might consider...")
├─ 3-4: Gentle ("We suggest...")
├─ 5-6: Clear ("Here's what to do...")
├─ 7-8: Direct ("Do this.")
└─ 9-10: Bold/Blunt ("Stop wasting time. Do this now.")

DIMENSION 5: TECHNICAL COMPLEXITY
├─ 1-2: Very Simple (5th grade reading level)
├─ 3-4: Accessible (8th grade, no jargon)
├─ 5-6: Moderate (Some industry terms, explained)
├─ 7-8: Technical (Industry jargon expected)
└─ 9-10: Expert (Dense, specialized vocabulary)

DIMENSION 6: WARMTH
├─ 1-2: Distant/Impersonal ("Users will find...")
├─ 3-4: Neutral ("You can...")
├─ 5-6: Friendly ("We're here for you...")
├─ 7-8: Warm ("We genuinely care about...")
└─ 9-10: Intimate ("You're part of our family...")
```

---

## Extraction Process

### Step 1: Gather Writing Samples

**Ideal Sample Set:**
- 3-5 pieces of existing content (website, emails, social)
- Stakeholder writing samples (founder emails, team communications)
- Content they admire (competitors or brands they like)
- Content they dislike (what to avoid)

**Minimum Viable:**
- At least 1 substantial piece (500+ words)
- OR questionnaire responses about voice preferences

**Document Your Inputs:**
```json
{
  "samples_analyzed": [
    {
      "source": "Homepage copy",
      "word_count": 450,
      "content_type": "marketing",
      "url_or_location": "https://..."
    }
  ]
}
```

### Step 2: Analyze Each Sample

For each writing sample, extract:

#### A. Sentence-Level Patterns

```markdown
SENTENCE LENGTH:
- Average words per sentence: [count]
- Range: [shortest] to [longest]
- Pattern: [short/medium/long/varied]

SENTENCE STRUCTURE:
- Simple sentences: [%]
- Compound sentences: [%]
- Complex sentences: [%]
- Questions used: [yes/no, frequency]
- Exclamations used: [yes/no, frequency]

EXAMPLES:
- Typical sentence: "[quote]"
- Atypical sentence: "[quote]"
```

#### B. Word-Level Patterns

```markdown
VOCABULARY:
- Preferred verbs: [list with examples]
- Avoided verbs: [list or note absence]
- Industry jargon used: [yes/no, examples]
- Contractions: [always/sometimes/never]

SPECIFIC WORD CHOICES:
- How do they say "you"? [you/y'all/folks/clients/customers]
- How do they say "we"? [we/our team/the company/I]
- Power words used: [list]
- Words conspicuously absent: [list]

EXAMPLES:
- Characteristic phrase: "[quote]"
- Repeated pattern: "[quote]"
```

#### C. Emotional Tone

```markdown
EMOTIONAL REGISTER:
- Primary emotion conveyed: [confidence/excitement/calm/urgency/etc.]
- Secondary emotions: [list]
- Emotions avoided: [list]

EVIDENCE:
- Quote showing primary emotion: "[quote]"
- Quote showing avoidance: "[quote]"
```

#### D. Structural Patterns

```markdown
PARAGRAPH LENGTH:
- Average sentences per paragraph: [count]
- Pattern: [short punchy/medium/long flowing]

FORMATTING:
- Uses bullet points: [frequently/occasionally/never]
- Uses headers: [frequently/occasionally/never]
- Uses bold/emphasis: [frequently/occasionally/never]

TRANSITIONS:
- Common transition phrases: [list]
- Paragraph openings pattern: [observation]
```

### Step 3: Score Each Dimension

For each of the six dimensions, assign a score (1-10) with evidence:

```json
{
  "dimension": "formality",
  "score": 6,
  "evidence": [
    {
      "quote": "We're excited to help you get started",
      "source": "Homepage",
      "analysis": "Contraction 'we're' + 'excited' suggests casual-professional balance"
    },
    {
      "quote": "Our team is dedicated to your success",
      "source": "About page", 
      "analysis": "More formal phrasing, no contractions"
    }
  ],
  "conclusion": "Balanced formality (5-7 range) - professional but not stiff, uses contractions selectively"
}
```

**CRITICAL: Every score needs evidence. No evidence = no score.**

### Step 4: Identify Patterns Across Samples

Look for consistency and inconsistency:

```markdown
CONSISTENT PATTERNS (appear in 80%+ of samples):
- [Pattern]: [evidence across samples]

INCONSISTENT PATTERNS (vary across samples):
- [Pattern]: [note the variation and possible reason]

ANOMALIES (one-off departures):
- [Anomaly]: [where it appeared, possible explanation]
```

### Step 5: Synthesize Voice Guidelines

Convert analysis into actionable guidelines:

```markdown
## DO's (with examples)

### DO use contractions in conversational contexts
- ✓ "We're here to help"
- ✓ "You'll love this"
- ✗ "We are pleased to inform you"

### DO lead with benefits
- ✓ "Save 3 hours every week"
- ✗ "Our software has automated scheduling"

## DON'Ts (with examples)

### DON'T use corporate jargon
- ✗ "Leverage synergies"
- ✗ "Best-in-class solutions"
- ✓ "Work better together"
- ✓ "Tools that actually help"

### DON'T be overly casual
- ✗ "OMG you guys!!!"
- ✗ "This is literally the best"
- ✓ "We're genuinely excited about this"
```

---

## Anti-Hallucination Rules for Voice Extraction

### Rule 1: Evidence or Nothing

```
✗ WRONG: "The brand voice is friendly and approachable"
✓ RIGHT: "The brand voice appears friendly [Evidence: 8/10 sentences use 'you' directly, contractions in 70% of copy, exclamation points in 3/5 headlines - Source: Homepage analysis]"
```

### Rule 2: Quote Don't Paraphrase

```
✗ WRONG: "They tend to be enthusiastic"
✓ RIGHT: "Enthusiasm is present [Example: 'We absolutely love helping small businesses thrive!' - Source: About page, para 2]"
```

### Rule 3: Note Sample Limitations

```
If only analyzing one sample:
→ State: "Based on limited sample (homepage only). Voice profile confidence: LOW. Recommend analyzing additional content before finalizing guidelines."
```

### Rule 4: Distinguish Preference from Practice

```
If client says they want to sound "bold and edgy" but their content is conservative:
→ Flag: "[INCONSISTENCY: Stated preference is 'bold/edgy' but existing content scores 4/10 on directness. Clarify: Should new content match existing voice or shift toward stated preference?]"
```

### Rule 5: Don't Invent "Competitor Voice"

```
✗ WRONG: "Competitors tend to be more formal"
✓ RIGHT: "Competitor voice not analyzed - no competitor samples provided"
OR
✓ RIGHT: "Competitor [Name] voice analyzed: [specific observations with quotes]"
```

---

## Output Schema: Brand Voice Profile

```json
{
  "profile_metadata": {
    "client_name": "",
    "created_date": "",
    "samples_analyzed": [
      {
        "source": "",
        "type": "",
        "word_count": 0,
        "url": ""
      }
    ],
    "confidence_level": "high|medium|low",
    "confidence_notes": ""
  },
  
  "voice_dimensions": {
    "formality": {
      "score": 1-10,
      "label": "Very Casual|Casual|Balanced|Professional|Very Formal",
      "evidence": [
        {
          "quote": "",
          "source": "",
          "analysis": ""
        }
      ],
      "summary": ""
    },
    "enthusiasm": {
      "score": 1-10,
      "label": "Reserved|Measured|Engaged|Energetic|Exuberant",
      "evidence": [],
      "summary": ""
    },
    "humor": {
      "score": 1-10,
      "label": "Serious|Occasional Wit|Playful|Witty|Comedy-Forward",
      "evidence": [],
      "summary": ""
    },
    "directness": {
      "score": 1-10,
      "label": "Soft|Gentle|Clear|Direct|Bold",
      "evidence": [],
      "summary": ""
    },
    "technical_complexity": {
      "score": 1-10,
      "label": "Very Simple|Accessible|Moderate|Technical|Expert",
      "evidence": [],
      "summary": ""
    },
    "warmth": {
      "score": 1-10,
      "label": "Distant|Neutral|Friendly|Warm|Intimate",
      "evidence": [],
      "summary": ""
    }
  },
  
  "tone_guidelines": {
    "primary_tone": {
      "tone": "",
      "description": "",
      "evidence": ""
    },
    "secondary_tones": [
      {
        "tone": "",
        "when_to_use": ""
      }
    ],
    "tones_to_avoid": [
      {
        "tone": "",
        "why_avoid": ""
      }
    ]
  },
  
  "language_patterns": {
    "sentence_patterns": {
      "average_length": "",
      "preferred_structure": "",
      "uses_questions": true|false,
      "uses_exclamations": true|false
    },
    "word_preferences": {
      "preferred_words": [
        {
          "word": "",
          "example_usage": "",
          "source": ""
        }
      ],
      "avoided_words": [
        {
          "word": "",
          "why_avoid": ""
        }
      ]
    },
    "pronoun_usage": {
      "first_person": "we|I|our team|[brand name]",
      "second_person": "you|y'all|folks|customers",
      "evidence": ""
    },
    "contractions": "always|usually|sometimes|rarely|never",
    "jargon_level": "none|minimal|moderate|heavy"
  },
  
  "dos_and_donts": {
    "dos": [
      {
        "guideline": "",
        "good_example": "",
        "source": ""
      }
    ],
    "donts": [
      {
        "guideline": "",
        "bad_example": "",
        "good_alternative": ""
      }
    ]
  },
  
  "application_notes": {
    "headlines": "",
    "body_copy": "",
    "ctas": "",
    "error_messages": "",
    "email_subject_lines": "",
    "social_media": ""
  },
  
  "inconsistencies_flagged": [
    {
      "observation": "",
      "sources": [],
      "resolution_needed": ""
    }
  ],
  
  "gaps_in_analysis": [
    {
      "what_missing": "",
      "impact": "",
      "recommendation": ""
    }
  ]
}
```

---

## Verification Checklist

Before finalizing voice profile:

### Evidence Check
- [ ] Every dimension score has at least 2 supporting quotes
- [ ] All quotes include source attribution
- [ ] No scores based on assumption alone

### Consistency Check
- [ ] Scores across dimensions form coherent picture
- [ ] Any inconsistencies are flagged and explained
- [ ] Stated preferences vs. actual practice are reconciled

### Completeness Check
- [ ] All six dimensions scored
- [ ] Do's and Don'ts have concrete examples
- [ ] Application notes cover key content types

### Usability Check
- [ ] Guidelines are specific enough to apply
- [ ] Examples are clear and representative
- [ ] A copywriter could use this to write on-brand content

---

## Integration Notes

This skill is typically used by:
- `client-discovery-agent` (during onboarding)
- `landing-page-copywriter` skill (for voice-consistent copy)
- `website-copywriter` skill (for voice-consistent copy)
- `/voice` command (for voice extraction or application)

Voice profiles should be saved to a consistent project location for downstream access.

---

## Quick Reference Card

For rapid voice extraction when time is limited:

```markdown
## 60-Second Voice Scan

Read 3 paragraphs of client content. Note:

1. FORMALITY: Contractions? (casual) or formal phrasing?
2. ENTHUSIASM: Exclamation points? Power words? Or measured?
3. HUMOR: Any wit/jokes? Or purely informational?
4. DIRECTNESS: "You should" (direct) or "You might consider" (soft)?
5. COMPLEXITY: Jargon? Or plain language?
6. WARMTH: "We care about you" or "Users will find"?

Note 1 quote per dimension. That's your baseline.
Flag: "Quick scan only - full analysis needed for production guidelines"
```

---

## References

For detailed examples and edge cases, see:
- `references/voice-examples.md` - Sample voice profiles from various industries
- `references/voice-edge-cases.md` - Handling difficult extraction scenarios