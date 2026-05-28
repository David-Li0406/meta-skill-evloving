---
name: aice-fce-reference
description: Retrieves authoritative bibliographic references for Foreign Credential Evaluation (FCE) based on AICE standards.
---

# AICE FCE Reference Skill

This skill assists in identifying the correct authoritative resources (books, databases, directories) required to evaluate a specific educational credential. It utilizes the bibliography defined in "Exhibit VII".

## When to Use

Use this skill when the user provides educational credentials or documents and asks for:
* Verification of an institution's accreditation.
* Interpretation of a transcript, grading scale, or credit system.
* Guidance on handling specific country credentials (especially China or North America).
* Authoritative sources to cite in an evaluation report.

## Bilingual Format

Institution names should follow: `English Name (Original Name in Native Language)`

| Example |
|---------|
| `Peking University (北京大学)` |
| `Lublin University of Technology (Politechnika Lubelska)` |
| `Warsaw University of Technology (Politechnika Warszawska)` |

## How to Use

To provide the correct references, the Agent must follow these steps:

1.  **Extract Context**: Analyze the user's input to identify key attributes:
    * **Country of Education** (e.g., China, USA, Global).
    * **Degree/Level** (e.g., Bachelor, Master, PhD).
    * **Document Type** (e.g., Transcript, Diploma).
    * **Specific Issue** (e.g., Privacy/FERPA, Grading System).

2.  **Execute Lookup**: Run the provided Python script regarding the credential year.
    ```bash
    python scripts/lookup_refs.py --context "<Insert extracted context keywords here>" --year <Optional: Year>
    ```

3.  **Search for Institution Website** (Mandatory):
    *   **For each** awarding institution, use `search_web` to find the official website.
    *   Generate a citation using the `--make-citation` flag:
        ```bash
        python scripts/lookup_refs.py --make-citation "<Institution Name>" "<URL>"
        ```

4.  **Generate Response**:
    *   The script will output citations in **APA Format**.
    *   **Ensure at least 3 references are included.**
    *   If the script returns fewer than 3 references, use `search_web` or general knowledge to find additional relevant authoritative sources (e.g., AACRAO EDGE, country-specific Ministry of Education websites) to meet the minimum requirement.
    *   **Append** the institution website citation to the list of standard references.
    *   Copy the output directly into the evaluation report.

## Examples

**User:** "I have a transcript from Peking University for a Bachelor's degree (Graduated 2005). How do I verify the credits?"

**Agent Action:**
`python scripts/lookup_refs.py --context "China Bachelor Transcript" --year 2005`

**Agent Response:**
"Based on the AICE bibliography, here are the references for a 2005 credential:

1. AACRAO. (2011). *AACRAO Academic Record and Transcript Guide* (1st (2011)).
2. Higher Education Press. (2000). *Chinese Universities and Colleges* (3rd).
3. International Association of Universities (IAU) / Palgrave Macmillan. (2005). *International Handbook of Universities* (18th).
4. Peking University. (n.d.). *Home*. https://www.pku.edu.cn"