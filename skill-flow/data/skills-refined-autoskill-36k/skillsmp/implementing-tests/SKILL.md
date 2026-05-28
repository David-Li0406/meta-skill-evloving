---
name: implementing-tests
description: You are an expert implementer of unit and integration tests.
---

# Implementing Tests Skill

This skill guides the process to implementing unit and integration tests.

## Implementing Tests Notes

- Ensure you understand the code area which requires additional unit tests and coverage.
- Determine if the code to be tested is more suited to unit testing or integration testing.
- Implement any missing unit and / or integration tests for the code area to be tested.
- Iterate using new output from `./utils/get-file-coverage.sh <file-path>` until coverage for the area to be tested has reached 100%.
- The task cannot be completed if there are failing tests.
- If coverage was already at 100% then close the issue without raising a PR.
- If the area to be tested is too complex or too large then create GitHub sub-issues beneath this issue for each of the areas which were not able to be covered.
- If coverage has been increased then create a PR so that the changes can be reviewed.
