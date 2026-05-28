# I18N - Sharp Edges

## String Concatenation

### **Id**
string-concatenation
### **Summary**
Building sentences from translated parts
### **Severity**
high
### **Situation**
  English: "Hello " + name + "!". Works fine. German translation:
  puts name first. Spanish: different punctuation. Sentence
  structure varies by language. Concatenation breaks.
  
### **Why**
  Languages have different word orders and grammatical rules.
  What is "Hello {name}!" in English might be "{name}, hello!"
  in another language.
  
### **Solution**
  # USE ICU MESSAGE FORMAT
  
  // messages/en.json
  {
    "greeting": "Hello, {name}!"
  }
  
  // messages/de.json
  {
    "greeting": "Hallo, {name}!"
  }
  
  // Usage
  t("greeting", { name: "John" })
  
  // Plurals
  {
    "items": "{count, plural, =0 {No items} one {# item} other {# items}}"
  }
  
  // Select (gender, etc)
  {
    "welcome": "{gender, select, male {Mr.} female {Ms.} other {}} {name}"
  }
  
### **Symptoms**
  - Broken sentences in translations
  - Awkward word order
  - Incorrect pluralization
### **Detection Pattern**


## Text Expansion

### **Id**
text-expansion
### **Summary**
UI breaks with longer translations
### **Severity**
medium
### **Situation**
  English button: "Submit". German: "Einreichen". Russian:
  something even longer. Button overflows. Layout breaks.
  Text truncated.
  
### **Why**
  Different languages have different text lengths. German is
  typically 30% longer than English. Some languages much more.
  
### **Solution**
  # DESIGN FOR EXPANSION
  
  // Allow flexible widths
  <button className="px-4 py-2 whitespace-nowrap">
    {t("submit")}
  </button>
  
  // Or min-width instead of fixed
  <button className="min-w-[100px] px-4">
    {t("submit")}
  </button>
  
  // Test with pseudo-localization
  // Expands text: "Submit" -> "[Šüƀɱîţ----]"
  // Reveals layout issues early
  
  // Set max-width with ellipsis for extreme cases
  <span className="max-w-[200px] truncate">
    {t("longText")}
  </span>
  
### **Symptoms**
  - Layout breaks in some languages
  - Text overflow
  - Truncated content
### **Detection Pattern**


## Hardcoded Dates

### **Id**
hardcoded-dates
### **Summary**
Dates formatted for one locale
### **Severity**
medium
### **Situation**
  Date displayed as "12/05/2024". US user sees December 5.
  European user sees May 12. Confusion. Wrong appointments.
  Wrong deadlines.
  
### **Why**
  Date formats vary by locale. MM/DD/YYYY vs DD/MM/YYYY vs
  YYYY-MM-DD. Never assume format.
  
### **Solution**
  # USE INTL.DATETIMEFORMAT
  
  // WRONG
  const formatted = date.getMonth() + "/" + date.getDate();
  
  // RIGHT
  const formatted = new Intl.DateTimeFormat(locale, {
    dateStyle: "medium",
  }).format(date);
  
  // With next-intl
  const format = useFormatter();
  format.dateTime(date, { dateStyle: "long" })
  
  // Relative time
  format.relativeTime(date) // "2 days ago"
  
### **Symptoms**
  - Date confusion between locales
  - Wrong month/day interpretation
### **Detection Pattern**


## Rtl Afterthought

### **Id**
rtl-afterthought
### **Summary**
RTL languages break layout
### **Severity**
medium
### **Situation**
  App looks great in English. Launch in Arabic. Everything
  backwards but not correctly mirrored. Icons pointing wrong
  way. Padding on wrong side.
  
### **Why**
  RTL requires more than just text direction. Layouts need
  to mirror. Some elements (arrows, progress) should flip.
  Others (phone numbers) should not.
  
### **Solution**
  # DESIGN FOR RTL FROM START
  
  // Use logical properties
  // WRONG: margin-left
  // RIGHT: margin-inline-start
  
  <div className="ms-4">  {/* margin-start */}
    <p className="text-start">{t("text")}</p>
  </div>
  
  // Tailwind RTL plugin
  <div className="rtl:space-x-reverse">
  
  // Auto-flip with dir attribute
  <html lang={locale} dir={dir}>
  
  // Icons that should flip
  <ChevronRight className="rtl:rotate-180" />
  
  // Icons that should NOT flip
  <Phone />  {/* No flip needed */}
  
### **Symptoms**
  - Broken RTL layouts
  - Icons pointing wrong direction
  - Spacing issues in RTL
### **Detection Pattern**
