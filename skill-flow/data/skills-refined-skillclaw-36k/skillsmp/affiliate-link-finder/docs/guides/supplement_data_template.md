# Supplement Data Template

This template defines the **standard format** for all supplement entries in the seeding service. Every supplement should follow this structure to ensure consistency across the app.

---

## Required Fields

### Basic Information
```json
{
  "id": "supplement-name-slug",           // Lowercase, hyphenated
  "name": "Supplement Name",               // Display name
  "category": "Category Name",             // Vitamins, Minerals, Nootropic, Herb, etc.
  "status": "beneficial"                   // beneficial | avoid | experimental
}
```

### Dosage Information
```json
{
  "dosage": "100mg",                       // Standard/default dose
  "timeOfDay": "morning",                  // morning | afternoon | evening | night | any
  "dosageFrequency": "Once daily with food", // Clear instruction
  "dosageWarnings": [                      // Array of cautions
    "Consult physician if...",
    "Do not exceed X mg"
  ]
}
```

### Weight-Based Dosing (Optional but Recommended)
```json
{
  "dosageByWeight": {
    "40-60": "100mg",
    "60-80": "150mg",
    "80-100": "200mg",
    "100-120": "250mg"
  }
}
```

### Benefits & Evidence
```json
{
  "benefits": ["Quick Benefit 1", "Benefit 2"],  // 2-4 concise benefits
  "detailedBenefits": [                          // Specific, measurable claims
    "Improves X by Y% in clinical trials",
    "Reduces Z in peer-reviewed studies"
  ],
  "evidenceLevel": "high",                       // high | moderate | low | preliminary
  "scientificEvidenceRank": 85                   // 0-100 score
}
```

### Scientific Details
```json
{
  "mechanismOfAction": "Clear explanation of how the supplement works at a biological level.",
  
  "timingRationale": "Explanation of why this timing is optimal (absorption, circadian rhythm, etc.)",
  
  "studyLinks": {
    "Study Title 1": "https://pubmed.ncbi.nlm.nih.gov/...",
    "Study Title 2": "https://pubmed.ncbi.nlm.nih.gov/..."
  }
}
```

### ADHD-Specific Data
```json
{
  "tldr": "One-sentence summary focused on ADHD benefits.",
  
  "adhdMedInteractions": {
    "Adderall": "How this supplement interacts with Adderall",
    "Vyvanse": "How this supplement interacts with Vyvanse",
    "Ritalin": "How this supplement interacts with Ritalin"
  },
  
  "contraindications": [                         // Who should avoid
    "People with X condition",
    "Those taking Y medication"
  ],
  
  "sideEffects": [                               // Potential adverse effects
    "Mild stomach upset in 5% of users",
    "Rare: headache if taken on empty stomach"
  ]
}
```

### Additional Notes
```json
{
  "notes": "Any additional context or usage tips"
}
```

---

## Complete Example: Magnesium Glycinate

```json
{
  "id": "magnesium-glycinate",
  "name": "Magnesium Glycinate",
  "category": "Mineral",
  "status": "beneficial",
  
  "dosage": "200mg",
  "timeOfDay": "evening",
  "dosageFrequency": "Once daily, preferably 1-2 hours before bed",
  "dosageWarnings": [
    "Start with 100mg to assess tolerance",
    "High doses (>400mg) may cause digestive discomfort",
    "Consult physician if you have kidney disease"
  ],
  
  "dosageByWeight": {
    "40-60": "150mg",
    "60-80": "200mg",
    "80-100": "300mg",
    "100-120": "400mg"
  },
  
  "benefits": ["Sleep Quality", "Muscle Relaxation", "Stress Reduction"],
  "detailedBenefits": [
    "Improves sleep latency by 17 minutes in clinical trials",
    "Reduces cortisol levels and anxiety symptoms",
    "Supports healthy dopamine regulation"
  ],
  
  "evidenceLevel": "high",
  "scientificEvidenceRank": 88,
  
  "mechanismOfAction": "Magnesium acts as a natural NMDA receptor antagonist, promoting GABA activity and regulating the HPA axis. Glycinate form has superior bioavailability and minimal GI side effects.",
  
  "timingRationale": "Evening dosing supports natural melatonin production and muscle relaxation before sleep. Glycinate's calming effect makes it ideal for bedtime.",
  
  "studyLinks": {
    "Magnesium supplementation for ADHD": "https://pubmed.ncbi.nlm.nih.gov/...",
    "Sleep quality improvement": "https://pubmed.ncbi.nlm.nih.gov/..."
  },
  
  "tldr": "Highly bioavailable magnesium that improves sleep quality and reduces anxiety without morning grogginess.",
  
  "adhdMedInteractions": {
    "Adderall": "May help reduce muscle tension and improve sleep quality disrupted by stimulants. Take 4+ hours after medication.",
    "Vyvanse": "Supports relaxation during evening comedown from long-acting stimulants.",
    "Ritalin": "No significant interaction; beneficial for sleep support."
  },
  
  "contraindications": [
    "People with kidney disease or impaired renal function",
    "Those taking magnesium-containing antacids concurrently"
  ],
  
  "sideEffects": [
    "Loose stools if dose exceeds tolerance (typically >500mg)",
    "Rare: mild drowsiness if taken during the day"
  ],
  
  "notes": "Glycinate form is preferred over oxide or citrate for ADHD due to better absorption and fewer GI side effects."
}
```

---

## Quality Standards

### ✅ DO:
- Use evidence-based claims with study citations
- Write in clear, accessible language (avoid excessive jargon)
- Include specific, measurable benefits where possible
- Provide actionable dosing guidance
- Address common ADHD medication interactions

### ❌ DON'T:
- Make unsubstantiated health claims
- Copy marketing language from supplement companies
- Omit safety warnings or contraindications
- Use vague benefits like "supports health"
- Forget to include timing rationale

---

## Evidence Ranking Guide

| Score | Level | Description |
|-------|-------|-------------|
| 90-100 | Gold Standard | Multiple high-quality RCTs, meta-analyses |
| 75-89 | High | Several RCTs, systematic reviews |
| 60-74 | Moderate | Some RCTs, observational studies |
| 40-59 | Low | Preliminary research, small studies |
| 0-39 | Minimal | Theoretical basis, anecdotal evidence |

---

## Category Definitions

- **Essential Fatty Acids**: Omega-3, Omega-6, etc.
- **Vitamins**: Fat-soluble (A, D, E, K) and water-soluble (B, C)
- **Minerals**: Magnesium, Zinc, Iron, etc.
- **Nootropic**: Cognitive enhancers (L-Theanine, Citicoline, etc.)
- **Herb**: Plant-based supplements (Ginkgo, Rhodiola, etc.)
- **Amino Acid**: L-Tyrosine, 5-HTP, etc.
- **Adaptogen**: Stress modulators (Ashwagandha, Rhodiola)

---

## Next Steps for Data Entry

1. Research the supplement on PubMed, examine.com, or similar reputable sources
2. Fill out all required fields using this template
3. Verify ADHD medication interactions for safety
4. Include at least 2 study links for credibility
5. Review against quality standards checklist
6. Test in the app to ensure proper display
