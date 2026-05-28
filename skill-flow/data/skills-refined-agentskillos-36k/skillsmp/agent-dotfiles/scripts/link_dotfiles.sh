#!/usr/bin/env bash
set -euo pipefail

DOTFILES_ROOT=""
MAPPING_FILE=""
FORCE=0

usage() {
  echo "Usage: link_dotfiles.sh --root <dotfiles_root> --map <mapping_file> [--force]"
}

while [ $# -gt 0 ]; do
  case "$1" in
    --root)
      DOTFILES_ROOT="$2"
      shift 2
      ;;
    --map)
      MAPPING_FILE="$2"
      shift 2
      ;;
    --force)
      FORCE=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [ -z "$DOTFILES_ROOT" ]; then
  DOTFILES_ROOT="$HOME/dotfiles"
fi
if [ -z "$MAPPING_FILE" ]; then
  MAPPING_FILE="$DOTFILES_ROOT/mappings.txt"
fi

if [ ! -f "$MAPPING_FILE" ]; then
  echo "Mapping file not found: $MAPPING_FILE" >&2
  exit 1
fi

while IFS= read -r line || [ -n "$line" ]; do
  line="${line%%#*}"
  line="$(printf "%s" "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
  if [ -z "$line" ]; then
    continue
  fi

  src="${line%%:*}"
  dest="${line#*:}"

  if [ -z "$src" ] || [ -z "$dest" ] || [ "$src" = "$dest" ]; then
    echo "Skip invalid line: $line" >&2
    continue
  fi

  src_path="$DOTFILES_ROOT/$src"
  if [ ! -e "$src_path" ]; then
    echo "Missing source: $src_path" >&2
    continue
  fi

  if [[ "$dest" == "~/"* ]]; then
    dest="$HOME/${dest:2}"
  fi

  dest_parent="$(dirname "$dest")"
  if [ -n "$dest_parent" ]; then
    mkdir -p "$dest_parent"
  fi

  if [ -e "$dest" ] || [ -L "$dest" ]; then
    if [ "$FORCE" -eq 1 ]; then
      ts="$(date +%Y%m%d%H%M%S)"
      mv "$dest" "${dest}.bak.${ts}"
    else
      echo "Skip existing: $dest" >&2
      continue
    fi
  fi

  ln -s "$src_path" "$dest"
  echo "Linked: $dest -> $src_path"
done < "$MAPPING_FILE"
