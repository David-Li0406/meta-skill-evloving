#!/usr/bin/env python3
"""
Generate HTML financing presentation from JSON data

This script reads project data from a JSON file and generates a complete
HTML financing presentation using the template.

Usage:
    python3 generate_presentation.py <input_json> <output_html>

Example:
    python3 generate_presentation.py project_data.json presentation.html
"""

import json
import sys
from pathlib import Path


def load_template(template_path):
    """Load the HTML template file."""
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def load_project_data(json_path):
    """Load project data from JSON file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_presentation(template, data):
    """
    Replace placeholders in the template with actual data.

    Args:
        template: HTML template string
        data: Dictionary containing project data

    Returns:
        HTML string with placeholders replaced
    """
    # Extract basic information
    project_name = data.get('project_name', '项目名称')
    slogan = data.get('slogan', '一句话Slogan')
    founder_name = data.get('founder_name', '创始人姓名')
    contact_info = data.get('contact_info', '联系方式')

    # Extract page content
    pages = data.get('pages', [])
    
    # Create content mapping
    content_map = {
        'PROJECT_NAME': project_name,
        'SLOGAN': slogan,
        'FOUNDER_NAME': founder_name,
        'CONTACT_INFO': contact_info,
    }

    # Map page content to placeholders
    for page in pages:
        page_number = page.get('number')
        page_type = page.get('type')
        title = page.get('title', '')
        content = page.get('content', '')

        if page_number == 1:
            content_map['PROJECT_NAME'] = title.replace('融资演示', '').strip()
            if '|' in content:
                parts = content.split('|')
                content_map['SLOGAN'] = parts[0].strip()
                contact_part = parts[1].strip()
                if '创始人' in contact_part:
                    content_map['FOUNDER_NAME'] = contact_part.split('：')[1].strip()
                if '联系方式' in contact_part:
                    content_map['CONTACT_INFO'] = contact_part.split('：')[1].strip()
        
        elif page_number == 2:
            content_map['PROBLEM_OPPORTUNITY'] = content
        
        elif page_number == 3:
            content_map['SOLUTION'] = content
        
        elif page_number == 4:
            content_map['PRODUCT_DEMO'] = content
        
        elif page_number == 5:
            content_map['MARKET_SIZE'] = content
        
        elif page_number == 6:
            content_map['COMPETITION'] = content
        
        elif page_number == 7:
            content_map['BUSINESS_MODEL'] = content
        
        elif page_number == 8:
            content_map['TRACTION'] = content
        
        elif page_number == 9:
            content_map['TEAM'] = content
        
        elif page_number == 10:
            content_map['FINANCIAL_PROJECTIONS'] = content
        
        elif page_number == 11:
            content_map['FUNDING_NEEDS'] = content
        
        elif page_number == 12:
            # Convert content to bullet points
            if '要点' in content or '点' in content:
                points = content.split('。')
                highlights = '\n'.join([f'<li>{point.strip()}。</li>' for point in points if point.strip()])
            else:
                highlights = f'<li>{content}</li>'
            content_map['INVESTMENT_HIGHLIGHTS'] = highlights

    # Replace all placeholders
    html = template
    for placeholder, value in content_map.items():
        html = html.replace(f'{{{{{placeholder}}}}}', value)

    return html


def save_presentation(html, output_path):
    """Save the generated HTML presentation."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 generate_presentation.py <input_json> <output_html>")
        print("\nExample:")
        print("  python3 generate_presentation.py project_data.json presentation.html")
        sys.exit(1)

    input_json = sys.argv[1]
    output_html = sys.argv[2]

    # Validate input file exists
    if not Path(input_json).exists():
        print(f"Error: Input file not found: {input_json}")
        sys.exit(1)

    # Get template path
    script_dir = Path(__file__).parent
    template_path = script_dir.parent / 'assets' / 'financing_template.html'

    if not template_path.exists():
        print(f"Error: Template file not found: {template_path}")
        sys.exit(1)

    try:
        # Load template and data
        print(f"Loading template from: {template_path}")
        template = load_template(template_path)
        
        print(f"Loading project data from: {input_json}")
        data = load_project_data(input_json)
        
        # Generate presentation
        print("Generating presentation...")
        html = generate_presentation(template, data)
        
        # Save presentation
        print(f"Saving presentation to: {output_html}")
        save_presentation(html, output_html)
        
        print("\n✅ Presentation generated successfully!")
        print(f"Open {output_html} in a browser to view the presentation.")
        
    except Exception as e:
        print(f"\n❌ Error generating presentation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
