# Scientific Method - Validations

## Missing Random Seed Setting

### **Id**
missing-random-seed
### **Severity**
error
### **Type**
regex
### **Pattern**
  - random\.shuffle|random\.choice|random\.sample(?![\s\S]{0,200}seed)
  - np\.random\.(rand|randn|choice|shuffle)(?![\s\S]{0,200}seed)
  - torch\.(rand|randn)(?![\s\S]{0,200}manual_seed)
  - train_test_split(?![\s\S]{0,200}random_state)
### **Message**
Random operations without seed setting destroy reproducibility.
### **Fix Action**
  Set all random seeds at the start of your script:
  random.seed(42)
  np.random.seed(42)
  torch.manual_seed(42)
  
### **Applies To**
  - **/*.py
  - **/*.ipynb

## Incomplete Random Seed Coverage

### **Id**
incomplete-seed-setting
### **Severity**
error
### **Type**
regex
### **Pattern**
  - torch\.manual_seed(?![\s\S]{0,100}cuda\.manual_seed)
  - np\.random\.seed(?![\s\S]{0,200}random\.seed)
### **Message**
Setting one seed but not others leaves reproducibility gaps.
### **Fix Action**
  Create a comprehensive seed function:
  def set_all_seeds(seed):
      random.seed(seed)
      np.random.seed(seed)
      torch.manual_seed(seed)
      torch.cuda.manual_seed_all(seed)
  
### **Applies To**
  - **/*.py

## Missing Dependency Version Pinning

### **Id**
no-environment-pinning
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - requirements\.txt.*\n(?![\s\S]*==)
  - pip install (?!.*==)
### **Message**
Dependencies without version pins lead to irreproducible environments.
### **Fix Action**
Pin exact versions: numpy==1.24.3 or use pip freeze > requirements.lock
### **Applies To**
  - **/requirements.txt
  - **/*.sh
  - **/*.md

## Multiple Statistical Tests Without Correction

### **Id**
multiple-comparisons-no-correction
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - for.*in.*:\n.*ttest_ind|for.*in.*:\n.*mannwhitneyu
  - ttest_ind.*\n.*ttest_ind.*\n.*ttest_ind
  - chi2_contingency.*\n.*chi2_contingency
### **Message**
Running multiple tests without correction inflates false positive rate.
### **Fix Action**
  Apply Bonferroni correction: adjusted_alpha = 0.05 / n_tests
  Or use FDR correction: statsmodels.stats.multitest.multipletests(pvals, method='fdr_bh')
  
### **Applies To**
  - **/*.py
  - **/*.R
  - **/*.ipynb

## Hardcoded P-Value Threshold

### **Id**
p-value-threshold-hardcoded
### **Severity**
info
### **Type**
regex
### **Pattern**
  - p.*<.*0\.05
  - pvalue.*<.*0\.05
  - p_value.*<.*0\.05
### **Message**
Consider if 0.05 is appropriate. Report exact p-value and effect size.
### **Fix Action**
  Instead of if p < 0.05:
  Report: f"p = {p:.4f}, d = {effect_size:.2f}, 95% CI [{ci_low:.2f}, {ci_high:.2f}]"
  
### **Applies To**
  - **/*.py
  - **/*.R
  - **/*.ipynb

## Statistical Test Without Effect Size

### **Id**
no-effect-size
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ttest_ind.*print.*p(?!.*cohen|.*effect)
  - mannwhitneyu.*pvalue(?!.*effect|.*r|.*cliff)
  - chisquare.*print(?!.*cramer|.*phi|.*odds)
### **Message**
Statistical tests should report effect sizes, not just p-values.
### **Fix Action**
  Calculate and report effect sizes:
  - t-test: Cohen's d = (mean1 - mean2) / pooled_std
  - Chi-square: Cramer's V
  - Mann-Whitney: Rank-biserial r
  
### **Applies To**
  - **/*.py
  - **/*.R

## Point Estimate Without Confidence Interval

### **Id**
no-confidence-interval
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - mean\(\).*print(?!.*ci|.*interval|.*std|.*se)
  - accuracy.*=.*\.\d+(?![\s\S]{0,100}±|\+/-|ci|interval)
### **Message**
Report confidence intervals to show precision of estimates.
### **Fix Action**
  For means: stats.t.interval(0.95, len(data)-1, loc=np.mean(data), scale=stats.sem(data))
  For proportions: statsmodels.stats.proportion.proportion_confint()
  
### **Applies To**
  - **/*.py
  - **/*.R

## Experiment Without Power Analysis

### **Id**
no-power-analysis
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - n.*=.*[1-5]\d(?!\d).*ttest|sample.*size.*=.*[1-5]\d(?!\d)
### **Message**
Small sample sizes may lack power to detect real effects.
### **Fix Action**
  Use power analysis before data collection:
  from statsmodels.stats.power import TTestIndPower
  analysis = TTestIndPower()
  n = analysis.solve_power(effect_size=0.5, alpha=0.05, power=0.8)
  
### **Applies To**
  - **/*.py
  - **/*.R

## Scaling Before Train-Test Split

### **Id**
data-leakage-scaling
### **Severity**
error
### **Type**
regex
### **Pattern**
  - StandardScaler\(\)\.fit_transform.*train_test_split
  - MinMaxScaler\(\)\.fit_transform.*train_test_split
  - normalize.*train_test_split
### **Message**
Fitting scaler on full data before split leaks test information.
### **Fix Action**
  Split first, then fit scaler on train only:
  X_train, X_test = train_test_split(X)
  scaler = StandardScaler().fit(X_train)
  X_train_scaled = scaler.transform(X_train)
  X_test_scaled = scaler.transform(X_test)
  
### **Applies To**
  - **/*.py
  - **/*.ipynb

## Feature Selection Before Split

### **Id**
data-leakage-feature-selection
### **Severity**
error
### **Type**
regex
### **Pattern**
  - SelectKBest.*fit.*train_test_split
  - RFE.*fit.*train_test_split
  - VarianceThreshold.*fit_transform.*split
### **Message**
Feature selection on full data leaks test set information.
### **Fix Action**
  Use Pipeline to ensure proper ordering:
  from sklearn.pipeline import Pipeline
  pipe = Pipeline([
      ('scaler', StandardScaler()),
      ('selector', SelectKBest(k=10)),
      ('model', LogisticRegression()),
  ])
  # Fit on train, evaluate on test
  
### **Applies To**
  - **/*.py
  - **/*.ipynb

## Random Split on Time Series Data

### **Id**
time-series-random-split
### **Severity**
error
### **Type**
regex
### **Pattern**
  - train_test_split.*shuffle.*=.*True.*time|date|timestamp
  - train_test_split(?![\s\S]{0,100}shuffle.*=.*False).*\bts\b|series
### **Message**
Time series data must use temporal splits, not random splits.
### **Fix Action**
  Use temporal split:
  split_date = df['date'].quantile(0.8)
  train = df[df['date'] < split_date]
  test = df[df['date'] >= split_date]
  
  Or use TimeSeriesSplit from sklearn
  
### **Applies To**
  - **/*.py
  - **/*.ipynb

## No Pre-Registration Reference

### **Id**
no-pre-registration
### **Severity**
info
### **Type**
regex
### **Pattern**
  - hypothesis.*test(?!.*osf|.*aspredicted|.*pre.?regist)
### **Message**
Consider pre-registering hypotheses to prevent HARKing.
### **Fix Action**
  Pre-register at:
  - OSF: https://osf.io/prereg/
  - AsPredicted: https://aspredicted.org/
  Include pre-registration link in your analysis code comments.
  
### **Applies To**
  - **/*.py
  - **/*.R
  - **/*.md

## Incorrect Significance Language

### **Id**
significance-language
### **Severity**
info
### **Type**
regex
### **Pattern**
  - statistically significant.*means
  - p.*<.*0\.05.*proves
  - significant.*therefore.*works
### **Message**
Statistical significance doesn't mean practical importance or proof.
### **Fix Action**
  Use careful language:
  - "Statistically detectable" not "significant"
  - "Associated with" not "causes"
  - Report effect size for practical significance
  
### **Applies To**
  - **/*.py
  - **/*.R
  - **/*.md

## No Experiment Manifest

### **Id**
no-reproducibility-manifest
### **Severity**
info
### **Type**
regex
### **Pattern**
  - def.*experiment|run.*experiment(?![\s\S]{0,1000}manifest|version|git.*commit)
### **Message**
Experiments should log environment, seeds, and versions for reproducibility.
### **Fix Action**
  Create a manifest:
  manifest = {
      'git_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD']),
      'python_version': sys.version,
      'seeds': {'numpy': 42, 'torch': 42, 'random': 42},
      'timestamp': datetime.utcnow().isoformat(),
  }
  json.dump(manifest, open('experiment_manifest.json', 'w'))
  
### **Applies To**
  - **/*.py
  - **/*.ipynb

## Hardcoded Data File Paths

### **Id**
hardcoded-data-paths
### **Severity**
info
### **Type**
regex
### **Pattern**
  - pd\.read_csv\(['"]C:|pd\.read_csv\(['"]D:
  - pd\.read_csv\(['"]Users/
  - open\(['"].*\.csv['"]\)
### **Message**
Hardcoded paths reduce reproducibility across systems.
### **Fix Action**
  Use relative paths or environment variables:
  DATA_DIR = Path(os.environ.get('DATA_DIR', './data'))
  df = pd.read_csv(DATA_DIR / 'experiment_data.csv')
  
### **Applies To**
  - **/*.py
  - **/*.ipynb

## Test Without Explicit Null Hypothesis

### **Id**
missing-null-hypothesis
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ttest_ind.*#(?!.*null|.*H0)
### **Message**
Document the null hypothesis for statistical tests.
### **Fix Action**
  Add comments documenting hypotheses:
  # H0: Mean response time is equal between groups
  # H1: Treatment group has lower mean response time
  t_stat, p_value = ttest_ind(control, treatment, alternative='greater')
  
### **Applies To**
  - **/*.py
  - **/*.R

## Potential Optional Stopping

### **Id**
optional-stopping
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - while.*p.*>.*0\.05|while.*pvalue.*>|for.*collect.*data.*if.*p
### **Message**
Optional stopping (checking p-value during data collection) inflates false positives.
### **Fix Action**
  Either:
  1. Pre-specify sample size and don't check until complete
  2. Use sequential analysis with proper alpha spending
  
  from statsmodels.stats.sequential_design import GSTDesign
  gst = GSTDesign(alpha=0.05, beta=0.2, ...)
  
### **Applies To**
  - **/*.py
  - **/*.R