# Lab Automation - Validations

## Tip Reuse Between Different Samples

### **Id**
tip-reuse-different-samples
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - new_tip.*=.*['"]?never['"]?
  - for.*sample.*in.*samples(?![\s\S]{0,100}pick_up_tip)
### **Message**
Change tips between different samples to prevent cross-contamination.
### **Fix Action**
Use new_tip='always' or add pick_up_tip() in loop
### **Applies To**
  - **/*.py

## Reagent Volume Without Dead Volume

### **Id**
no-dead-volume-consideration
### **Severity**
info
### **Type**
regex
### **Pattern**
  - volume.*=.*\d+\s*\*\s*\d+(?![\s\S]{0,100}dead|extra|margin)
### **Message**
Add dead volume allowance when calculating reagent needs.
### **Applies To**
  - **/*.py

## Controls in Edge Wells

### **Id**
edge-well-controls
### **Severity**
info
### **Type**
regex
### **Pattern**
  - control.*['"][AH][1-9]|1[0-2]['"]
  - standard.*A1|H12|A12|H1
### **Message**
Consider placing critical controls in inner wells to avoid edge effects.
### **Applies To**
  - **/*.py
  - **/*.json

## Dispense Without Blow-Out

### **Id**
no-blow-out
### **Severity**
info
### **Type**
regex
### **Pattern**
  - dispense\([^)]*\)(?![\s\S]{0,50}blow_out)
### **Message**
Consider adding blow_out() after dispense for complete liquid transfer.
### **Applies To**
  - **/*.py

## Hardcoded Deck Position Without Label

### **Id**
hardcoded-deck-position
### **Severity**
info
### **Type**
regex
### **Pattern**
  - load_labware\([^,]+,\s*['"]\d+['"]\s*\)(?![\s\S]{0,50}label)
### **Message**
Add descriptive labels to labware for better protocol readability.
### **Fix Action**
Add label='Descriptive Name' parameter
### **Applies To**
  - **/*.py

## Protocol Without Error Handling

### **Id**
no-error-handling
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - def run\(protocol(?![\s\S]{0,500}try:|except|pause)
### **Message**
Add error handling and pause points for error recovery.
### **Applies To**
  - **/*.py

## Protocol Missing Metadata

### **Id**
no-protocol-metadata
### **Severity**
info
### **Type**
regex
### **Pattern**
  - def run\(protocol(?![\s\S]{0,200}metadata.*=)
### **Message**
Include metadata dict with protocolName, author, apiLevel.
### **Applies To**
  - **/*.py

## Aspirating from Bottom of Well

### **Id**
aspirate-bottom-zero
### **Severity**
info
### **Type**
regex
### **Pattern**
  - \.bottom\(0\)|bottom\(\s*\)
### **Message**
Aspirate from bottom(1) or higher to avoid tip contact with well bottom.
### **Fix Action**
Use .bottom(1) instead of .bottom() or .bottom(0)
### **Applies To**
  - **/*.py

## Fast Rate for Viscous Liquids

### **Id**
viscous-liquid-fast-rate
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - (glycerol|dmso|serum).*aspirate(?![\s\S]{0,100}rate.*0\.[0-3])
### **Message**
Use slower aspirate/dispense rates for viscous liquids.
### **Applies To**
  - **/*.py