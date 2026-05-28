#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: introspect-skill.sh <skill-path>

Analyzes a Claude Code skill and reports:
- Structure summary (files, references, scripts)
- Description quality assessment
- Suggestions for improvement and missing best practices
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

strip_frontmatter() {
  awk 'BEGIN{front=0} /^---$/{front++; next} front>=2{print}' "$1"
}

frontmatter=""
name_value="(missing)"
desc_value=""
desc_third_person="no"
desc_has_triggers="no"

if [[ -f "$skill_file" ]]; then
  frontmatter=$(awk 'BEGIN{capture=0} /^---/{if(capture==0){capture=1; next} else {exit}} capture==1{print}' "$skill_file")
  name_line=$(printf '%s\n' "$frontmatter" | grep '^name:' || true)
  desc_line=$(printf '%s\n' "$frontmatter" | grep '^description:' || true)
  if [[ -n "$name_line" ]]; then
    name_value=$(printf '%s\n' "$name_line" | sed 's/^name:[[:space:]]*//')
  fi
  if [[ -n "$desc_line" ]]; then
    desc_value=$(printf '%s\n' "$desc_line" | sed 's/^description:[[:space:]]*//')
    [[ "$desc_value" =~ This\ skill\ should\ be\ used ]] && desc_third_person="yes"
    [[ "$desc_value" =~ (when|for|upon) ]] && desc_has_triggers="yes"
  fi
fi

references_count=0
scripts_count=0
assets_count=0
reference_link_warnings=()

if [[ -d "$skill_dir/references" ]]; then
  references_count=$(find "$skill_dir/references" -type f | wc -l | tr -d ' ')
fi
if [[ -d "$skill_dir/scripts" ]]; then
  scripts_count=$(find "$skill_dir/scripts" -type f | wc -l | tr -d ' ')
fi
if [[ -d "$skill_dir/assets" ]]; then
  assets_count=$(find "$skill_dir/assets" -type f | wc -l | tr -d ' ')
fi

if [[ -f "$skill_file" && -d "$skill_dir/references" ]]; then
  while IFS= read -r -d '' ref; do
    rel_path="${ref#"$skill_dir/"}"
    ref_token="${rel_path#references/}"
    if ! grep -q "$rel_path" "$skill_file" && ! grep -q "$ref_token" "$skill_file"; then
      reference_link_warnings+=("Reference not linked: $rel_path")
    fi
  done < <(find "$skill_dir/references" -type f -print0)
fi

suggestions=()

if [[ ! -f "$skill_file" ]]; then
  suggestions+=("Add SKILL.md with frontmatter (name, description)")
fi
if [[ -z "$desc_value" ]]; then
  suggestions+=("Add a third-person description (e.g., 'This skill should be used when...')")
elif [[ "$desc_third_person" != "yes" ]]; then
  suggestions+=("Rewrite description in third-person trigger style")
fi
if [[ "$desc_has_triggers" != "yes" ]]; then
  suggestions+=("Include trigger phrases in description to aid activation")
fi

if [[ $references_count -eq 0 ]]; then
  suggestions+=("Add references/ with detailed docs; keep SKILL.md lean")
fi
if [[ ${#reference_link_warnings[@]} -gt 0 ]]; then
  suggestions+=("Link all references from SKILL.md")
fi

if [[ -f "$skill_file" ]]; then
  line_count=$(wc -l "$skill_file" | awk '{print $1}')
  fences=$(grep -c '```' "$skill_file" || true)
  if [[ $line_count -gt 200 ]]; then
    suggestions+=("SKILL.md is long ($line_count lines); move detail into references/")
  fi
  if [[ $fences -gt 1 && $scripts_count -eq 0 ]]; then
    suggestions+=("Convert repeated code blocks into scripts/ helpers")
  fi
fi

# Output
printf 'Skill: %s\n' "$skill_dir"
printf 'Name: %s\n' "$name_value"
printf 'Description: %s\n' "${desc_value:-'(missing)'}"
printf 'Description quality: third-person=%s, triggers=%s\n' "$desc_third_person" "$desc_has_triggers"
printf 'Structure:\n'
[[ -d "$skill_dir" ]] && find "$skill_dir" -maxdepth 2 -type f | sed "s|$skill_dir/||" | sort
printf 'Counts: references=%s, scripts=%s, assets=%s\n' "$references_count" "$scripts_count" "$assets_count"

if [[ ${#reference_link_warnings[@]} -gt 0 ]]; then
  printf 'Linking warnings:\n'
  for msg in "${reference_link_warnings[@]}"; do
    printf ' - %s\n' "$msg"
  done
fi

if [[ ${#suggestions[@]} -gt 0 ]]; then
  printf 'Suggestions:\n'
  for s in "${suggestions[@]}"; do
    printf ' - %s\n' "$s"
  done
else
  printf 'Suggestions: none (looks good)\n'
fi
