# flywheel-web

Web E2E testing and browser automation loop with agent-browser CLI.

## philosophy

> "test the user's journey, not the implementation"

agent-browser provides AI-native browser automation. use it for E2E tests, visual regression, user flow validation, and web scraping.

## prerequisites

| requirement | check |
|-------------|-------|
| agent-browser | `agent-browser --version` |
| chromium | `agent-browser install` |

## core commands

| command | purpose |
|---------|---------|
| `open <url>` | navigate to URL |
| `snapshot -i -c` | AI-optimized accessibility tree |
| `click @eN` | click element by ref |
| `fill @eN "text"` | fill input by ref |
| `find role X click` | semantic interaction |
| `screenshot` | capture state |
| `wait` | wait for element/condition |

## flywheel sequence

### 1. discover

```bash
# list existing tests
fd -e spec.ts -e test.ts . tests/e2e

# check test config
cat playwright.config.ts | head -30
```

### 2. run tests

```bash
# all tests
npx playwright test

# specific test
npx playwright test tests/e2e/auth.spec.ts

# headed mode (for debugging)
npx playwright test --headed
```

### 3. debug via agent-browser

when test fails, use agent-browser to reproduce:

```bash
# 1. navigate to failing page
agent-browser open https://app.example.com/failing-route

# 2. get AI-optimized snapshot
agent-browser snapshot -i -c

# 3. screenshot current state
agent-browser screenshot failure.png

# 4. interact to reproduce
agent-browser find role button click --name "Submit"
agent-browser wait --text "Error"
```

### 4. analyze failures

```bash
# snapshot gives refs like @e1, @e2
agent-browser snapshot -i -c

# check specific element state
agent-browser is visible @e5
agent-browser get text @e5

# get page context
agent-browser get title
agent-browser get url
```

### 5. fix & repeat

on failure:
1. identify failing selector/action
2. check element exists via `snapshot -i -c`
3. use semantic find instead of CSS selectors
4. update test or fix code
5. rerun specific test

## agent-browser patterns

### login flow

```bash
agent-browser open https://app.example.com/login
agent-browser snapshot -i -c
agent-browser find label "Email" fill "test@example.com"
agent-browser find label "Password" fill "secret"
agent-browser find role button click --name "Sign in"
agent-browser wait --url "**/dashboard"
agent-browser state save ~/.agent-browser/auth-state.json
```

### form validation

```bash
agent-browser open https://app.example.com/form
agent-browser snapshot -i -c
agent-browser find label "Name" fill ""
agent-browser find role button click --name "Submit"
agent-browser wait --text "required"
agent-browser snapshot -i -c  # check error state
```

### waiting strategies

```bash
# wait for element
agent-browser wait "#dashboard"

# wait for text
agent-browser wait --text "Welcome back"

# wait for URL
agent-browser wait --url "**/success"

# wait for network idle
agent-browser wait --load networkidle

# wait for JS condition
agent-browser wait --fn "window.appReady === true"
```

### parallel sessions

```bash
# session 1: user A
agent-browser --session userA open https://app.example.com
agent-browser --session userA find label "Email" fill "a@test.com"

# session 2: user B (concurrent)
agent-browser --session userB open https://app.example.com
agent-browser --session userB find label "Email" fill "b@test.com"

# list active
agent-browser session list
```

## AI agent loop

standard pattern for browser automation in loop:

```
1. agent-browser open <url>
2. agent-browser snapshot -i -c → parse refs
3. reason about next action based on refs
4. execute: click @eN, fill @eN "text", find role X click
5. agent-browser wait --text "expected" or wait <selector>
6. repeat 2-5 until goal achieved
7. agent-browser close
```

## copilot integration

use copilot for failure analysis:

```bash
SNAPSHOT=$(agent-browser snapshot -i -c)
SCREENSHOT_PATH=$(agent-browser screenshot /tmp/failure.png && echo "/tmp/failure.png")

copilot -p --model gemini-3-pro "
Browser test failure analysis.

URL: $(agent-browser get url)
Snapshot: $SNAPSHOT

Task: Diagnose why the expected element is not found.

Output JSON:
{
  \"diagnosis\": \"why it failed\",
  \"fix_type\": \"test_update | code_fix | selector_change\",
  \"fix\": \"specific change\",
  \"confidence\": 0-10
}
"
```

## common issues

| symptom | likely cause | fix |
|---------|--------------|-----|
| element not found | timing issue | `wait <selector>` before interaction |
| ref not in snapshot | element not interactive | use `-d 5` for deeper tree |
| flaky test | race condition | use `wait --load networkidle` |
| wrong element clicked | ambiguous selector | use `find role X --name "specific"` |

## projects

| project | path | test dir |
|---------|------|----------|
| arbor | ~/Developer/arbor/arbor-xyz | tests/e2e |
| webs | ~/Developer/webs/webs-xyz | tests/e2e |
| hostagent web | ~/Developer/zo/hostagent/ts-packages/web | tests |

## visual-verify integration

on test failure, capture and analyze visuals:

```bash
# capture failure state
agent-browser screenshot /tmp/failure.png --full
SNAPSHOT=$(agent-browser snapshot -i -c)

# analyze with copilot
ANALYSIS=$(copilot -p --model gemini-3-pro --output-format json "
Visual verification for failed test.

Test: $TEST_NAME
Error: $ERROR_MESSAGE
Snapshot: $SNAPSHOT

Analyze and identify:
1. Visual issues (layout, missing elements, incorrect state)
2. Potential root cause
3. Suggested fix

Output JSON:
{
  \"visual_issues\": [],
  \"root_cause\": \"string\",
  \"suggested_fix\": \"string\",
  \"confidence\": 0-10
}
")
```

### Linear integration

```bash
# upload screenshot and add to Linear issue
if [ -n "$LINEAR_ISSUE" ] && [ -f "/tmp/failure.png" ]; then
  SCREENSHOT_URL=$(gh gist create "/tmp/failure.png" --public | tail -1)

  linear comment create -i "$LINEAR_ISSUE" -b "
## Visual Verification Failed

**Test**: $TEST_NAME
**Error**: $ERROR_MESSAGE

![Screenshot]($SCREENSHOT_URL)

### Analysis
$ANALYSIS
"
fi
```

## loop integration

in loop phase 4 (execute flywheel), on test failure:

```yaml
on_test_failure:
  - capture: agent-browser screenshot + snapshot
  - analyze: copilot gemini-3-pro
  - if: analysis.confidence >= 7
    then:
      - apply_fix()
      - rerun_test()
    else:
      - attach_to_linear()
      - escalate_hil()
```

## anti-patterns

| pattern | problem | fix |
|---------|---------|-----|
| hardcoded waits | flaky, slow | use `wait <selector>` or `wait --text` |
| CSS selectors only | brittle | prefer `find role/label/text` |
| ignoring snapshot | blind interactions | always snapshot before acting |
| no session isolation | state pollution | use `--session` for parallel work |
| skipping networkidle | premature interaction | `wait --load networkidle` for SPAs |
