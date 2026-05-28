#!/bin/bash
# sync-skill.sh - Sync a skill from various sources to AI coding tool directories
#
# Usage:
#   ./sync-skill.sh <source>
#   <source> can be:
#     - Local folder path
#     - GitHub URL
#     - skillsmp.com URL

set -euo pipefail

# All target directories to check
TARGET_DIRS=(
  "$HOME/.claude/skills"
  "$HOME/.qoder/skills"
  "$HOME/.copilot/skills"
  "$HOME/.gemini/antigravity/skills"
  "$HOME/.cursor/skills"
  "$HOME/.config/opencode/skill"
  "$HOME/.codex/skills"
  "$HOME/.gemini/skills"
  "$HOME/.codeium/windsurf/skills"
  "$HOME/.qwen/skills"
)

# Detect source type
detect_source_type() {
  local source="$1"

  # Local folder (starts with /, ./, or ~)
  if [[ "$source" =~ ^/ ]] || [[ "$source" =~ ^\./ ]] || [[ "$source" =~ ^~ ]]; then
    echo "local"
  # GitHub URL
  elif [[ "$source" =~ github\.com ]]; then
    echo "github"
  # skillsmp.com URL
  elif [[ "$source" =~ skillsmp\.com ]]; then
    echo "skillsmp"
  else
    echo "unknown"
  fi
}

# Get existing target directories
get_existing_targets() {
  local existing=()
  for target in "${TARGET_DIRS[@]}"; do
    if [ -d "$target" ]; then
      existing+=("$target")
    fi
  done
  printf '%s\n' "${existing[@]}"
}

# Sync local folder
sync_local_folder() {
  local source_path="$1"
  local skill_name
  skill_name=$(basename "$source_path")

  if [ ! -d "$source_path" ]; then
    echo "❌ Error: Source folder does not exist: $source_path"
    exit 1
  fi

  echo "📁 Syncing local folder: $source_path"
  sync_to_targets "$source_path" "$skill_name"
}

# Sync GitHub repository
sync_github_repo() {
  local repo_url="$1"
  local temp_dir
  temp_dir=$(mktemp -d -t skill-sync-XXXXXX)

  echo "📦 Cloning GitHub repository: $repo_url"

  # Strip .git suffix if present
  repo_url="${repo_url%.git}"

  # Clone repository (full history as per requirement)
  if ! git clone "$repo_url" "$temp_dir"; then
    echo "❌ Error: Failed to clone repository"
    rm -rf "$temp_dir"
    exit 1
  fi

  # Find skill folder
  local skill_folder=""

  # Check if SKILL.md is in root
  if [ -f "$temp_dir/SKILL.md" ]; then
    skill_folder="$temp_dir"
  # Check if there's a skills subdirectory
  elif [ -d "$temp_dir/skills" ]; then
    skill_folder="$temp_dir/skills"
  fi

  if [ -z "$skill_folder" ]; then
    echo "❌ Error: Could not find skill folder in repository"
    rm -rf "$temp_dir"
    exit 1
  fi

  # Get skill name
  local skill_name
  skill_name=$(basename "$skill_folder")

  echo "📦 Found skill: $skill_name"

  # Sync to targets
  sync_to_targets "$skill_folder" "$skill_name"

  # Cleanup
  rm -rf "$temp_dir"
  echo "🧹 Cleaned up temporary files"
}

# Sync skillsmp.com page
sync_skillsmp_page() {
  local page_url="$1"
  local temp_dir
  temp_dir=$(mktemp -d -t skill-sync-XXXXXX)

  echo "🌐 Fetching skillsmp.com page: $page_url"

  # Fetch page content
  if ! curl -sL "$page_url" > "$temp_dir/page.html"; then
    echo "❌ Error: Failed to fetch page"
    rm -rf "$temp_dir"
    exit 1
  fi

  # Extract skill name (this is a placeholder - actual parsing depends on page structure)
  local skill_name
  skill_name=$(grep -o '<h1[^>]*>.*</h1>' "$temp_dir/page.html" | sed 's/<[^>]*>//g' | head -1 | tr '[:upper:]' '[:lower:]' | tr ' ' '-')

  if [ -z "$skill_name" ]; then
    echo "❌ Error: Could not extract skill name from page"
    rm -rf "$temp_dir"
    exit 1
  fi

  echo "📄 Extracted skill name: $skill_name"

  # Note: Actual implementation would need to parse the page structure
  # and extract skill files. This is a placeholder that shows the flow.
  echo "⚠️  Note: skillsmp.com parsing requires page-specific implementation"

  rm -rf "$temp_dir"
}

# Confirm with user before syncing
confirm_sync() {
  local skill_name="$1"

  echo ""
  echo "📋 Found $(get_existing_targets | wc -l | tr -d ' ') existing target directory(s):"
  echo ""

  local index=1
  while IFS= read -r target; do
    if [ -n "$target" ]; then
      echo "  $index. $target"
      index=$((index + 1))
    fi
  done < <(get_existing_targets)

  echo ""
  echo "Skill to sync: $skill_name"
  read -p "✅ Sync to these directories? (y/N): " confirm

  if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo ""
    echo "❌ Sync cancelled by user."
    exit 1
  fi

  echo ""
  echo "🚀 Starting sync..."
}

# Sync to all existing target directories
sync_to_targets() {
  local source="$1"
  local skill_name="$2"
  local synced_count=0

  # First: show confirmation dialog
  confirm_sync "$skill_name"

  echo ""
  echo "🎯 Syncing to:"

  # Get list of existing targets and sync
  local synced_count=0
  local target

  while IFS= read -r target; do
    if [ -z "$target" ]; then
      continue
    fi
    local target_path="$target/$skill_name"

    # Check if skill already exists
    if [ -e "$target_path" ]; then
      echo "  📝 Overwriting: $target_path"
      rm -rf "$target_path"
    else
      echo "  ➕ Creating: $target_path"
    fi

    # Copy skill folder
    if cp -r "$source" "$target_path"; then
      synced_count=$((synced_count + 1))
    else
      echo "  ❌ Failed to sync to: $target_path"
    fi
  done < <(get_existing_targets)

  echo ""
  echo "✅ Synced to $synced_count target directory(s)"
}

# Main execution
main() {
  if [ $# -eq 0 ]; then
    echo "Usage: $0 <source>"
    echo ""
    echo "Source can be:"
    echo "  - Local folder path: /path/to/skill"
    echo "  - GitHub URL: https://github.com/user/repo"
    echo "  - skillsmp.com URL: https://skillsmp.com/skills/skill-name"
    exit 1
  fi

  local source="$1"
  local source_type
  source_type=$(detect_source_type "$source")

  echo "🔍 Detected source type: $source_type"
  echo ""

  case "$source_type" in
    local)
      sync_local_folder "$source"
      ;;
    github)
      sync_github_repo "$source"
      ;;
    skillsmp)
      sync_skillsmp_page "$source"
      ;;
    *)
      echo "❌ Error: Unknown source type"
      echo "Source must be a local folder, GitHub URL, or skillsmp.com URL"
      exit 1
      ;;
  esac
}

main "$@"
