import sys
import json
import re

def normalize_entity(text):
    """Simple normalization for comparison (lowercase, remove punctuation)."""
    return re.sub(r'[^\w\s]', '', text.lower()).strip()

def extract_entities(resume_json):
    """
    Extracts critical entities (Company Names, Job Titles, Dates) from a resume JSON.
    Returns a set of normalized strings.
    """
    entities = set()
    
    # 1. Work History
    if "work" in resume_json:
        for job in resume_json["work"]:
            if "name" in job: entities.add(normalize_entity(job["name"]))
            if "position" in job: entities.add(normalize_entity(job["position"]))
            if "startDate" in job: entities.add(normalize_entity(job["startDate"]))
            if "endDate" in job: entities.add(normalize_entity(job["endDate"]))

    # 2. Education
    if "education" in resume_json:
        for edu in resume_json["education"]:
            if "institution" in edu: entities.add(normalize_entity(edu["institution"]))
            if "area" in edu: entities.add(normalize_entity(edu["area"]))
    
    return entities

def audit_resume(original_path, tailored_path):
    """
    Compares the Tailored Resume against the Master Resume.
    Fails if the Tailored Resume contains specific entity types NOT present in the Master.
    """
    try:
        with open(original_path, 'r') as f:
            original_data = json.load(f)
        with open(tailored_path, 'r') as f:
            tailored_data = json.load(f)
    except Exception as e:
        print(f"Error loading files: {e}")
        sys.exit(1)

    original_entities = extract_entities(original_data)
    tailored_entities = extract_entities(tailored_data)

    # Check for fabrication: Are there entities in Tailored that are NOT in Original?
    # Note: We only strictly check "Facts" (Companies, Titles, Dates). 
    # Skills/Bullets change by definition, so we don't strict-match those here.
    
    fabrications = []
    for entity in tailored_entities:
        if entity not in original_entities:
            fabrications.append(entity)

    if fabrications:
        result = {
            "status": "FAIL",
            "message": "Potential fabrication detected. The following entities appear in the tailored resume but NOT in the master source.",
            "flagged_entities": fabrications
        }
        print(json.dumps(result, indent=2))
        sys.exit(1) # Fail the process
    else:
        result = {
            "status": "PASS",
            "message": "No entity fabrication detected."
        }
        print(json.dumps(result, indent=2))
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python audit_fabrication.py <master_resume.json> <tailored_resume.json>")
        sys.exit(1)

    audit_resume(sys.argv[1], sys.argv[2])
