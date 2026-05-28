# Supplement Intelligence & Data Plan

## 1. Classification & Ratings (Stars)
**Problem**: Currently all supplements default to 3/5 stars for `focusLevel`.
**Proposed Solution**: Implement a dynamic rating system based on:
- **Evidence Level**: High (5 stars), Moderate (4 stars), Low (3 stars).
- **ADHD-Specific Utility**: Boost or penalize based on study relevance to ADHD.
- **User Feedback**: (Future) Aggregate user efficacy scores.

### Implementation:
- [ ] Update `SupplementSeedingService` to assign varied `focusLevel` based on the research summary.
- [ ] Add `scientificEvidenceRank` (int 1-100) to `Supplement` entity for finer sorting.

---

## 2. Expanded Detail Info
**Goal**: Make the supplement detail page a "Mini Science Hub" for each item.

### New Data Fields to Add:
- [ ] **How it Works**: Simple explanation of the neurochemical mechanism (e.g., "Increases Dopamine availability").
- [ ] **ADHD Benefits**: Specific bullet points on how it helps with (Focus, Executive Function, Hyperactivity).
- [ ] **Clinical Studies**: Links or summaries of key research papers.
- [ ] **Timing Rationale**: Why it's recommended for Morning vs Night based on its half-life.
- [ ] **Visual Pill Registry**: High-quality images or detailed visual descriptions.

---

## 3. Action Plan for Tomorrow
1. **Domain Update**: Modify `Supplement` entity to include `mechanismOfAction`, `studyLinks`, and `detailedBenefits`.
2. **Infrastructure Update**: Update `firebase_supplement_repository` to handle new fields.
3. **Data Refresh**: Update the hardcoded/initial seeding data with rich information for the top 5 ADHD supplements (Omega-3, L-Theanine, Caffeine, Magnesium, Zinc).
4. **UI Update**: Overhaul `SupplementDetailScreen` with a tiered layout:
    - Quick Stats (Stars, Benefit Tag)
    - Mechanism (How it works)
    - Deep Dive (Scientific evidence)
    - Interactions & Safety (Current existing info)
