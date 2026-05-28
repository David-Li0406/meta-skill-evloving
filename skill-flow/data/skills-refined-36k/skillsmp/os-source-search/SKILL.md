---
name: os-source-search
description: Search reference OS source code online (Linux, xv6, seL4, MINIX3, Fuchsia/Zircon, FreeBSD). Use when looking up implementation patterns, understanding how production or teaching OSes handle specific features, or finding reference code for scheduler, memory management, IPC, drivers, syscalls.
allowed-tools: WebFetch, WebSearch
---

# OS Source Search Skill

Search reference operating system source code using online code browsers and
repositories. Covers both monolithic kernels and microkernels (including
userspace servers).

## When to Use

- **Implementation reference**: See how production kernels implement features
- **Learning**: Understand OS concepts through real code examples
- **API patterns**: Find syscall implementations, driver interfaces
- **Algorithm details**: Scheduler policies, memory allocators, lock implementations
- **Code structure**: How kernels organize subsystems, headers, Makefiles

## Online Resources

**Linux Kernel:**

- **Bootlin Elixir**: `https://elixir.bootlin.com/linux/latest/source` — Best for browsing and cross-references
- **GitHub mirror**: `https://github.com/torvalds/linux`

**xv6 (MIT teaching OS):**

- **xv6-riscv**: `https://github.com/mit-pdos/xv6-riscv` — RISC-V version

**seL4 (verified microkernel):**

- **GitHub**: `https://github.com/seL4/seL4`

**MINIX3:**

- **GitHub**: `https://github.com/Stichting-MINIX-Research-Foundation/minix`

**Fuchsia/Zircon (Google microkernel):**

- **Fuchsia source**: `https://fuchsia.googlesource.com/fuchsia`
- **Zircon kernel**: `https://fuchsia.googlesource.com/fuchsia/+/refs/heads/main/zircon/kernel/`
- **Docs**: `https://fuchsia.dev/fuchsia-src/concepts/kernel`

**FreeBSD:**

- **CGit**: `https://cgit.freebsd.org/src/tree/sys` — Official source browser
- **GitHub mirror**: `https://github.com/freebsd/freebsd-src`

## Search Patterns

### Using WebFetch for specific files

```text
# Linux
WebFetch: https://raw.githubusercontent.com/torvalds/linux/master/kernel/sched/core.c

# xv6
WebFetch: https://raw.githubusercontent.com/mit-pdos/xv6-riscv/riscv/kernel/proc.c

# seL4
WebFetch: https://raw.githubusercontent.com/seL4/seL4/master/src/syscall.c

# MINIX3
WebFetch: https://raw.githubusercontent.com/Stichting-MINIX-Research-Foundation/minix/master/minix/kernel/proc.c

# Fuchsia/Zircon (googlesource needs ?format=TEXT)
WebFetch: https://fuchsia.googlesource.com/fuchsia/+/refs/heads/main/zircon/kernel/kernel/scheduler.cc?format=TEXT

# FreeBSD
WebFetch: https://raw.githubusercontent.com/freebsd/freebsd-src/main/sys/kern/sched_ule.c
```

### Using WebSearch for discovery

```text
# Linux
WebSearch: "linux kernel site:elixir.bootlin.com <feature>"

# xv6
WebSearch: "xv6 site:github.com <feature>"

# seL4
WebSearch: "seL4 site:github.com <feature>"

# MINIX3
WebSearch: "minix site:github.com <feature>"

# Fuchsia/Zircon
WebSearch: "zircon site:fuchsia.googlesource.com <feature>"

# FreeBSD
WebSearch: "freebsd site:cgit.freebsd.org <feature>"
```
