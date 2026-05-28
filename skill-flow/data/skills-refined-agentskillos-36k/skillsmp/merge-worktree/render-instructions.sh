#!/usr/bin/env bash
set -euo pipefail

git_worktree_path=$(realpath "${1:-.}")
cd "${git_worktree_path}"

git_root() {
  git -C "${git_worktree_path}" worktree list --porcelain | awk 'NR==1{print $2; exit}'
}

current_branch() {
  git -C "${git_worktree_path}" rev-parse --abbrev-ref HEAD
}

current_sha() {
  git -C "${git_worktree_path}" rev-parse HEAD
}

clean_or_dirty() {
  if [[ -n "$(git -C "${git_worktree_path}" status --porcelain=v1)" ]]; then
    echo "dirty"
  else
    echo "clean"
  fi
}

default_branch() {
  git -C "${git_worktree_path}" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main"
}

git_root_val=$(git_root)
current_branch_val=$(current_branch)
current_sha_val=$(current_sha)
worktree_status_val=$(clean_or_dirty)
default_branch_val=$(default_branch)
default_branch_line_val="origin/${default_branch_val}"
repo_status_val=$(clean_or_dirty)
worktree_diff_summary_val=$(git -C "${git_worktree_path}" --no-pager diff --stat || true)

instruction_template=$(cat <<INSTR
[developer] Finish the merge manually with the steps below.

Context:
- Worktree path: ${git_worktree_path} — branch ${current_branch_val} @ ${current_sha_val}, status ${worktree_status_val}
- Repo root path: ${git_root_val} — target ${default_branch_line_val} checkout, status ${repo_status_val}

NOTE: Each command runs in its own shell. \`/merge\` switches the working directory to the repo root; use \`git -C <path> ...\` or \`cd <path> && ...\` whenever you need to operate in a different directory.

1. Worktree prep (worktree ${git_worktree_path} on ${current_branch_val}):
   - cd into ${git_worktree_path}
   - Review \`git status\`.
   - Stage and commit every change (including new files). Use descriptive messages; no network commands and no resets.
   - If unsure, clarify with user to make sure all the required changes is commited.
   - Run worktree commands as \`git -C ${git_worktree_path}\` (or \`cd ${git_worktree_path} && ...\`) so they execute inside the worktree.
2. Default-branch checkout prep (repo root ${git_root_val}):
   - If HEAD is not ${default_branch_val}, run \`git checkout ${default_branch_val}\`.
   - If this checkout is dirty, stash with a clear message before continuing.
3. Squash merge locally (repo root ${git_root_val} on ${default_branch_val}):
   - Run \`git merge --squash ${current_branch_val}\`.
   - Resolve conflicts line by line; keep intent from both branches.
   - Look at \`git diff\` to decide what to name the squash commit.
   - Run \`git commit -m "<appropriate commit message>"\` once staged changes look correct.
   - No network commands, no \`git reset --hard\`, no \`git checkout -- .\`, no \`git clean\`, and no \`-X ours/theirs\`.
   - WARNING: Do not delete files, rewrite them in full, or checkout/prefer commits from one branch over another. Instead use apply_patch to surgically resolve conflicts, even if they are large in scale. Work on each conflict, line by line, so both branches' changes survive.
   - If you stashed in step 2, apply/pop it now and commit if needed.
4. Verify in ${git_root_val}:
   - \`git status\` is clean.
   - No MERGE_HEAD/rebase/cherry-pick artifacts remain.
5. Cleanup:
   - \`git worktree remove ${git_worktree_path}\` (only after verification).
   - \`git branch -D ${current_branch_val}\` in ${git_root_val} if the branch still exists.
6. Report back with a concise command log and any conflicts you resolved.
7. cd back into ${git_root_val}

Absolute rules: no network operations, no resets, no dropping local history, no blanket "ours/theirs" strategies.

Worktree diff summary:
${worktree_diff_summary_val}
INSTR
)
printf '%s\n' "${instruction_template}"
