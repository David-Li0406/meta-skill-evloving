---
name: testing-sync-skills
description: Use this skill when you need to test the functionality of sync-skills in a clean environment to avoid conflicts.
---

# Skill body

1. **Setup Test Environment**:
   - Create a subdirectory for your tests, e.g., `mkdir test-dir`.
   - Navigate into the test directory: `cd test-dir`.

2. **Run Integration Tests**:
   - Execute your integration tests within this subdirectory to ensure they run in isolation from other tests or files.

3. **Verify Results**:
   - Check the output of your tests to confirm that the sync-skills functionality is working as expected.

4. **Cleanup**:
   - After testing, you may remove the test directory if no longer needed: `cd .. && rm -rf test-dir`.