---
name: playwright
description: Automate browser interactions with Playwright MCP. Use for web scraping, form filling, testing, or any browser-based automation tasks.
allowed-tools: mcp__playwright__*
user-invocable: false
---

<skill name="Playwright Browser Automation">
  <purpose>Efficiently automate browser interactions using the Playwright MCP tools.</purpose>

  <tool-preference>
    <principle>Prefer `browser_run_code` for batch operations - it executes multiple Playwright operations in a single call, reducing round-trips.</principle>
    
    <example type="good" title="Single call for multiple operations">
      <code>
browser_run_code: async (page) => {
  await page.goto('https://example.com');
  await page.fill('#email', 'user@test.com');
  await page.fill('#password', 'secret');
  await page.click('button[type="submit"]');
}
      </code>
    </example>
    
    <example type="avoid" title="Multiple individual tool calls">
      <description>browser_navigate → browser_type → browser_type → browser_click</description>
    </example>
  </tool-preference>

  <when-to-use-individual-tools>
    <use-case name="Snapshot needed">Use `browser_snapshot` to read page state for decision-making</use-case>
    <use-case name="Dynamic interaction">When next action depends on page response</use-case>
    <use-case name="Debugging">Step-by-step execution for troubleshooting</use-case>
  </when-to-use-individual-tools>

  <screenshot-rule>
    <principle>After any screen-modifying action, call `browser_take_screenshot`</principle>
    <default-filename>latest.png</default-filename>
    <note>ALWAYS use "latest.png" unless user specifies another name</note>
  </screenshot-rule>

  <screen-changing-tools title="Tools that modify visible page and require screenshots">
    <tool>browser_navigate</tool>
    <tool>browser_click</tool>
    <tool>browser_type</tool>
    <tool>browser_fill_form</tool>
    <tool>browser_select_option</tool>
    <tool>browser_press_key</tool>
    <tool>browser_handle_dialog</tool>
    <tool>browser_file_upload</tool>
    <tool>browser_tabs (select/new)</tool>
    <tool>browser_run_code</tool>
  </screen-changing-tools>

  <storage-state>
    <path>/playwright-data/state.json</path>
    <note>Browser session persists cookies, localStorage, and auth</note>
  </storage-state>

  <patterns>
    <pattern name="Batch operation with screenshot">
      <step>browser_run_code(code)</step>
      <step>browser_take_screenshot(filename: "latest.png")</step>
    </pattern>
    <pattern name="Individual operation with screenshot">
      <step>browser_click(element, ref)</step>
      <step>browser_take_screenshot(filename: "latest.png")</step>
    </pattern>
  </patterns>
</skill>
