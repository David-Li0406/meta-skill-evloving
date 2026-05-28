#!/bin/bash

set -euo pipefail

echo_err() {
  echo "$@" >&2
}

# parse arguments for --rule-file and outline
repo="" # `gh repo view --json nameWithOwner -q '.nameWithOwner'` で確認可能
pr_num=""
target_branch=""
base_branch="main"
while [[ $# -gt 0 ]]; do
  case $1 in
    --repo)
      repo="$2"
      shift 2
      ;;
    --pr)
      pr_num="$2"
      shift 2
      ;;
    --branch)
      if [[ -z "$2" ]] || [[ "$2" =~ ^-+ ]]
      then
        echo_err "❌: $1 option is required"
        return
      fi
      target_branch="$2"
      shift 2
      ;;
    --base)
      base_branch="$2"
      shift 2
      ;;
    -*)
      echo_err "❌ illegal option '${1}'"
      return
      ;;
    *)
      break
      ;;
  esac
done

# Validate variables
# 以下の条件のいずれかを満たすこと
#  成功条件1: $target_branch と $base_branch 両方が空文字ではない
#  成功条件2: $repo と $pr_num 両方が空文字でない
if [[ -n "${repo}" && -n "${pr_num}" ]]
then
  echo_err "ℹ️ Mode is PR: ${repo}#${pr_num}"
elif [[ -n "${target_branch}" && -n "${base_branch}" ]]
then
  echo_err "ℹ️ Mode is compare branches: ${target_branch}..${base_branch}"
else
  echo_err "❌ Either both --branch and --base or both --repo and --pr must be specified."
  return 1
fi


# Output diff patches
if [[ -n "${repo}" && -n "${pr_num}" ]]; then
  # pull request diff
  gh pr diff "${pr_num}" --repo "${repo}"
else
  # local branches diff
  # git fetch --all
  git diff \
    --unified=3 \
    --diff-algorithm=patience \
    --find-renames \
    -M50% \
    --find-copies \
    -C \
    --no-color \
    "${target_branch}..${base_branch}"
fi
