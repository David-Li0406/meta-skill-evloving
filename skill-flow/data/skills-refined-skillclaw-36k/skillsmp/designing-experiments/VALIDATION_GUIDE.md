# Experiment Configuration Validation Guide

Manual validation checklist for experiment configurations. Use this guide after editing a generated configuration to
ensure it meets system requirements.

---

## Validation Checklist

```text
Configuration Validation:
- [ ] At least one experiment state is defined
- [ ] All system_state_code values are valid for the target system
- [ ] All experiment_state_code values are unique positive integers
- [ ] Trial zone positions are valid (end >= start, stimulus location >= start)
- [ ] Guidance parameters are non-negative integers
- [ ] States with supports_trials=false have all guidance parameters set to 0
```

---

## System State Code Validation

Each acquisition system defines valid system state codes in its runtime module. You MUST verify codes against the
actual source before finalizing configurations.

### Verification Steps

1. Locate the system's state enumeration:
   ```
   src/sl_experiment/<system>/data_acquisition.py
   ```

2. Search for the state enum class (e.g., `_MesoscopeVRStates` for Mesoscope-VR)

3. Search for `system_state_code` validation logic to determine which codes are valid for experiment configurations
   (not all defined states may be valid for experiments)

4. Verify each `system_state_code` in the configuration matches a valid code

---

## Trial Zone Position Validation

For each trial structure, verify:

| Check             | Condition                                                        |
|-------------------|------------------------------------------------------------------|
| Zone ordering     | `stimulus_trigger_zone_end_cm >= stimulus_trigger_zone_start_cm` |
| Stimulus position | `stimulus_location_cm >= stimulus_trigger_zone_start_cm`         |
| Zone bounds       | All zone positions are within `trial_length_cm`                  |

---

## Guidance Parameter Validation

For each experiment state:

| Parameter                               | Valid Range | Notes                              |
|-----------------------------------------|-------------|------------------------------------|
| `reinforcing_initial_guided_trials`     | >= 0        | Set to 0 if no water reward trials |
| `reinforcing_recovery_failed_threshold` | >= 0        | Set to 0 if no water reward trials |
| `reinforcing_recovery_guided_trials`    | >= 0        | Set to 0 if no water reward trials |
| `aversive_initial_guided_trials`        | >= 0        | Set to 0 if no gas puff trials     |
| `aversive_recovery_failed_threshold`    | >= 0        | Set to 0 if no gas puff trials     |
| `aversive_recovery_guided_trials`       | >= 0        | Set to 0 if no gas puff trials     |

**For states with `supports_trials: false`:** All guidance parameters should be set to 0.

---

## Trial Type Consistency

Verify guidance parameters match the trial types present in the configuration:

1. Read the `trial_structures` section to identify trial types (check `trigger_type` field)
2. If no `lick` trigger types exist, reinforcing guidance parameters should be 0
3. If no `occupancy` trigger types exist, aversive guidance parameters should be 0
