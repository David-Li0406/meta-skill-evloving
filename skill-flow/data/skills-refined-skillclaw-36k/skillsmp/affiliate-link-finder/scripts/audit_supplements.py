import re
import os

def audit_supplements():
    file_path = 'lib/infrastructure/services/seeding_service.dart'
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract list content
    list_match = re.search(r'final List<Map<String, dynamic>> supplements = \[(.*?)\];', content, re.DOTALL)
    if not list_match:
        print("Could not find supplements list")
        return
        
    list_content = list_match.group(1)
    
    # Split by blocks that look like maps
    # We'll look for blocks starting with { and ending with }
    # This is still a bit rough for Nested maps but let's try
    blocks = []
    current_block = []
    brace_count = 0
    in_string = False
    
    for char in list_content:
        if char == '"' and (not current_block or current_block[-1] != '\\'):
            in_string = not in_string
        
        if not in_string:
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
        
        current_block.append(char)
        
        if brace_count == 0 and char == '}' and not in_string:
            blocks.append("".join(current_block))
            current_block = []

    standardized = []
    thin = []
    incomplete = []
    all_ids = []
    duplicates = []
    
    required_fields = [
        '"mechanismOfAction"',
        '"detailedBenefits"',
        '"timingRationale"',
        '"dosageByWeight"',
        '"tldr"',
        '"adhdMedInteractions"',
        '"focusLevel"'
    ]
    
    for block in blocks:
        id_match = re.search(r'"id":\s*"([^"]+)"', block)
        if id_match:
            supp_id = id_match.group(1)
            if supp_id in all_ids:
                duplicates.append(supp_id)
            all_ids.append(supp_id)
            
            missing = [f for f in required_fields if f not in block]
            
            if not missing:
                standardized.append(supp_id)
            elif len(missing) == len(required_fields):
                thin.append(supp_id)
            else:
                incomplete.append((supp_id, missing))
                
    print(f"Total Unique IDs: {len(set(all_ids))}")
    print(f"Duplicates found: {', '.join(set(duplicates)) if duplicates else 'None'}")
    print(f"\nFully Standardized ({len(standardized)}): {', '.join(standardized)}")
    print(f"\nThin (Missing ALL deep fields) ({len(thin)}): {', '.join(thin)}")
    print(f"\nIncomplete (Missing SOME deep fields) ({len(incomplete)}):")
    for s_id, missing in incomplete:
        print(f"  - {s_id}: {', '.join(missing)}")

if __name__ == "__main__":
    audit_supplements()
