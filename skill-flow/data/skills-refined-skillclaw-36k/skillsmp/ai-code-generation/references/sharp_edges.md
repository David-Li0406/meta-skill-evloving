# Ai Code Generation - Sharp Edges

## Hallucinated Apis

### **Id**
hallucinated-apis
### **Summary**
LLMs hallucinate non-existent APIs and methods
### **Severity**
high
### **Situation**
Generated code uses APIs that don't exist
### **Why**
  LLMs are trained on historical data and may:
  - Invent methods that seem plausible but don't exist
  - Mix up APIs from different libraries
  - Use outdated API signatures from older versions
  - Combine patterns from different languages incorrectly
  
  Studies show 4x increase in defects with AI-assisted code.
  
### **Detection Pattern**
  await.*generate.*code(?!.*type.*check|lint|validate)
  
### **Solution**
  Always validate generated code:
  
  ```typescript
  import ts from "typescript";
  
  async function validateGeneratedCode(code: string): Promise<{
    valid: boolean;
    errors: string[];
  }> {
    // 1. TypeScript type checking
    const result = ts.transpileModule(code, {
      compilerOptions: {
        module: ts.ModuleKind.ESNext,
        target: ts.ScriptTarget.ESNext,
        strict: true,
        noEmit: true,
      },
      reportDiagnostics: true,
    });
  
    const errors = result.diagnostics?.map(
      (d) => ts.flattenDiagnosticMessageText(d.messageText, "\n")
    ) || [];
  
    // 2. ESLint check
    const lintResults = await eslint.lintText(code);
    errors.push(...lintResults.flatMap((r) => r.messages.map((m) => m.message)));
  
    return {
      valid: errors.length === 0,
      errors,
    };
  }
  
  // Use it
  const generated = await generateCode(prompt);
  const validation = await validateGeneratedCode(generated.code);
  
  if (!validation.valid) {
    console.error("Generated code has issues:", validation.errors);
    // Retry with feedback
    const fixed = await generateCode(prompt + "\n\nFix these issues: " + validation.errors.join("\n"));
  }
  ```
  

## Security Vulnerabilities

### **Id**
security-vulnerabilities
### **Summary**
Generated code contains security vulnerabilities
### **Severity**
critical
### **Situation**
AI generates code with SQL injection, XSS, or other vulnerabilities
### **Why**
  LLMs learn patterns from training data that includes insecure code.
  They optimize for "looks correct" not "is secure."
  Common issues:
  - SQL string concatenation
  - Unsanitized user input in HTML
  - Hardcoded credentials
  - Missing input validation
  - Insecure cryptography
  
### **Detection Pattern**
  generate.*code(?!.*security.*scan|semgrep|snyk)
  
### **Solution**
  Run security scanning on all generated code:
  
  ```typescript
  import { exec } from "child_process";
  
  async function securityScan(code: string, language: string) {
    const tempFile = `/tmp/scan-${Date.now()}.${language === "python" ? "py" : "ts"}`;
    fs.writeFileSync(tempFile, code);
  
    try {
      // Run semgrep with security rules
      const { stdout } = await exec(
        `semgrep --config=p/security-audit --json ${tempFile}`
      );
  
      const results = JSON.parse(stdout);
      return {
        vulnerabilities: results.results.map((r: any) => ({
          rule: r.check_id,
          severity: r.extra.severity,
          message: r.extra.message,
          line: r.start.line,
        })),
      };
    } finally {
      fs.unlinkSync(tempFile);
    }
  }
  
  // Integration in generation pipeline
  async function safeGenerateCode(prompt: string) {
    const generated = await generateCode(prompt);
    const scan = await securityScan(generated.code, generated.language);
  
    if (scan.vulnerabilities.length > 0) {
      // Either fix or reject
      const criticals = scan.vulnerabilities.filter((v) => v.severity === "ERROR");
      if (criticals.length > 0) {
        throw new Error(`Generated code has critical vulnerabilities: ${criticals.map((c) => c.message).join(", ")}`);
      }
    }
  
    return generated;
  }
  ```
  

## Function Calling Injection

### **Id**
function-calling-injection
### **Summary**
Malicious prompts can trigger unintended tool calls
### **Severity**
critical
### **Situation**
User input influences function calling decisions
### **Why**
  If user input is included in prompts that trigger function calling,
  attackers can craft inputs that:
  - Trigger file deletion
  - Execute arbitrary commands
  - Exfiltrate data via tool calls
  - Bypass access controls
  
  This is "prompt injection" applied to tool use.
  
### **Detection Pattern**
  tools.*function.*user.*input|tool_choice.*auto.*user
  
### **Solution**
  Sanitize inputs and validate tool calls:
  
  ```typescript
  // Dangerous tools that modify state
  const DANGEROUS_TOOLS = ["write_file", "delete_file", "run_command"];
  
  // Validate tool calls before execution
  function validateToolCall(
    toolName: string,
    args: any,
    userTier: "admin" | "user" | "readonly"
  ): { allowed: boolean; reason?: string } {
    // Check user permissions
    if (DANGEROUS_TOOLS.includes(toolName) && userTier !== "admin") {
      return { allowed: false, reason: "Insufficient permissions" };
    }
  
    // Validate file paths
    if (toolName === "write_file" || toolName === "read_file") {
      const path = args.path;
      // Prevent directory traversal
      if (path.includes("..") || path.startsWith("/")) {
        return { allowed: false, reason: "Invalid path" };
      }
      // Block sensitive files
      if (path.includes(".env") || path.includes("credentials")) {
        return { allowed: false, reason: "Access to sensitive files denied" };
      }
    }
  
    // Validate commands
    if (toolName === "run_command") {
      const dangerous = ["rm -rf", "sudo", "chmod", "curl | sh", "eval"];
      if (dangerous.some((d) => args.command.includes(d))) {
        return { allowed: false, reason: "Dangerous command blocked" };
      }
    }
  
    return { allowed: true };
  }
  
  // Use in agent loop
  for (const toolCall of message.tool_calls) {
    const validation = validateToolCall(
      toolCall.function.name,
      JSON.parse(toolCall.function.arguments),
      userTier
    );
  
    if (!validation.allowed) {
      messages.push({
        role: "tool",
        tool_call_id: toolCall.id,
        content: `Blocked: ${validation.reason}`,
      });
      continue;
    }
  
    // Execute only if validated
    const result = await toolHandlers[toolCall.function.name](args);
  }
  ```
  

## Unbounded Token Costs

### **Id**
unbounded-token-costs
### **Summary**
Code generation agents consume unlimited tokens
### **Severity**
high
### **Situation**
Agent loops without cost limits
### **Why**
  Code generation is token-intensive:
  - Large code context = many input tokens
  - Multiple iterations = multiplicative cost
  - Function calling adds overhead
  - No limits = $100+ bills in minutes
  
### **Detection Pattern**
  while.*agent|for.*iteration.*generate(?!.*max|limit|budget)
  
### **Solution**
  Implement token budgets and limits:
  
  ```typescript
  const TOKEN_COSTS = {
    "gpt-4o": { input: 5, output: 15 },      // per million
    "claude-sonnet": { input: 3, output: 15 },
  };
  
  class TokenBudget {
    private used = { input: 0, output: 0 };
  
    constructor(
      private maxCost: number = 1.0,
      private model: keyof typeof TOKEN_COSTS = "gpt-4o"
    ) {}
  
    record(inputTokens: number, outputTokens: number) {
      this.used.input += inputTokens;
      this.used.output += outputTokens;
    }
  
    get currentCost(): number {
      const rates = TOKEN_COSTS[this.model];
      return (
        (this.used.input / 1_000_000) * rates.input +
        (this.used.output / 1_000_000) * rates.output
      );
    }
  
    canContinue(): boolean {
      return this.currentCost < this.maxCost;
    }
  
    remainingBudget(): number {
      return this.maxCost - this.currentCost;
    }
  }
  
  // Use in agent
  async function runBudgetedAgent(task: string, maxCost: number = 1.0) {
    const budget = new TokenBudget(maxCost);
  
    for (let i = 0; i < 20; i++) {
      if (!budget.canContinue()) {
        return { error: "Budget exhausted", cost: budget.currentCost };
      }
  
      const response = await openai.chat.completions.create({...});
  
      budget.record(
        response.usage?.prompt_tokens || 0,
        response.usage?.completion_tokens || 0
      );
  
      // ... process response
    }
  }
  ```
  

## Json Parsing Failures

### **Id**
json-parsing-failures
### **Summary**
LLM structured output breaks JSON parsing
### **Severity**
medium
### **Situation**
LLM returns malformed JSON despite instructions
### **Why**
  Even with clear JSON instructions, LLMs often:
  - Add markdown code fences around JSON
  - Include explanatory text before/after
  - Use trailing commas (invalid JSON)
  - Include comments in JSON
  - Escape characters incorrectly
  - Truncate long outputs mid-JSON
  
### **Detection Pattern**
  JSON\.parse\(.*response(?!.*match|extract|repair)
  
### **Solution**
  Use robust JSON extraction:
  
  ```typescript
  function extractJSON(text: string): any {
    // Try to find JSON object in text
    const patterns = [
      /```json\s*([\s\S]*?)\s*```/,  // Markdown code block
      /```\s*([\s\S]*?)\s*```/,       // Any code block
      /(\{[\s\S]*\})/,                 // Raw JSON object
      /(\[[\s\S]*\])/,                 // Raw JSON array
    ];
  
    for (const pattern of patterns) {
      const match = text.match(pattern);
      if (match) {
        try {
          // Clean common issues
          let cleaned = match[1]
            .replace(/,\s*([}\]])/g, "$1")  // Remove trailing commas
            .replace(/\/\/.*$/gm, "")        // Remove // comments
            .replace(/\/\*[\s\S]*?\*\//g, ""); // Remove /* */ comments
  
          return JSON.parse(cleaned);
        } catch {
          continue;
        }
      }
    }
  
    throw new Error("No valid JSON found in response");
  }
  
  // Or use response_format for guaranteed JSON (OpenAI)
  const response = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [...],
    response_format: { type: "json_object" }, // Guarantees valid JSON
  });
  ```
  

## Outdated Library Usage

### **Id**
outdated-library-usage
### **Summary**
Generated code uses deprecated or old API patterns
### **Severity**
medium
### **Situation**
LLM generates code with outdated patterns
### **Why**
  LLM training data has a cutoff date.
  Libraries evolve faster than model updates.
  Common issues:
  - Next.js Pages Router when App Router is standard
  - React class components instead of hooks
  - Old Express.js patterns
  - Deprecated npm packages
  
### **Detection Pattern**
  generate.*code(?!.*version|latest)
  
### **Solution**
  Include version context in prompts:
  
  ```typescript
  async function generateCurrentCode(
    prompt: string,
    dependencies: Record<string, string>
  ) {
    const versionContext = Object.entries(dependencies)
      .map(([pkg, version]) => `${pkg}@${version}`)
      .join(", ");
  
    const enhancedPrompt = `${prompt}
  
    IMPORTANT: Use these exact library versions and their current APIs:
    ${versionContext}
  
    For React, use:
    - Function components with hooks (not class components)
    - TypeScript with strict mode
    - Modern patterns (use client/server if Next.js App Router)
  
    For Next.js 14+:
    - Use App Router (/app directory)
    - Server Components by default
    - Server Actions for mutations`;
  
    return generateCode(enhancedPrompt);
  }
  
  // Read versions from package.json
  const pkg = JSON.parse(fs.readFileSync("package.json", "utf-8"));
  const result = await generateCurrentCode(
    "Add user authentication",
    pkg.dependencies
  );
  ```
  

## Context Length Truncation

### **Id**
context-length-truncation
### **Summary**
Large codebases exceed context window
### **Severity**
medium
### **Situation**
Trying to include too much code context
### **Why**
  Even with 128k+ context windows:
  - Performance degrades with length
  - Costs scale linearly
  - Important info gets "lost in the middle"
  - Truncation may cut off critical context
  
### **Detection Pattern**
  codebase.*context|include.*all.*files(?!.*limit|chunk|select)
  
### **Solution**
  Use intelligent context selection:
  
  ```typescript
  async function selectRelevantContext(
    query: string,
    codebase: Map<string, string>,
    maxTokens: number = 50000
  ): Promise<string[]> {
    // 1. Embed the query
    const queryEmbedding = await embed(query);
  
    // 2. Embed and rank code files
    const rankedFiles: { path: string; score: number }[] = [];
  
    for (const [path, content] of codebase.entries()) {
      const embedding = await embed(content.slice(0, 2000)); // First 2k chars
      const score = cosineSimilarity(queryEmbedding, embedding);
      rankedFiles.push({ path, score });
    }
  
    rankedFiles.sort((a, b) => b.score - a.score);
  
    // 3. Select files until token limit
    const selected: string[] = [];
    let tokens = 0;
  
    for (const { path } of rankedFiles) {
      const content = codebase.get(path)!;
      const fileTokens = estimateTokens(content);
  
      if (tokens + fileTokens > maxTokens) break;
  
      selected.push(`## ${path}\n\`\`\`\n${content}\n\`\`\``);
      tokens += fileTokens;
    }
  
    return selected;
  }
  ```
  

## Async Code Race Conditions

### **Id**
async-code-race-conditions
### **Summary**
Generated async code has race conditions
### **Severity**
medium
### **Situation**
LLM generates concurrent code without proper synchronization
### **Why**
  LLMs often generate async code that:
  - Doesn't properly await promises
  - Has race conditions in parallel operations
  - Missing error handling in Promise.all
  - Doesn't handle cancellation
  
### **Detection Pattern**
  generate.*async(?!.*race|concurr|sync)
  
### **Solution**
  Review async patterns in generated code:
  
  ```typescript
  const asyncAntiPatterns = [
    // Missing await
    /async\s+\w+\([^)]*\)\s*{[^}]*(?<!await\s)fetch\(/,
    // Promise.all without error handling
    /Promise\.all\([^)]+\)(?!\s*\.catch)/,
    // forEach with async (doesn't await)
    /\.forEach\(\s*async/,
    // Race condition: read-modify-write without lock
    /let\s+\w+\s*=\s*await[^;]+;\s*\w+\s*[+\-*/]=.*await/,
  ];
  
  function checkAsyncPatterns(code: string): string[] {
    const issues: string[] = [];
  
    for (const pattern of asyncAntiPatterns) {
      if (pattern.test(code)) {
        issues.push(`Potential async issue: ${pattern.source}`);
      }
    }
  
    return issues;
  }
  ```
  