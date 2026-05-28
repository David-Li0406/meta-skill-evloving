---
name: take-latest-schema-timestamp
description: Used for resolving schema conflicts by keeping the more recent timestamp
---

# Instructions

Use `git diff` to fetch the current status. If there's a conflict in db/schema.rb related to the `version` timestamp, resolve that conflict by accepting whichever timestamp is more recent.

Don't make any other changes in schema.rb

If there isn't a change in schema.rb, no-op and explain that to the user.
