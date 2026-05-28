# Monte Carlo - Validations

## Using Global Random State

### **Id**
global-random-state
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - np\.random\.seed\(|random\.seed\(
  - np\.random\.(rand|randn|uniform|normal)\(
### **Message**
Global random state is not thread-safe and hard to reproduce. Use Generator.
### **Fix Action**
Use rng = np.random.Generator(np.random.PCG64(seed)) with rng.uniform()
### **Applies To**
  - **/*.py

## Fixed Sample Size Without Convergence Check

### **Id**
fixed-sample-size
### **Severity**
info
### **Type**
regex
### **Pattern**
  - for\s+_\s+in\s+range\(\d+\):\s*\n.*sample
  - n_samples\s*=\s*\d+(?!.*converge|error|std)
### **Message**
Fixed sample size may waste computation or stop before convergence.
### **Fix Action**
Use adaptive sampling with target error: while std_error > target: sample more
### **Applies To**
  - **/*.py

## MCMC Without Burn-in

### **Id**
no-burn-in-mcmc
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - mcmc\.sample\(.*\)(?!.*burn|warm)
  - metropolis.*\(.*\)(?!.*burn)
### **Message**
MCMC chains need burn-in to reach equilibrium.
### **Fix Action**
Add burn_in parameter: mcmc.sample(n_samples, burn_in=1000)
### **Applies To**
  - **/*.py

## MCMC Without Effective Sample Size Check

### **Id**
no-ess-check
### **Severity**
info
### **Type**
regex
### **Pattern**
  - samples\s*=.*mcmc(?!.*ess|effective)
### **Message**
MCMC effective sample size may be much less than nominal.
### **Fix Action**
Compute ESS: if ess < 100: warn or run longer
### **Applies To**
  - **/*.py

## Importance Sampling Without Weight Diagnostics

### **Id**
importance-no-weight-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - weight.*=.*density.*\/.*density(?!.*ess|max|var)
  - importance_weight(?!.*check|valid|ess)
### **Message**
Importance weights can have huge variance. Check ESS and max weights.
### **Fix Action**
Check: ess = 1/sum(w_norm**2); if ess < n/10: proposal is poor
### **Applies To**
  - **/*.py

## Halton Sequence in High Dimensions

### **Id**
halton-high-dim
### **Severity**
info
### **Type**
regex
### **Pattern**
  - halton.*dim\s*=\s*[1-9]\d+|halton.*d\s*=\s*[1-9]\d+
### **Message**
Halton sequences show correlation patterns in d > 10. Use Sobol instead.
### **Fix Action**
For high dimensions: sampler = qmc.Sobol(d=dim, scramble=True)
### **Applies To**
  - **/*.py

## Parallel MC Without Proper Seeding

### **Id**
no-seed-parallel
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - Pool\(.*\)\.map.*random(?!.*SeedSequence|spawn)
  - parallel.*random(?!.*seed.*sequence)
### **Message**
Parallel random streams may overlap without proper seeding.
### **Fix Action**
Use SeedSequence.spawn() for independent parallel streams
### **Applies To**
  - **/*.py

## MCMC With Single Chain Only

### **Id**
single-chain-mcmc
### **Severity**
info
### **Type**
regex
### **Pattern**
  - mcmc\.sample\(.*\)(?!.*chain|n_chain|multiple)
### **Message**
Single MCMC chain can't detect convergence issues. Run multiple chains.
### **Fix Action**
Run 4+ chains from dispersed starts, compute R-hat diagnostic
### **Applies To**
  - **/*.py

## MC Estimate Without Error Bound

### **Id**
no-variance-estimate
### **Severity**
info
### **Type**
regex
### **Pattern**
  - np\.mean\(.*sample.*\)(?!.*std|var|error|ci)
### **Message**
Monte Carlo estimates should include uncertainty quantification.
### **Fix Action**
Compute std error: stderr = np.std(samples) / np.sqrt(n)
### **Applies To**
  - **/*.py

## QMC Sequence Without Scrambling

### **Id**
qmc-without-scramble
### **Severity**
info
### **Type**
regex
### **Pattern**
  - Sobol\(.*scramble\s*=\s*False
  - Halton\((?!.*scramble)
### **Message**
Unscrambled QMC sequences can show bias. Enable scrambling.
### **Fix Action**
Use scramble=True: qmc.Sobol(d=dim, scramble=True)
### **Applies To**
  - **/*.py