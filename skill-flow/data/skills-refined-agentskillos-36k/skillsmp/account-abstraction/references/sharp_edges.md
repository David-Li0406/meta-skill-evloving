# Account Abstraction - Sharp Edges

## Bundler Rejection

### **Id**
bundler-rejection
### **Summary**
UserOperation rejected by bundler for subtle reasons
### **Severity**
high
### **Situation**
  Your UserOperation is valid but bundlers reject it. Reasons
  range from insufficient prefund to banned opcodes.
  
### **Why**
  Bundlers run simulation before including UserOps. Any reason
  for potential failure or MEV extraction causes rejection.
  
### **Solution**
  Common Rejection Reasons:
  1. Insufficient prefund (need gas * gasPrice + extra)
  2. Account not deployed and no initCode
  3. Banned opcodes in validation
  4. Storage access violations
  5. Paymaster validation failed
  
  // Proper gas estimation
  const gasEstimate = await bundler.estimateUserOperationGas(userOp);
  userOp.callGasLimit = gasEstimate.callGasLimit;
  userOp.verificationGasLimit = gasEstimate.verificationGasLimit;
  userOp.preVerificationGas = gasEstimate.preVerificationGas;
  

## Initcode Gas

### **Id**
initcode-gas
### **Summary**
First transaction fails due to deployment cost
### **Severity**
medium
### **Situation**
  User's first transaction includes initCode for account
  deployment. You underestimate gas, transaction fails.
  
### **Why**
  Account deployment costs 200k-500k gas extra. First UserOp
  must cover both deployment and execution.
  
### **Solution**
  // Add deployment overhead for first transaction
  if (isFirstTransaction) {
      userOp.verificationGasLimit += 500000n;
      userOp.preVerificationGas += 100000n;
  }
  

## Paymaster Frontrun

### **Id**
paymaster-frontrun
### **Summary**
Paymaster approval can be front-run
### **Severity**
high
### **Situation**
  Verifying paymaster signs approval off-chain. Attacker
  intercepts signature and uses it for their own UserOp.
  
### **Why**
  If paymaster signature doesn't bind to specific UserOp,
  it can be extracted and reused.
  
### **Solution**
  // Include UserOp hash in paymaster signature
  bytes32 hash = keccak256(abi.encode(
      userOp.sender,
      userOp.nonce,
      keccak256(userOp.callData),
      userOpHash // Bind to this specific UserOp
  ));
  