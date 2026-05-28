# Contract Analysis

## Patterns

### **Golden Rules**
  
---
    ##### **Rule**
Never skip human review
    ##### **Reason**
AI finds patterns, lawyers find issues
  
---
    ##### **Rule**
Benchmark against playbook
    ##### **Reason**
Standard terms define 'acceptable'
  
---
    ##### **Rule**
Flag missing clauses
    ##### **Reason**
What's NOT there matters most
  
---
    ##### **Rule**
Track versions
    ##### **Reason**
Changes between drafts reveal intent
  
---
    ##### **Rule**
Context matters
    ##### **Reason**
Same clause means different things in different contracts
### **Analysis Pipeline**
  - INGEST - PDF/DOCX, OCR
  - PARSE - Structure, Sections
  - EXTRACT - Clauses, Dates, Parties
  - ANALYZE - Compare to Playbook
  - REPORT - Risk Summary
### **Critical Clauses**
  #### **Indemnification**
    - Mutual vs. one-way
    - Scope of covered claims
    - Cap on liability
    - Exclusions and carve-outs
  #### **Limitation Of Liability**
    - Cap amount (ideally = contract value)
    - Exclusions from cap
    - Consequential damages waiver
    - Carve-outs for IP infringement
  #### **Termination**
    - Termination for convenience
    - Cure period for material breach
    - Wind-down obligations
    - Data return/destruction
  #### **Intellectual Property**
    - Ownership of work product
    - License scope and restrictions
    - Background IP rights
    - IP indemnification
  #### **Confidentiality**
    - Definition of confidential information
    - Permitted disclosures
    - Term of obligations
    - Return/destruction requirements
  #### **Data Protection**
    - Data processing scope
    - Subprocessor rights
    - Breach notification timeline
    - Data subject rights compliance
### **Risk Levels**
  #### **Low**
Standard terms, minor variations
  #### **Medium**
Some deviations, negotiable
  #### **High**
Significant risk, requires attention
  #### **Critical**
Unacceptable terms, must negotiate

## Anti-Patterns


---
  #### **Pattern**
Keyword-only search
  #### **Problem**
Misses synonyms and context
  #### **Solution**
Use NLP with semantic understanding

---
  #### **Pattern**
No playbook baseline
  #### **Problem**
Can't identify deviations
  #### **Solution**
Define standard acceptable terms

---
  #### **Pattern**
Ignoring missing clauses
  #### **Problem**
Silent risks
  #### **Solution**
Check for expected clause presence

---
  #### **Pattern**
Single-pass review
  #### **Problem**
Misses cross-references
  #### **Solution**
Analyze clause interactions

---
  #### **Pattern**
No version tracking
  #### **Problem**
Can't see negotiation history
  #### **Solution**
Compare all drafts