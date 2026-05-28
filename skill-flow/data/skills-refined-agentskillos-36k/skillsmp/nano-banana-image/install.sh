#!/bin/bash

SKILL_DIR="$HOME/.claude/skills/nano-banana-image"

echo "Installing nano-banana-image skill..."

mkdir -p "$SKILL_DIR"
cp -r package.json skill.md README.md scripts inputs outputs "$SKILL_DIR"
cd "$SKILL_DIR"

if command -v bun &> /dev/null; then
  bun install
elif command -v npm &> /dev/null; then
  npm install
else
  echo "Error: bun or npm required"
  exit 1
fi

echo ""
echo "Installed to $SKILL_DIR"
echo ""
echo "Make sure GEMINI_API_KEY is set in your shell:"
echo "  export GEMINI_API_KEY=\"your-key-here\""
echo ""
echo "Get a key at: https://aistudio.google.com/apikey"
