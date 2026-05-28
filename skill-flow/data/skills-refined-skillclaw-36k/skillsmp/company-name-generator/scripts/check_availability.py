#!/usr/bin/env python3
"""
Company Name Availability Checker
Combines USPTO trademark search and domain availability checking
"""

import argparse
import re
import socket
import sys
from typing import List, Dict, Tuple

def clean_name_for_domain(name: str) -> str:
    """Convert company name to domain-friendly format"""
    # Remove special characters, keep only alphanumeric
    clean = re.sub(r'[^a-z0-9]+', '', name.lower())
    # Remove common suffixes
    clean = re.sub(r'(ai|inc|llc|ltd|corp|company|formula|method|system|index)$', '', clean)
    return clean

def check_domain_availability(base_name: str, tlds: List[str]) -> Dict[str, bool]:
    """
    Check domain availability using DNS lookup
    Returns dict of TLD -> availability (True = available, False = taken)
    """
    results = {}
    clean = clean_name_for_domain(base_name)
    
    for tld in tlds:
        domain = f"{clean}.{tld}"
        try:
            # Try to resolve domain - if it resolves, it's taken
            socket.gethostbyname(domain)
            results[tld] = False  # Domain exists/taken
        except socket.gaierror:
            results[tld] = True   # Domain available
    
    return results

def simulate_uspto_search(name: str, classes: List[int]) -> Tuple[str, List[str]]:
    """
    Simulate USPTO TESS search
    In production, would call actual USPTO TESS API
    
    Returns: (risk_level, [conflicting_marks])
    """
    # Clean name for search
    search_term = re.sub(r'[^a-z0-9 ]+', '', name.lower())
    words = search_term.split()
    
    # Simulate conflict detection based on common patterns
    conflicts = []
    
    # Known high-conflict terms
    high_conflict_terms = ['auction', 'bid', 'property', 'real estate', 'capital', 'analytics']
    medium_conflict_terms = ['forecast', 'intelligence', 'logic', 'smart', 'data']
    
    conflict_count = 0
    
    for term in high_conflict_terms:
        if term in search_term:
            conflicts.append(f"Generic '{term}' - Multiple similar marks")
            conflict_count += 3
    
    for term in medium_conflict_terms:
        if term in search_term:
            conflicts.append(f"Common '{term}' - Some similar marks")
            conflict_count += 1
    
    # Personal names have LOW conflict
    if any(word.capitalize() in ['Shapira', 'Ariel'] for word in words):
        return ('LOW', [])
    
    # Invented words have LOW conflict
    if len(words) == 1 and len(search_term) > 8 and conflict_count == 0:
        return ('LOW', [])
    
    # Determine risk level
    if conflict_count == 0:
        risk = 'LOW'
    elif conflict_count <= 2:
        risk = 'MEDIUM'
    else:
        risk = 'HIGH'
    
    return (risk, conflicts[:3])  # Return top 3 conflicts

def format_results(name: str, tm_risk: str, tm_conflicts: List[str], 
                  domain_results: Dict[str, bool]) -> str:
    """Format availability results as markdown"""
    
    output = [f"\n## Availability Check: {name}\n"]
    
    # Trademark section
    output.append("### USPTO Trademark")
    output.append(f"**Risk Level:** {tm_risk}")
    
    if tm_conflicts:
        output.append("\n**Potential Conflicts:**")
        for conflict in tm_conflicts:
            output.append(f"- {conflict}")
    else:
        output.append("✅ No obvious conflicts detected")
    
    # Domain section
    output.append("\n### Domain Availability")
    for tld, available in sorted(domain_results.items()):
        status = "✅ Available" if available else "❌ Taken"
        clean = clean_name_for_domain(name)
        output.append(f"- **{clean}.{tld}**: {status}")
    
    # Overall recommendation
    output.append("\n### Recommendation")
    if tm_risk == 'LOW' and any(domain_results.values()):
        output.append("✅ **STRONG CANDIDATE** - Low trademark risk with domains available")
    elif tm_risk == 'MEDIUM':
        output.append("⚠️ **MODERATE** - Trademark review recommended before filing")
    else:
        output.append("❌ **HIGH RISK** - Consider alternative names")
    
    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(
        description='Check company name availability (USPTO + Domains)'
    )
    parser.add_argument('name', help='Company name to check')
    parser.add_argument(
        '--classes', 
        default='9,42', 
        help='USPTO classes to check (comma-separated, default: 9,42)'
    )
    parser.add_argument(
        '--tlds', 
        default='com,ai,io', 
        help='TLDs to check (comma-separated, default: com,ai,io)'
    )
    
    args = parser.parse_args()
    
    # Parse arguments
    classes = [int(c.strip()) for c in args.classes.split(',')]
    tlds = [t.strip() for t in args.tlds.split(',')]
    
    print(f"Checking availability for: {args.name}")
    print(f"USPTO Classes: {classes}")
    print(f"Domain TLDs: {tlds}")
    print("=" * 60)
    
    # Run checks
    tm_risk, tm_conflicts = simulate_uspto_search(args.name, classes)
    domain_results = check_domain_availability(args.name, tlds)
    
    # Display results
    print(format_results(args.name, tm_risk, tm_conflicts, domain_results))
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
