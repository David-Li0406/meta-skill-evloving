#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: validate-skill.sh <skill-path>

Checks a Claude Code skill for structure and quality:
- SKILL.md exists with valid frontmatter
- name and description present
- description uses third-person trigger style
- references/ files are linked in SKILL.md
- highlights duplicated content between SKILL.md and references/
USAGE
}

if [[ "${1-}" == "-h" || "${1-}" == "--help" || $# -eq 0 ]]; then
  usage
  exit 0
fi

skill_dir="$1"
if [[ ! -d "$skill_dir" ]]; then
  echo "Skill path not found: $skill_dir" >&2
  exit 1
fi

skill_dir="$(cd "$skill_dir" && pwd)"
skill_file="$skill_dir/SKILL.md"

errors=()
warnings=()

error() { errors+=("$1"); }
warn() { warnings+=("$1"); }

strip_frontmatter() {
  # Print file without YAML frontmatter
  awk 'BEGIN{front=0} /^---$/{front++; next} front>=2{print}' "$1"
}

if [[ ! -f "$skill_file" ]]; then
  error "Missing SKILL.md"
else
  frontmatter=$(awk 'BEGIN{capture=0} /^---/{if(capture==0){capture=1; next} else {exit}} capture==1{print}' "$skill_file")
  if [[ -z "$frontmatter" ]]; then
    error "SKILL.md missing YAML frontmatter block"
  else
    name_line=$(printf '%s\n' "$frontmatter" | grep '^name:' || true)
    desc_line=$(printf '%s\n' "$frontmatter" | grep '^description:' || true)

    if [[ -z "$name_line" ]]; then
      error "Frontmatter missing name"
    fi

    if [[ -z "$desc_line" ]]; then
      error "Frontmatter missing description"
    else
      desc_value=$(printf '%s\n' "$desc_line" | sed 's/^description:[[:space:]]*//')
      if ! [[ "$desc_value" =~ This\ skill\ should\ be\ used ]]; then
        error "Description should use third-person trigger phrasing (e.g., 'This skill should be used when...')"
      fi
      if [[ "$desc_value" =~ \b(I|we|my|our|me|us)\b ]]; then
        warn "Description may not be third-person (found first-person pronouns)"
      fi
    fi
  fi
fi

# Verify references are linked
if [[ -f "$skill_file" && -d "$skill_dir/references" ]]; then
  while IFS= read -r -d '' ref; do
    rel_path="${ref#"$skill_dir/"}"
    ref_token="${rel_path#references/}"
    if ! grep -q "$rel_path" "$skill_file" && ! grep -q "$ref_token" "$skill_file"; then
      warn "Reference not linked in SKILL.md: $rel_path"
    fi
  done < <(find "$skill_dir/references" -type f -print0)
fi

# Check for duplicated lines between SKILL.md and references
if [[ -f "$skill_file" && -d "$skill_dir/references" ]]; then
  skill_tmp=$(mktemp)
  trap 'rm -f "$skill_tmp"' EXIT
  strip_frontmatter "$skill_file" | sed '/^$/d' | grep -v '^#' | sort -u > "$skill_tmp"

  while IFS= read -r -d '' ref; do
    ref_tmp=$(mktemp)
    sed '/^$/d' "$ref" | grep -v '^#' | sort -u > "$ref_tmp"
    dup=$(comm -12 "$skill_tmp" "$ref_tmp" | head -n 3)
    if [[ -n "$dup" ]]; then
      warn "Duplicated lines between SKILL.md and ${ref#"$skill_dir/"}:
$dup"
    fi
    rm -f "$ref_tmp"
  done < <(find "$skill_dir/references" -type f -print0)
fi

# Output results
if [[ ${#errors[@]} -eq 0 && ${#warnings[@]} -eq 0 ]]; then
  echo "Validation passed for $skill_dir"
  exit 0
fi

echo "Validation results for $skill_dir"
if [[ ${#errors[@]} -gt 0 ]]; then
  for msg in "${errors[@]}"; do
    echo "ERROR: $msg"
  done
fi
if [[ ${#warnings[@]} -gt 0 ]]; then
  for msg in "${warnings[@]}"; do
    echo "WARN: $msg"
  done
fi

if [[ ${#errors[@]} -gt 0 ]]; then
  exit 1
fi
