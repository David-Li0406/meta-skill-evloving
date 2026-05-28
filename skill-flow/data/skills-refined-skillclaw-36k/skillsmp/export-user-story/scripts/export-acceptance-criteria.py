import requests
from requests.auth import HTTPBasicAuth
import re
import os
import sys
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration - loaded from .env file
ORGANIZATION = os.getenv("AZURE_DEVOPS_ORGANIZATION")
PROJECT = os.getenv("AZURE_DEVOPS_PROJECT")
PAT = os.getenv("AZURE_DEVOPS_PAT")
PRODUCT_PREFIX = os.getenv("PRODUCT_PREFIX", "eNr")  # Default to "eNr" if not set

# Validate required environment variables at module level
if not ORGANIZATION or not PROJECT or not PAT:
    missing = []
    if not ORGANIZATION:
        missing.append("AZURE_DEVOPS_ORGANIZATION")
    if not PROJECT:
        missing.append("AZURE_DEVOPS_PROJECT")
    if not PAT:
        missing.append("AZURE_DEVOPS_PAT")
    
    print("❌ ERROR: Missing required environment variables:")
    for var in missing:
        print(f"  - {var}")
    print("\nPlease ensure your .env file contains all required variables.")
    print("See .env.example for reference.")
    sys.exit(1)

# Type assertions for type checker - these are guaranteed to be str after validation above
assert ORGANIZATION is not None
assert PROJECT is not None
assert PAT is not None

# Output directory for exported files (absolute path based on script location)
# Script is in .claude/skills/export-user-story/scripts/
# Target is docs/user-stories/
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../../"))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "docs", "user-stories")

def sanitize_filename(text):
    """Convert text to lowercase and replace spaces/special chars with underscores"""
    # Remove special characters and replace spaces with underscores
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s]+', '_', text)
    return text.lower().strip('_')

def extract_title_suffix(title):
    """Extract the part after the colon in the title
    Example: 'eNcounter Refresh: Loading Screen' -> 'loading_screen'
    """
    if ':' in title:
        # Get everything after the colon and strip whitespace
        suffix = title.split(':', 1)[1].strip()
    else:
        # If no colon, use the whole title
        suffix = title
    
    return sanitize_filename(suffix)

def get_work_item(work_item_id):
    """Fetch work item details from Azure DevOps API"""
    url = f"https://dev.azure.com/{ORGANIZATION}/{PROJECT}/_apis/wit/workitems/{work_item_id}?api-version=7.0"
    
    response = requests.get(
        url,
        auth=HTTPBasicAuth('', str(PAT))
    )
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        print("Error: Authentication failed. Check your PAT.")
        return None
    elif response.status_code == 404:
        print(f"Error: Work item {work_item_id} not found.")
        return None
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def extract_acceptance_criteria(work_item):
    """Extract acceptance criteria from work item fields"""
    fields = work_item.get('fields', {})
    
    # Get the dedicated Acceptance Criteria field
    acceptance_criteria = fields.get('Microsoft.VSTS.Common.AcceptanceCriteria', '')
    
    if not acceptance_criteria:
        print("Warning: Acceptance Criteria field is empty.")
    
    # Convert HTML line breaks to newlines before removing tags
    acceptance_criteria = acceptance_criteria.replace('<br>', '\n')
    acceptance_criteria = acceptance_criteria.replace('<br/>', '\n')
    acceptance_criteria = acceptance_criteria.replace('<br />', '\n')
    acceptance_criteria = acceptance_criteria.replace('</p>', '\n')
    acceptance_criteria = acceptance_criteria.replace('</div>', '\n')
    
    # Convert HTML list items to markdown bullet points
    # Handle both <li> and </li> tags to preserve list structure
    acceptance_criteria = re.sub(r'<li[^>]*>', '\n- ', acceptance_criteria)
    acceptance_criteria = acceptance_criteria.replace('</li>', '')
    acceptance_criteria = acceptance_criteria.replace('</ul>', '\n')
    acceptance_criteria = acceptance_criteria.replace('</ol>', '\n')
    
    # Remove remaining HTML tags
    acceptance_criteria = re.sub(r'<[^>]+>', '', acceptance_criteria)
    
    # Decode HTML entities
    acceptance_criteria = acceptance_criteria.replace('&nbsp;', ' ')
    acceptance_criteria = acceptance_criteria.replace('&lt;', '<')
    acceptance_criteria = acceptance_criteria.replace('&gt;', '>')
    acceptance_criteria = acceptance_criteria.replace('&amp;', '&')
    acceptance_criteria = acceptance_criteria.replace('&quot;', '"')
    
    # Clean up initial whitespace and excessive blank lines
    acceptance_criteria = re.sub(r'\n\s*\n', '\n', acceptance_criteria)
    acceptance_criteria = acceptance_criteria.strip()
    
    # Ensure Scenario starts on a fresh line (handle cases where it's concatenated with previous text)
    acceptance_criteria = re.sub(r'(\S)(\s*)(Scenario \d+:)', r'\1\n\n\3', acceptance_criteria)
    
    # Ensure Given, When, Then each start on their own line
    acceptance_criteria = re.sub(r'(\s+)(Given )', r'\n\2', acceptance_criteria)
    acceptance_criteria = re.sub(r'(\s+)(When )', r'\n\2', acceptance_criteria)
    acceptance_criteria = re.sub(r'(\s+)(Then )', r'\n\2', acceptance_criteria)
    
    # Add single blank line before each Scenario (except the first)
    lines = acceptance_criteria.split('\n')
    formatted_lines = []
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith('Scenario ') and i > 0:
            formatted_lines.append('')  # Add one blank line
        if line:  # Only add non-empty lines
            formatted_lines.append(line)
    
    acceptance_criteria = '\n'.join(formatted_lines)
    
    return acceptance_criteria

def generate_filename(work_item_id, work_item_title, product_prefix):
    """Generate filename following the specified convention
    Example: eNr_118556_loading_screen.us.txt
    """
    # Extract the part after the colon
    title_suffix = extract_title_suffix(work_item_title)
    filename = f"{product_prefix}_{work_item_id}_{title_suffix}.us.txt"
    return filename

def main():
    print("Azure DevOps Acceptance Criteria Exporter")
    print("=" * 50)
    
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Export Azure DevOps work item acceptance criteria',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python export-acceptance-criteria.py 124661
  python export-acceptance-criteria.py 124661 --auto
  python export-acceptance-criteria.py --id 124661 --auto
        '''
    )
    parser.add_argument('work_item_id', nargs='?', type=str, 
                        help='Azure DevOps work item ID')
    parser.add_argument('--id', type=str, dest='work_item_id_flag',
                        help='Azure DevOps work item ID (alternative syntax)')
    parser.add_argument('--auto', action='store_true',
                        help='Automatically use default filename without prompting')
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"\n✓ Created output directory: {OUTPUT_DIR}/")
    
    # Get work item ID from arguments or prompt
    work_item_id = args.work_item_id or args.work_item_id_flag
    
    if not work_item_id:
        work_item_id = input("\nEnter User Story ID: ").strip()
    
    if not work_item_id.isdigit():
        print("Error: Please enter a valid numeric ID.")
        return
    
    print(f"\nFetching work item {work_item_id}...")
    work_item = get_work_item(work_item_id)
    
    if not work_item:
        return
    
    # Extract fields
    fields = work_item.get('fields', {})
    work_item_title = fields.get('System.Title', 'untitled')
    work_item_type = fields.get('System.WorkItemType', 'Unknown')
    
    print(f"Work Item Type: {work_item_type}")
    print(f"Title: {work_item_title}")
    
    # Extract acceptance criteria
    acceptance_criteria = extract_acceptance_criteria(work_item)
    
    if not acceptance_criteria:
        print("\nWarning: No acceptance criteria found for this work item.")
        proceed = input("Do you want to create an empty file? (y/n): ").lower()
        if proceed != 'y':
            return
    
    # Generate filename
    default_filename = generate_filename(work_item_id, work_item_title, PRODUCT_PREFIX)
    print(f"\nDefault filename: {default_filename}")
    
    # Use default filename if --auto flag provided or take custom input
    if args.auto:
        filename = default_filename
        print("Using default filename (auto mode)")
    else:
        custom_filename = input("Press Enter to use default, or type a custom filename: ").strip()
        filename = custom_filename if custom_filename else default_filename
    
    # Ensure .us.txt extension
    if not filename.endswith('.us.txt'):
        if filename.endswith('.txt'):
            filename = filename[:-4] + '.us.txt'
        elif filename.endswith('.us'):
            filename = filename + '.txt'
        else:
            filename = filename + '.us.txt'
    
    # Prepend output directory to filename
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    # Save to file
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"User Story ID: {work_item_id}\n")
            f.write(f"Title: {work_item_title}\n")
            f.write(f"Type: {work_item_type}\n")
            f.write("=" * 50 + "\n\n")
            f.write("ACCEPTANCE CRITERIA:\n\n")
            f.write(acceptance_criteria if acceptance_criteria else "(No acceptance criteria found)")
        
        print(f"\n✓ Successfully exported to: {filepath}")
        print(f"  File size: {os.path.getsize(filepath)} bytes")
        
        # Return the filename for use by calling scripts
        return filename
        
    except Exception as e:
        print(f"\nError saving file: {e}")
        return None

if __name__ == "__main__":
    main()