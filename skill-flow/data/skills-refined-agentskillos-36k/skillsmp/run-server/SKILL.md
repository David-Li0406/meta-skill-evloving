---
name: run-server
description: Run the server with npm run dev
disable-model-invocation: true
---
Run the server with: `npm run dev 2>&1 | tee /tmp/server.log` (use `is_background: true`)
If available in the project, prepend: `npm run ts -- bin/kill-watch.ts &&` to kill the existing server.
Check logs: `sleep 5 && tail /tmp/server.log`
Read skill `query-graphql` for how to test with GraphQL.
