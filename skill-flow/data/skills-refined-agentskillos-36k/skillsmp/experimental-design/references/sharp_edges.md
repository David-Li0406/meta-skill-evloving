# Experimental Design - Sharp Edges

## One-Factor-At-A-Time Misses All Interactions

### **Id**
ofat-misses-interactions
### **Severity**
critical
### **Summary**
OFAT requires more runs and can never detect interaction effects
### **Symptoms**
  - Changing one variable at a time
  - Optimal found but doesn't work in practice
  - Variables tested independently
### **Why**
  OFAT assumes factors are independent. In reality, factor A's
  effect often depends on factor B's level (interaction).
  Factorial designs detect these interactions.
  
  OFAT also requires MORE total runs for the same information.
  
### **Gotcha**
  # OFAT approach (BAD)
  # Vary temperature: 100, 150, 200 (best: 200)
  # Vary pressure at T=200: 1, 2, 3 (best: 2)
  # Conclude: T=200, P=2 is optimal
  
  # Reality: Optimal might be T=150, P=3
  # Interaction: High temp needs low pressure
  # OFAT could never find this!
  
### **Solution**
  Use factorial design:
  from pyDOE2 import ff2n
  design = ff2n(2)  # 2 factors, 4 runs
  # Tests all combinations including interaction
  

## Systematic Run Order Creates False Effects

### **Id**
no-randomization-confound
### **Severity**
critical
### **Summary**
Running all treatment A first biases results with time effects
### **Symptoms**
  - Experiments run in convenient order
  - All replicates of condition X run consecutively
  - Unexpected 'treatment effects'
### **Why**
  Equipment drifts over time. Operators get fatigued.
  Materials age. If all treatment A runs are first,
  time effects get confounded with treatment effects.
  
### **Solution**
  np.random.shuffle(run_order)
  # Run experiments in random order
  # Or use blocking if time effects are expected
  

## No Center Points to Check for Curvature

### **Id**
missing-center-points
### **Severity**
high
### **Summary**
Linear model fit when relationship is actually curved
### **Symptoms**
  - 2-level factorial shows no effect
  - Optimal settings don't work as expected
  - Model has poor prediction accuracy
### **Solution**
  # Add center points to 2-level factorial
  design = np.vstack([
      ff2n(2),           # Corner points
      [[0, 0], [0, 0]]   # Center points (replicates)
  ])
  # If center point response differs from corner average,
  # curvature exists → need higher-order model
  

## Fractional Factorial Aliasing Confusion

### **Id**
resolution-aliasing
### **Severity**
high
### **Summary**
In fractional designs, some effects are mathematically confounded
### **Symptoms**
  - Using fractional factorial without understanding resolution
  - Main effect 'significant' but actually aliased with interaction
### **Why**
  Fractional factorials trade runs for information.
  Resolution III: Main effects aliased with 2-way interactions
  Resolution IV: Main effects clear, 2-way aliased with 2-way
  Resolution V: Main and 2-way clear, aliased with 3-way
  
### **Solution**
  # Check resolution before interpreting
  # Use Resolution V or higher for main + 2-way interactions
  # Or use foldover to de-alias
  

## No Replication = No Error Estimate

### **Id**
inadequate-replication
### **Severity**
medium
### **Summary**
Without replicates, can't distinguish signal from noise
### **Symptoms**
  - One run per condition
  - Every effect looks 'significant'
  - No pure error estimate
### **Solution**
  # Include replicates, especially at center points
  design = full_factorial(factors)
  design = pd.concat([design, design])  # Duplicate for replicates
  # Or at minimum, replicate center points
  