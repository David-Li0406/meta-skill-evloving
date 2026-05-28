# Contract Analysis - Sharp Edges

## Unlimited Indemnification Exposure

### **Id**
unlimited-indemnification
### **Severity**
critical
### **Summary**
Indemnity obligations with no cap create unlimited liability
### **Symptoms**
  - Contract has indemnification clause
  - No cap or limit specified
  - Survives termination indefinitely
### **Why**
  Indemnification means you pay for the other party's losses from
  third-party claims. Without a cap, you could owe unlimited amounts.
  This is especially dangerous for IP indemnification where a single
  patent claim could cost millions.
  
### **Gotcha**
  "Vendor shall indemnify and hold harmless Customer from any and all
   claims, damages, losses, and expenses arising from Vendor's services."
  
  # No cap! No exclusions! Survives forever!
  
### **Solution**
  Negotiate for:
  1. Mutual indemnification (both parties indemnify each other)
  2. Cap tied to contract value or insurance limits
  3. Exclusions for gross negligence, willful misconduct
  4. Reasonable survival period (1-3 years)
  
  Example cap language:
  "Vendor's aggregate indemnification liability shall not exceed
   two times (2x) the fees paid under this Agreement."
  

## Liability Cap Only Applies to Counterparty

### **Id**
asymmetric-liability-cap
### **Severity**
high
### **Summary**
You have unlimited liability while counterparty has a cap
### **Symptoms**
  - Limitation of liability section exists
  - Cap applies only to 'Vendor' or 'Provider'
  - Your liability has no cap
### **Why**
  One-sided liability caps mean you bear all the risk. If something
  goes wrong, the other party's exposure is limited but yours is not.
  This is common in vendor-drafted contracts.
  
### **Gotcha**
  "IN NO EVENT SHALL VENDOR'S LIABILITY EXCEED THE AMOUNTS PAID
   UNDER THIS AGREEMENT."
  
  # Note: Nothing about Customer's liability being capped!
  
### **Solution**
  Insist on mutual caps:
  
  "NEITHER PARTY'S AGGREGATE LIABILITY SHALL EXCEED [2X] THE FEES
   PAID OR PAYABLE UNDER THIS AGREEMENT IN THE [12] MONTHS PRECEDING
   THE CLAIM."
  
  Also review carve-outs - unlimited liability for:
  - Gross negligence/willful misconduct (usually acceptable)
  - Indemnification (review separately)
  - Confidentiality breach (negotiate cap)
  

## No Termination for Convenience Rights

### **Id**
missing-termination-convenience
### **Severity**
high
### **Summary**
Locked into contract with no exit option
### **Symptoms**
  - Termination clause only allows for material breach
  - No termination for convenience provision
  - Long contract term with auto-renewal
### **Why**
  Without termination for convenience, you're locked in even if
  the service is terrible or your needs change. Combined with
  auto-renewal, this can trap you for years.
  
### **Gotcha**
  "Term: 3 years, automatically renewing for successive 1-year terms
   unless either party provides 90 days written notice.
  
   Termination: Either party may terminate for material breach
   that remains uncured for 30 days after written notice."
  
  # No way out except breach or waiting for renewal window!
  
### **Solution**
  Add termination for convenience:
  
  "Either party may terminate this Agreement for any reason upon
   [60/90] days prior written notice."
  
  Or at minimum:
  "Customer may terminate upon [30] days notice, subject to payment
   of fees for services already rendered."
  

## Automatic IP Assignment of All Work

### **Id**
broad-ip-assignment
### **Severity**
high
### **Summary**
Counterparty owns everything you create, including background IP
### **Symptoms**
  - IP section assigns 'all work product'
  - No carve-out for pre-existing IP
  - License-back provisions unclear
### **Why**
  Broad IP assignment can transfer ownership of your background
  intellectual property used in the work. You could lose rights
  to your own tools, frameworks, or prior work.
  
### **Gotcha**
  "Vendor hereby assigns to Customer all right, title, and interest
   in and to all work product, deliverables, and materials created
   or developed in connection with this Agreement."
  
  # Does "in connection with" include your background IP?
  
### **Solution**
  1. Carve out background IP:
     "Vendor's Background IP shall remain the property of Vendor.
      Vendor grants Customer a perpetual license to use Background IP
      solely as incorporated in the Deliverables."
  
  2. Define work product narrowly:
     "Work Product means new and original works created specifically
      for Customer under this Agreement, excluding Background IP."
  
  3. Clearly list your background IP in an exhibit.
  

## No Data Breach Notification Requirements

### **Id**
silent-on-data-breach
### **Severity**
high
### **Summary**
Contract doesn't require timely breach notification
### **Symptoms**
  - Handles personal data but no DPA
  - No breach notification timeline
  - No security requirements specified
### **Why**
  GDPR requires 72-hour breach notification. If your vendor doesn't
  have to notify you promptly, you can't meet your regulatory
  obligations. You're liable even if the vendor caused the breach.
  
### **Gotcha**
  "Vendor shall maintain reasonable security measures for Customer data."
  
  # No breach notification! No specific security standards!
  
### **Solution**
  Add Data Protection Addendum (DPA) with:
  
  1. Breach notification timeline:
     "Vendor shall notify Customer of any Security Breach within
      [24-48] hours of becoming aware."
  
  2. Security standards:
     "Vendor shall maintain security measures consistent with
      SOC 2 Type II / ISO 27001 standards."
  
  3. Audit rights:
     "Customer may audit Vendor's security practices annually."
  