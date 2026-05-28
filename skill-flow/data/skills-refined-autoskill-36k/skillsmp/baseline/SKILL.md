---
name: baseline
description: Guidance for working with the Baseline Ruby gem. Use whenever Baseline is mentioned by the user or in another skill, or when writing code in Baseline itself or in a Ruby app that uses Baseline.
---

# Baseline

## Overview

**Baseline** is a Ruby gem providing reusable modules, patterns, and infrastructure for Ruby applications: authentication, task management, invoicing, messaging, admin panels, and third-party service integrations. Baseline can be used in Rails apps via its Rails engine but also in non-Rails Ruby apps, e.g. Sinatra.

## Source

Find the source of Baseline in `~/code/own/baseline`. Warn the user if that folder cannot be found.

## Local app testing

When updating an app to use local Baseline changes, find the `baseline` line in the app's `Gemfile` and replace it with a line referencing the local code:

```
gem "baseline", path: "~/code/own/baseline"
```

## Reference

See [the reference guide](references/REFERENCE.md) for details.
