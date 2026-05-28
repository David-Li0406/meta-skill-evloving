#!/usr/bin/env python3
"""
Extract and classify clauses from contract text using taxonomy keywords.

Usage:
    from extract_clauses import extract_clauses, get_clause_weight

    clauses = extract_clauses(contract_text)
    for clause in clauses:
        print(f"{clause['type']} ({clause['weight']}) - Section {clause['section']}")
"""

import re
from typing import List, Dict, Optional

# Clause taxonomy with keywords (Primary + Secondary)
CLAUSE_KEYWORDS = {
    # Critical Weight
    'Indemnification': [
        'indemnify', 'indemnification', 'indemnities',
        'hold harmless', 'defend', 'defense costs',
        'third-party claims'
    ],
    'Limitation of Liability': [
        'limitation of liability', 'liability cap', 'maximum liability',
        'consequential damages', 'indirect damages', 'special damages',
        'punitive damages', 'lost profits', 'exclusions'
    ],
    'IP/Work Ownership': [
        'intellectual property', 'work product', 'deliverables',
        'ownership', 'title', 'license', 'assignment',
        'background ip', 'foreground ip', 'joint ownership'
    ],

    # High Weight
    'Termination': [
        'termination', 'terminate', 'cancellation', 'cancel',
        'cure period', 'breach', 'material breach',
        'wind-down', 'transition', 'survival'
    ],
    'Insurance': [
        'insurance', 'coverage', 'policy',
        'certificate', 'additional insured', 'endorsement',
        'general liability', 'professional liability', 'cyber liability'
    ],
    'Vendor Displacement': [
        'transition', 'displacement', 'incumbent',
        'handover', 'knowledge transfer', 'cooperation',
        'successor', 'replacement', 'outgoing vendor'
    ],
    'Non-Solicitation': [
        'non-solicitation', 'non-solicit', 'non-compete',
        'hiring restriction', 'recruitment', 'employee',
        'key personnel', 'cooling-off period'
    ],

    # Standard Weight
    'Confidentiality': [
        'confidential', 'confidentiality', 'nda',
        'proprietary', 'trade secret', 'disclose',
        'permitted disclosure', 'return of information'
    ],
    'Payment/Fees': [
        'payment', 'fees', 'compensation',
        'invoice', 'billing', 'net terms',
        'late payment', 'interest', 'expenses'
    ],
    'Warranties': [
        'warranty', 'warranties', 'warrant',
        'represent', 'representation', 'guarantee',
        'disclaimer', 'as-is', 'fitness for purpose'
    ],
    'Force Majeure': [
        'force majeure', 'act of god',
        'pandemic', 'natural disaster', 'government action',
        'excused performance', 'suspension'
    ],
    'Governing Law': [
        'governing law', 'applicable law', 'choice of law',
        'jurisdiction', 'venue', 'forum',
        'dispute resolution', 'arbitration'
    ]
}

# Three-tier clause weighting
CLAUSE_WEIGHTS = {
    'Critical': ['Indemnification', 'Limitation of Liability', 'IP/Work Ownership'],
    'High': ['Termination', 'Insurance', 'Vendor Displacement', 'Non-Solicitation'],
    'Standard': ['Confidentiality', 'Payment/Fees', 'Warranties', 'Force Majeure', 'Governing Law']
}

# Section number patterns
SECTION_PATTERNS = [
    r'^\s*(\d+\.?\d*\.?\d*)\s+',           # 1.2.3
    r'^\s*Section\s+(\d+\.?\d*)',          # Section 1.2
    r'^\s*Article\s+([IVX]+)',             # Article IV
    r'^\s*\(([a-z])\)',                    # (a)
]


def get_clause_weight(clause_type: str) -> str:
    """Return weight tier for clause type."""
    for weight, types in CLAUSE_WEIGHTS.items():
        if clause_type in types:
            return weight
    return 'Standard'


def extract_section_number(text: str) -> Optional[str]:
    """Extract section number from beginning of text."""
    for pattern in SECTION_PATTERNS:
        match = re.match(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def split_into_sections(contract_text: str) -> List[Dict[str, str]]:
    """Split contract into sections based on headers."""
    sections = []
    lines = contract_text.split('\n')

    current_section = None
    current_text = []

    for line in lines:
        # Check if line is a section header
        section_num = extract_section_number(line)

        # Also check for bold headers (markdown format)
        if line.startswith('#') or (section_num and len(line.strip()) < 100):
            # Save previous section
            if current_section is not None:
                sections.append({
                    'section': current_section,
                    'text': '\n'.join(current_text).strip()
                })

            # Start new section
            current_section = section_num if section_num else 'Header'
            current_text = [line]
        else:
            current_text.append(line)

    # Add final section
    if current_section is not None:
        sections.append({
            'section': current_section,
            'text': '\n'.join(current_text).strip()
        })

    return sections


def detect_clause_type(text: str) -> List[str]:
    """Detect all clause types that match keywords in text."""
    text_lower = text.lower()
    matches = []

    for clause_type, keywords in CLAUSE_KEYWORDS.items():
        # Count keyword matches
        match_count = sum(1 for keyword in keywords if keyword.lower() in text_lower)

        # Require at least 2 keyword matches for confidence
        if match_count >= 2:
            matches.append((clause_type, match_count))

    # Return clause types sorted by match count (most matches first)
    matches.sort(key=lambda x: x[1], reverse=True)
    return [clause_type for clause_type, _ in matches]


def extract_clauses(contract_text: str, min_text_length: int = 50) -> List[Dict]:
    """
    Extract and classify clauses from contract text.

    Args:
        contract_text: Full contract text (markdown or plain text)
        min_text_length: Minimum text length to consider as a clause (default 50)

    Returns:
        List of clause dictionaries with keys:
        - type: Clause type name
        - section: Section number
        - text: Clause text
        - weight: Critical/High/Standard
        - confidence: Number of keyword matches
    """
    clauses = []
    sections = split_into_sections(contract_text)

    for section in sections:
        # Skip very short sections
        if len(section['text']) < min_text_length:
            continue

        # Detect clause types
        detected_types = detect_clause_type(section['text'])

        # Add each detected clause type
        for clause_type in detected_types:
            clause = {
                'type': clause_type,
                'section': section['section'],
                'text': section['text'],
                'weight': get_clause_weight(clause_type),
                'confidence': 'high' if len(detected_types) == 1 else 'medium'
            }
            clauses.append(clause)

    return clauses


def group_clauses_by_type(clauses: List[Dict]) -> Dict[str, List[Dict]]:
    """Group clauses by type for reporting."""
    grouped = {}
    for clause in clauses:
        clause_type = clause['type']
        if clause_type not in grouped:
            grouped[clause_type] = []
        grouped[clause_type].append(clause)
    return grouped


def get_clause_summary(clauses: List[Dict]) -> Dict:
    """Generate summary statistics for clauses."""
    summary = {
        'total': len(clauses),
        'by_weight': {'Critical': 0, 'High': 0, 'Standard': 0},
        'by_type': {}
    }

    for clause in clauses:
        # Count by weight
        weight = clause['weight']
        summary['by_weight'][weight] = summary['by_weight'].get(weight, 0) + 1

        # Count by type
        clause_type = clause['type']
        summary['by_type'][clause_type] = summary['by_type'].get(clause_type, 0) + 1

    return summary


# Example usage
if __name__ == '__main__':
    # Test with sample contract text
    sample_text = """
    # Master Services Agreement

    1. Definitions
    This Agreement defines the terms...

    2. Services
    The Vendor shall provide services...

    8. Indemnification
    The Vendor shall indemnify, defend, and hold harmless the Client from any
    third-party claims arising from the Vendor's breach of this Agreement.

    9. Limitation of Liability
    IN NO EVENT SHALL EITHER PARTY BE LIABLE FOR ANY CONSEQUENTIAL, INDIRECT,
    SPECIAL, OR PUNITIVE DAMAGES. THE MAXIMUM LIABILITY OF VENDOR SHALL NOT
    EXCEED THE FEES PAID IN THE 12 MONTHS PRECEDING THE CLAIM.

    10. Intellectual Property
    All work product and deliverables created by Vendor shall be the exclusive
    property of Client. Vendor assigns all intellectual property rights to Client.

    11. Termination
    Either party may terminate this Agreement upon 30 days written notice. In the
    event of material breach, the non-breaching party may terminate immediately
    after a 15-day cure period.
    """

    clauses = extract_clauses(sample_text)

    print(f"Detected {len(clauses)} clauses:\n")

    for clause in clauses:
        print(f"[{clause['weight']}] {clause['type']}")
        print(f"  Section: {clause['section']}")
        print(f"  Confidence: {clause['confidence']}")
        print(f"  Text preview: {clause['text'][:100]}...")
        print()

    summary = get_clause_summary(clauses)
    print(f"\nSummary:")
    print(f"  Total clauses: {summary['total']}")
    print(f"  By weight: {summary['by_weight']}")
    print(f"  By type: {summary['by_type']}")
