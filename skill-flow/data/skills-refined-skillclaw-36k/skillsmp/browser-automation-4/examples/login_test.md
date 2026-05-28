# Login Test Example

## Use Case
Testing authentication flow and verifying successful login.

## Task Setup

```
TaskName: "Testing Login Flow"

Task: Navigate to https://app.example.com/login and perform the following:
1. Wait for the login form to be fully loaded
2. Enter "demo@example.com" in the email input field
3. Enter "password123" in the password field
4. Click the "Sign In" button
5. Wait for navigation to complete
6. Verify that you've reached the dashboard by checking for a welcome message
7. Return: 
   - Status: "Success" or "Failed"
   - Dashboard URL if successful
   - Error message if login failed
   - Screenshot of the final page

RecordingName: login_flow_test
```

## Expected Return

Success case:
```
Status: Success
Dashboard URL: https://app.example.com/dashboard
Welcome message: "Welcome back, Demo User!"
Screenshot: Saved to artifacts
```

Failure case:
```
Status: Failed
Error message: "Invalid email or password"
Screenshot: Saved to artifacts
```

## Variations

### Testing Invalid Credentials
```
Task: Test login failure by entering "invalid@example.com" with 
password "wrongpass". Verify that an appropriate error message appears 
and return the error message text.
```

### Testing Remember Me
```
Task: Log in with "demo@example.com" / "password123", check the 
"Remember Me" checkbox before clicking Sign In. After successful login, 
verify that a session cookie was set.
```

### Testing Password Reset Flow
```
Task: From the login page, click "Forgot Password?", enter 
"demo@example.com" in the reset form, submit it, and verify that a 
confirmation message appears. Return the confirmation message.
```
