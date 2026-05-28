# Optimization: Design Tips

These tips help reduce sync cost and keep the experience stable.

## 1. Reduce sync frequency

High-frequency sync can hit bandwidth limits and cause backlogs.

**Example**: Instead of syncing remaining time every second:
- Sync the timer end time once
- Display remaining time by comparing with local time

## 2. State sync vs event sync

- **Late joiners must reproduce state** → use synced variables
- **Only simultaneous playback is needed** → `SendCustomNetworkEvent`

## 3. When to use Continuous

Use `Continuous` only when frequent updates are required (e.g., position interpolation).
Otherwise, control sync frequency with `Manual`.
