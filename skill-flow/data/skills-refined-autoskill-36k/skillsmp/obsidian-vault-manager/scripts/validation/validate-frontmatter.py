#!/usr/bin/env python3
"""
Validate frontmatter in markdown content.
Can be run by Claude during workflow or configured as a hook in settings.json
"""
import sys
import yaml

def validate_content(content):
    """Validate frontmatter in markdown content"""
    if not content.startswith("---"):
        return False, "No frontmatter detected"

    try:
        # Extract frontmatter
        parts = content.split("---", 2)
        if len(parts) < 3:
            return False, "Malformed frontmatter (missing closing ---)"

        frontmatter = yaml.safe_load(parts[1])

        if not frontmatter:
            return False, "Empty frontmatter"

        # Required fields
        required = ["title", "tags", "date", "type"]
        missing = [f for f in required if f not in frontmatter]

        if missing:
            return False, f"Missing required fields: {', '.join(missing)}"

        # Validate tags is a list
        tags = frontmatter.get("tags", [])
        if not isinstance(tags, list):
            return False, "Tags must be a list"

        if len(tags) == 0:
            return False, "Tags list is empty"

        # Check for content type tag
        valid_types = ["video", "article", "book", "podcast", "idea", "study-guide", "repository", "reference", "project"]
        has_type = any(tag in valid_types for tag in tags)
        if not has_type:
            return False, f"No content type tag found. Expected one of: {', '.join(valid_types)}"

        # Check for inbox tag
        if "inbox" not in tags:
            return False, "Warning: 'inbox' tag recommended for new content"

        return True, "✅ Validation passed"

    except yaml.YAMLError as e:
        return False, f"Invalid YAML syntax: {e}"
    except Exception as e:
        return False, f"Validation error: {e}"

def main():
    """Main entry point for validation script"""
    if len(sys.argv) > 1:
        # Read from file if provided
        filename = sys.argv[1]
        try:
            with open(filename, 'r') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"❌ Error: File not found: {filename}", file=sys.stderr)
            sys.exit(1)
    else:
        # Read from stdin
        content = sys.stdin.read()

    valid, message = validate_content(content)

    if valid:
        print(message)
        sys.exit(0)
    else:
        print(f"❌ {message}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
