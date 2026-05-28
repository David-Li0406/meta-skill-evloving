#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: fetch.sh <url>" >&2
  exit 2
fi

url="$1"
cache_dir=".llms-cache"
mkdir -p "$cache_dir"

slug="$(python3 - "$url" <<'PY'
import hashlib,sys
url=sys.argv[1]
print(hashlib.sha256(url.encode("utf-8")).hexdigest()[:16])
PY
)"

out="$cache_dir/$slug.txt"

ttl_seconds=$((7 * 24 * 60 * 60))
lower_url="$(printf '%s' "$url" | tr '[:upper:]' '[:lower:]')"
skip_ttl=0
if [[ "$lower_url" == *"release-note"* || "$lower_url" == *"release-notes"* || "$lower_url" == *"releasenote"* ]]; then
  skip_ttl=1
fi

if [[ -s "$out" ]]; then
  if [[ "$skip_ttl" -eq 1 ]]; then
    echo "$out"
    exit 0
  fi
  is_fresh="$(python3 - "$out" "$ttl_seconds" <<'PY'
import os,sys,time
path=sys.argv[1]
ttl=int(sys.argv[2])
mtime=os.path.getmtime(path)
age=time.time()-mtime
print("1" if age <= ttl else "0")
PY
)"
  if [[ "$is_fresh" == "1" ]]; then
    echo "$out"
    exit 0
  fi
  echo "$out"
  rm -f "$out"
fi

curl -fsSL --max-time 60 "$url" -o "$out"
echo "$out"
