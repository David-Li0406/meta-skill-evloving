---
name: read-symbol
description: Find definitions with read_symbol tool
disable-model-invocation: true
---
Find definitions with `read_symbol` tool:
Prisma models: `read_symbol ["EntityName"] prisma/schema.prisma`
Prisma types: `read_symbol ["UserWhereInput"] node_modules/.prisma/client/index.d.ts`
GraphQL schema: `read_symbol ["CreateOrganizationInput"] src/graphql/schema/**/*.graphql`
GraphQL queries: `read_symbol ["queryName"] docs/playground.graphql`
QBO types: `read_symbol ["EntityName"] node_modules/quickbooks-node-promise/dist/*.d.ts`
Plaid types: `read_symbol ["EntityName"] node_modules/plaid/dist/*.d.ts`

Note it removes comments and simplifies indentation, only avoid if you will search_replace based on it. If you need the orignal version to replace it, use the same line range.
To minimize requests, read all symbol names and all file paths in one call when known.
