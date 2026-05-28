#!/usr/bin/env bash
#
# Skill Initializer - Creates a new skill from template
#
# Usage:
#     init_skill.sh <skill-name> --path <path>
#
# Examples:
#     init_skill.sh my-new-skill --path skills/public
#     init_skill.sh my-api-helper --path skills/private
#     init_skill.sh custom-skill --path /custom/location
#

set -euo pipefail

# Convert hyphenated skill name to Title Case
title_case_skill_name() {
    echo "$1" | tr '-' ' ' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))}1'
}

# Generate SKILL.md content
generate_skill_template() {
    local skill_name="$1"
    local skill_title="$2"

    cat <<EOF
---
name: ${skill_name}
description: [TODO: Complete and informative explanation of what the skill does and when to use it. Include WHEN to use this skill - specific scenarios, file types, or tasks that trigger it.]
---

# ${skill_title}

## Overview

[TODO: 1-2 sentences explaining what this skill enables]

## Structuring This Skill

[TODO: Choose the structure that best fits this skill's purpose. Common patterns:

**1. Workflow-Based** (best for sequential processes)
- Works well when there are clear step-by-step procedures
- Example: DOCX skill with "Workflow Decision Tree" → "Reading" → "Creating" → "Editing"
- Structure: ## Overview → ## Workflow Decision Tree → ## Step 1 → ## Step 2...

**2. Task-Based** (best for tool collections)
- Works well when the skill offers different operations/capabilities
- Example: PDF skill with "Quick Start" → "Merge PDFs" → "Split PDFs" → "Extract Text"
- Structure: ## Overview → ## Quick Start → ## Task Category 1 → ## Task Category 2...

**3. Reference/Guidelines** (best for standards or specifications)
- Works well for brand guidelines, coding standards, or requirements
- Example: Brand styling with "Brand Guidelines" → "Colors" → "Typography" → "Features"
- Structure: ## Overview → ## Guidelines → ## Specifications → ## Usage...

**4. Capabilities-Based** (best for integrated systems)
- Works well when the skill provides multiple interrelated features
- Example: Product Management with "Core Capabilities" → numbered capability list
- Structure: ## Overview → ## Core Capabilities → ### 1. Feature → ### 2. Feature...

Patterns can be mixed and matched as needed. Most skills combine patterns (e.g., start with task-based, add workflow for complex operations).

Delete this entire "Structuring This Skill" section when done - it's just guidance.]

## [TODO: Replace with the first main section based on chosen structure]

[TODO: Add content here. See examples in existing skills:
- Code samples for technical skills
- Decision trees for complex workflows
- Concrete examples with realistic user requests
- References to scripts/templates/references as needed]

## Resources

This skill includes example resource directories that demonstrate how to organize different types of bundled resources:

### scripts/
Executable code (Python/Bash/etc.) that can be run directly to perform specific operations.

**Examples from other skills:**
- PDF skill: \`fill_fillable_fields.py\`, \`extract_form_field_info.py\` - utilities for PDF manipulation
- DOCX skill: \`document.py\`, \`utilities.py\` - Python modules for document processing

**Appropriate for:** Python scripts, shell scripts, or any executable code that performs automation, data processing, or specific operations.

**Note:** Scripts may be executed without loading into context, but can still be read by Claude for patching or environment adjustments.

### references/
Documentation and reference material intended to be loaded into context to inform Claude's process and thinking.

**Examples from other skills:**
- Product management: \`communication.md\`, \`context_building.md\` - detailed workflow guides
- BigQuery: API reference documentation and query examples
- Finance: Schema documentation, company policies

**Appropriate for:** In-depth documentation, API references, database schemas, comprehensive guides, or any detailed information that Claude should reference while working.

### assets/
Files not intended to be loaded into context, but rather used within the output Claude produces.

**Examples from other skills:**
- Brand styling: PowerPoint template files (.pptx), logo files
- Frontend builder: HTML/React boilerplate project directories
- Typography: Font files (.ttf, .woff2)

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Any unneeded directories can be deleted.** Not every skill requires all three types of resources.
EOF
}

# Generate example script content
generate_example_script() {
    local skill_name="$1"

    cat <<EOF
#!/usr/bin/env python3
"""
Example helper script for ${skill_name}

This is a placeholder script that can be executed directly.
Replace with actual implementation or delete if not needed.

Example real scripts from other skills:
- pdf/scripts/fill_fillable_fields.py - Fills PDF form fields
- pdf/scripts/convert_pdf_to_images.py - Converts PDF pages to images
"""

def main():
    print("This is an example script for ${skill_name}")
    # TODO: Add actual script logic here
    # This could be data processing, file conversion, API calls, etc.

if __name__ == "__main__":
    main()
EOF
}

# Generate example reference content
generate_example_reference() {
    local skill_title="$1"

    cat <<'REFERENCE_EOF'
# Reference Documentation for SKILL_TITLE_PLACEHOLDER

This is a placeholder for detailed reference documentation.
Replace with actual reference content or delete if not needed.

Example real reference docs from other skills:
- product-management/references/communication.md - Comprehensive guide for status updates
- product-management/references/context_building.md - Deep-dive on gathering context
- bigquery/references/ - API references and query examples

## When Reference Docs Are Useful

Reference docs are ideal for:
- Comprehensive API documentation
- Detailed workflow guides
- Complex multi-step processes
- Information too lengthy for main SKILL.md
- Content that's only needed for specific use cases

## Structure Suggestions

### API Reference Example
- Overview
- Authentication
- Endpoints with examples
- Error codes
- Rate limits

### Workflow Guide Example
- Prerequisites
- Step-by-step instructions
- Common patterns
- Troubleshooting
- Best practices
REFERENCE_EOF
}

# Generate example asset content
generate_example_asset() {
    cat <<'EOF'
# Example Asset File

This placeholder represents where asset files would be stored.
Replace with actual asset files (templates, images, fonts, etc.) or delete if not needed.

Asset files are NOT intended to be loaded into context, but rather used within
the output Claude produces.

Example asset files from other skills:
- Brand guidelines: logo.png, slides_template.pptx
- Frontend builder: hello-world/ directory with HTML/React boilerplate
- Typography: custom-font.ttf, font-family.woff2
- Data: sample_data.csv, test_dataset.json

## Common Asset Types

- Templates: .pptx, .docx, boilerplate directories
- Images: .png, .jpg, .svg, .gif
- Fonts: .ttf, .otf, .woff, .woff2
- Boilerplate code: Project directories, starter files
- Icons: .ico, .svg
- Data files: .csv, .json, .xml, .yaml

Note: This is a text placeholder. Actual assets can be any file type.
EOF
}

# Show usage information
usage() {
    cat <<EOF
Usage: init_skill.sh <skill-name> --path <path>

Skill name requirements:
  - Hyphen-case identifier (e.g., 'data-analyzer')
  - Lowercase letters, digits, and hyphens only
  - Max 40 characters
  - Must match directory name exactly

Examples:
  init_skill.sh my-new-skill --path skills/public
  init_skill.sh my-api-helper --path skills/private
  init_skill.sh custom-skill --path /custom/location
EOF
    exit 1
}

# Initialize a new skill
init_skill() {
    local skill_name="$1"
    local path="$2"

    # Resolve full path
    local skill_dir
    skill_dir="$(cd "$path" 2>/dev/null && pwd)/${skill_name}" || skill_dir="${path}/${skill_name}"

    # Check if directory already exists
    if [[ -e "$skill_dir" ]]; then
        echo "❌ Error: Skill directory already exists: ${skill_dir}"
        return 1
    fi

    # Create skill directory
    if ! mkdir -p "$skill_dir"; then
        echo "❌ Error creating directory: ${skill_dir}"
        return 1
    fi
    echo "✅ Created skill directory: ${skill_dir}"

    # Generate title case name
    local skill_title
    skill_title="$(title_case_skill_name "$skill_name")"

    # Create SKILL.md from template
    if ! generate_skill_template "$skill_name" "$skill_title" > "${skill_dir}/SKILL.md"; then
        echo "❌ Error creating SKILL.md"
        return 1
    fi
    echo "✅ Created SKILL.md"

    # Create scripts/ directory with example script
    mkdir -p "${skill_dir}/scripts"
    if ! generate_example_script "$skill_name" > "${skill_dir}/scripts/example.py"; then
        echo "❌ Error creating scripts/example.py"
        return 1
    fi
    chmod 755 "${skill_dir}/scripts/example.py"
    echo "✅ Created scripts/example.py"

    # Create references/ directory with example reference doc
    mkdir -p "${skill_dir}/references"
    if ! generate_example_reference "$skill_title" | sed "s/SKILL_TITLE_PLACEHOLDER/${skill_title}/g" > "${skill_dir}/references/api_reference.md"; then
        echo "❌ Error creating references/api_reference.md"
        return 1
    fi
    echo "✅ Created references/api_reference.md"

    # Create assets/ directory with example asset placeholder
    mkdir -p "${skill_dir}/assets"
    if ! generate_example_asset > "${skill_dir}/assets/example_asset.txt"; then
        echo "❌ Error creating assets/example_asset.txt"
        return 1
    fi
    echo "✅ Created assets/example_asset.txt"

    # Print next steps
    echo ""
    echo "✅ Skill '${skill_name}' initialized successfully at ${skill_dir}"
    echo ""
    echo "Next steps:"
    echo "1. Edit SKILL.md to complete the TODO items and update the description"
    echo "2. Customize or delete the example files in scripts/, references/, and assets/"
    echo "3. Run the validator when ready to check the skill structure"

    return 0
}

# Main entry point
main() {
    if [[ $# -lt 3 ]] || [[ "$2" != "--path" ]]; then
        usage
    fi

    local skill_name="$1"
    local path="$3"

    echo "🚀 Initializing skill: ${skill_name}"
    echo "   Location: ${path}"
    echo ""

    if init_skill "$skill_name" "$path"; then
        exit 0
    else
        exit 1
    fi
}

main "$@"
