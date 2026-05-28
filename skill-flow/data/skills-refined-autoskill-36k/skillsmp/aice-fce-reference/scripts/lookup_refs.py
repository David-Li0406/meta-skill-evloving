
import json
import argparse
import sys
import os
from datetime import datetime

def load_references(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find references file at {json_path}", file=sys.stderr)
        return []
    except json.JSONDecodeError:
        print(f"Error: references file at {json_path} is invalid JSON", file=sys.stderr)
        return []

def calculate_relevance(reference, context_terms):
    score = 0
    
    # Normalize context terms
    context_terms = [term.lower() for term in context_terms]
    
    # Check text fields
    text_fields = [
        reference.get('title', ''),
        reference.get('description', ''),
        reference.get('publisher', '')
    ]
    # Check keywords
    keywords = reference.get('keywords', [])
    
    # Title match weight
    if any(term in reference.get('title', '').lower() for term in context_terms):
        score += 5
        
    # Keyword match weight
    for term in context_terms:
        # Exact keyword match
        if term in [k.lower() for k in keywords]:
            score += 3
        # Partial keyword match
        elif any(term in k.lower() for k in keywords):
            score += 1
            
    # Description/Body match weight
    combined_text = " ".join(text_fields).lower()
    for term in context_terms:
        if term in combined_text:
            score += 1
            
    return score

def get_best_edition(reference, target_year=None):
    """
    Finds the best edition match.
    If target_year is provided, finds the latest edition that was published ON or BEFORE matched year.
    If no such edition (all newer), finds the oldest edition.
    If no target_year, returns the latest edition.
    """
    editions = reference.get('editions', [])
    if not editions:
        return None
        
    # Sort editions by year ascending
    sorted_editions = sorted(editions, key=lambda x: x.get('year', 0))
    
    if target_year is None:
        return sorted_editions[-1] # Return latest
        
    # Find candidates <= target_year
    valid_candidates = [e for e in sorted_editions if e.get('year', 0) <= target_year]
    
    if valid_candidates:
        return valid_candidates[-1] # Newest of the valid ones
    else:
        # If the credential matches nothing (e.g. year 1990 but first book is 2004),
        # return the oldest book available as the best approximation
        return sorted_editions[0]

def format_apa_citation(reference, edition_data):
    """
    Format: Author. (Year). Title (Edition). Publisher.
    """
    publisher = reference.get('publisher', 'Unknown Publisher')
    author = reference.get('author', publisher)  # Default author to publisher if missing
    year = edition_data.get('year', 'n.d.')
    title = reference.get('title', 'Unknown Title')
    edition_name = edition_data.get('edition', '')
    
    edition_str = f" ({edition_name})" if edition_name and "Online" not in edition_name else ""
    
    # If Author is the same as Publisher (e.g. AACRAO), omit publisher at end.
    if author == publisher:
         citation = f"{author}. ({year}). *{title}*{edition_str}."
    else:
         citation = f"{author}. ({year}). *{title}*{edition_str}. {publisher}."
    
    if "url" in reference:
        citation += f" Retrieved from {reference['url']}"
        
    return citation

def format_website_citation(institution, url):
    """
    Format: Institution. (n.d.). Home Page. Retrieved from <URL>
    """
    citation = f"{institution}. (n.d.). *Home Page*. Retrieved from {url}"
    return citation

def main():
    parser = argparse.ArgumentParser(description="Lookup AICE FCE References")
    parser.add_argument("--context", help="Context string (e.g., 'China Bachelor Transcript')")
    parser.add_argument("--year", type=int, help="Year of the credential (e.g., 2005) to match reference edition")
    parser.add_argument("--limit", type=int, default=3, help="Number of results to return")
    parser.add_argument("--make-citation", nargs=2, metavar=('INSTITUTION', 'URL'), help="Generate a website citation (e.g., 'HKUST' 'http://...')")
    
    args = parser.parse_args()
    
    if args.make_citation:
        inst, url = args.make_citation
        print(format_website_citation(inst, url))
        sys.exit(0)

    if not args.context:
        parser.error("the following arguments are required: --context (unless --make-citation is used)")

    # Locate json relative to script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, "../resources/references.json")
    
    refs = load_references(json_path)
    if not refs:
        sys.exit(1)
        
    context_terms = args.context.split()
    
    scored_refs = []
    for ref in refs:
        score = calculate_relevance(ref, context_terms)
        if score > 0:
            scored_refs.append((score, ref))
            
    # Sort by score descending
    scored_refs.sort(key=lambda x: x[0], reverse=True)
    
    top_refs = scored_refs[:args.limit]
    
    # Fallback
    if not top_refs:
        print("No specific high-relevance references found. Showing general defaults:\n")
        defaults = ["iau_handbook", "europa_world", "aacrao_transcript_guide"]
        top_refs = [(0, r) for r in refs if r['id'] in defaults]
    
    print(f"### References matching context '{args.context}'" + (f" (Year: {args.year})" if args.year else "") + "\n")
    
    for i, (score, ref) in enumerate(top_refs, 1):
        best_edition = get_best_edition(ref, args.year)
        citation = format_apa_citation(ref, best_edition)
        
        print(f"{i}. {citation}")
        if best_edition.get('isbn'):
             print(f"   ISBN: {best_edition['isbn']}")
        # print(f"   (Rationale: relevant to '{', '.join(context_terms)}')") # Optional debug
        print("")

if __name__ == "__main__":
    main()
