# Radulator Calculator Test Cases - Complete Reference

This file contains predefined test inputs and expected outputs for all 18 Radulator calculators organized by specialty.

## RADIOLOGY CALCULATORS (6)

### 1. Adrenal CT Washout Calculator

#### Test Case 1: Typical Adenoma
**Inputs:**
- Unenhanced HU: 10
- Portal Venous HU: 100
- Delayed (15 min) HU: 40

**Expected Outputs:**
- Absolute Washout: 66.7% (calculated as: ((100 - 40) / (100 - 10)) × 100)
- Relative Washout: 60.0% (calculated as: ((100 - 40) / 100) × 100)
- Interpretation: Suggests benign adenoma (both washouts meet thresholds)

#### Test Case 2: Non-adenoma
**Inputs:**
- Unenhanced HU: 20
- Portal Venous HU: 80
- Delayed (15 min) HU: 70

**Expected Outputs:**
- Absolute Washout: 16.7% (calculated as: ((80 - 70) / (80 - 20)) × 100)
- Relative Washout: 12.5% (calculated as: ((80 - 70) / 80) × 100)
- Interpretation: Does not meet criteria for adenoma

---

### 2. Adrenal MRI Chemical Shift

#### Test Case 1: Lipid-rich Adenoma
**Inputs:**
- In-phase Signal Intensity: 1000
- Out-of-phase Signal Intensity: 500

**Expected Outputs:**
- Signal Intensity Index (SII): 50.0% (calculated as: ((1000 - 500) / 1000) × 100)
- Chemical Shift Ratio (CSR): 2.0 (calculated as: 1000 / 500)
- Interpretation: Consistent with lipid-rich adenoma (SII > 16.5%)

#### Test Case 2: Non-adenoma
**Inputs:**
- In-phase Signal Intensity: 800
- Out-of-phase Signal Intensity: 750

**Expected Outputs:**
- Signal Intensity Index (SII): 6.25% (calculated as: ((800 - 750) / 800) × 100)
- Chemical Shift Ratio (CSR): 1.067 (calculated as: 800 / 750)
- Interpretation: Does not meet criteria for lipid-rich adenoma

---

### 3. Prostate Volume & PSA Density

#### Test Case 1: Normal Prostate
**Inputs:**
- Length: 4 cm
- Height: 3 cm
- Width: 3.5 cm
- PSA: 2 ng/mL

**Expected Outputs:**
- Prostate Volume: 21.84 mL (calculated as: 4 × 3 × 3.5 × 0.52)
- PSA Density: 0.092 ng/mL/mL (calculated as: 2 / 21.84)
- Interpretation: Normal PSA density (< 0.15 ng/mL/mL)

#### Test Case 2: Elevated PSA Density
**Inputs:**
- Length: 3.5 cm
- Height: 2.5 cm
- Width: 3 cm
- PSA: 5.5 ng/mL

**Expected Outputs:**
- Prostate Volume: 13.65 mL (calculated as: 3.5 × 2.5 × 3 × 0.52)
- PSA Density: 0.403 ng/mL/mL (calculated as: 5.5 / 13.65)
- Interpretation: Elevated PSA density (> 0.15 ng/mL/mL)

---

### 4. Renal Cyst (Bosniak Classification)

#### Test Case 1: Simple Cyst (Bosniak I)
**Inputs:**
- Homogeneous water attenuation: Yes
- Thin imperceptible wall: Yes
- No septa, calcifications, or enhancement: Yes

**Expected Output:**
- Classification: Bosniak I
- Interpretation: Benign simple cyst, no follow-up needed

#### Test Case 2: Complex Cyst (Bosniak III)
**Inputs:**
- Thickened irregular walls or septa: Yes
- Measurable enhancement present: Yes
- Multiple thin septa: Yes

**Expected Output:**
- Classification: Bosniak III
- Interpretation: Indeterminate cystic mass, surgical exploration recommended

---

### 5. Spleen Size (Upper Limit of Normal)

#### Test Case 1: Normal Spleen
**Inputs:**
- Craniocaudal Length: 11 cm
- Age: 40 years
- Sex: Male

**Expected Outputs:**
- Upper Limit Normal (ULN): 12.5 cm (varies by age/sex)
- Assessment: Normal (within ULN)

#### Test Case 2: Splenomegaly
**Inputs:**
- Craniocaudal Length: 15 cm
- Age: 35 years
- Sex: Female

**Expected Outputs:**
- Upper Limit Normal (ULN): 11.5 cm (varies by age/sex)
- Assessment: Splenomegaly (exceeds ULN)

---

### 6. Hip Dysplasia Indices (DDH)

#### Test Case 1: Normal Hip
**Inputs:**
- Alpha Angle: 62°
- Beta Angle: 52°
- Femoral Head Coverage: 60%

**Expected Outputs:**
- Classification: Normal (Type Ia: α > 60°, β < 55°)
- Interpretation: Normal hip development

#### Test Case 2: Dysplastic Hip
**Inputs:**
- Alpha Angle: 45°
- Beta Angle: 65°
- Femoral Head Coverage: 40%

**Expected Outputs:**
- Classification: Dysplastic (Type III: α 43-49°, β > 77°)
- Interpretation: Hip dysplasia, treatment required

---

## HEPATOLOGY/LIVER CALCULATORS (9)

### 7. ALBI Score (Albumin-Bilirubin Grade)

#### Test Case 1: Grade 1 (Best Liver Function) - SI Units
**Inputs:**
- Unit System: SI units (μmol/L, g/L)
- Serum Albumin: 40 g/L
- Total Bilirubin: 15 μmol/L

**Expected Outputs:**
- ALBI Score: -2.872 (calculated as: (log₁₀(15) × 0.66) + (40 × −0.0852))
- ALBI Grade: Grade 1
- Interpretation: Best liver function - well-compensated
- Prognosis: Suitable for curative therapies

#### Test Case 2: Grade 2 (Intermediate) - US Units
**Inputs:**
- Unit System: US units (mg/dL, g/dL)
- Serum Albumin: 3.2 g/dL (32 g/L)
- Total Bilirubin: 2.5 mg/dL (42.76 μmol/L)

**Expected Outputs:**
- ALBI Score: -1.832 (approximately)
- ALBI Grade: Grade 2
- Interpretation: Intermediate liver function - moderately compensated

#### Test Case 3: Grade 3 (Worst Liver Function)
**Inputs:**
- Unit System: SI units
- Serum Albumin: 25 g/L
- Total Bilirubin: 80 μmol/L

**Expected Outputs:**
- ALBI Score: -0.873 (approximately)
- ALBI Grade: Grade 3
- Interpretation: Worst liver function - poorly compensated

---

### 8. Child-Pugh Score

#### Test Case 1: Class A (Well-Compensated)
**Inputs:**
- Total Bilirubin: 1.5 mg/dL
- Serum Albumin: 3.8 g/dL
- INR: 1.2
- Ascites: None
- Hepatic Encephalopathy: None

**Expected Outputs:**
- Total Score: 5 points
- Child-Pugh Class: A
- 1-Year Mortality: 5-10%
- Perioperative Mortality: 10%

#### Test Case 2: Class B (Significant Compromise)
**Inputs:**
- Total Bilirubin: 2.5 mg/dL
- Serum Albumin: 3.0 g/dL
- INR: 1.9
- Ascites: Slight
- Hepatic Encephalopathy: Grade 1-2

**Expected Outputs:**
- Total Score: 8 points
- Child-Pugh Class: B
- 1-Year Mortality: 15-20%
- Perioperative Mortality: 30%

#### Test Case 3: Class C (Decompensated)
**Inputs:**
- Total Bilirubin: 4.0 mg/dL
- Serum Albumin: 2.5 g/dL
- INR: 2.5
- Ascites: Moderate to Severe
- Hepatic Encephalopathy: Grade 3-4

**Expected Outputs:**
- Total Score: 13 points
- Child-Pugh Class: C
- 1-Year Mortality: 45-55%
- Perioperative Mortality: 70-80%

---

### 9. MELD-Na Score

#### Test Case 1: Low Risk (MELD-Na ≤9)
**Inputs:**
- Creatinine: 0.8 mg/dL
- Total Bilirubin: 1.0 mg/dL
- INR: 1.0
- Sodium: 140 mEq/L
- Dialysis: No

**Expected Outputs:**
- MELD Score: 6 (lower bounded)
- MELD-Na Score: 6
- 3-Month Mortality: 1.9%
- Risk Category: Low risk

#### Test Case 2: High Risk (MELD-Na 20-29)
**Inputs:**
- Creatinine: 3.5 mg/dL
- Total Bilirubin: 5.0 mg/dL
- INR: 2.0
- Sodium: 130 mEq/L
- Dialysis: No

**Expected Outputs:**
- MELD Score: 24 (approximately)
- MELD-Na Score: 28 (approximately, with sodium correction)
- 3-Month Mortality: 19.6%
- Risk Category: High risk
- Interpretation: High priority for transplantation

#### Test Case 3: On Dialysis
**Inputs:**
- Creatinine: 5.0 mg/dL
- Total Bilirubin: 3.0 mg/dL
- INR: 1.8
- Sodium: 135 mEq/L
- Dialysis: Yes

**Expected Outputs:**
- MELD Score: ~20 (creatinine set to 4.0 due to dialysis)
- Clinical Notes: "Creatinine set to 4.0 mg/dL (dialysis ≥2x/week or 24hr CVVHD)"

---

### 10. BCLC Staging (HCC)

#### Test Case 1: Stage 0 (Very Early)
**Inputs:**
- Number of Tumors: Single tumor
- Largest Tumor Size: 1.5 cm
- Vascular Invasion: None
- Extrahepatic Spread: None
- ECOG Performance Status: 0
- Bilirubin: 1.0 mg/dL
- Albumin: 4.0 g/dL
- INR: 1.1
- Ascites: None
- Encephalopathy: None

**Expected Outputs:**
- BCLC Stage: 0
- Child-Pugh Score: 5 points (Class A)
- Recommended Treatment: Resection or ablation (RFA/MWA) preferred
- Expected Prognosis: >5 years (5-year survival: 75%)

#### Test Case 2: Stage C (Advanced)
**Inputs:**
- Number of Tumors: Single tumor
- Largest Tumor Size: 6 cm
- Vascular Invasion: Portal vein - main trunk
- Extrahepatic Spread: None
- ECOG Performance Status: 0
- Bilirubin: 1.5 mg/dL
- Albumin: 3.5 g/dL
- INR: 1.3
- Ascites: None
- Encephalopathy: None

**Expected Outputs:**
- BCLC Stage: C
- Recommended Treatment: Systemic therapy (Atezolizumab + Bevacizumab)
- Expected Prognosis: ~2 years with systemic therapy

---

### 11. Milan Criteria (HCC Transplant Eligibility)

#### Test Case 1: Within Milan Criteria
**Inputs:**
- Number of Tumors: 2
- Largest Tumor Diameter: 2.5 cm
- Second Tumor Diameter: 2.0 cm
- Macrovascular Invasion: No
- Extrahepatic Disease: No

**Expected Outputs:**
- Milan Criteria: WITHIN CRITERIA (2 tumors, both ≤3 cm)
- UCSF Criteria: WITHIN CRITERIA
- Transplant Eligibility: Excellent candidate
- Post-transplant Survival: >70% 4-year survival

#### Test Case 2: Exceeds Milan, Within UCSF
**Inputs:**
- Number of Tumors: 1
- Largest Tumor Diameter: 6.0 cm
- Macrovascular Invasion: No
- Extrahepatic Disease: No

**Expected Outputs:**
- Milan Criteria: EXCEEDS (single tumor >5 cm)
- UCSF Criteria: WITHIN CRITERIA (single tumor ≤6.5 cm)
- Transplant Eligibility: May qualify under extended criteria

---

### 12. MR Elastography (Liver Fibrosis Staging)

#### Test Case 1: No/Minimal Fibrosis (F0-F1)
**Inputs:**
- Average Liver Stiffness: 2.2 kPa

**Expected Outputs:**
- Fibrosis Stage: F0-F1 (No or minimal fibrosis)
- Metavir Score: F0-F1
- Clinical Significance: Normal or minimal fibrosis

#### Test Case 2: Advanced Fibrosis (F3)
**Inputs:**
- Average Liver Stiffness: 4.5 kPa

**Expected Outputs:**
- Fibrosis Stage: F3 (Advanced fibrosis)
- Metavir Score: F3
- Clinical Significance: Advanced fibrosis, high risk for cirrhosis

#### Test Case 3: Cirrhosis (F4)
**Inputs:**
- Average Liver Stiffness: 6.0 kPa

**Expected Outputs:**
- Fibrosis Stage: F4 (Cirrhosis)
- Metavir Score: F4
- Clinical Significance: Cirrhosis, requires HCC surveillance

---

### 13. Adrenal Vein Sampling - Cortisol (Cushing)

**Note:** This calculator has complex multi-sample inputs. Simplified test case below.

#### Test Case 1: Right-sided Lateralization
**Inputs:**
- Infrarenal IVC Cortisol: 15 μg/dL
- Left Adrenal Vein Cortisol: 45 μg/dL
- Right Adrenal Vein Cortisol: 180 μg/dL
- Left Adrenal Epinephrine: 500 pg/mL
- Right Adrenal Epinephrine: 800 pg/mL

**Expected Outputs:**
- Lateralization: Right adrenal hypersecretion
- Cannulation Success: Both adrenals successfully cannulated (epinephrine gradients >100)
- Recommendation: Right adrenalectomy

---

### 14. Adrenal Vein Sampling - Aldosterone (Hyperaldosteronism)

**Note:** Similar complexity to AVS-Cortisol.

#### Test Case 1: Left-sided Lateralization
**Inputs:**
- IVC Aldosterone: 100 pg/mL
- Left Adrenal Aldosterone: 15000 pg/mL
- Right Adrenal Aldosterone: 1200 pg/mL
- Aldosterone-to-Cortisol Ratios confirm lateralization

**Expected Outputs:**
- Lateralization: Left adrenal adenoma
- Lateralization Index: >4:1 (left:right)
- Recommendation: Left adrenalectomy

---

### 15. Y-90 Radiation Segmentectomy

#### Test Case 1: MIRD Model - Segmentectomy
**Inputs:**
- Treatment Intent: Segmentectomy
- Dosimetry Model: MIRD (uniform)
- Target Segment Volume: 250 mL
- Target Dose: 190 Gy
- Lung Shunt Fraction: 8%

**Expected Outputs:**
- Prescribed Activity: ~2.3 GBq (calculated as: (190 × 0.25 × 0.92) / 49.67)
- Lung Dose: ~3.7 Gy (well below 30 Gy threshold)
- Safety Assessment: Safe to proceed

#### Test Case 2: Partition Model
**Inputs:**
- Treatment Intent: Segmentectomy
- Dosimetry Model: Partition (tumor/normal)
- Target Segment Volume: 300 mL
- Tumor Volume: 100 mL
- Tumor/Normal Ratio: 3:1
- Target Dose: 250 Gy
- Lung Shunt Fraction: 5%

**Expected Outputs:**
- Prescribed Activity: ~3.0 GBq (approximately)
- Tumor Dose: 250 Gy (target achieved)
- Normal Liver Dose: ~83 Gy
- Lung Dose: ~3.0 Gy

---

## UROLOGY CALCULATORS (3)

### 16. IPSS (International Prostate Symptom Score)

#### Test Case 1: Mild Symptoms
**Inputs:**
- Q1 (Incomplete emptying): 1
- Q2 (Frequency): 1
- Q3 (Intermittency): 0
- Q4 (Urgency): 1
- Q5 (Weak stream): 1
- Q6 (Straining): 0
- Q7 (Nocturia): 1
- Q8 (QoL): 2

**Expected Outputs:**
- Total IPSS Score: 5 points
- Severity: Mild (0-7)
- QoL Score: 2/6
- Management: Watchful waiting

#### Test Case 2: Moderate Symptoms
**Inputs:**
- Q1-Q7: All rated 2 (less than half the time)
- Q8 (QoL): 4

**Expected Outputs:**
- Total IPSS Score: 14 points
- Severity: Moderate (8-19)
- QoL Score: 4/6 (Mostly dissatisfied)
- Management: Medical therapy recommended

#### Test Case 3: Severe Symptoms
**Inputs:**
- Q1-Q7: All rated 4-5 (almost always)
- Average: 4.5 → Total ~32
- Q8 (QoL): 6 (Terrible)

**Expected Outputs:**
- Total IPSS Score: 30-35 points
- Severity: Severe (20-35)
- Management: Medical/surgical intervention

---

### 17. RENAL Nephrometry Score

#### Test Case 1: Low Complexity Tumor
**Inputs:**
- Tumor Diameter: 3.5 cm (R=1)
- Exophytic Nature: ≥50% exophytic (E=1)
- Nearness to Collecting System: ≥7 mm (N=1)
- Location Relative to Polar Line: Entirely above polar line (L=1)
- Anterior/Posterior: Anterior
- Hilar Location: No

**Expected Outputs:**
- RENAL Score: 4 points (1+1+1+1)
- Complexity: Low (4-6)
- Descriptor: 4a (anterior, non-hilar)
- Surgical Approach: Excellent candidate for partial nephrectomy

#### Test Case 2: High Complexity Tumor
**Inputs:**
- Tumor Diameter: 8.0 cm (R=3)
- Exophytic Nature: Entirely endophytic (E=3)
- Nearness to Collecting System: ≤4 mm (N=3)
- Location Relative to Polar Line: Crosses midline (L=3)
- Anterior/Posterior: Neither
- Hilar Location: Yes

**Expected Outputs:**
- RENAL Score: 12 points (3+3+3+3)
- Complexity: High (10-12)
- Descriptor: 12xh (indeterminate location, hilar)
- Surgical Approach: High surgical complexity, consider radical nephrectomy

---

### 18. SHIM Score (Sexual Health Inventory for Men)

#### Test Case 1: No ED
**Inputs:**
- Q1 (Confidence): 5 (Very high)
- Q2 (Erection hardness): 5 (Almost always)
- Q3 (Maintain erection): 5 (Almost always)
- Q4 (Difficulty maintaining): 5 (Not difficult)
- Q5 (Intercourse satisfaction): 5 (Almost always)

**Expected Outputs:**
- Total SHIM Score: 25 points
- Interpretation: No erectile dysfunction
- Classification: Normal erectile function

#### Test Case 2: Mild ED
**Inputs:**
- Q1: 4 (High)
- Q2: 4 (Most times)
- Q3: 3 (Sometimes)
- Q4: 3 (Difficult)
- Q5: 3 (Sometimes)

**Expected Outputs:**
- Total SHIM Score: 17 points
- Interpretation: Mild erectile dysfunction
- Management: Consider lifestyle modifications and counseling

#### Test Case 3: Severe ED
**Inputs:**
- Q1: 1 (Very low)
- Q2: 1 (Almost never)
- Q3: 1 (Almost never)
- Q4: 1 (Extremely difficult)
- Q5: 1 (Almost never)

**Expected Outputs:**
- Total SHIM Score: 5 points
- Interpretation: Severe erectile dysfunction
- Management: Medical/surgical intervention recommended

---

## Testing Notes

### General Testing Principles

1. **Precision**: All calculations should match expected values within tolerance:
   - Percentages: ±0.5%
   - Decimals: ±0.01
   - Integers: Exact match

2. **Console Errors**: No JavaScript errors should appear during calculation

3. **Network Requests**: Static app - no external API calls expected

4. **Performance**: Results should render within 500ms of clicking "Calculate"

5. **Validation**: Each calculator should validate inputs and show appropriate error messages for invalid data

### Formula References

All expected values are calculated using formulas documented in:
- Calculator source code comments
- Referenced peer-reviewed medical literature
- CLAUDE.md project documentation

### Test Data Sources

Test values are selected to represent:
- **Normal/typical cases**: Common clinical scenarios
- **Borderline cases**: Values near decision thresholds
- **Extreme cases**: Edge values within valid ranges
- **Mixed results**: Combinations showing different severity levels

---

*This test data supports automated QA testing via Playwright MCP and manual verification via Python scripts.*
