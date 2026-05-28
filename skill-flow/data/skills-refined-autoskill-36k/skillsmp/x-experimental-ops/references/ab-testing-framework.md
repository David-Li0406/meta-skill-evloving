# Reference: DuckDuckGoose (DDG)

DuckDuckGoose (DDG) is the framework used to run thousands of simultaneous A/B tests on the X platform.

### Experiment Lifecycle
1. **Configuration:** Engineers define "Parameters" (e.g., `rt_weight: 22.0` vs. `rt_weight: 20.0`).
2. **Bucketing:** Users are hashed into 1,000 "Buckets." An experiment might take 1% of traffic (10 buckets).
3. **Telemetry:** Every interaction (Click, Like, App-Close) is tagged with the experiment ID.
4. **Analysis:** The DDG dashboard calculates "Delta" scores for key metrics to see if the change was positive.

### Feature Flags
DDG also manages feature flags, allowing the team to "Kill-switch" a new ranking model or filter if it causes a sudden drop in engagement or a spike in latency.
