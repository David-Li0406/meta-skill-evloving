# AI Code Security

## Patterns


---
  #### **Name**
AI Output Validation Pipeline
  #### **Description**
Validate all LLM outputs before execution or storage
  #### **When**
LLM generates code, SQL, commands, or structured data
  #### **Example**
    import { z } from 'zod';
    import { scanForSecrets } from './security';
    
    // Schema validation for LLM-generated structured output
    const LLMOutputSchema = z.object({
        code: z.string().max(10000),
        language: z.enum(['typescript', 'python', 'sql']),
        explanation: z.string()
    });
    
    async function validateLLMOutput(rawOutput: unknown): Promise<ValidatedOutput> {
        // 1. Schema validation
        const parsed = LLMOutputSchema.parse(rawOutput);
    
        // 2. Secret detection
        const secrets = await scanForSecrets(parsed.code);
        if (secrets.length > 0) {
            throw new SecurityError('LLM output contains secrets', { secrets });
        }
    
        // 3. Dangerous pattern detection
        const dangerousPatterns = [
            /eval\s*\(/,
            /exec\s*\(/,
            /rm\s+-rf/,
            /DROP\s+TABLE/i,
            /TRUNCATE/i,
            /__import__/,
            /subprocess\.call/
        ];
    
        for (const pattern of dangerousPatterns) {
            if (pattern.test(parsed.code)) {
                throw new SecurityError('LLM output contains dangerous pattern', {
                    pattern: pattern.source
                });
            }
        }
    
        // 4. Static analysis (language-specific)
        const analysisResult = await runStaticAnalysis(parsed.code, parsed.language);
        if (analysisResult.criticalIssues.length > 0) {
            throw new SecurityError('LLM code has critical vulnerabilities', {
                issues: analysisResult.criticalIssues
            });
        }
    
        return {
            ...parsed,
            analysisResult,
            validatedAt: new Date()
        };
    }
    

---
  #### **Name**
Sandboxed Code Execution
  #### **Description**
Execute AI-generated code in isolated environments
  #### **When**
LLM output must be executed (code interpreters, agents)
  #### **Example**
    import { NodeVM } from 'vm2';
    import { spawn } from 'child_process';
    
    class SecureSandbox {
        private readonly timeout = 5000;
        private readonly memoryLimit = 128 * 1024 * 1024; // 128MB
    
        // JavaScript/TypeScript sandbox
        async executeJS(code: string, context: Record<string, unknown> = {}): Promise<unknown> {
            const vm = new NodeVM({
                timeout: this.timeout,
                sandbox: {
                    ...context,
                    // Explicitly deny dangerous globals
                    process: undefined,
                    require: undefined,
                    __dirname: undefined,
                    __filename: undefined
                },
                eval: false,
                wasm: false,
                sourceExtensions: ['js']
            });
    
            try {
                return vm.run(code);
            } catch (error) {
                if (error.message.includes('Script execution timed out')) {
                    throw new SecurityError('Code execution timeout', { code });
                }
                throw error;
            }
        }
    
        // Python sandbox using subprocess with cgroups
        async executePython(code: string): Promise<string> {
            return new Promise((resolve, reject) => {
                const proc = spawn('firejail', [
                    '--quiet',
                    '--private',
                    '--net=none',
                    '--rlimit-as=' + this.memoryLimit,
                    'python3', '-c', code
                ], {
                    timeout: this.timeout,
                    stdio: ['pipe', 'pipe', 'pipe']
                });
    
                let stdout = '';
                let stderr = '';
    
                proc.stdout.on('data', (data) => stdout += data);
                proc.stderr.on('data', (data) => stderr += data);
    
                proc.on('close', (code) => {
                    if (code === 0) resolve(stdout);
                    else reject(new Error(stderr || `Exit code: ${code}`));
                });
            });
        }
    
        // Docker-based sandbox for full isolation
        async executeInDocker(code: string, image: string): Promise<string> {
            const containerId = await this.createContainer(image, {
                NetworkDisabled: true,
                Memory: this.memoryLimit,
                CpuPeriod: 100000,
                CpuQuota: 50000, // 50% CPU
                ReadonlyRootfs: true,
                SecurityOpt: ['no-new-privileges']
            });
    
            try {
                return await this.execInContainer(containerId, code);
            } finally {
                await this.removeContainer(containerId);
            }
        }
    }
    

---
  #### **Name**
Supply Chain Verification
  #### **Description**
Verify AI model and dependency integrity
  #### **When**
Using third-party models, fine-tuned models, or AI dependencies
  #### **Example**
    import { createHash } from 'crypto';
    import { readFile } from 'fs/promises';
    
    interface ModelManifest {
        name: string;
        version: string;
        sha256: string;
        source: string;
        signedBy?: string;
        attestation?: string;
    }
    
    class ModelVerifier {
        private readonly trustedSources = [
            'huggingface.co',
            'anthropic.com',
            'openai.com'
        ];
    
        async verifyModel(modelPath: string, manifest: ModelManifest): Promise<boolean> {
            // 1. Verify source trust
            const sourceUrl = new URL(manifest.source);
            if (!this.trustedSources.some(s => sourceUrl.hostname.endsWith(s))) {
                throw new SecurityError('Untrusted model source', {
                    source: manifest.source,
                    trusted: this.trustedSources
                });
            }
    
            // 2. Verify hash integrity
            const modelData = await readFile(modelPath);
            const actualHash = createHash('sha256').update(modelData).digest('hex');
    
            if (actualHash !== manifest.sha256) {
                throw new SecurityError('Model hash mismatch', {
                    expected: manifest.sha256,
                    actual: actualHash
                });
            }
    
            // 3. Verify signature if available
            if (manifest.signedBy && manifest.attestation) {
                const valid = await this.verifySignature(
                    modelData,
                    manifest.attestation,
                    manifest.signedBy
                );
                if (!valid) {
                    throw new SecurityError('Model signature invalid');
                }
            }
    
            // 4. Scan for known malicious patterns
            await this.scanForMaliciousPatterns(modelPath);
    
            return true;
        }
    
        async verifyDependencies(packageJson: string): Promise<void> {
            const pkg = JSON.parse(await readFile(packageJson, 'utf-8'));
            const aiDeps = this.extractAIDependencies(pkg);
    
            for (const dep of aiDeps) {
                // Check for known vulnerable versions
                const vulns = await this.checkVulnerabilities(dep.name, dep.version);
                if (vulns.critical.length > 0) {
                    throw new SecurityError('Critical AI dependency vulnerability', {
                        package: dep.name,
                        vulnerabilities: vulns.critical
                    });
                }
            }
        }
    }
    

---
  #### **Name**
OWASP LLM Top 10 Mitigation
  #### **Description**
Systematic mitigation of OWASP LLM vulnerabilities
  #### **When**
Building or auditing LLM applications
  #### **Example**
    // Comprehensive LLM security middleware
    
    interface LLMSecurityConfig {
        maxTokens: number;
        rateLimitPerMinute: number;
        allowedTools: string[];
        sensitiveDataPatterns: RegExp[];
    }
    
    class LLMSecurityMiddleware {
        constructor(private config: LLMSecurityConfig) {}
    
        // LLM01: Prompt Injection Defense
        async sanitizeInput(input: string): Promise<string> {
            // Remove known injection patterns
            const sanitized = input
                .replace(/ignore previous instructions/gi, '[FILTERED]')
                .replace(/system:/gi, '[FILTERED]')
                .replace(/\[INST\]/gi, '[FILTERED]');
    
            // Validate input doesn't exceed token budget
            const tokens = await this.countTokens(sanitized);
            if (tokens > this.config.maxTokens) {
                throw new SecurityError('Input exceeds token limit');
            }
    
            return sanitized;
        }
    
        // LLM02: Insecure Output Handling
        async sanitizeOutput(output: string): Promise<string> {
            // Remove any embedded code that could execute
            let safe = output.replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '');
    
            // Detect and mask sensitive data
            for (const pattern of this.config.sensitiveDataPatterns) {
                safe = safe.replace(pattern, '[REDACTED]');
            }
    
            return safe;
        }
    
        // LLM03: Training Data Poisoning (at inference time)
        validateModelSource(source: string): boolean {
            const trustedSources = ['anthropic', 'openai', 'internal'];
            return trustedSources.some(s => source.includes(s));
        }
    
        // LLM04: Model Denial of Service
        async enforceRateLimits(userId: string): Promise<void> {
            const key = `ratelimit:${userId}`;
            const count = await this.redis.incr(key);
    
            if (count === 1) {
                await this.redis.expire(key, 60);
            }
    
            if (count > this.config.rateLimitPerMinute) {
                throw new SecurityError('Rate limit exceeded');
            }
        }
    
        // LLM05: Supply Chain Vulnerabilities (handled by ModelVerifier)
    
        // LLM06: Sensitive Information Disclosure
        async detectPII(text: string): Promise<PIIResult> {
            const patterns = {
                ssn: /\b\d{3}-\d{2}-\d{4}\b/g,
                creditCard: /\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b/g,
                email: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g,
                phone: /\b\d{3}[-.]?\d{3}[-.]?\d{4}\b/g,
                apiKey: /\b(sk-|api[_-]?key)[a-zA-Z0-9]{20,}\b/gi
            };
    
            const found: PIIMatch[] = [];
            for (const [type, pattern] of Object.entries(patterns)) {
                const matches = text.match(pattern);
                if (matches) {
                    found.push({ type, count: matches.length });
                }
            }
    
            return { hasPII: found.length > 0, matches: found };
        }
    
        // LLM07: Insecure Plugin Design
        validateToolCall(toolName: string, args: unknown): boolean {
            if (!this.config.allowedTools.includes(toolName)) {
                throw new SecurityError('Unauthorized tool', { tool: toolName });
            }
    
            // Validate arguments against schema
            const schema = this.getToolSchema(toolName);
            return schema.safeParse(args).success;
        }
    
        // LLM08: Excessive Agency
        async enforceLeastPrivilege(action: LLMAction): Promise<void> {
            const dangerousActions = ['delete', 'execute', 'admin', 'sudo'];
    
            if (dangerousActions.some(a => action.type.includes(a))) {
                // Require human approval for dangerous actions
                const approved = await this.requestHumanApproval(action);
                if (!approved) {
                    throw new SecurityError('Action requires human approval');
                }
            }
        }
    }
    

## Anti-Patterns


---
  #### **Name**
Trusting AI Output Directly
  #### **Description**
Executing or storing AI-generated content without validation
  #### **Why**
LLMs hallucinate, can be manipulated, and generate insecure code
  #### **Instead**
Always validate, sanitize, and sandbox AI outputs before use.

---
  #### **Name**
Static Prompts as Security
  #### **Description**
Relying solely on system prompts for security constraints
  #### **Why**
Prompt injection bypasses prompt-level controls easily
  #### **Instead**
Implement multi-layer defense with output validation and sandboxing.

---
  #### **Name**
Using Outdated AI Dependencies
  #### **Description**
Not updating AI SDKs, models, or related dependencies
  #### **Why**
AI security landscape evolves rapidly; new vulnerabilities discovered weekly
  #### **Instead**
Regular dependency audits, automated updates, vulnerability scanning.

---
  #### **Name**
No Model Provenance
  #### **Description**
Using models without verifying source and integrity
  #### **Why**
Poisoned models can contain backdoors, biased outputs, or malware
  #### **Instead**
Verify model hashes, sources, and maintain audit trail.

---
  #### **Name**
Excessive LLM Permissions
  #### **Description**
Giving LLMs access to all tools, data, or systems
  #### **Why**
Compromised LLM (via injection) gains all those permissions
  #### **Instead**
Apply least privilege principle; LLM gets only what it needs.