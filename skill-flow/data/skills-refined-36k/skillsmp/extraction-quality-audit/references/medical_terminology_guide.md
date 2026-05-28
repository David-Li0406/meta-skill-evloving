# Medical Terminology Verification Guide

Domain-specific guide for verifying medical document extraction quality.

## Overview

Medical documents require careful verification of:
- **Anatomical terminology** (body parts, organs, structures)
- **Diagnostic terminology** (conditions, findings, impressions)
- **Procedural terminology** (exams, tests, interventions)
- **Measurements with units** (15 mm, 120/80 mmHg, 98.6°F)
- **Portuguese accents** (for Portuguese medical documents)
- **Medical abbreviations** (ECG, MRI, CBC, etc.)

**Why medical terminology matters:**
- Clinical accuracy depends on precise terminology
- Misinterpretation can affect patient care
- Legal/regulatory compliance requires accuracy
- Medical records are often multi-decade archives

---

## Portuguese Accent Preservation

For Portuguese medical documents, accent preservation is critical for meaning.

### Portuguese Diacritics

| Character | Name | Example Medical Terms | Verification |
|-----------|------|----------------------|--------------|
| á, é, í, ó, ú | Acute accent | análise, métodos, índice, tórax, útero | Must be preserved exactly |
| â, ê, ô | Circumflex | exâme, três, oftalmológico | Must be preserved exactly |
| ã, õ | Tilde | transição, órgão, lesão | Must be preserved exactly |
| ç | Cedilla | coração, cirurgia, solução | Must be preserved exactly |

### Common Medical Terms with Accents

**Anatomical:**
- tórax (thorax)
- órgão (organ)
- útero (uterus)
- fígado (liver)
- coração (heart)
- estômago (stomach)
- pâncreas (pancreas)
- três (three)

**Diagnostic:**
- lesão (lesion)
- transição (transition)
- compressão (compression)
- solução (solution)
- análise (analysis)
- índice (index)
- crítico (critical)
- pélvico (pelvic)

**Procedural:**
- cirurgia (surgery)
- injeção (injection)
- radiológico (radiological)
- ecográfico (ultrasound)
- endoscópico (endoscopic)

### Verification Checklist

- [ ] All ó, ã, ç characters preserved?
- [ ] Common terms like "pólipo", "úlcera", "radiográfico" have accents?
- [ ] Doctor names with accents preserved (António, José)?
- [ ] Facility names with accents preserved (São Paulo)?

### Common Accent Loss Patterns

**Before extraction:**
```
Radiográfico do Tórax
Úlcera solitária do cólon
Dr. António José Silva
São Paulo, Brasil
```

**After extraction (WRONG):**
```
Radiografico do Torax  ❌
Ulcera solitaria do colon  ❌
Dr. Antonio Jose Silva  ❌
Sao Paulo, Brasil  ❌
```

**After extraction (CORRECT):**
```
Radiográfico do Tórax  ✓
Úlcera solitária do cólon  ✓
Dr. António José Silva  ✓
São Paulo, Brasil  ✓
```

---

## Anatomical Terminology

### Body Regions

**Common Terms:**
- Abdomen / Abdominal
- Torácico / Toráx (thoracic / thorax)
- Pélvico / Pélvis (pelvic / pelvis)
- Cervical (neck/cervical)
- Lombar (lumbar)
- Craniano (cranial)

**Verification:**
- Correct body part identified?
- Laterality correct (direito/esquerdo = right/left)?
- Anatomical position terms (anterior, posterior, lateral, medial)?

### Organs

**Digestive System:**
- Esôfago (esophagus)
- Estômago (stomach)
- Intestino (intestine)
- Cólon (colon)
- Reto (rectum)
- Fígado (liver)
- Vesícula biliar (gallbladder)
- Pâncreas (pancreas)

**Respiratory System:**
- Pulmão/Pulmões (lung/lungs)
- Brônquio (bronchus)
- Traqueia (trachea)
- Pleura (pleura)

**Cardiovascular:**
- Coração (heart)
- Aorta (aorta)
- Veia (vein)
- Artéria (artery)

**Nervous System:**
- Cérebro (brain)
- Medula (spinal cord/marrow)
- Nervo (nerve)

**Musculoskeletal:**
- Osso (bone)
- Músculo (muscle)
- Articulação (joint)
- Vértebra (vertebra)
- Joelho (knee)
- Ombro (shoulder)

### Verification Points

- [ ] Organ names spelled correctly?
- [ ] Plural forms correct (pulmão → pulmões)?
- [ ] Compound terms preserved (vesícula biliar)?
- [ ] Anatomical structures with correct accents?

---

## Diagnostic Terminology

### Common Findings

**Normal Findings:**
- Normal (normal)
- Sem alterações (without alterations)
- Dentro dos limites normais (within normal limits)
- Ausência de (absence of)

**Abnormal Findings:**
- Lesão (lesion)
- Úlcera (ulcer)
- Pólipo (polyp)
- Nódulo (nodule)
- Massa (mass)
- Tumor (tumor)
- Inflamação (inflammation)
- Edema (edema)
- Hemorragia (hemorrhage)
- Fratura (fracture)

### Imaging Findings

**X-ray/Radiography:**
- Radiograma (radiograph)
- Radiográfico (radiographic)
- Planos perpendiculares (perpendicular planes)
- Imagem de face (AP/frontal view)
- Radiograma de perfil (lateral view)
- Orientação segmentar (segmental orientation)
- Estrutura óssea (bone structure)

**Ultrasound:**
- Ecográfico (ultrasound/sonographic)
- Hiperecóico (hyperechoic)
- Hipoecóico (hypoechoic)
- Anecóico (anechoic)

**Endoscopy:**
- Mucosa (mucosa)
- Submucosa (submucosa)
- Biópsia (biopsy)
- Erosão (erosion)
- Ulceração (ulceration)

### Verification Points

- [ ] Diagnostic terms spelled correctly?
- [ ] "Normal" vs "abnormal" findings not confused?
- [ ] Negation preserved ("sem alterações" not changed to "alterações")?
- [ ] Severity descriptors preserved (leve, moderado, grave)?

---

## Measurements and Units

**Critical:** Measurements MUST be accurate. Errors can affect clinical decisions.

### Common Medical Measurements

**Length/Distance:**
- 15 mm (millimeters)
- 3.5 cm (centimeters)
- 1.2 m (meters)

**Volume:**
- 500 ml (milliliters)
- 1.5 L (liters)
- 250 cc (cubic centimeters)

**Weight:**
- 75 kg (kilograms)
- 180 g (grams)

**Frequency (EEG/ECG):**
- 10 Hz (Hertz)
- 60 bpm (beats per minute)

**Pressure:**
- 120/80 mmHg (millimeters of mercury)

**Temperature:**
- 37°C (Celsius)
- 98.6°F (Fahrenheit)

**Electrical (EEG):**
- 7 µV/mm (microvolts per millimeter)
- 50 µV (microvolts)

### Verification Checklist

- [ ] **Number correct?** 15 mm ≠ 16 mm
- [ ] **Unit present?** 15 mm ✓, 15 ❌
- [ ] **Unit correct?** 15 mm ✓, 15 cm ❌ (if source says mm)
- [ ] **Decimal preserved?** 3.5 cm ✓, 35 cm ❌
- [ ] **Range preserved?** 120/80 mmHg ✓, 120 mmHg ❌

### Common Measurement Errors

**WRONG:**
- "15" (unit missing) ❌
- "15cm" (no space acceptable: "15 cm") ✓
- "15 mm" transcribed as "15 cm" ❌
- "3.5 cm" transcribed as "35 cm" ❌
- "120/80 mmHg" transcribed as "120 mmHg" ❌

---

## Medical Abbreviations

### Common Abbreviations

**Exams:**
- ECG / EKG (electrocardiogram)
- EEG (electroencephalogram)
- RX (X-ray)
- TC / CT (computed tomography)
- RM / MRI (magnetic resonance imaging)
- ECO (ultrasound/echocardiography)
- RMN (ressonância magnética nuclear)

**Body Parts:**
- AP (anteroposterior)
- PA (posteroanterior)
- LL (lateral left)
- Rx (prescription)

**Medical Terms:**
- HTA (hipertensão arterial = hypertension)
- DM (diabetes mellitus)
- ICC (insuficiência cardíaca congestiva = CHF)

### Verification Points

- [ ] Abbreviations preserved as-is (don't expand unless explicitly done)?
- [ ] Period handling consistent (Dr. vs Dr)?
- [ ] Abbreviation spelled correctly (ECG not EGC)?

---

## Specialty-Specific Terminology

### Radiology

**Key terms:**
- Opacidade (opacity)
- Radiolucência (radiolucency)
- Consolidação (consolidation)
- Derrame (effusion)
- Pneumotórax (pneumothorax)
- Atelectasia (atelectasis)

**Verification:**
- Radiological descriptors accurate?
- Anatomical location correct?
- Comparison terms preserved (aumentado, reduzido)?

### Gastroenterology

**Key terms:**
- Esofagite (esophagitis)
- Gastrite (gastritis)
- Úlcera gástrica (gastric ulcer)
- Pólipo (polyp)
- Divertículo (diverticulum)
- Hemorroida (hemorrhoid)

**Verification:**
- GI tract location correct (esôfago, estômago, cólon)?
- Endoscopic findings preserved?
- Biopsy results captured?

### Cardiology

**Key terms:**
- Arritmia (arrhythmia)
- Taquicardia (tachycardia)
- Bradicardia (bradycardia)
- Hipertensão (hypertension)
- Sopro (murmur)
- Estenose (stenosis)

**Verification:**
- Heart rate/rhythm terms correct?
- Valve terms accurate?
- Blood pressure readings exact?

### Neurology

**Key terms:**
- Paroxístico (paroxysmal)
- Convulsão (seizure)
- Tremor (tremor)
- Paresia (paresis)
- Plegia (plegia)
- Ataxia (ataxia)

**Verification:**
- Neurological terms spelled correctly?
- EEG technical parameters accurate?
- Frequency measurements exact (Hz)?

---

## Clinical Findings Preservation

**Critical:** All findings must be preserved in summaries.

### What Must Be Captured

**Always include:**
- All abnormal findings
- All normal findings (establishes baseline)
- Measurements with units
- Impressions/conclusions
- Recommendations

**Examples:**

**Source Finding:**
```
Radiogramas dos joelhos obtidos em planos perpendiculares revelam
normal orientação segmentar na imagem de face e no radiograma de
perfil não há alterações quer da orientação quer da estrutura.
```

**Summary (CORRECT):**
```
Radiographs of the knees were obtained in perpendicular planes.
The frontal (AP) view reveals normal segmental orientation.
The lateral view shows no alterations in either orientation or structure.
```

**Summary (WRONG - missing details):**
```
Knee X-rays were normal.  ❌ (too brief, loses clinical details)
```

### Verification Checklist

- [ ] All abnormal findings mentioned?
- [ ] All normal findings mentioned?
- [ ] Measurements included in summary?
- [ ] Conclusions/impressions preserved?
- [ ] Recommendations included?
- [ ] No hallucinated findings?

---

## De-identification

Medical summaries often require de-identification while preserving clinical utility.

### What to Remove

**Personal Identifiers:**
- Patient name (full name, first name, last name)
- Patient ID numbers
- Address, phone number, email
- Social security numbers

**What to Keep:**
- Age (clinically relevant: "27-year-old patient")
- Gender (clinically relevant)
- Dates (clinically relevant for timeline)
- Doctor/provider names (may remove depending on use case)
- Facility names (may remove depending on use case)

### Verification Checklist

- [ ] Patient name removed from summary?
- [ ] Patient ID not included?
- [ ] Age preserved (if relevant)?
- [ ] Dates preserved?
- [ ] Clinical context maintained?

### Examples

**Source:**
```
Tiago André Dias Silva, 27 anos, masculino
Data: 2012-05-10
Exame: EEG
```

**Summary (CORRECT):**
```
A 27-year-old patient underwent EEG on 2012-05-10...
```

**Summary (WRONG):**
```
Tiago Silva, age 27, underwent EEG...  ❌ (name not removed)
```

---

## Common Extraction Challenges

### Handwritten Prescriptions

**Challenges:**
- Illegible handwriting
- Abbreviated medication names
- Dosage instructions unclear

**Verification:**
- Compare printed portions (header, footer) - should be perfect
- Handwritten portions: reasonable interpretation acceptable
- Medication names: verify against common drugs
- Flag uncertainties: `[uncertain: text]`

### Image-Heavy Pages

**Challenges:**
- Endoscopy photos, X-ray images
- Minimal text on page
- Descriptive text may vary

**Verification:**
- Image count correct?
- Image descriptions appropriate (no hallucinations)?
- Associated text captured?
- Low confidence expected and justified?

### Multi-Page Reports

**Challenges:**
- Consistency across pages
- Integration in summary

**Verification:**
- Metadata consistent across all pages?
- Each page content captured?
- Summary integrates findings from all pages?
- No duplicate content?

### Faded or Low-Quality Scans

**Challenges:**
- Difficult to read text
- OCR uncertainty

**Verification:**
- Is text legible to human?
- If barely legible to human, acceptable that LLM struggles
- Compare extraction to what is visible
- Low confidence justified?

---

## Quality Examples

### Example 1: Excellent Medical Terminology

**Source:**
```
Achado: úlcera solitária na transição recto sigmoideia,
pólipo submucoso de 15 mm com biópsia
```

**Extraction:**
```
Finding: solitary ulcer at the rectosigmoid transition,
15 mm submucosal polyp with biopsy
```

**Quality:** ★★★★★ Excellent
- All medical terms correct (úlcera, transição, pólipo, submucoso)
- Accents preserved in source
- Measurement with unit (15 mm)
- Accurate English translation

### Example 2: Good with Minor Issue

**Source:**
```
Mano pH: 5.2
```

**Extraction:**
```
Mano pH: 5.2
```

**Quality:** ★★★★ Good
- Slight spacing variation (minor)
- Measurement correct
- All essential information preserved

### Example 3: Fair - Accent Loss

**Source:**
```
Cirurgia cardíaca em São Paulo
```

**Extraction:**
```
Cirurgia cardiaca em Sao Paulo  ❌
```

**Quality:** ★★★ Fair
- Accent loss (í → i, ã → a)
- Otherwise correct
- Affects grade

---

## Tips for Medical Document Verification

1. **Use medical dictionaries** for unfamiliar terms
2. **Verify measurements twice** - critical for clinical accuracy
3. **Check Portuguese accents systematically** - common pattern
4. **Don't skip footers** - often contain facility/contact info
5. **Pay attention to negations** - "sem alterações" vs "alterações"
6. **Compare technical parameters** - EEG sensitivity, imaging planes
7. **Verify all numbers** - ages, dates, measurements, frequencies

---

## Resources

**Portuguese Medical Terminology:**
- DeCS (Descritores em Ciências da Saúde): https://decs.bvs.br/
- Portuguese medical dictionaries

**Medical Abbreviations:**
- Common medical abbreviation lists
- Specialty-specific glossaries

**Accent Reference:**
- Portuguese diacritics chart
- Unicode character reference

---

## Creating Guides for Other Domains

Use this guide as a template for other domains:

**Legal Documents:**
- Contract terminology
- Legal citations format
- Case law references
- Jurisdictional terms

**Financial Documents:**
- Accounting terminology
- Currency handling
- Numerical precision
- Financial abbreviations

**Scientific Documents:**
- Chemical formulas
- Mathematical equations
- Scientific notation
- Citation formats

**Technical Documents:**
- Code syntax
- API references
- Version numbers
- Technical specifications

---

## Version History

- **v1.0** (2026-01-21): Initial guide based on Portuguese medical document verification
