#!/bin/bash
# Repo Recap HTML Generator
# Usage: ./generate-recap.sh <data.json> > repo-recap-2025.html

set -e

DATA_FILE="${1:-/dev/stdin}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TEMPLATE="${SCRIPT_DIR}/templates/recap.html"

if [ ! -f "$TEMPLATE" ]; then
  echo "Error: Template not found at $TEMPLATE" >&2
  exit 1
fi

# Read data from JSON file
REPO_NAME=$(jq -r '.repoName' "$DATA_FILE")
YEAR=$(jq -r '.year' "$DATA_FILE")

# Write JSON to temp files to avoid shell escaping issues
TMP_RAW=$(mktemp)
TMP_PRS=$(mktemp)
TMP_ISSUES=$(mktemp)
TMP_ALIASES=$(mktemp)
trap "rm -f $TMP_RAW $TMP_PRS $TMP_ISSUES $TMP_ALIASES" EXIT

jq -c '.rawCommits' "$DATA_FILE" > "$TMP_RAW"
jq -c '.prs' "$DATA_FILE" > "$TMP_PRS"
jq -c '.issues' "$DATA_FILE" > "$TMP_ISSUES"
jq -c '.contributorAliases // {}' "$DATA_FILE" > "$TMP_ALIASES"

# Use perl with file slurping for safe replacement
perl -e '
  use strict;
  use warnings;

  my $repo = shift;
  my $year = shift;
  my $raw_file = shift;
  my $prs_file = shift;
  my $issues_file = shift;
  my $aliases_file = shift;
  my $template = shift;

  # Read JSON files
  open my $fh, "<", $raw_file or die $!;
  my $raw = do { local $/; <$fh> }; close $fh; chomp $raw;

  open $fh, "<", $prs_file or die $!;
  my $prs = do { local $/; <$fh> }; close $fh; chomp $prs;

  open $fh, "<", $issues_file or die $!;
  my $issues = do { local $/; <$fh> }; close $fh; chomp $issues;

  open $fh, "<", $aliases_file or die $!;
  my $aliases = do { local $/; <$fh> }; close $fh; chomp $aliases;

  # Read template
  open $fh, "<", $template or die $!;
  my $html = do { local $/; <$fh> }; close $fh;

  # Replace placeholders
  $html =~ s/\{\{REPO_NAME\}\}/$repo/g;
  $html =~ s/\{\{YEAR\}\}/$year/g;
  $html =~ s/\{\{RAW_COMMITS_JSON\}\}/$raw/g;
  $html =~ s/\{\{PRS_JSON\}\}/$prs/g;
  $html =~ s/\{\{ISSUES_JSON\}\}/$issues/g;
  $html =~ s/\{\{CONTRIBUTOR_ALIASES_JSON\}\}/$aliases/g;

  print $html;
' "$REPO_NAME" "$YEAR" "$TMP_RAW" "$TMP_PRS" "$TMP_ISSUES" "$TMP_ALIASES" "$TEMPLATE"
