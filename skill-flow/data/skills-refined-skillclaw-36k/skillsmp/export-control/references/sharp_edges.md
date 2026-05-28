# Export Control - Sharp Edges

## ITAR Data on Foreign Cloud Servers

### **Id**
itar-cloud-exposure
### **Severity**
critical
### **Summary**
ITAR data stored on servers outside US or accessed by foreign persons
### **Symptoms**
  - Using cloud provider without ITAR compliance
  - Data replicated to foreign regions
  - Foreign nationals have admin access
### **Why**
  ITAR prohibits export of defense articles and technical data to
  foreign persons or countries without license. Cloud storage outside
  US or access by foreign cloud personnel constitutes export. This
  can result in criminal penalties and debarment.
  
### **Gotcha**
  "We use AWS for our defense contractor data. It's all encrypted
   so there's no export issue."
  
  # Encryption doesn't matter! Where is the data stored?
  # Who can access the encryption keys?
  # AWS GovCloud ≠ regular AWS!
  
### **Solution**
  1. Use ITAR-compliant cloud:
     - AWS GovCloud (US persons only)
     - Azure Government
     - On-premise with controlled access
  
  2. Data location controls:
     - Restrict to US regions only
     - Disable replication to foreign regions
     - Verify physical server location
  
  3. Access controls:
     - US persons only for admin access
     - Verify citizenship of cloud personnel
     - Contractual commitments from provider
  

## Uncontrolled Deemed Export

### **Id**
deemed-export-violation
### **Severity**
critical
### **Summary**
Foreign national employees accessing controlled technology
### **Symptoms**
  - Engineers from embargoed countries on team
  - No license for foreign national access
  - Shared development environment
### **Why**
  "Deemed export" treats release to foreign national in the US as
  export to their home country. Many engineering teams unknowingly
  violate by giving foreign nationals access to controlled source
  code, designs, or specifications.
  
### **Gotcha**
  "Our senior engineer is from [Country X] but he's been here
   10 years. He has a green card so it's fine."
  
  # Green card ≠ US person under ITAR!
  # Only citizens and permanent residents qualify.
  # Country of birth still matters for licensing!
  
### **Solution**
  1. Determine US person status:
     - Citizens (by birth or naturalization)
     - Permanent residents (green card)
     - Protected persons (asylum, refugee)
     NOT: H-1B, L-1, F-1, B-1, etc.
  
  2. Technology Control Plan:
     - Identify controlled items
     - Map to foreign national access
     - Implement access controls
     - Obtain licenses if needed
  
  3. Practical controls:
     - Separate repositories
     - Access-controlled networks
     - Badging for restricted areas
  

## Incorrect Encryption License Exception

### **Id**
encryption-exemption-misuse
### **Severity**
high
### **Summary**
Claiming encryption exemption for software that doesn't qualify
### **Symptoms**
  - Exporting encryption software as EAR99
  - No ENC classification review
  - Custom cryptographic implementation
### **Why**
  Encryption software often qualifies for License Exception ENC,
  but the requirements are specific. Mass market encryption has
  different rules than custom implementations. Misclassification
  can result in export violations.
  
### **Gotcha**
  "Our software uses AES-256 encryption, which is standard,
   so it's exempt and we can export anywhere."
  
  # Not automatic! Need classification review.
  # Some countries still restricted (Cuba, Iran, etc.)
  # Custom crypto may have different requirements.
  
### **Solution**
  1. Proper classification:
     - Submit for ECCN classification
     - Get BIS commodity classification
     - Document encryption functionality
  
  2. License Exception ENC requirements:
     - Mass market (retail) exception
     - Or submit encryption registration
     - Annual self-classification report
  
  3. Country restrictions:
     - Even with ENC, some countries restricted
     - E:1 and E:2 countries have limits
     - Verify destination before export
  

## Incomplete Party Screening

### **Id**
party-screening-gap
### **Severity**
high
### **Summary**
Not screening all parties in transaction chain
### **Symptoms**
  - Only screening direct customer
  - Not screening intermediaries
  - Missing list updates
### **Why**
  Export regulations require screening all parties: customer,
  intermediaries, end users, and involved individuals. Failure
  to screen any party can result in violation even if the direct
  customer is clean.
  
### **Gotcha**
  "We screened the distributor and they're clean. They handle
   the end customer relationship."
  
  # Who is the actual end user?
  # Are there intermediaries in the chain?
  # Distributor's customers may be on denied lists!
  
### **Solution**
  1. Screen all parties:
     - Buyer/customer
     - Intermediary/distributor
     - End user
     - Consignee
     - Named individuals
  
  2. Multiple lists:
     - Denied Persons List
     - Entity List
     - SDN List
     - Unverified List
     - ITAR Debarred
  
  3. Ongoing screening:
     - Screen at order entry
     - Re-screen at shipment
     - Screen against list updates
  