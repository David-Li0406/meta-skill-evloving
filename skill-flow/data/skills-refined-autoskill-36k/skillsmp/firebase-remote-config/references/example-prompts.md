# Firebase Remote Config - Example Prompts

Example prompts and minimal syntax snippets for `firebase-remote-config` skill.

---

## Condition expression example

```
app.version >= ('2.0.0') && device.country in ['US','IN']
```

## Minimal template JSON example

```json
{
  "conditions": [
    { "name": "is_us_or_new_app", "expression": "app.version >= ('2.0.0') && device.country in ['US']", "tagColor": "BLUE" },
    { "name": "rollout_10_percent", "expression": "percent <= 10", "tagColor": "GREEN" }
  ],
  "parameters": {
    "feature_dark_mode_enabled": {
      "defaultValue": { "value": "false" },
      "conditionalValues": {
        "is_us_or_new_app": { "value": "true" },
        "rollout_10_percent": { "value": "true" }
      }
    }
  }
}
```

See:
- Remote Config Conditional Expression Reference: <https://firebase.google.com/docs/remote-config/condition-reference>
- RemoteConfig REST API: <https://firebase.google.com/docs/reference/remote-config/rest/v1/RemoteConfig>