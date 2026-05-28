# Prompt Engineering Creative - Validations

## User input must be sanitized before prompt

### **Id**
no-user-input-concatenation
### **Severity**
critical
### **Description**
Direct user input in prompts enables injection attacks
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
prompt.*`[^`]*\$\{.*user|prompt.*\+.*user.*input|f".*{user
  #### **Exclude**
sanitize|escape|filter|validate|clean
### **Message**
User input concatenated into prompt without sanitization. Add input validation.
### **Autofix**


## System prompts should not be exposed

### **Id**
no-system-prompt-exposure
### **Severity**
critical
### **Description**
Exposing system prompts enables prompt extraction attacks
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
console\.log.*system.*prompt|print.*system.*prompt|response.*system
  #### **Exclude**
debug.*false|production|process\.env\.NODE_ENV
### **Message**
System prompt may be exposed in output. Remove or guard with debug flag.
### **Autofix**


## Image prompts should have structured elements

### **Id**
prompt-has-structure
### **Severity**
high
### **Description**
Effective prompts include subject, style, and technical parameters
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py,yaml}
  #### **Match**
(midjourney|dalle|flux|stable.diffusion).*prompt.*['"][^'"]{10,50}['"]
  #### **Exclude**
style|subject|lighting|camera|--ar|quality
### **Message**
Short image prompt may lack structure. Include subject, style, and technical elements.
### **Autofix**


## Vague adjectives need specific qualifiers

### **Id**
no-vague-adjectives-alone
### **Severity**
medium
### **Description**
Words like beautiful, amazing, cool need concrete descriptors
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py,yaml,md}
  #### **Match**
prompt.*(beautiful|amazing|cool|nice|perfect|epic)['",\s]
  #### **Exclude**
symmetrical|detailed|specific|style of|technique
### **Message**
Vague adjective in prompt. Add specific visual descriptors.
### **Autofix**


## Primary subject should be near prompt start

### **Id**
front-loaded-subject
### **Severity**
medium
### **Description**
Models weight earlier tokens more heavily
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py,yaml}
  #### **Match**
prompt.*['"][^'"]{100,}(portrait|photo|image|shot) of
### **Message**
Subject appears late in prompt. Consider front-loading important elements.
### **Autofix**


## Use model-appropriate prompt syntax

### **Id**
model-specific-syntax
### **Severity**
medium
### **Description**
Different models use different prompt languages
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
(dalle|openai).*::\d|midjourney.*\(\w+:\d\.\d\)
### **Message**
Prompt syntax may not match model. Midjourney uses ::weights, SD uses (word:weight).
### **Autofix**


## Image generation should include negative prompts

### **Id**
negative-prompt-present
### **Severity**
medium
### **Description**
Negative prompts prevent common artifacts
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
(stable.diffusion|flux|comfy).*generate(?!.*negative)
  #### **Exclude**
negative|--no|exclude
### **Message**
Image generation without negative prompt. Add to prevent artifacts.
### **Autofix**


## Prompt length should be appropriate for model

### **Id**
prompt-length-reasonable
### **Severity**
low
### **Description**
Very long prompts may be truncated or cause confusion
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py,yaml}
  #### **Match**
prompt.*['"][^'"]{500,}['"]
### **Message**
Very long prompt detected. Consider if all elements are necessary.
### **Autofix**


## Specify aspect ratio for image generation

### **Id**
aspect-ratio-specified
### **Severity**
low
### **Description**
Default aspect ratios may not suit content
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
(midjourney|dalle|flux).*generate
  #### **Exclude**
--ar|aspect|ratio|size|width.*height|dimension
### **Message**
Image generation without aspect ratio. Specify for better composition.
### **Autofix**


## Save seeds for reproducible results

### **Id**
seed-documented
### **Severity**
low
### **Description**
Seeds enable recreation of successful generations
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
seed.*=.*random|Math\.random.*seed
  #### **Exclude**
log|save|store|document
### **Message**
Random seed without logging. Save seed for reproducibility.
### **Autofix**


## Temperature setting matches use case

### **Id**
temperature-appropriate
### **Severity**
low
### **Description**
High temperature for creativity, low for consistency
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
temperature.*[01]\.\d
  #### **Exclude**
comment|config|documented
### **Message**
Temperature setting present. Verify it matches creativity/consistency needs.
### **Autofix**


## Prompt templates should validate variables

### **Id**
prompt-template-validated
### **Severity**
medium
### **Description**
Missing variables cause malformed prompts
### **Pattern**
  #### **File Glob**
**/*.{ts,js,py}
  #### **Match**
template.*\$\{|`.*\$\{.*prompt
  #### **Exclude**
validate|required|check|undefined|null
### **Message**
Prompt template without variable validation. Check for missing values.
### **Autofix**
