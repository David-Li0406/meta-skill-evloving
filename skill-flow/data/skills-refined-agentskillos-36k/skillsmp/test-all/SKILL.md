---
name: test-all
description: Test all components of the project. Use after each edit to ensure code changes do not regress.
---

# Testing

In order to test the Rust code, you should use the Dagger function `test`:

```bash
dagger call test --source=.
```

To test the Cloudflare Worker, you should use the Dagger function `cf-worker-test`:

```bash
dagger call cf-worker-test --source=.
```

Note that these can take some time to complete.
