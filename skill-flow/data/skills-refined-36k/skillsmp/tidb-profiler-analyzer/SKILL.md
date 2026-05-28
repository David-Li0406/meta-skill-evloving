---
name: tidb-profiler-analyzer
description: Processes and analyzes TiDB profiler zip packages (CPU or heap) for components like TiDB, TiKV, PD, or TiFlash. It unzips, aggregates the profiler data, and uses `go tool pprof` to report on the most time-consuming functions (CPU) or highest memory allocations (heap).
---

# TiDB Profiler Analyzer Skill

Your primary goal is to organize and analyze profiler data from various TiDB component (`tidb`, `pd`, `tikv`, `tiflash`) `.zip` archives.
Follow these steps meticulously:

1.  **Unzip all the zip files**: Locate and extract the contents of all `.zip` files present in the current working directory. Each zip file should be unzipped into a separate, appropriately named directory.
2.  **Create 'profiler_data' directory**: Create a new directory named `'profiler_data'` at the root of the current working directory. This directory will house all collected profiler files.
3.  **Move profiler files**: Recursively search through all the directories created in step 1. Identify and move *all* files found within these unzipped directories to the newly created `'profiler_data'` directory.
4.  **Analyze Profiler Data**:
    a.  Identify the type of profiler data in the `'profiler_data'` directory (CPU or Heap). You can often infer this from filenames (e.g., containing "cpu" vs "heap"). If unsure, you may need to ask the user.
    b.  Use the `go tool pprof` to analyze the collected data.
        *   **For CPU profiles**: Run `go tool pprof -top <path_to_profiler_file>` to find the most time-consuming functions.
        *   **For Heap profiles**: Run `go tool pprof -top --alloc_space <path_to_profiler_file>` to find the functions with the most memory allocations.
    c.  Present a summary of the analysis results to the user.
5.  **Confirmation and Cleanup**: After the analysis is complete, you must prompt the user for confirmation before proceeding with cleanup. If the user approves, delete the original `.zip` files and the now empty unzipped directories to tidy up the workspace.
