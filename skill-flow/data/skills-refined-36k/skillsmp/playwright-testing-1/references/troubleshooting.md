# Troubleshooting Guide

Common issues and solutions when working with Playwright BDD tests.

## Step Not Found Errors

### Symptom
```
Error: Step definition not found: "I login with valid credentials"
```

### Solutions

1. **Verify step text matches exactly**
   ```typescript
   // Gherkin
   When I login with valid credentials
   
   // Step definition - must match exactly
   When('I login with valid credentials', async () => { ... });
   ```

2. **Check step is exported from fixtures.ts**
   ```typescript
   // fixtures.ts must export Given, When, Then
   export const { Given, When, Then } = createBdd(test);
   ```

3. **Ensure step file is in config**
   ```typescript
   // playwright.config.ts
   const testDir = defineBddConfig({
     steps: [
       'steps/fixtures.ts',
       'steps/**/*.steps.ts',  // Must include your steps file
     ],
   });
   ```

4. **Regenerate tests**
   ```bash
   npx bddgen
   ```

## Element Not Found

### Symptom
```
Error: locator.click: Error: Timeout 30000ms exceeded
```

### Solutions

1. **Wait for element visibility**
   ```typescript
   await element.waitFor({ state: 'visible' });
   await element.click();
   ```

2. **Check locator strategy**
   ```typescript
   // Prefer semantic locators
   page.getByRole('button', { name: 'Submit' })
   
   // Over CSS selectors
   page.locator('.btn-submit')
   ```

3. **Verify element is in viewport**
   ```typescript
   await element.scrollIntoViewIfNeeded();
   await element.click();
   ```

## Timeout Errors

### Symptom
```
Error: Test timeout of 30000ms exceeded
```

### Solutions

1. **Increase test timeout**
   ```typescript
   test.setTimeout(60000);  // 60 seconds
   ```

2. **Add action timeout to config**
   ```typescript
   // playwright.config.ts
   use: {
     actionTimeout: 10000,
   }
   ```

3. **Check for slow network**
   - Use `waitForLoadState('networkidle')` sparingly
   - Prefer waiting for specific elements

## Flaky Tests

### Solutions

1. **Use explicit waits**
   ```typescript
   // Wait for element state
   await expect(element).toBeVisible();
   await element.click();
   ```

2. **Wait for navigation**
   ```typescript
   await Promise.all([
     page.waitForURL('**/dashboard'),
     loginButton.click(),
   ]);
   ```

3. **Configure retries**
   ```typescript
   // playwright.config.ts
   retries: process.env.CI ? 2 : 0,
   ```

## Assertion Failures

### Wrong place for assertions
```typescript
// ❌ WRONG: Assertion in POM
class LoginPage {
  async verifyError() {
    await expect(this.errorAlert).toBeVisible();
  }
}

// ✅ CORRECT: Assertion in step definition
Then('I should see a login error', async ({ loginPage }) => {
  await expect(loginPage.errorAlert).toBeVisible();
});
```

## BDD Decorator Errors

### Symptom
Using decorators in POMs causes issues.

### Solution
Keep POMs pure - no decorators:

```typescript
// ❌ WRONG
class LoginPage {
  @Given('I am on login page')
  async goto() { }
}

// ✅ CORRECT
class LoginPage {
  async goto() {
    await this.page.goto('/login');
  }
}
```

## Configuration Issues

### Duplicate step definitions
Ensure each step is defined only once. Check:
- `fixtures.ts` for shared steps
- Feature-specific `*.steps.ts` files
- No overlapping patterns

### Features not found
```typescript
// playwright.config.ts
const testDir = defineBddConfig({
  features: 'features/**/*.feature',  // Check path
  steps: ['steps/**/*.ts'],
});
```
