# Experimental Design

## Patterns

### **Factorial Design**
  #### **Name**
Factorial Experimental Design
  #### **Description**
Test multiple factors efficiently
  #### **When**
Need to study multiple variables and their interactions
  #### **Pattern**
    from itertools import product
    import pandas as pd
    from pyDOE2 import fullfact, ff2n, fracfact
    
    # Full factorial: All combinations of factors
    def full_factorial_design(factors: dict) -> pd.DataFrame:
        """
        Full factorial design - tests ALL combinations.
    
        factors = {
            'temperature': [100, 150, 200],
            'pressure': [1, 2],
            'catalyst': ['A', 'B']
        }
        # Results in 3 x 2 x 2 = 12 experiments
        """
        names = list(factors.keys())
        levels = [factors[name] for name in names]
        combinations = list(product(*levels))
    
        return pd.DataFrame(combinations, columns=names)
    
    # 2^k factorial (two levels per factor)
    def two_level_factorial(n_factors: int) -> np.ndarray:
        """
        2^k factorial design with coded levels (-1, +1).
        Efficient for screening many factors.
        """
        return ff2n(n_factors)
    
    # Fractional factorial for many factors
    def fractional_factorial(design_string: str) -> np.ndarray:
        """
        Fractional factorial - fewer runs, some aliasing.
    
        'a b c ab' = 2^(3-1) design, 4 runs instead of 8
        """
        return fracfact(design_string)
    
    # Example: Screening 7 factors in 8 runs
    # Full factorial would need 2^7 = 128 runs
    screening = fracfact('a b c d e f g')  # Resolution III
    
  #### **Why**
Factorials reveal interaction effects that one-at-a-time can't detect
### **Blocking Design**
  #### **Name**
Blocking to Control Confounds
  #### **Description**
Account for known sources of variation
  #### **Pattern**
    import numpy as np
    from scipy.stats import f_oneway
    
    def randomized_block_design(
        treatments: list,
        blocks: list,
        n_per_cell: int = 1
    ) -> pd.DataFrame:
        """
        Randomized Complete Block Design (RCBD).
    
        Blocks account for known nuisance variation.
        Example: Days as blocks, treatments randomized within each day.
        """
        design = []
        for block in blocks:
            block_treatments = treatments.copy()
            np.random.shuffle(block_treatments)
    
            for treatment in block_treatments:
                for _ in range(n_per_cell):
                    design.append({
                        'block': block,
                        'treatment': treatment
                    })
    
        return pd.DataFrame(design)
    
    # Latin Square: Block on two factors
    def latin_square(n: int) -> np.ndarray:
        """
        Latin Square design - block on row AND column.
        Each treatment appears once in each row and column.
        """
        square = np.zeros((n, n), dtype=int)
        for i in range(n):
            for j in range(n):
                square[i, j] = (i + j) % n
        return square
    
  #### **Why**
Blocking increases precision by removing known variation
### **Sample Size Design**
  #### **Name**
Sample Size Determination
  #### **Description**
Calculate required samples before running experiment
  #### **Pattern**
    from statsmodels.stats.power import TTestIndPower, FTestAnovaPower
    
    def required_sample_size(
        effect_size: float,
        alpha: float = 0.05,
        power: float = 0.80,
        design: str = "two_group"
    ) -> int:
        """
        Calculate sample size for desired power.
    
        effect_size: Cohen's d for t-test, f for ANOVA
        """
        if design == "two_group":
            analysis = TTestIndPower()
            n = analysis.solve_power(
                effect_size=effect_size,
                alpha=alpha,
                power=power,
            )
        elif design == "anova":
            analysis = FTestAnovaPower()
            n = analysis.solve_power(
                effect_size=effect_size,
                alpha=alpha,
                power=power,
                k_groups=3  # Number of groups
            )
        return int(np.ceil(n))
    
    # Effect size conventions
    EFFECT_SIZES = {
        'small': 0.2,
        'medium': 0.5,
        'large': 0.8,
    }
    
### **Response Surface**
  #### **Name**
Response Surface Methodology
  #### **Description**
Optimize continuous factors
  #### **When**
Finding optimal settings for process parameters
  #### **Pattern**
    from pyDOE2 import ccdesign, bbdesign
    
    def central_composite_design(n_factors: int) -> np.ndarray:
        """
        Central Composite Design (CCD) for response surface.
        Combines factorial with star points and center points.
        """
        return ccdesign(n_factors, center=(4, 4), face='circumscribed')
    
    def box_behnken_design(n_factors: int) -> np.ndarray:
        """
        Box-Behnken Design - 3 levels, no extreme corners.
        Good when extreme combinations are impractical.
        """
        return bbdesign(n_factors)
    
    # Fit response surface model
    def fit_response_surface(X, y):
        """Fit quadratic model with interactions."""
        from sklearn.preprocessing import PolynomialFeatures
        from sklearn.linear_model import LinearRegression
    
        poly = PolynomialFeatures(degree=2, include_bias=False)
        X_poly = poly.fit_transform(X)
        model = LinearRegression().fit(X_poly, y)
    
        return model, poly
    
  #### **Why**
RSM efficiently finds optimal conditions in fewer runs

## Anti-Patterns

### **One At A Time**
  #### **Name**
One-Factor-at-a-Time (OFAT)
  #### **Problem**
    # Change only one variable at a time
    # Miss ALL interaction effects
    # Requires many more runs for same information
    
  #### **Solution**
Use factorial designs to capture interactions
### **No Randomization**
  #### **Name**
Running Experiments in Systematic Order
  #### **Problem**
Run all treatment A first, then treatment B
  #### **Solution**
Randomize run order to prevent time-based confounds