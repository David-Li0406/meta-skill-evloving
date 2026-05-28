#!/usr/bin/env bash
set -euo pipefail

if ! command -v dotnet >/dev/null 2>&1; then
  echo "dotnet is required but not found." >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required but not found." >&2
  exit 1
fi

out_dir="artifacts/codex"
mkdir -p "$out_dir"

summary_path="$out_dir/build-summary.txt"

solutions=""
if command -v rg >/dev/null 2>&1; then
  solutions=$(rg --files -g "*.sln" -g "*.slnx")
else
  solutions=$(find . -type f \( -name "*.sln" -o -name "*.slnx" \) | sed 's|^\./||')
fi

if [ -z "$solutions" ]; then
  echo "No .sln or .slnx files found." >&2
  exit 1
fi

primary_sln=$(printf '%s\n' "$solutions" | python3 -c 'import sys
lines = [line.strip() for line in sys.stdin if line.strip()]
root = [line for line in lines if "/" not in line]
print(sorted(root)[0] if root else sorted(lines, key=len)[0])
')

{
  echo "# Build Diagnostics Summary"
  echo ""
  echo "Solution: \"$primary_sln\""
  echo ""
  echo "## dotnet --info"
  echo ""
  dotnet --info
  echo ""
  echo "## dotnet restore"
  echo ""
  dotnet restore "$primary_sln"
  echo ""
  echo "## dotnet build"
  echo ""
} | tee "$summary_path"

set +e

dotnet build "$primary_sln" \
  /m \
  /bl:"$out_dir/build.binlog" \
  /p:ContinuousIntegrationBuild=true \
  /p:Deterministic=true \
  /p:TreatWarningsAsErrors=true \
  /p:WarningsAsErrors= \
  /p:RunAnalyzers=true \
  /p:AnalysisMode=All \
  /p:RestoreLockedMode=true \
  /p:UseSharedCompilation=false \
  /p:BuildInParallel=true \
  /p:GenerateDocumentationFile=true \
  /p:DebugType=portable \
  /p:DebugSymbols=true \
  2>&1 | tee -a "$summary_path"

build_exit=${PIPESTATUS[0]}

if [ $build_exit -ne 0 ]; then
  echo "" | tee -a "$summary_path"
  echo "Build failed with exit code $build_exit" | tee -a "$summary_path"
else
  echo "" | tee -a "$summary_path"
  echo "Build succeeded" | tee -a "$summary_path"
fi

exit $build_exit
