---
name: performance-and-accessibility-review
description: Use this skill to analyze and optimize code performance while ensuring accessibility compliance.
---

# Body of the merged SKILL.md

## Skill: Performance and Accessibility Review

This skill combines performance analysis and accessibility review capabilities, enabling developers to identify performance bottlenecks and accessibility issues in their code.

### Performance Review

#### Core Performance Analysis

1. **Algorithm Complexity Analysis**
   - **Time Complexity**: Analyze how execution time grows with data size.
   - **Space Complexity**: Evaluate memory usage as data size changes.
   - **Big Data Processing**: Identify performance bottlenecks in large datasets.
   - **Algorithm Selection**: Recommend more efficient algorithms and data structures.

2. **Resource Usage Analysis**
   - **CPU Usage**: Check for CPU-intensive operations and optimization opportunities.
   - **Memory Usage**: Analyze memory allocation, usage, and release.
   - **I/O Operations**: Evaluate file read/write and network request efficiency.
   - **Cache Usage**: Check cache strategies and hit rates.

3. **Concurrency Performance**
   - **Thread Safety**: Check for safety in concurrent access.
   - **Lock Contention**: Analyze lock usage and contention.
   - **Asynchronous Processing**: Evaluate the effectiveness of asynchronous operations.
   - **Parallel Computing**: Identify opportunities for parallelization.

4. **Database Performance**
   - **Query Optimization**: Analyze SQL query execution plans.
   - **Index Usage**: Check the effectiveness of indexes.
   - **Connection Pooling**: Evaluate database connection management.
   - **N+1 Queries**: Identify and optimize related queries.

#### Performance Metrics

- **Response Time**: Classify response times into categories (e.g., Excellent: < 100ms).
- **Throughput**: Measure requests per second for APIs and data processing.
- **Resource Utilization**: Monitor CPU, memory, disk I/O, and network bandwidth usage.

#### Performance Optimization Strategies

- **Algorithm Optimization**: Choose appropriate data structures and reduce nested loops.
- **Memory Optimization**: Implement object pooling and memory mapping.
- **I/O Optimization**: Use batch operations and asynchronous I/O.
- **Concurrency Optimization**: Utilize parallel processing and read/write locks.

### Accessibility (A11y) Review

#### Accessibility Audit

- **Semantic Tags**: Ensure the use of semantic HTML elements (nav, main, aside).
- **ARIA Attributes**: Verify the correct use of ARIA attributes for enhanced accessibility.
- **Keyboard Accessibility**: Ensure all interactive elements are accessible via keyboard (tabindex, focus).
- **Image Alt Text**: Check that all images have appropriate alt text.

#### Common Commands

1. **Quick Audit**
   ```bash
   /ui-design audit <code_snippet>
   ```

2. **Contrast Check**
   ```bash
   /ui-design check-contrast <color_pair>
   ```

3. **Fix Suggestions**
   ```bash
   /ui-design fix <form_issue>
   ```

#### Self-Checklist for Accessibility

Before submitting code, check:
- [ ] Do all `<img>` elements have `alt` attributes?
- [ ] Do all form inputs have corresponding `<label>` elements?
- [ ] Are buttons clearly described (avoid using icons only)?
- [ ] Can the page be navigated using only the keyboard?
- [ ] Is the color contrast sufficient for readability?

By integrating performance analysis with accessibility reviews, developers can enhance both the efficiency and inclusivity of their applications.