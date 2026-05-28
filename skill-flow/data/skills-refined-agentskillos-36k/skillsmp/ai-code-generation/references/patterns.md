# AI Code Generation

## Patterns


---
  #### **Name**
Structured Code Output with Zod
  #### **Description**
Generate code with strict schema validation
  #### **When**
User needs reliable structured code output
  #### **Implementation**
    import Anthropic from "@anthropic-ai/sdk";
    import { z } from "zod";
    import { zodToJsonSchema } from "zod-to-json-schema";
    
    const anthropic = new Anthropic();
    
    // Define schema for code generation output
    const CodeGenerationSchema = z.object({
      language: z.enum(["typescript", "python", "javascript", "rust", "go"]),
      code: z.string().describe("The generated code"),
      imports: z.array(z.string()).describe("Required imports/dependencies"),
      dependencies: z.array(z.object({
        name: z.string(),
        version: z.string().optional(),
      })).describe("NPM/pip packages needed"),
      explanation: z.string().describe("Brief explanation of the code"),
      usage: z.string().describe("Example usage of the generated code"),
    });
    
    type CodeGeneration = z.infer<typeof CodeGenerationSchema>;
    
    async function generateCode(
      prompt: string,
      options?: {
        language?: string;
        context?: string;
        style?: "concise" | "documented" | "production";
      }
    ): Promise<CodeGeneration> {
      const { language = "typescript", context = "", style = "documented" } = options || {};
    
      const styleGuides = {
        concise: "Write minimal code without comments",
        documented: "Include JSDoc/docstrings and inline comments",
        production: "Production-ready with error handling, types, and tests",
      };
    
      const jsonSchema = zodToJsonSchema(CodeGenerationSchema);
    
      const response = await anthropic.messages.create({
        model: "claude-sonnet-4-20250514",
        max_tokens: 4096,
        messages: [
          {
            role: "user",
            content: `Generate ${language} code for the following request:
    
            ${prompt}
    
            ${context ? `Context:\n${context}` : ""}
    
            Style: ${styleGuides[style]}
    
            Return ONLY valid JSON matching this schema:
            ${JSON.stringify(jsonSchema, null, 2)}`,
          },
        ],
      });
    
      const text = response.content[0].type === "text" ? response.content[0].text : "";
      const jsonMatch = text.match(/\{[\s\S]*\}/);
    
      if (!jsonMatch) {
        throw new Error("No JSON found in response");
      }
    
      return CodeGenerationSchema.parse(JSON.parse(jsonMatch[0]));
    }
    
    // Usage
    const result = await generateCode(
      "Create a rate limiter using sliding window algorithm",
      { language: "typescript", style: "production" }
    );
    

---
  #### **Name**
Function Calling for Tool Use
  #### **Description**
Enable LLM to call external functions/APIs
  #### **When**
Building agents that interact with external systems
  #### **Implementation**
    import OpenAI from "openai";
    
    const openai = new OpenAI();
    
    // Define available tools
    const tools: OpenAI.ChatCompletionTool[] = [
      {
        type: "function",
        function: {
          name: "search_codebase",
          description: "Search the codebase for files, functions, or patterns",
          parameters: {
            type: "object",
            properties: {
              query: { type: "string", description: "Search query" },
              fileTypes: {
                type: "array",
                items: { type: "string" },
                description: "File extensions to search (e.g., ['.ts', '.tsx'])",
              },
              maxResults: { type: "number", description: "Maximum results to return" },
            },
            required: ["query"],
          },
        },
      },
      {
        type: "function",
        function: {
          name: "read_file",
          description: "Read the contents of a file",
          parameters: {
            type: "object",
            properties: {
              path: { type: "string", description: "File path relative to project root" },
              startLine: { type: "number", description: "Start line (optional)" },
              endLine: { type: "number", description: "End line (optional)" },
            },
            required: ["path"],
          },
        },
      },
      {
        type: "function",
        function: {
          name: "write_file",
          description: "Write or update a file",
          parameters: {
            type: "object",
            properties: {
              path: { type: "string", description: "File path" },
              content: { type: "string", description: "File content" },
              createDirs: { type: "boolean", description: "Create parent directories" },
            },
            required: ["path", "content"],
          },
        },
      },
      {
        type: "function",
        function: {
          name: "run_command",
          description: "Execute a shell command",
          parameters: {
            type: "object",
            properties: {
              command: { type: "string", description: "Command to run" },
              cwd: { type: "string", description: "Working directory" },
            },
            required: ["command"],
          },
        },
      },
    ];
    
    // Tool implementations
    const toolHandlers: Record<string, (args: any) => Promise<string>> = {
      search_codebase: async ({ query, fileTypes, maxResults }) => {
        // Implement actual search
        const results = await searchFiles(query, { fileTypes, maxResults });
        return JSON.stringify(results);
      },
      read_file: async ({ path, startLine, endLine }) => {
        const content = await readFile(path);
        if (startLine !== undefined) {
          const lines = content.split("\n");
          return lines.slice(startLine - 1, endLine || lines.length).join("\n");
        }
        return content;
      },
      write_file: async ({ path, content, createDirs }) => {
        await writeFile(path, content, { createDirs });
        return `File written: ${path}`;
      },
      run_command: async ({ command, cwd }) => {
        const result = await exec(command, { cwd });
        return result.stdout + result.stderr;
      },
    };
    
    // Agent loop with tool use
    async function runCodeAgent(task: string, maxIterations: number = 10) {
      const messages: OpenAI.ChatCompletionMessageParam[] = [
        {
          role: "system",
          content: `You are a code assistant that can search, read, write files and run commands.
            Complete the user's task step by step.
            Always explain what you're doing before taking action.`,
        },
        { role: "user", content: task },
      ];
    
      for (let i = 0; i < maxIterations; i++) {
        const response = await openai.chat.completions.create({
          model: "gpt-4o",
          messages,
          tools,
          tool_choice: "auto",
        });
    
        const message = response.choices[0].message;
        messages.push(message);
    
        // Check if done
        if (!message.tool_calls || message.tool_calls.length === 0) {
          return message.content;
        }
    
        // Execute tool calls
        for (const toolCall of message.tool_calls) {
          const handler = toolHandlers[toolCall.function.name];
          const args = JSON.parse(toolCall.function.arguments);
    
          console.log(`Calling ${toolCall.function.name}:`, args);
    
          try {
            const result = await handler(args);
            messages.push({
              role: "tool",
              tool_call_id: toolCall.id,
              content: result,
            });
          } catch (error: any) {
            messages.push({
              role: "tool",
              tool_call_id: toolCall.id,
              content: `Error: ${error.message}`,
            });
          }
        }
      }
    
      return "Max iterations reached";
    }
    

---
  #### **Name**
AI Code Review
  #### **Description**
Automated code review with suggestions
  #### **When**
User wants AI-powered code review in CI/CD
  #### **Implementation**
    import Anthropic from "@anthropic-ai/sdk";
    
    const anthropic = new Anthropic();
    
    interface ReviewComment {
      file: string;
      line: number;
      severity: "error" | "warning" | "suggestion" | "info";
      category: "bug" | "security" | "performance" | "style" | "maintainability";
      message: string;
      suggestion?: string;
    }
    
    interface CodeReviewResult {
      summary: string;
      score: number; // 0-100
      comments: ReviewComment[];
      approved: boolean;
    }
    
    async function reviewCode(
      files: { path: string; content: string; diff?: string }[],
      options?: {
        focus?: ("security" | "performance" | "style" | "bugs")[];
        context?: string;
      }
    ): Promise<CodeReviewResult> {
      const { focus = ["security", "bugs", "performance"], context = "" } = options || {};
    
      const fileContents = files.map((f) =>
        `## ${f.path}\n${f.diff ? `### Diff:\n${f.diff}\n### Full file:` : ""}\n\`\`\`\n${f.content}\n\`\`\``
      ).join("\n\n");
    
      const response = await anthropic.messages.create({
        model: "claude-sonnet-4-20250514",
        max_tokens: 4096,
        messages: [
          {
            role: "user",
            content: `Review the following code changes.
    
            Focus areas: ${focus.join(", ")}
    
            ${context ? `Context: ${context}` : ""}
    
            Files to review:
            ${fileContents}
    
            Provide your review as JSON:
            {
              "summary": "Brief overall assessment",
              "score": 0-100,
              "approved": true/false,
              "comments": [
                {
                  "file": "path/to/file",
                  "line": 123,
                  "severity": "error|warning|suggestion|info",
                  "category": "bug|security|performance|style|maintainability",
                  "message": "What's wrong",
                  "suggestion": "How to fix (optional)"
                }
              ]
            }
    
            Return ONLY valid JSON.`,
          },
        ],
      });
    
      const text = response.content[0].type === "text" ? response.content[0].text : "";
      const jsonMatch = text.match(/\{[\s\S]*\}/);
    
      if (!jsonMatch) {
        throw new Error("No JSON in response");
      }
    
      return JSON.parse(jsonMatch[0]) as CodeReviewResult;
    }
    
    // GitHub PR integration
    async function reviewPullRequest(
      prNumber: number,
      owner: string,
      repo: string
    ) {
      // Fetch PR files
      const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });
    
      const { data: files } = await octokit.pulls.listFiles({
        owner,
        repo,
        pull_number: prNumber,
      });
    
      // Get file contents
      const fileContents = await Promise.all(
        files.map(async (file) => ({
          path: file.filename,
          content: await fetchFileContent(owner, repo, file.sha),
          diff: file.patch,
        }))
      );
    
      // Run review
      const review = await reviewCode(fileContents);
    
      // Post comments
      for (const comment of review.comments) {
        await octokit.pulls.createReviewComment({
          owner,
          repo,
          pull_number: prNumber,
          body: `**${comment.severity.toUpperCase()}** [${comment.category}]: ${comment.message}${
            comment.suggestion ? `\n\n**Suggestion:** ${comment.suggestion}` : ""
          }`,
          path: comment.file,
          line: comment.line,
          side: "RIGHT",
        });
      }
    
      return review;
    }
    

---
  #### **Name**
Multi-File Code Generation
  #### **Description**
Generate complete features spanning multiple files
  #### **When**
User needs to scaffold entire features or components
  #### **Implementation**
    import Anthropic from "@anthropic-ai/sdk";
    
    const anthropic = new Anthropic();
    
    interface GeneratedFile {
      path: string;
      content: string;
      description: string;
    }
    
    interface FeatureGeneration {
      files: GeneratedFile[];
      instructions: string[];
      dependencies: { name: string; version?: string }[];
    }
    
    async function generateFeature(
      description: string,
      options: {
        framework: "nextjs" | "express" | "fastapi" | "nest";
        includeTests?: boolean;
        includeTypes?: boolean;
      }
    ): Promise<FeatureGeneration> {
      const { framework, includeTests = true, includeTypes = true } = options;
    
      const frameworkPatterns = {
        nextjs: `
          - Use App Router conventions
          - Server Components by default, 'use client' when needed
          - API routes in app/api/
          - Zod for validation`,
        express: `
          - Use Express 4.x patterns
          - Controllers, services, routes separation
          - Error handling middleware`,
        fastapi: `
          - Use FastAPI with Pydantic models
          - Async/await patterns
          - Dependency injection`,
        nest: `
          - Use NestJS decorators
          - Module/Controller/Service pattern
          - DTOs with class-validator`,
      };
    
      const response = await anthropic.messages.create({
        model: "claude-sonnet-4-20250514",
        max_tokens: 8192,
        messages: [
          {
            role: "user",
            content: `Generate a complete feature implementation:
    
            Feature: ${description}
    
            Framework: ${framework}
            ${frameworkPatterns[framework]}
    
            Requirements:
            - ${includeTypes ? "Include TypeScript types/interfaces" : "JavaScript only"}
            - ${includeTests ? "Include test files" : "No tests"}
            - Follow best practices for ${framework}
            - Include error handling
            - Add comments for complex logic
    
            Return JSON:
            {
              "files": [
                {
                  "path": "relative/path/to/file.ts",
                  "content": "file contents",
                  "description": "what this file does"
                }
              ],
              "instructions": ["Step 1: Install X", "Step 2: Run Y"],
              "dependencies": [{ "name": "package", "version": "^1.0.0" }]
            }
    
            Return ONLY valid JSON.`,
          },
        ],
      });
    
      const text = response.content[0].type === "text" ? response.content[0].text : "";
      const jsonMatch = text.match(/\{[\s\S]*\}/);
    
      if (!jsonMatch) {
        throw new Error("No JSON in response");
      }
    
      return JSON.parse(jsonMatch[0]) as FeatureGeneration;
    }
    
    // Write generated files to disk
    async function scaffoldFeature(
      description: string,
      baseDir: string,
      options: Parameters<typeof generateFeature>[1]
    ) {
      const feature = await generateFeature(description, options);
    
      // Write files
      for (const file of feature.files) {
        const fullPath = path.join(baseDir, file.path);
        await fs.mkdir(path.dirname(fullPath), { recursive: true });
        await fs.writeFile(fullPath, file.content);
        console.log(`Created: ${file.path}`);
      }
    
      // Install dependencies
      if (feature.dependencies.length > 0) {
        const deps = feature.dependencies.map(
          (d) => d.version ? `${d.name}@${d.version}` : d.name
        );
        console.log(`\nInstall dependencies:\nnpm install ${deps.join(" ")}`);
      }
    
      return feature;
    }
    

---
  #### **Name**
Test Generation from Code
  #### **Description**
Generate tests for existing code
  #### **When**
User needs to add tests to existing code
  #### **Implementation**
    import Anthropic from "@anthropic-ai/sdk";
    
    const anthropic = new Anthropic();
    
    interface GeneratedTest {
      testFile: string;
      content: string;
      coverage: {
        functions: string[];
        scenarios: string[];
      };
    }
    
    async function generateTests(
      sourceCode: string,
      options: {
        framework: "vitest" | "jest" | "pytest" | "mocha";
        style: "unit" | "integration" | "e2e";
        coverage?: "basic" | "comprehensive";
      }
    ): Promise<GeneratedTest> {
      const { framework, style, coverage = "comprehensive" } = options;
    
      const response = await anthropic.messages.create({
        model: "claude-sonnet-4-20250514",
        max_tokens: 4096,
        messages: [
          {
            role: "user",
            content: `Generate ${style} tests for this code using ${framework}:
    
            \`\`\`
            ${sourceCode}
            \`\`\`
    
            Coverage level: ${coverage}
            ${coverage === "comprehensive" ? "Include edge cases, error handling, and boundary conditions." : "Cover happy paths."}
    
            Requirements:
            - Use ${framework} syntax and best practices
            - Include descriptive test names
            - Add setup/teardown if needed
            - Mock external dependencies
            - Test error cases
    
            Return JSON:
            {
              "testFile": "filename.test.ts",
              "content": "test file content",
              "coverage": {
                "functions": ["list of functions tested"],
                "scenarios": ["list of test scenarios"]
              }
            }
    
            Return ONLY valid JSON.`,
          },
        ],
      });
    
      const text = response.content[0].type === "text" ? response.content[0].text : "";
      const jsonMatch = text.match(/\{[\s\S]*\}/);
    
      if (!jsonMatch) {
        throw new Error("No JSON in response");
      }
    
      return JSON.parse(jsonMatch[0]) as GeneratedTest;
    }
    

---
  #### **Name**
Automated Refactoring
  #### **Description**
Suggest and apply code refactoring
  #### **When**
User needs to improve existing code structure
  #### **Implementation**
    import Anthropic from "@anthropic-ai/sdk";
    
    const anthropic = new Anthropic();
    
    interface RefactoringResult {
      original: string;
      refactored: string;
      changes: {
        type: string;
        description: string;
        before: string;
        after: string;
      }[];
      improvements: string[];
    }
    
    async function suggestRefactoring(
      code: string,
      options?: {
        focus?: ("readability" | "performance" | "maintainability" | "dry")[];
        preserveApi?: boolean;
      }
    ): Promise<RefactoringResult> {
      const { focus = ["readability", "maintainability"], preserveApi = true } = options || {};
    
      const response = await anthropic.messages.create({
        model: "claude-sonnet-4-20250514",
        max_tokens: 4096,
        messages: [
          {
            role: "user",
            content: `Refactor this code:
    
            \`\`\`
            ${code}
            \`\`\`
    
            Focus areas: ${focus.join(", ")}
            ${preserveApi ? "Preserve the public API (function signatures, exports)" : "API changes allowed"}
    
            Apply these refactoring patterns where appropriate:
            - Extract functions for repeated logic
            - Simplify conditional expressions
            - Use modern language features
            - Improve naming
            - Reduce complexity
    
            Return JSON:
            {
              "original": "original code",
              "refactored": "refactored code",
              "changes": [
                {
                  "type": "extract-function|simplify|rename|etc",
                  "description": "what changed and why",
                  "before": "code snippet before",
                  "after": "code snippet after"
                }
              ],
              "improvements": ["List of improvements made"]
            }
    
            Return ONLY valid JSON.`,
          },
        ],
      });
    
      const text = response.content[0].type === "text" ? response.content[0].text : "";
      const jsonMatch = text.match(/\{[\s\S]*\}/);
    
      if (!jsonMatch) {
        throw new Error("No JSON in response");
      }
    
      return JSON.parse(jsonMatch[0]) as RefactoringResult;
    }
    

## Anti-Patterns


---
  #### **Name**
Blindly accepting generated code
  #### **Why Bad**
AI generates plausible but often incorrect code
  #### **Example Bad**
    const code = await generateCode(prompt);
    fs.writeFileSync("feature.ts", code); // No review!
    
  #### **Example Good**
    const code = await generateCode(prompt);
    // Review, test, then write
    const review = await reviewCode([{ path: "feature.ts", content: code }]);
    if (review.score < 80) {
      console.log("Review issues:", review.comments);
    }
    

---
  #### **Name**
No schema validation on outputs
  #### **Why Bad**
LLMs produce malformed JSON, missing fields
  #### **Example Bad**
    const result = JSON.parse(response);
    return result.code; // May be undefined
    
  #### **Example Good**
    const result = CodeGenerationSchema.parse(JSON.parse(response));
    return result.code; // Guaranteed to exist
    

---
  #### **Name**
Unbounded agent loops
  #### **Why Bad**
Agents can loop forever, consuming tokens/money
  #### **Example Bad**
    while (!done) {
      await agent.step(); // May never finish
    }
    
  #### **Example Good**
    for (let i = 0; i < MAX_ITERATIONS; i++) {
      const result = await agent.step();
      if (result.done) break;
    }
    

---
  #### **Name**
Executing generated code without sandboxing
  #### **Why Bad**
Generated code may be malicious or destructive
  #### **Example Bad**
    const code = await generateCode("delete unused files");
    eval(code); // DANGEROUS
    
  #### **Example Good**
    const code = await generateCode("delete unused files");
    // Review, then run in sandbox
    await runInSandbox(code, { fs: "read-only" });
    