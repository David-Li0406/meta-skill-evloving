---
name: context7
description: Look up current library documentation via Context7 MCP. Use when writing code that uses external libraries, frameworks, or packages to ensure correct API usage.
allowed-tools: mcp__context7__resolve-library-id, mcp__context7__query-docs
user-invocable: false
---

<skill name="Context7 Documentation Lookup">
  <purpose>Query up-to-date documentation for any library before writing code that uses it.</purpose>

  <workflow>
    <step order="1" name="Resolve library ID">Call `resolve-library-id` with the library name and your query</step>
    <step order="2" name="Query documentation">Call `query-docs` with the resolved library ID and specific question</step>
    <step order="3" name="Implement">Write code based on the retrieved documentation</step>
  </workflow>

  <when-to-use>
    <trigger>External libraries (React, FastAPI, Prisma, Next.js, etc.)</trigger>
    <trigger>Frequently-updated packages where APIs may have changed</trigger>
    <trigger>Uncertain about API syntax or method signatures</trigger>
    <trigger>Any non-trivial import or library usage</trigger>
  </when-to-use>

  <example title="Adding NextAuth">
    <description>User: "Add NextAuth"</description>
    <step>resolve-library-id("nextauth", "how to set up authentication")</step>
    <step>query-docs(libraryId, "NextAuth setup and configuration")</step>
    <step>Implement based on current docs</step>
  </example>

  <critical-rules>
    <rule>Never trust training data alone for library APIs</rule>
    <rule>Query docs BEFORE writing library code</rule>
    <rule>Use specific queries to get relevant documentation</rule>
    <rule>Limit to 3 calls per question - use best result if not found</rule>
  </critical-rules>
</skill>
