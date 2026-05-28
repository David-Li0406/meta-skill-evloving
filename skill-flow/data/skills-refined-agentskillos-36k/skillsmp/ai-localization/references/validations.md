# Ai Localization - Validations

## Customer-facing translations must have native review

### **Id**
native-review-required
### **Severity**
critical
### **Description**
AI translations need human validation before publishing
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
(translate|localize).*publish|deploy.*translation
  #### **Exclude**
review|approve|validate|native|human
### **Message**
Publishing translation without review step. Add native speaker review.
### **Autofix**


## Localized content should have compliance check

### **Id**
legal-compliance-check
### **Severity**
critical
### **Description**
Different markets have different legal requirements
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py,yaml}
  #### **Match**
market|region.*publish|launch.*locale
  #### **Exclude**
legal|compliance|regulatory|disclaimer
### **Message**
Market launch without compliance check. Verify local legal requirements.
### **Autofix**


## RTL languages need proper layout support

### **Id**
rtl-support-check
### **Severity**
high
### **Description**
Arabic, Hebrew, Farsi need RTL layout handling
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py,css}
  #### **Match**
(ar|he|fa|ur).*locale|language.*(arabic|hebrew)
  #### **Exclude**
rtl|direction|dir=|logical|start|end
### **Message**
RTL language without RTL handling. Implement RTL layout support.
### **Autofix**


## UI elements should handle text expansion

### **Id**
text-expansion-buffer
### **Severity**
high
### **Description**
German text is 30% longer; layouts must accommodate
### **Pattern**
  #### **File Glob**
**/*.{ts,js,tsx,jsx,css}
  #### **Match**
width.*fixed|max-width.*px.*text|button.*width
  #### **Exclude**
flex|auto|%|min-content|fit-content
### **Message**
Fixed-width text element may truncate in longer languages. Use flexible sizing.
### **Autofix**


## Fonts must support target language characters

### **Id**
character-set-support
### **Severity**
high
### **Description**
CJK, Arabic, Cyrillic need appropriate font support
### **Pattern**
  #### **File Glob**
**/*.{css,scss}
  #### **Match**
font-family
  #### **Exclude**
Noto|sans-serif|system-ui|unicode|fallback
### **Message**
Font may not support all target languages. Include Unicode-complete fallback.
### **Autofix**


## Product/brand terms should use consistent translations

### **Id**
terminology-consistency
### **Severity**
medium
### **Description**
Same terms translated differently causes confusion
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
translate.*product|brand|name
  #### **Exclude**
terminology|glossary|dictionary|do.not.translate
### **Message**
Translating brand/product terms. Verify against terminology database.
### **Autofix**


## Translations should use translation memory

### **Id**
translation-memory-usage
### **Severity**
medium
### **Description**
Reusing approved translations ensures consistency
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
translate|localize
  #### **Exclude**
memory|tm|cache|stored|approved
### **Message**
Translation without memory lookup. Consider using translation memory.
### **Autofix**


## Translations should include context

### **Id**
context-provided
### **Severity**
medium
### **Description**
Context improves translation quality significantly
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
(ai|gpt|claude|deepl).*translate
  #### **Exclude**
context|description|where|usage
### **Message**
Translation without context. Provide usage context for better results.
### **Autofix**


## Source content should be translation-ready

### **Id**
source-quality-check
### **Severity**
low
### **Description**
Clear source produces better translations
### **Pattern**
  #### **File Glob**
**/*.{md,yaml}
  #### **Match**
translate|localize
  #### **Exclude**
reviewed|simplified|clear|i18n
### **Message**
Consider reviewing source content clarity before translation.
### **Autofix**


## Localized voice should match original speaker characteristics

### **Id**
voice-matching
### **Severity**
medium
### **Description**
Voice mismatch is jarring to viewers
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
voice.*translate|dub|localize.*audio
  #### **Exclude**
match|similar|characteristic|gender|age
### **Message**
Voice localization without matching. Verify voice characteristics match speaker.
### **Autofix**


## Dubbed audio must sync with video

### **Id**
audio-sync-check
### **Severity**
medium
### **Description**
Lip sync and timing must be considered
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
dub|voice.*video|audio.*localize
  #### **Exclude**
sync|timing|duration|lip|align
### **Message**
Audio localization without sync consideration. Verify timing alignment.
### **Autofix**


## Multiple items should be batch translated

### **Id**
batch-localization
### **Severity**
low
### **Description**
Batching is more efficient and consistent
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
for.*translate|forEach.*localize
  #### **Exclude**
batch|parallel|bulk|all
### **Message**
Sequential translation could be batched for efficiency.
### **Autofix**


## Specify fallback for missing translations

### **Id**
fallback-language
### **Severity**
low
### **Description**
Missing translations should fall back gracefully
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
getTranslation|i18n|t\(
  #### **Exclude**
fallback|default|en|english
### **Message**
Translation lookup without fallback. Add fallback language handling.
### **Autofix**
