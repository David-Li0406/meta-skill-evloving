# Browser Automation - Validations

## Using waitForTimeout

### **Id**
arbitrary-timeout
### **Severity**
error
### **Description**
waitForTimeout causes flaky tests and slow execution
### **Pattern**
  waitForTimeout\(|page\.waitForTimeout
  
### **Message**
Using waitForTimeout - remove it. Playwright auto-waits for elements. Use waitForResponse, waitForURL, or assertions instead.
### **Autofix**


## Using setTimeout in Test Code

### **Id**
set-timeout-in-test
### **Severity**
warning
### **Description**
setTimeout is unreliable for timing in tests
### **Pattern**
  setTimeout\([^,]+,\s*\d+\)
  
### **Message**
Using setTimeout instead of Playwright waits. Replace with await expect(...).toBeVisible() or page.waitFor*.
### **Autofix**


## Custom Sleep Function

### **Id**
sleep-function
### **Severity**
warning
### **Description**
Sleep functions indicate improper waiting strategy
### **Pattern**
  const\s+sleep|function\s+sleep|async.*sleep.*=>.*Promise
  
### **Message**
Custom sleep function detected. Use Playwright's built-in waiting mechanisms instead.
### **Autofix**


## CSS Class Selector Used

### **Id**
css-class-selector
### **Severity**
warning
### **Description**
CSS class selectors are fragile
### **Pattern**
  locator\(['"]\.[\w-]+['"]\)|page\.\$\(['"]\.[\w-]+['"]\)
  
### **Message**
Using CSS class selector. Prefer getByRole, getByText, getByLabel, or getByTestId for more stable selectors.
### **Autofix**


## nth-child CSS Selector

### **Id**
nth-child-selector
### **Severity**
warning
### **Description**
Position-based selectors are very fragile
### **Pattern**
  nth-child\(|:nth-of-type\(|:first-child|:last-child
  
### **Message**
Using position-based selector. These break when DOM order changes. Use user-facing locators instead.
### **Autofix**


## XPath Selector Used

### **Id**
xpath-selector
### **Severity**
info
### **Description**
XPath should be last resort
### **Pattern**
  locator\(['"]/|page\.locator\(['"]/|xpath=
  
### **Message**
Using XPath selector. Consider getByRole, getByText first. XPath should be last resort for complex DOM traversal.
### **Autofix**


## Auto-Generated Selector

### **Id**
auto-generated-selector
### **Severity**
warning
### **Description**
Framework-generated selectors are extremely fragile
### **Pattern**
  data-v-[\da-f]+|data-reactid|__next|_ngcontent|ng-reflect
  
### **Message**
Using auto-generated selector. These change on every build. Use data-testid instead.
### **Autofix**


## Puppeteer Without Stealth Plugin

### **Id**
no-stealth-plugin
### **Severity**
info
### **Description**
Scraping without stealth is easily detected
### **Pattern**
  require\(['"]puppeteer['"]\)|from\s+['"]puppeteer['"]
  
### **Anti Pattern**
  puppeteer-extra|StealthPlugin|stealth
  
### **Message**
Using Puppeteer without stealth plugin. Consider puppeteer-extra-plugin-stealth for anti-detection.
### **Autofix**


## navigator.webdriver Not Hidden

### **Id**
webdriver-exposed
### **Severity**
info
### **Description**
navigator.webdriver exposes automation
### **Pattern**
  chromium\.launch|puppeteer\.launch
  
### **Anti Pattern**
  AutomationControlled|webdriver.*undefined|stealth
  
### **Message**
Launching browser without hiding automation flags. For scraping, add stealth measures.
### **Autofix**


## Scraping Loop Without Error Handling

### **Id**
no-try-catch-in-loop
### **Severity**
warning
### **Description**
One failure shouldn't crash entire scrape
### **Pattern**
  for.*await.*goto\(|for.*await.*page\.|forEach.*await.*goto
  
### **Anti Pattern**
  try|catch
  
### **Message**
Scraping loop without try/catch. One page failure will crash the entire scrape. Add error handling.
### **Autofix**


## Error Handler Without Screenshot

### **Id**
no-screenshot-on-error
### **Severity**
info
### **Description**
Screenshots are essential for debugging failures
### **Pattern**
  catch.*\{[^}]*throw|catch.*\{[^}]*console\.error
  
### **Anti Pattern**
  screenshot
  
### **Message**
Error handler without screenshot capture. Add page.screenshot() for debugging.
### **Autofix**


## Shared Page Variable Across Tests

### **Id**
shared-page-variable
### **Severity**
warning
### **Description**
Shared page causes test pollution
### **Pattern**
  let\s+page\s*:\s*Page|let\s+page\s*=|var\s+page\s*=
  
### **Message**
Global page variable detected. Each test should get fresh page from context for isolation.
### **Autofix**


## Login in beforeAll Hook

### **Id**
beforeall-login
### **Severity**
warning
### **Description**
Shared authentication state can cause issues
### **Pattern**
  beforeAll.*login|beforeAll.*signIn|beforeAll.*authenticate
  
### **Message**
Login in beforeAll shares auth state. Use storageState for auth instead.
### **Autofix**


## Browser Not Closed

### **Id**
browser-not-closed
### **Severity**
warning
### **Description**
Unclosed browsers leak resources
### **Pattern**
  await.*browser\.launch\(|await.*chromium\.launch\(
  
### **Anti Pattern**
  browser\.close\(\)|finally.*close
  
### **Message**
Browser launched but may not be closed. Add browser.close() in finally block.
### **Autofix**


## Context Not Closed in Loop

### **Id**
context-not-closed
### **Severity**
warning
### **Description**
Unclosed contexts leak memory
### **Pattern**
  for.*newContext\(|map.*newContext\(
  
### **Anti Pattern**
  context\.close\(\)|finally.*close
  
### **Message**
Context created in loop but may not be closed. Add context.close() in finally block.
### **Autofix**


## No Delay Between Requests

### **Id**
no-delay-between-requests
### **Severity**
info
### **Description**
Rapid requests may cause rate limiting
### **Pattern**
  for.*await.*goto\([^)]*\)|Promise\.all.*goto
  
### **Anti Pattern**
  setTimeout|delay|sleep|randomDelay|wait
  
### **Message**
Multiple requests without delay. Consider adding delays to avoid rate limiting.
### **Autofix**
