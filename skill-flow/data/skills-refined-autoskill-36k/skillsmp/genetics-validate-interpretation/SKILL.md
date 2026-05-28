---
name: genetics-validate-interpretation
description: Validate genetic variant interpretations against SNPedia and clinical databases. Use when interpreting unknown SNPs, verifying allele orientation, or cross-checking risk assessments.
---

# Genetics Interpretation Validation

Validate genetic variant interpretations by cross-referencing with SNPedia and clinical databases.

## When to Use

- Interpreting SNPs NOT in reference files
- Verifying allele orientation (which genotype is risk allele)
- Cross-checking genetic risk assessments
- Investigating novel or rare variants
- Confirming Gilbert syndrome, pharmacogenomics, or health risk interpretations

## Workflow

1. Receive SNP rsID and observed genotype
2. Fetch SNPedia page for that SNP
3. Extract genotype interpretations and clinical significance
4. Compare observed genotype to reported risk/protective genotypes
5. Return validated interpretation with confidence level

## SNPedia Lookup

SNPedia URL format: `https://www.snpedia.com/index.php/{rsid}`

Example: `https://www.snpedia.com/index.php/rs887829`

### Information to Extract

- **Genotype interpretations**: (C;C), (C;T), (T;T) meanings
- **Risk allele**: Which allele increases risk
- **Clinical significance**: Magnitude and penetrance
- **Population frequency**: How common is each genotype
- **Related conditions**: Associated diseases/traits

## Output Format

```markdown
## SNP Validation: {rsid}

**Observed Genotype**: {genotype} (from 23andMe)

**SNPedia Interpretation**:
- **{genotype}**: {interpretation from SNPedia}
- **Risk Allele**: {allele}
- **Clinical Significance**: {description}

**Validation Status**: ✅ CONFIRMED / ⚠️ UNCERTAIN / ❌ CONTRADICTS

**Confidence**: HIGH / MODERATE / LOW

**Recommendation**:
{Any follow-up actions or caveats}

---

**Sources**:
- SNPedia: https://www.snpedia.com/index.php/{rsid}
```

## Example Use Cases

### Validate Gilbert Syndrome Interpretation

Input: rs887829 = CC
Output:
```
✅ CONFIRMED: CC genotype is normal/wild-type
❌ INCORRECT prior interpretation as risk allele
Correct interpretation: TT = Gilbert syndrome risk
```

### Check Unknown Pharmacogenomics SNP

Input: rs12345 = AG (not in reference files)
Output:
```
⚠️ MODERATE CONFIDENCE: AG = intermediate metabolizer for CYP2C19
Recommend: Cross-check with clinical pharmacogenomics database
```

## Integration Points

### In investigate-root-cause skill

Add validation step after genetics analysis:

```markdown
7. **Validate Genetics** (if genetics used): Use `genetics-validate-interpretation`
   skill to cross-check any SNP interpretations not in reference files
```

### In genetics-snp-lookup skill

Add note to interpretation section:

```markdown
⚠️ **If SNP not in reference files**: Use `genetics-validate-interpretation`
skill to fetch interpretation from SNPedia before making assumptions about allele orientation.
```

## Error Handling

- **SNPedia page not found**: Report "No SNPedia entry - interpretation uncertain"
- **Ambiguous results**: Report "Multiple interpretations found - recommend clinical genetic testing"
- **Web fetch fails**: Fallback to reference files only, note validation unavailable

## Execution Instructions

1. **Receive input**: rsID and genotype from user or calling skill
2. **Use WebFetch tool** to fetch SNPedia page:
   ```
   WebFetch(url="https://www.snpedia.com/index.php/{rsid}", prompt="Extract genotype interpretations, risk alleles, clinical significance, and population frequencies for this SNP")
   ```
3. **Parse response**: Extract key information from SNPedia content
4. **Compare**: Match observed genotype against SNPedia interpretations
5. **Format output**: Use standard output format above
6. **Return**: Validation status with confidence level

## Key Validation Checks

### Allele Orientation
- Verify which allele is the risk allele (major vs minor)
- Confirm genotype notation matches 23andMe format
- Check for strand orientation issues (+ vs - strand)

### Clinical Significance
- Is this SNP clinically actionable?
- What is the magnitude of effect?
- What is the penetrance (how often does genotype cause phenotype)?

### Population Context
- How common is this genotype in the population?
- Are there ethnic-specific interpretations?

## Limitations

- SNPedia coverage varies by SNP
- Some SNPs have conflicting research findings
- 23andMe genotyping may miss important variants (e.g., UGT1A1*28)
- Tag SNPs may not be the functional variant
- Recommend clinical genetic testing for diagnostic confirmation

---

## Advanced Validation: Allele Orientation Detection

### The Strand Problem

23andMe reports genotypes on the **forward (+) strand**, but research literature may report on the **reverse (-) strand**. This causes confusion when matching genotypes to risk alleles.

**Example**: rs1801133 (MTHFR C677T)
- 23andMe reports: A/G (forward strand)
- Some literature reports: T/C (reverse strand - complementary bases)
- These are the **same genotype** on different strands

### Complementary Base Pairs

| Forward (+) | Reverse (-) |
|-------------|-------------|
| A | T |
| T | A |
| C | G |
| G | C |

### Validation Workflow for Strand Issues

1. **Get genotype from 23andMe** (always forward strand):
   ```bash
   grep "^rs1801133" "{genetics_23andme_path}"
   # Returns: rs1801133  1  11856378  AG
   ```

2. **Fetch SNPedia page** and check reported alleles:
   ```
   WebFetch(url="https://www.snpedia.com/index.php/rs1801133",
            prompt="What strand does this page report? List all genotype variations and their interpretations.")
   ```

3. **Compare and translate**:
   ```markdown
   **23andMe (forward)**: A/G
   **SNPedia (if reverse)**: T/C (complementary)
   **Match**: A↔T, G↔C → Same genotype, different notation
   ```

4. **Report with clarification**:
   ```markdown
   ## Strand Reconciliation: rs1801133

   | Source | Reported | Strand | Normalized |
   |--------|----------|--------|------------|
   | 23andMe | A/G | + (forward) | A/G |
   | SNPedia | T/C | - (reverse) | A/G |

   **Resolution**: Genotypes match after strand normalization.
   ```

### Common SNPs with Strand Confusion

| rsID | Gene | 23andMe (forward) | Literature often reports | Notes |
|------|------|-------------------|-------------------------|-------|
| rs1801133 | MTHFR | A/G | T/C | C677T naming uses reverse |
| rs1801131 | MTHFR | T/G | A/C | A1298C naming uses reverse |
| rs1799945 | HFE | C/G | C/G | Same on both strands |
| rs1800562 | HFE | G/A | G/A | Same on both strands |

### When to Suspect Strand Issues

- Your genotype doesn't appear in SNPedia's genotype list
- The reported risk allele is the complement of what you have
- Literature uses gene-centric notation (e.g., "C677T") instead of rsID

---

## Advanced Validation: Population Frequency Analysis

### Why Population Frequency Matters

A rare genotype in European populations might be common in Asian populations. Interpretation must consider the patient's ancestry.

### Workflow for Population Frequency Check

1. **Get genotype and patient ancestry** from profile demographics

2. **Query SNPedia for frequency data**:
   ```
   WebFetch(url="https://www.snpedia.com/index.php/{rsid}",
            prompt="Extract population allele frequencies by ethnic group if available. Look for gnomAD, 1000 Genomes, or HapMap data.")
   ```

3. **Calculate genotype expected frequency**:
   ```
   For a genotype AA with allele frequency p(A):
   Expected frequency = p(A)² (Hardy-Weinberg)

   For heterozygote AG with p(A) and p(G):
   Expected frequency = 2 × p(A) × p(G)
   ```

4. **Interpret in context**:
   ```markdown
   ## Population Context: rs429358 (APOE)

   **Your Genotype**: C/C (ε4/ε4)

   | Population | ε4 Frequency | ε4/ε4 Expected | Interpretation |
   |------------|--------------|----------------|----------------|
   | European | ~14% | ~2% | Uncommon but not rare |
   | African | ~20% | ~4% | More common |
   | East Asian | ~9% | ~0.8% | Relatively rare |
   | Finnish | ~23% | ~5% | Most common |

   **Patient ancestry**: European
   **Expected frequency**: ~2% (1 in 50)
   **Clinical note**: Uncommon genotype with highest Alzheimer's risk
   ```

### Population Frequency Categories

| Category | Frequency | Interpretation |
|----------|-----------|----------------|
| Very common | >10% | Population variant, normal |
| Common | 1-10% | Frequent, often benign |
| Uncommon | 0.1-1% | May warrant attention |
| Rare | 0.01-0.1% | Often clinically significant |
| Very rare | <0.01% | High likelihood of pathogenicity if phenotype matches |

---

## Advanced Validation: Penetrance Assessment

### What is Penetrance?

**Penetrance** = Probability that a person with a genotype will express the associated phenotype.

- **Complete penetrance** (100%): Everyone with genotype has phenotype
- **High penetrance** (>80%): Most people with genotype have phenotype
- **Reduced penetrance** (20-80%): Variable expression
- **Low penetrance** (<20%): Most carriers are unaffected

### Penetrance Factors

1. **Age-dependent penetrance**: Risk increases with age (e.g., BRCA, APOE)
2. **Sex-dependent penetrance**: Different risk by gender (e.g., hemochromatosis)
3. **Modifier genes**: Other variants affect expression
4. **Environment**: Lifestyle, exposures, epigenetics

### Penetrance Assessment Workflow

1. **Look up penetrance data**:
   ```
   WebFetch(url="https://www.snpedia.com/index.php/{rsid}",
            prompt="What is the penetrance of this variant? Is it age-dependent? Are there modifier factors?")
   ```

2. **Apply to patient context**:
   ```markdown
   ## Penetrance Assessment: rs80357906 (BRCA1)

   **Variant**: BRCA1 185delAG (Ashkenazi founder)
   **Your Genotype**: Heterozygous carrier

   **Penetrance Data**:
   | Age | Breast Cancer Risk | Ovarian Cancer Risk |
   |-----|-------------------|---------------------|
   | 40 | 20% | 3% |
   | 50 | 40% | 10% |
   | 70 | 55-65% | 39-44% |

   **Modifiers**:
   - Family history of early-onset cancer → increases risk
   - BRCA2 co-carrier → substantially increases risk
   - Lifestyle factors (alcohol, obesity) → modulate risk

   **Clinical Note**: High but incomplete penetrance. Not all carriers develop cancer.
   Recommend: Genetic counseling, enhanced screening protocol.
   ```

3. **Quantify confidence based on penetrance**:

   | Penetrance | Risk Statement Confidence |
   |------------|---------------------------|
   | Complete (100%) | "Will develop" → HIGH |
   | High (>80%) | "Very likely to develop" → HIGH |
   | Moderate (50-80%) | "May develop" → MODERATE |
   | Reduced (20-50%) | "At increased risk" → MODERATE |
   | Low (<20%) | "Slightly increased risk" → LOW |

---

## Validation Checklist

Use this checklist for every genetic interpretation validation:

### Pre-Validation Checks

- [ ] **Genotype confirmed**: Verified genotype from 23andMe raw data
- [ ] **rsID format valid**: Matches rs[0-9]+ pattern
- [ ] **SNPedia page exists**: WebFetch returned content (not 404)

### Strand and Allele Checks

- [ ] **Strand identified**: Determined if SNPedia uses forward or reverse strand
- [ ] **Genotype translated**: If strand mismatch, converted to matching notation
- [ ] **Risk allele identified**: Know which allele increases/decreases risk
- [ ] **Genotype in SNPedia list**: Your genotype appears in documented genotypes

### Clinical Context Checks

- [ ] **Population frequency obtained**: Have frequency for patient's ancestry
- [ ] **Penetrance assessed**: Know likelihood genotype causes phenotype
- [ ] **Age-dependence noted**: If applicable, risk by age documented
- [ ] **Modifier factors considered**: Other genes, environment, lifestyle

### Quality Checks

- [ ] **Multiple sources consulted**: Not relying solely on SNPedia
- [ ] **Recent research checked**: SNPedia may be outdated
- [ ] **Clinical actionability assessed**: Is this finding clinically useful?
- [ ] **Limitations documented**: What don't we know?

### Output Requirements

- [ ] **Validation status clear**: CONFIRMED / UNCERTAIN / CONTRADICTS
- [ ] **Confidence level stated**: HIGH / MODERATE / LOW with reasoning
- [ ] **Sources cited**: URLs to SNPedia pages and any other references
- [ ] **Recommendations included**: What should user/provider do with this info?

---

## Extended Error Handling

### SNPedia Page Not Found

When SNPedia returns 404 or empty content:

```markdown
## SNP Validation: rs999999999

**Status**: ⚠️ NOT FOUND IN SNPEDIA

**Possible reasons**:
1. **Invalid rsID**: Check for typos. Verify rsID in dbSNP.
2. **Very new SNP**: Recently discovered, not yet in SNPedia.
3. **Merged rsID**: Old rsID merged into another. Search dbSNP for current ID.
4. **Very rare variant**: Low research interest, limited documentation.

**Alternative lookup methods**:
1. **dbSNP**: https://www.ncbi.nlm.nih.gov/snp/{rsid}
2. **ClinVar**: https://www.ncbi.nlm.nih.gov/clinvar/?term={rsid}
3. **gnomAD**: https://gnomad.broadinstitute.org/variant/{rsid}
4. **PubMed search**: "rs999999999" or gene name + variant

**Recommendation**:
If SNP is clinically important, search alternative databases.
If still not found, interpretation confidence is VERY LOW.
```

### Conflicting Information

When SNPedia shows contradictory research:

```markdown
## SNP Validation: rs12345 - CONFLICTING DATA

**Your Genotype**: A/G

**Conflicting interpretations found**:

| Study | Year | Finding | Sample Size |
|-------|------|---------|-------------|
| Smith et al. | 2018 | AG = increased risk | n=500 |
| Jones et al. | 2021 | AG = no association | n=5000 |
| Lee et al. | 2023 | AG = protective | n=12000 |

**Resolution strategy**:
1. **Prefer larger studies**: Jones and Lee have more statistical power
2. **Prefer recent studies**: Lee 2023 is most current
3. **Check for confounders**: Different populations, methods, endpoints?
4. **Meta-analysis available?**: Look for systematic reviews

**Interpretation**: UNCERTAIN
More recent, larger studies suggest AG may be neutral or protective.
Earlier small study may have been false positive.

**Confidence**: LOW (conflicting evidence)
```

### Malformed Cache Recovery

If cache file is corrupted:

```bash
cache_file=".claude/skills/health-agent/genetics-snp-lookup/.cache/${rsid}.json"

# Try to load cache
if ! python3 -c "import json; json.load(open('$cache_file'))" 2>/dev/null; then
  echo "WARNING: Corrupted cache for $rsid, removing and fetching fresh"
  rm -f "$cache_file"
  # Proceed to fresh fetch
fi
```

### Network Timeout Handling

```bash
# Use timeout command (30 seconds default)
timeout 30 curl -A "health-agent/1.0" -s \
  "https://bots.snpedia.com/api.php?action=parse&page=${rsid}&format=json" \
  > "/tmp/claude/${rsid}_snpedia.json"

if [ $? -eq 124 ]; then
  echo "ERROR: SNPedia request timed out after 30s"
  # Try cache fallback
  if [ -f "$cache_file" ]; then
    echo "Using stale cache for $rsid"
    cat "$cache_file"
  else
    echo "No cache available, validation incomplete"
  fi
fi
```

---

## Integration with Other Genetics Skills

### Calling from investigate-root-cause

When the investigate-root-cause skill finds a potentially relevant SNP:

```markdown
## Phase: Genetics Validation

For each SNP mentioned in hypothesis:

1. **Verify genotype** using `genetics-snp-lookup`
2. **Validate interpretation** using this skill (`genetics-validate-interpretation`)
3. **Document validation status** in hypothesis evidence

**Example integration**:
Hypothesis mentions rs887829 (Gilbert syndrome marker)
→ genetics-snp-lookup returns: CC genotype
→ genetics-validate-interpretation confirms:
   - SNPedia says CC = normal (NOT Gilbert)
   - Previous interpretation was WRONG
   - Adjusted hypothesis confidence accordingly
```

### Calling from genetics-snp-lookup

When genetics-snp-lookup encounters ambiguous or unexpected results:

```markdown
## Auto-Validation Triggers

genetics-snp-lookup should invoke genetics-validate-interpretation when:

1. **Genotype not in reference files**: Unknown clinical significance
2. **Strand confusion suspected**: Genotype doesn't match expected patterns
3. **User explicitly requests validation**: "Validate this interpretation"
4. **High-stakes interpretation**: BRCA, APOE, pharmacogenomics results
```

### Calling from genetics-selfdecode-lookup

When comparing SelfDecode imputed data with SNPedia:

```markdown
## Cross-Source Validation

1. **Get imputed genotype** from SelfDecode
2. **If 23andMe also has this SNP**, compare for concordance
3. **Validate interpretation** against SNPedia
4. **Note imputation confidence** in output

**Example**:
SelfDecode (imputed): rs12345 = AG
23andMe (direct): rs12345 = AG (if available)
SNPedia: AG interpretation
→ High confidence if all sources agree
→ Use 23andMe if sources disagree (direct genotyping > imputation)
```

---

## Example: Complete Validation Workflow

**User request**: "Validate my interpretation of rs887829 for Gilbert syndrome"

### Step 1: Get Genotype

```bash
grep "^rs887829" "{genetics_23andme_path}"
# Output: rs887829  2  234668879  CC
```

### Step 2: Fetch SNPedia

```
WebFetch(url="https://www.snpedia.com/index.php/rs887829",
         prompt="Extract all genotype interpretations, risk alleles, and Gilbert syndrome association")
```

### Step 3: Parse and Compare

SNPedia returns:
- TT = Gilbert syndrome (elevated bilirubin)
- CT = Carrier, mildly elevated bilirubin
- CC = Normal (wild-type)

Patient genotype: CC

### Step 4: Validate

```markdown
## SNP Validation: rs887829

**Observed Genotype**: CC (from 23andMe)

**SNPedia Interpretation**:
- **TT**: Gilbert syndrome - Elevated unconjugated bilirubin
- **CT**: Carrier - Mildly elevated bilirubin
- **CC**: Normal - Wild-type UGT1A1 promoter

**Your Genotype (CC)**: Normal/wild-type. NOT associated with Gilbert syndrome.

**Validation Checklist**:
- [x] Genotype confirmed in raw data
- [x] SNPedia page found
- [x] Strand verified (forward strand, matches 23andMe)
- [x] Genotype in documented list
- [x] Clinical interpretation clear

**Validation Status**: ✅ CONFIRMED

**Confidence**: HIGH

**Clinical Note**:
If patient has elevated bilirubin, Gilbert syndrome via this SNP is ruled out.
Consider other causes: other UGT1A1 variants (not on 23andMe), hemolysis, liver disease.

**If prior interpretation said CC = Gilbert**: ❌ INCORRECT
The risk allele is T, not C. CC is wild-type (normal).

---

**Sources**:
- SNPedia: https://www.snpedia.com/index.php/rs887829
- 23andMe raw data: verified CC genotype
```
