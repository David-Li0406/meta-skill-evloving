# Performance Analysis Procedure

> **Version**: 1.1.0
> **Extracted from**: workflow.md
> **Purpose**: Systematic approach for analyzing performance in unfamiliar codebases

## 1. Establish Analysis Constraints

- **Document assumptions**: List all assumptions about the system's behavior
- **Identify constraints**: Note environmental limitations (network access, execution capabilities, required dependencies)
- **Define scope**: Clarify what "performance analysis" means in this context (throughput, latency, resource usage, etc.)
- **List unknowns**: Explicitly state what information is missing or unclear

## 2. Gather Required Information

Before diving into code, determine:

- **Build system**: How to compile/build the project (CMake, Make, scripts, etc.)
- **Documentation**: Existence of performance-related docs, benchmarks, or profiling guides
- **Test infrastructure**: Available test data, workloads, or benchmark suites
- **Execution requirements**: Dependencies, runtime environment, configuration needs

## 3. Progressive Exploration Strategy

Follow this step-by-step approach:

### 3.1 Repository Structure Survey
- Map directory organization and key source files
- Locate build scripts, documentation, test files
- Identify main entry points and core components

### 3.2 Code Flow and Component Analysis
- Trace thread management and lifecycle
- Examine queue/synchronization mechanisms
- Identify potential bottleneck points
- Review resource allocation patterns

### 3.3 Performance Measurement Point Identification
- Determine what metrics are currently collected
- Assess existing logging/monitoring support
- Identify where new instrumentation could be added
- Note any existing profiling or benchmark code

### 3.4 Execution and Testing Verification
- Check for runnable scripts or test suites
- Execute available benchmarks (with user approval if needed)
- Collect and analyze output/logs
- Document any issues preventing execution

### 3.5 Comprehensive Analysis Synthesis
- Summarize potential performance indicators
- Highlight expected bottlenecks and optimization opportunities
- Propose measurement strategies for missing metrics
- Recommend next steps for performance improvement

## 4. Present Analysis Plan

Before executing the analysis:

- **Share the planned approach**: Present the exploration strategy to the user
- **Confirm priorities**: Ask if certain aspects should be prioritized or skipped
- **Get approval for execution**: Request permission before running code or tests
- **Adjust based on feedback**: Modify the plan according to user input

## 5. Report Findings

When presenting results:

- **Start with executive summary**: High-level findings and key takeaways
- **Detail methodology**: Explain what was analyzed and how
- **Present data**: Share metrics, measurements, or observations
- **Acknowledge limitations**: Be clear about what couldn't be measured or verified
- **Recommend actions**: Suggest concrete next steps for performance optimization

---
*Part of the workflow guidelines module*
