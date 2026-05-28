---
name: qa-test-management
description: Use this skill when you need to manage QA testing tasks, including requesting tests, executing tests, and updating results.
---

# Skill body

## Purpose

This skill allows QA personnel to manage testing tasks effectively, including requesting tests, executing them, and updating results.

## Workflow

1. **Request a Test**
   - Use this when you need to request a QA test for a completed task card.
   - Ensure the task card includes QA test items.
   - Assign a QA personnel and send a Slack notification.

### Request Test Steps

```bash
# Step 1: Check if the task card has QA test items
gh issue view {issue_number} --repo {repo_name} --json body

# Step 2: Assign QA personnel
gh issue edit {issue_number} --repo {repo_name} --add-assignee {qa_person}

# Step 3: Send Slack notification
curl -X POST -H "Authorization: Bearer {slack_token}" -d '{"channel": "{channel_id}", "text": "QA test requested for issue {issue_number}"}' https://slack.com/api/chat.postMessage
```

2. **Execute Tests**
   - Use this when you need to run tests and analyze results.
   - Execute unit, integration, or all tests using Gradle.

### Execute Tests Steps

```bash
# Run unit tests
./gradlew test

# Run integration tests
./gradlew integrationTest

# Run all tests
./gradlew check
```

3. **Update Test Results**
   - Use this when you need to update the results of a test.
   - Mark tests as pass or fail and add comments.

### Update Test Results Steps

```bash
# Step 1: View the issue
gh issue view {issue_number} --repo {repo_name} --json body

# Step 2: Update the test result in the issue body
gh issue edit {issue_number} --repo {repo_name} --body "{updated_body}"

# Step 3: Add a comment with the test result
gh issue comment {issue_number} --repo {repo_name} --body "Test result: {result} - Comments: {comments}"

# Step 4: Change the label from testing to tested
gh issue edit {issue_number} --repo {repo_name} --remove-label testing --add-label tested
```

## Output Format

### Request Test Output

```markdown
[SEMO] Skill: request-test → Test request completed

✅ Test requested for issue: {issue_number}
📢 Notification sent to Slack channel: {channel_name}
```

### Execute Tests Output

```markdown
[SEMO] Skill: run-tests → Test execution completed

✅ Total tests: {total_tests}
✅ Passed: {passed_tests}
❌ Failed: {failed_tests}
```

### Update Test Results Output

```markdown
[SEMO] Skill: qa-test → Test results updated

✅ Test completed: {issue_number}
📋 Result: {result}
💬 Comments: {comments}
```