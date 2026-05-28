# Evaluation Criteria

This document provides the grading rubric for student assignment reports. Each section is weighted and has specific criteria for Pass (G) and Distinction (VG) grades.

## Grading Scale

All feedback should be framed positively. Use these terms consistently:

| Swedish Term | English | Grade Level | Description |
|--------------|---------|-------------|-------------|
| **Okej** | Okay | Pass (G) | Meets minimum requirements, just passed |
| **Bra** | Good | Pass (G) | Clearly meets requirements, solid work |
| **Mycket bra** | Very Good | VG level | Exceeds requirements, deeper understanding |
| **Utmärkt** | Excellent | Beyond VG | Exceptional work, goes beyond requirements |

**Important:** Never use negative critique. Frame areas for improvement in positive terms.

## Overall Grades

| Grade | Swedish | Criteria |
|-------|---------|----------|
| **G** | Godkänt (Pass) | All sections meet minimum criteria |
| **VG** | Väl godkänt (Distinction) | G criteria met AND Security section shows "more secure and robust solution" |

## Section Weights

| Section | Weight | VG Opportunity |
|---------|--------|----------------|
| 1. Sammanfattning (Summary) | 5% | No |
| 2. Teknisk arkitektur (Technical Architecture) | 30% | Yes |
| 3. Applikationsstack (Application Stack) | 30% | Yes |
| 4. Säkerhet (Security) | 20% | **Yes (primary)** |
| 5. Riskmedvetenhet (Risk Awareness) | 5% | No |
| 6. Processreflektion (Process Reflection) | 10% | No |

## Section-by-Section Criteria

### 1. Sammanfattning (Summary) - 5%

**Pass (G) Criteria:**
- Project purpose is stated
- Main components are listed

**Indicators:**
| Term | Description |
|------|-------------|
| Okej | Brief mention of purpose and components |
| Bra | Clear overview connecting purpose to solution |

### 2. Teknisk arkitektur (Technical Architecture) - 30%

**Pass (G) Criteria:**
- Network layout described (VNet, subnets)
- Server roles explained (bastion, proxy, app server)
- Database configuration mentioned
- Verification steps with screenshots

**Distinction (VG) Indicators:**
- NSG rules clearly explained with security rationale
- Automation approach documented (scripts, CLI)
- Reproducibility considered

**Indicators:**
| Term | Description |
|------|-------------|
| Okej | Basic description, minimal verification |
| Bra | Clear descriptions with screenshots showing working configuration |
| Mycket bra | Detailed explanations with security rationale, automation documented |
| Utmärkt | Professional-grade documentation, could be used as reference |

### 3. Applikationsstack (Application Stack) - 30%

**Pass (G) Criteria:**
- Stack components described (Ubuntu, nginx, Gunicorn, Flask, PostgreSQL)
- Data flow explained (form → proxy → app → database)
- Form functionality verified with screenshots
- Database queries shown

**Distinction (VG) Indicators:**
- Deep understanding of component interactions
- Thorough testing documented
- Error handling considered

**Indicators:**
| Term | Description |
|------|-------------|
| Okej | Components listed, basic verification |
| Bra | Clear flow description, working form demonstrated |
| Mycket bra | Comprehensive testing, understands why each component is needed |
| Utmärkt | Could troubleshoot issues based on documentation |

### 4. Säkerhet (Security) - 20% — PRIMARY VG SECTION

**Pass (G) Criteria:**
- Network security mentioned (NSG, segmentation)
- SSH access documented
- Basic verification of security measures

**Distinction (VG) Criteria:**
- Demonstrates a **more secure and robust solution**
- Multiple security layers implemented and explained
- Security decisions justified
- Blocked connection attempts shown (not just allowed)

**Indicators:**
| Term | Description |
|------|-------------|
| Okej | Security measures listed but minimal verification |
| Bra | Security measures implemented and verified |
| Mycket bra | Defense-in-depth approach, understands attack vectors |
| Utmärkt | Security-first thinking throughout, proactive risk mitigation |

### 5. Riskmedvetenhet (Risk Awareness) - 5%

**Pass (G) Criteria:**
- At least 2-3 risks identified
- Mitigation suggestions provided

**Indicators:**
| Term | Description |
|------|-------------|
| Okej | Generic risks mentioned |
| Bra | Relevant risks with practical mitigations |

### 6. Processreflektion (Process Reflection) - 10%

**Pass (G) Criteria:**
- Iterative development reflected upon
- AI usage described honestly
- Automation level assessed

**Indicators:**
| Term | Description |
|------|-------------|
| Okej | Brief answers to each point |
| Bra | Thoughtful reflection showing learning |

## Evaluation Decision Flow

```
1. Does the report meet ALL Pass criteria?
   - No → Grade: Not approved (discuss with instructor)
   - Yes → Continue to step 2

2. Does the Security section show "more secure solution"?
   - No → Grade: Godkänt (G)
   - Yes → Grade: Väl godkänt (VG)
```

## Common Patterns

### Solid Pass (G)
- All sections present with reasonable depth
- Screenshots verify working system
- Basic security measures documented
- Honest reflection on AI usage

### Strong Distinction (VG)
- Security section shows defense-in-depth
- NSG rules explained with rationale
- Both allowed AND blocked connections tested
- Automation documented for reproducibility
- Deep understanding of component interactions

### Borderline Cases

When uncertain between G and VG:
- Primary question: Does Security section demonstrate a "more secure solution"?
- Supporting evidence: Is there automation? Is there verification of blocked traffic?
- If still unclear: Default to G with note for instructor

## Notes for Reviewers

1. **Be generous with Pass (G)** - If student put in genuine effort, they should pass
2. **VG requires Security depth** - This is the primary differentiator
3. **Feedback should be encouraging** - Focus on strengths, not weaknesses
4. **Use Swedish consistently** - All assessments in Swedish terms
5. **Consider learning context** - Students are learning, not professionals
