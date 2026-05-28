# Citation Styles Reference

## Contents
1. [Style Selection](#style-selection)
2. [AMA Style](#ama-style)
3. [Vancouver Style](#vancouver-style)
4. [APA Style](#apa-style)
5. [IEEE Style](#ieee-style)
6. [Journal-Specific Notes](#journal-specific-notes)

---

## Style Selection

| Style | Disciplines | In-Text Format |
|-------|-------------|----------------|
| AMA | Medicine, health sciences | Superscript¹ |
| Vancouver | Biomedical sciences | Brackets [1] |
| APA | Psychology, social sciences | Author-date (Smith, 2023) |
| IEEE | Engineering, CS | Brackets [1] |
| Nature | Multidisciplinary | Superscript¹ |

**Rule**: Always check target journal's author guidelines first.

---

## AMA Style

**In-text**: Superscript numbers in order of appearance, outside periods/commas.
```
Several studies demonstrated this effect.¹ The results were inconclusive,² 
although Smith et al³ reported otherwise. Multiple studies¹,³,⁵⁻⁷ confirmed this.
```

**Journal article**:
```
1. Smith JD, Johnson AB, Williams CD. Title of article. JAMA Psychiatry. 
   2023;80(5):456-464. doi:10.1001/jamapsychiatry.2023.0123
```

**Book**:
```
2. Author AA. Book Title. 2nd ed. Publisher; 2023.
```

**>6 authors**: List first 3, then "et al."

---

## Vancouver Style

**In-text**: Numbers in square brackets before periods.
```
Several studies showed this effect [1]. The results were inconclusive [2], 
although Smith et al [3] reported otherwise. Multiple studies [1,3,5-7] confirmed this.
```

**Journal article**:
```
1. Smith JD, Johnson AB, Williams CD. Title of article. JAMA Psychiatry. 
   2023;80(5):456-464.
```

**>6 authors**: List first 6, then "et al."

**Journal abbreviations**: Use PubMed/Index Medicus abbreviations.

---

## APA Style (7th Edition)

**In-text**: Author-date format.
```
One study found significant effects (Smith, 2023).
Smith (2023) found significant effects.
(Smith & Jones, 2023) — two authors
(Smith et al., 2023) — three+ authors
"Direct quote" (Smith, 2023, p. 45).
```

**Journal article**:
```
Smith, J. D., Johnson, A. B., & Williams, C. D. (2023). Title of article. 
   JAMA Psychiatry, 80(5), 456-464. https://doi.org/10.1001/jamapsychiatry.2023.0123
```

**Capitalization**: Sentence case for titles, title case for journals.

---

## IEEE Style

**In-text**: Numbers in square brackets.
```
Several studies [1] demonstrated this. The findings [1]-[3] suggest...
Smith [4] showed that multiple factors [4], [5] contributed.
```

**Journal article**:
```
[1] J. D. Smith and A. B. Johnson, "Title of article," JAMA Psychiatry, 
    vol. 80, no. 5, pp. 456-464, 2023, doi: 10.1001/jamapsychiatry.2023.0123.
```

**Conference paper**:
```
[2] J. D. Smith, "Title of paper," in Proc. Conf. Name, City, Country, 2023, pp. 1-8.
```

---

## Journal-Specific Notes

| Journal | Style | Key Features |
|---------|-------|--------------|
| JAMA Network | AMA | Superscript, abbreviated journals, no issue |
| NEJM | Vancouver | Brackets, 3 authors then et al |
| Lancet | Vancouver | PubMed abbreviations |
| Nature | Nature style | Superscript, no article titles |
| Cell Press | Cell style | Author-year |
| PLOS | Vancouver | Brackets, some use full journal names |
| IEEE journals | IEEE | Brackets, specific conference format |

### High-Impact Journals
- **Nature/Science**: Numbered, abbreviated, space-saving
- **NEJM/Lancet/JAMA**: Vancouver/AMA numbered
- **Cell family**: Author-date

### ML Conferences
- **NeurIPS/ICML/ICLR**: Check template; arXiv preprints accepted
- **CVPR/ICCV**: IEEE-like numbered
- **ACL/EMNLP**: Author-year (ACL style)

---

## Special Cases

**Preprints**:
```
APA: Author, A. A. (Year). Title [Preprint]. bioRxiv. https://doi.org/xx.xxxx
```

**Software**:
```
APA: Author, A. A. (Year). Package name (Version X.X) [Software]. URL
```

**Datasets**:
```
APA: Author, A. A. (Year). Dataset title (Version X) [Data set]. Repository. 
     https://doi.org/xx.xxxx
```

---

## Citation Quality Checklist

- [ ] ≥50% from last 5-10 years (2-3 years for ML conferences)
- [ ] <20% self-citations
- [ ] Primary sources (not citation chains)
- [ ] All in-text citations in reference list
- [ ] DOIs included where available
- [ ] Style matches target venue exactly
