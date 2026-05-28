---
name: environment-setup
description: Use this skill when you need to initialize a project-specific environment after checking out a repository.
---

# Environment Setup (Vive)

## Goal
リポジトリをチェックアウトした後に必要な **プロジェクト環境の初期化** を行う。
ワークツリーの有無は問わない。

## Inputs
- リポジトリのルートパス

## Procedure (must follow in order)

1) Check Rust Toolchain
   - Run: `cd <repo-root> && cargo check`
   - This ensures dependencies are fetched and the environment is ready for compiling.

2) Output next steps
   - Print:
     - Repo path
     - Command to start session: `cd <repo-root> && claude`

## Safety constraints
- Do not remove worktrees unless explicitly asked.
- Keep changes scoped to the requested repo.