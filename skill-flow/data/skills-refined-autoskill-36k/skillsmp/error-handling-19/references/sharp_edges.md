# Error Handling - Sharp Edges

## Swallowing Errors

### **Id**
swallowing-errors
### **Summary**
Catching errors and doing nothing
### **Severity**
critical
### **Situation**
  Payment fails silently. User thinks payment went through. No
  error logged. Days later, angry user calls.
  
### **Why**
  Empty catch blocks hide failures. You cannot fix what you
  cannot see.
  
### **Solution**
  // WRONG
  try {
    await processPayment(order);
  } catch (e) {
    // Silent failure
  }
  
  // RIGHT
  try {
    await processPayment(order);
  } catch (error) {
    logger.error({ error, orderId: order.id }, "Payment failed");
    Sentry.captureException(error);
    throw error;
  }
  
### **Symptoms**
  - Users report issues not in logs
  - Silent failures
### **Detection Pattern**


## Exposing Internal Errors

### **Id**
exposing-internal-errors
### **Summary**
Showing internal errors to users
### **Severity**
high
### **Situation**
  Database connection fails. Error shows to user with internal
  details like IP addresses or table names.
  
### **Why**
  Internal error messages contain sensitive information.
  
### **Solution**
  app.use((err, req, res, next) => {
    logger.error({ error: err.message, stack: err.stack });
    
    if (err instanceof AppError) {
      return res.status(err.statusCode).json({
        error: err.userMessage,
      });
    }
    
    res.status(500).json({
      error: "Something went wrong. Please try again.",
    });
  });
  
### **Symptoms**
  - Stack traces in API responses
  - Database errors visible to users
### **Detection Pattern**


## Async Error Lost

### **Id**
async-error-lost
### **Summary**
Unhandled promise rejection
### **Severity**
high
### **Situation**
  Async function throws. No await or catch. Promise rejects
  silently or crashes Node.js process.
  
### **Why**
  Async errors need explicit handling. Without await, errors
  are not caught by surrounding try/catch.
  
### **Solution**
  // WRONG
  processOrder(order); // Error lost!
  
  // RIGHT
  await processOrder(order);
  
  // Or explicit catch
  processOrder(order).catch(handleError);
  
### **Symptoms**
  - UnhandledPromiseRejection warnings
  - App in inconsistent state
### **Detection Pattern**


## Error Boundary Missing

### **Id**
error-boundary-missing
### **Summary**
React app crashes completely on error
### **Severity**
medium
### **Situation**
  User clicks button. Component throws error. Entire app goes
  white - complete crash.
  
### **Why**
  React unmounts the entire tree when a component throws without
  an error boundary.
  
### **Solution**
  <ErrorBoundary fallback={<FallbackUI />}>
    <UserProfile userId={id} />
  </ErrorBoundary>
  
  // Next.js App Router - error.tsx
  export default function Error({ error, reset }) {
    return (
      <div>
        <h2>Something went wrong</h2>
        <button onClick={reset}>Retry</button>
      </div>
    );
  }
  
### **Symptoms**
  - White screen of death
  - Entire app crashes on one error
### **Detection Pattern**
