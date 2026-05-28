---
name: make
description: Use Makefile to config and build the project
license: MIT
compatibility: opencode
metadata:
  audience: coders
---

## What I do

When a project uses a **Makefile** for building, I follow **safe and preferred build behavior** instead of blindly invoking destructive targets.

My goal is to build and iterate efficiently **without forcing unnecessary cleanups or redownloads**.

---

## ⚠️ CRITICAL: How to Run Make Commands

**NEVER do this:**
```bash
cd /path/to/project && make build 2>&1 | tail -10
make build && make test
make config && make build && make run
```

**ALWAYS do this - one make command per invocation, nothing else:**
```bash
make build
```

Then read the compilation log:
```bash
cat .complog
```

**Each `make` command MUST be run alone.** No `&&` chaining, no `cd` prefix, no pipes, no redirects. Just `make <target>` by itself.

The Makefile automatically writes all build output to `.complog`. Do NOT pipe, redirect, or tail the output - just run `make` and read `.complog` afterwards.

For errors/quickfix:
```bash
cat .quickfix
```

---

## Preferred Targets

- Prefer using:
  - `make config`
  - `make build`
  - `make test` - run all tests
  - `make test TEST=<name>` - run a specific test binary

- Avoid using:
  - `make clean`
  - `make reconfig`

**Running tests:**
```bash
make test                    # run all tests
make test TEST=test_parser   # run only test_parser binary
```

These targets are **more destructive** and may:
- remove build caches
- force redownloads
- significantly slow down iteration

If `make config` or `make build` fails:

1. Read `.complog` to analyze the failure
2. Retry using the least destructive target possible
3. Use `make clean` or `make reconfig` **only if necessary** and only after simpler options fail

I do not default to clean or reconfigure unless explicitly instructed.

---

## Rules

- I DO NOT RUN BARE "cmake", "gcc", "g++", "xmake", etc...
- I DO NOT pipe or redirect make output - I read `.complog` instead
- I DO NOT chain make commands with `&&` - one `make` per invocation
- I DO NOT prefix make with `cd` - I use the workdir parameter instead
- I assume the user wants **fast, incremental builds**
- I explain which Makefile target I am choosing and why
- I warn before running destructive targets
- I ask before forcing a full clean or reconfigure

---

## When to use me

Use this skill when:

- the Makefile defines both incremental and destructive targets
- clean or reconfig triggers heavy rebuilds or downloads
- you want cautious, developer-friendly build behavior
