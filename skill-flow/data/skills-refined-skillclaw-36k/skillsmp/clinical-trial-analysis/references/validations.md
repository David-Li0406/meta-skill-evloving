# Clinical Trial Analysis - Validations

## Cox Model Without PH Assumption Check

### **Id**
no-ph-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - CoxPH.*fit(?![\s\S]{0,500}check_assumptions|schoenfeld)
  - coxph.*formula(?![\s\S]{0,500}cox\.zph|proportional)
### **Message**
Test proportional hazards assumption before interpreting Cox model.
### **Fix Action**
Add cph.check_assumptions() or cox.zph() in R
### **Applies To**
  - **/*.py
  - **/*.R
  - **/*.ipynb

## Multiple Subgroups Without Adjustment

### **Id**
no-multiplicity-adjustment
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - subgroup.*p.*<.*0\.05(?![\s\S]{0,300}bonferroni|holm|multiplicity)
  - for.*subgroup.*in.*subgroups(?![\s\S]{0,500}adjust)
### **Message**
Adjust for multiplicity when testing multiple subgroups.
### **Applies To**
  - **/*.py
  - **/*.R
  - **/*.ipynb

## Survival Analysis Without Censoring Check

### **Id**
no-censoring-check
### **Severity**
info
### **Type**
regex
### **Pattern**
  - KaplanMeier(?![\s\S]{0,500}censor|at_risk)
  - survfit(?![\s\S]{0,500}censor)
### **Message**
Verify censoring is non-informative and report at-risk numbers.
### **Applies To**
  - **/*.py
  - **/*.R
  - **/*.ipynb

## Interpreting Hazard Ratio as Relative Risk

### **Id**
hr-as-relative-risk
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - hazard.*ratio.*relative.*risk
  - HR.*=.*RR
  - risk.*reduction.*hazard
### **Message**
Hazard ratio is not the same as relative risk. Don't conflate.
### **Applies To**
  - **/*.py
  - **/*.R
  - **/*.md

## No Crossover Adjustment in Analysis

### **Id**
missing-itm-for-crossover
### **Severity**
info
### **Type**
regex
### **Pattern**
  - crossover(?![\s\S]{0,500}RPSFT|IPCW|adjust)
  - switch.*treatment(?![\s\S]{0,500}sensitivity)
### **Message**
Consider RPSFT or IPCW methods to adjust for treatment crossover.
### **Applies To**
  - **/*.py
  - **/*.R

## Post-Hoc Biomarker Cutoff Optimization

### **Id**
post-hoc-cutoff
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - optimize.*cutoff.*biomarker
  - find.*best.*threshold
  - for.*cut.*in.*range.*p.*value
### **Message**
Pre-specify biomarker cutoffs; post-hoc optimization invalidates inference.
### **Applies To**
  - **/*.py
  - **/*.R
  - **/*.ipynb

## Potential Immortal Time Bias

### **Id**
immortal-time-risk
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - time.*from.*diagnosis.*treatment
  - survival.*drug.*exposure(?![\s\S]{0,300}landmark|time.*varying)
### **Message**
Check for immortal time bias; use landmark or time-varying analysis.
### **Applies To**
  - **/*.py
  - **/*.R
  - **/*.ipynb

## PFS Primary Without OS Safety

### **Id**
no-os-safety-endpoint
### **Severity**
info
### **Type**
regex
### **Pattern**
  - primary.*endpoint.*PFS(?![\s\S]{0,500}OS.*safety)
  - progression.*free.*survival.*primary(?![\s\S]{0,500}overall.*survival)
### **Message**
Per FDA 2024 guidance, pre-specify OS as safety endpoint when PFS is primary.
### **Applies To**
  - **/*.py
  - **/*.R
  - **/*.md