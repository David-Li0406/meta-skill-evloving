import argparse
import os
import sys
import re
from collections import defaultdict, Counter
from difflib import SequenceMatcher

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install PyYAML")
    sys.exit(1)


def extract_frontmatter_tags(content):
    """Extract tags from YAML frontmatter."""
    tags = []
    
    # Check if file starts with frontmatter
    if not content.startswith('---'):
        return tags
    
    # Find the end of frontmatter
    parts = content.split('---', 2)
    if len(parts) < 3:
        return tags
    
    frontmatter = parts[1]
    
    try:
        metadata = yaml.safe_load(frontmatter)
        if metadata and 'tags' in metadata:
            tag_data = metadata['tags']
            if isinstance(tag_data, list):
                tags.extend([str(t).strip() for t in tag_data])
            elif isinstance(tag_data, str):
                tags.append(tag_data.strip())
    except yaml.YAMLError:
        pass
    
    return tags


def extract_inline_tags(content):
    """Extract inline tags (#tag format) from markdown content."""
    # Remove code blocks to avoid false positives
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    content = re.sub(r'`[^`]+`', '', content)
    
    # Find all #tags (allowing letters, numbers, underscores, hyphens, slashes)
    # Tags must start with a letter
    pattern = r'#([a-zA-Z][a-zA-Z0-9_\-/]*)'
    tags = re.findall(pattern, content)
    
    return tags


def scan_vault(vault_path, verbose=False):
    """Scan all markdown files in the vault and extract tags."""
    tag_frequency = Counter()
    tag_files = defaultdict(list)  # tag -> list of files using it
    total_files = 0
    files_with_tags = 0
    
    if not os.path.exists(vault_path):
        print(f"Error: Vault path '{vault_path}' does not exist.")
        sys.exit(1)
    
    for root, dirs, files in os.walk(vault_path):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.endswith('.md'):
                total_files += 1
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, vault_path)
                
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    # Extract tags
                    frontmatter_tags = extract_frontmatter_tags(content)
                    inline_tags = extract_inline_tags(content)
                    all_tags = frontmatter_tags + inline_tags
                    
                    if all_tags:
                        files_with_tags += 1
                    
                    # Update statistics
                    for tag in all_tags:
                        tag_frequency[tag] += 1
                        tag_files[tag].append(rel_path)
                    
                    if verbose and all_tags:
                        print(f"  {rel_path}: {', '.join(all_tags)}")
                        
                except Exception as e:
                    if verbose:
                        print(f"Warning: Could not read {rel_path}: {e}", file=sys.stderr)
    
    return {
        'tag_frequency': tag_frequency,
        'tag_files': tag_files,
        'total_files': total_files,
        'files_with_tags': files_with_tags
    }


def analyze_tag_hierarchy(tags):
    """Analyze tag hierarchy (nested tags with /)."""
    hierarchy = defaultdict(list)
    
    for tag in tags:
        if '/' in tag:
            parts = tag.split('/')
            parent = '/'.join(parts[:-1])
            child = parts[-1]
            hierarchy[parent].append(tag)
    
    return hierarchy


def find_similar_tags(tags, threshold=0.8):
    """Find tags with similar names that might be duplicates."""
    similar_groups = []
    tags_list = list(tags)
    checked = set()
    
    for i, tag1 in enumerate(tags_list):
        if tag1 in checked:
            continue
        
        similar = [tag1]
        for tag2 in tags_list[i+1:]:
            if tag2 in checked:
                continue
            
            # Compare similarity
            ratio = SequenceMatcher(None, tag1.lower(), tag2.lower()).ratio()
            if ratio >= threshold:
                similar.append(tag2)
                checked.add(tag2)
        
        if len(similar) > 1:
            similar_groups.append(similar)
            checked.add(tag1)
    
    return similar_groups


def generate_report(analysis, vault_path):
    """Generate a markdown report of the tag analysis."""
    tag_frequency = analysis['tag_frequency']
    tag_files = analysis['tag_files']
    total_files = analysis['total_files']
    files_with_tags = analysis['files_with_tags']
    
    report = []
    report.append("# Tag Analysis Report")
    report.append(f"\n**Vault**: `{vault_path}`")
    report.append(f"\n**Generated**: {os.popen('date').read().strip()}")
    
    # Summary
    report.append("\n## Summary")
    report.append(f"- **Total notes**: {total_files}")
    report.append(f"- **Notes with tags**: {files_with_tags} ({files_with_tags/total_files*100:.1f}%)")
    report.append(f"- **Unique tags**: {len(tag_frequency)}")
    report.append(f"- **Total tag usages**: {sum(tag_frequency.values())}")
    
    # Tag Frequency
    report.append("\n## Tag Frequency")
    report.append("\n| Rank | Tag | Count | % of Tagged Notes |")
    report.append("|------|-----|-------|-------------------|")
    
    for rank, (tag, count) in enumerate(tag_frequency.most_common(50), 1):
        percentage = (count / files_with_tags * 100) if files_with_tags > 0 else 0
        report.append(f"| {rank} | `{tag}` | {count} | {percentage:.1f}% |")
    
    if len(tag_frequency) > 50:
        report.append(f"\n*... and {len(tag_frequency) - 50} more tags*")
    
    # Tag Hierarchy
    hierarchy = analyze_tag_hierarchy(tag_frequency.keys())
    if hierarchy:
        report.append("\n## Tag Hierarchy")
        report.append("\nNested tags detected:")
        for parent, children in sorted(hierarchy.items()):
            report.append(f"\n### `{parent}/`")
            for child in sorted(children):
                count = tag_frequency[child]
                report.append(f"- `{child}` ({count} uses)")
    
    # Similar Tags
    similar_groups = find_similar_tags(tag_frequency.keys(), threshold=0.75)
    if similar_groups:
        report.append("\n## Similar Tags (Potential Duplicates)")
        report.append("\nThese tags have similar names and might need consolidation:")
        for group in similar_groups:
            counts = [f"`{tag}` ({tag_frequency[tag]})" for tag in group]
            report.append(f"\n- {', '.join(counts)}")
    
    # Orphaned Tags
    orphaned = [(tag, count) for tag, count in tag_frequency.items() if count <= 2]
    if orphaned:
        report.append("\n## Low-Usage Tags")
        report.append(f"\nTags used in 2 or fewer notes ({len(orphaned)} tags):")
        for tag, count in sorted(orphaned, key=lambda x: x[1]):
            report.append(f"- `{tag}` ({count} use{'s' if count > 1 else ''})")
    
    # Recommendations
    report.append("\n## Recommendations")
    recommendations = []
    
    if similar_groups:
        recommendations.append("- **Review similar tags**: Consider consolidating tags with similar names to reduce duplication.")
    
    if orphaned:
        recommendations.append(f"- **Review low-usage tags**: {len(orphaned)} tags are used in 2 or fewer notes. Consider removing or consolidating them.")
    
    if files_with_tags < total_files * 0.5:
        recommendations.append(f"- **Increase tag coverage**: Only {files_with_tags/total_files*100:.1f}% of notes are tagged. Consider adding tags to more notes for better organization.")
    
    if hierarchy:
        recommendations.append("- **Tag hierarchy detected**: You're using nested tags effectively. Consider documenting your tag structure for consistency.")
    
    if not recommendations:
        recommendations.append("- **Good job!** Your tag organization appears well-maintained.")
    
    report.extend(recommendations)
    
    return '\n'.join(report)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze tags in an Obsidian vault")
    parser.add_argument("--vault", required=True, help="Path to the Obsidian vault root")
    parser.add_argument("--output", help="Output file for the report (default: print to stdout)")
    parser.add_argument("--verbose", action="store_true", help="Show detailed progress")
    
    args = parser.parse_args()
    
    if args.verbose:
        print(f"Scanning vault: {args.vault}")
    
    analysis = scan_vault(args.vault, verbose=args.verbose)
    
    if args.verbose:
        print(f"\nFound {len(analysis['tag_frequency'])} unique tags in {analysis['files_with_tags']} files")
    
    report = generate_report(analysis, args.vault)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Report saved to: {args.output}")
    else:
        print(report)
