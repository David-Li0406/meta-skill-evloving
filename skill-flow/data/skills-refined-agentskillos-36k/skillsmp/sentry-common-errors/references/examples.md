# Examples

**Example: Debug Missing Events**
Request: "Sentry isn't showing any of our errors"
Result: DSN was unset in production environment, fixed by adding SENTRY_DSN to deployment config.