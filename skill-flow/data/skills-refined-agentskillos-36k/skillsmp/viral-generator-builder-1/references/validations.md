# Viral Generator Builder - Validations

## Missing Social Meta Tags

### **Id**
no-og-tags
### **Severity**
high
### **Type**
pattern
### **Check**
Should have Open Graph meta tags for sharing
### **Pattern**
og:image|og:title|twitter:card
### **Indicators**
  - No og: meta tags
  - Generic share previews
  - Missing twitter:card
### **Message**
Missing social meta tags - shares will look bad.
### **Fix Action**
Add dynamic og:image, og:title, og:description for each result

## Non-Deterministic Results

### **Id**
math-random-results
### **Severity**
medium
### **Type**
pattern
### **Check**
Results should be deterministic for same input
### **Pattern**
Math\.random\(\)
### **Indicators**
  - Math.random() without seed
  - Different results for same name
  - Pure randomness in results
### **Message**
Using Math.random() may give different results for same input.
### **Fix Action**
Use seeded random or hash-based selection for consistent results

## No Share Functionality

### **Id**
no-share-buttons
### **Severity**
medium
### **Type**
conceptual
### **Check**
Should have easy sharing options
### **Indicators**
  - No share buttons
  - No copy link option
  - No native share API
### **Message**
No easy way for users to share results.
### **Fix Action**
Add share buttons for major platforms and copy link option

## No Shareable Result Image

### **Id**
no-result-image
### **Severity**
medium
### **Type**
conceptual
### **Check**
Should generate shareable result images
### **Indicators**
  - Text-only results
  - No downloadable image
  - No screenshot-friendly design
### **Message**
No shareable image for results.
### **Fix Action**
Generate or design shareable result cards/images

## Desktop-First Result Design

### **Id**
desktop-first-design
### **Severity**
medium
### **Type**
conceptual
### **Check**
Results should be mobile-first
### **Indicators**
  - Wide layouts
  - Small mobile text
  - Horizontal scrolling
### **Message**
Results not optimized for mobile sharing.
### **Fix Action**
Design result cards mobile-first, test screenshots on phone