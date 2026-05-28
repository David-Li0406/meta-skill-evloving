#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: init-skill.sh <skill-name> [--template workflow|tool|domain] [--category <category>] [--path ~/.claude/skills]

Creates a new Claude Code skill from the provided template.
- Copies the chosen template into the destination path
- Replaces placeholder names with the provided skill name

Categories (optional): meta, orchestration, review, connections, clarify, enrich, persona, scaffold
If --category is provided, skill is created in ~/.claude/skills/<category>/<skill-name>
USAGE
}

if [[ "${1-}" == "-h" || "${1-}" == "--help" || $# -eq 0 ]]; then
  usage
  exit 0
fi

skill_name=""
template="workflow"
category=""
base_path="$HOME/.claude/skills"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --template)
      template="$2"
      shift 2
      ;;
    --category)
      category="$2"
      shift 2
      ;;
    --path)
      base_path="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      if [[ -z "$skill_name" ]]; then
        skill_name="$1"
        shift 1
      else
        echo "Unexpected argument: $1" >&2
        usage
        exit 1
      fi
      ;;
  esac
done

if [[ -z "$skill_name" ]]; then
  echo "Skill name is required." >&2
  usage
  exit 1
fi

case "$template" in
  workflow|tool|domain)
    ;;
  *)
    echo "Unsupported template: $template (expected workflow|tool|domain)" >&2
    exit 1
    ;;
 esac

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
templates_dir="$script_dir/../assets/templates"
template_dir="$templates_dir/${template}-skill"

if [[ ! -d "$template_dir" ]]; then
  echo "Template directory not found: $template_dir" >&2
  exit 1
fi

# Handle category path
if [[ -n "$category" ]]; then
  # Validate category
  valid_categories="meta orchestration review connections clarify enrich persona scaffold"
  if ! echo "$valid_categories" | grep -qw "$category"; then
    echo "Invalid category: $category" >&2
    echo "Valid categories: $valid_categories" >&2
    exit 1
  fi
  skill_dir="$base_path/$category/$skill_name"
else
  skill_dir="$base_path/$skill_name"
fi

mkdir -p "$(dirname "$skill_dir")"

if [[ -e "$skill_dir" ]]; then
  echo "Target skill already exists: $skill_dir" >&2
  exit 1
fi

mkdir -p "$skill_dir"
cp -R "$template_dir/." "$skill_dir"

if [[ -f "$skill_dir/SKILL.template.md" ]]; then
  mv "$skill_dir/SKILL.template.md" "$skill_dir/SKILL.md"
fi

# Replace placeholder skill names
while IFS= read -r -d '' file; do
  perl -pi -e "s|TODO-skill-name|$skill_name|g" "$file"
done < <(find "$skill_dir" -type f -print0)

echo "Created skill scaffold at $skill_dir (template: $template)."
