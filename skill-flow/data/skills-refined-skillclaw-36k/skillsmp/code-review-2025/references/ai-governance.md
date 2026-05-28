# AI Governance & Agentic Security (2025-2026)
## 1. The Agentic Shift: From Output to Action
By Dec 2025, AI is no longer just writing code—it is an **Active Identity** in the system. Reviewers must evaluate not just what the AI says, but what it is **allowed to do**.
### Excessive Agency & Tool Safety (LLM06:2025)
- [ ] **Least Agency Principle:** Does the AI agent have the minimum set of tool permissions required? (e.g., Read-only DB access vs. Write access).
- [ ] **Human-in-the-Loop (HITL):** Are "Consequential Actions" (deleting data, spending money, changing permissions) gated by a manual human approval step?
- [ ] **Sandboxed Execution:** Is the AI-generated code or tool-use executed in an isolated, ephemeral environment (e.g., Docker, WebAssembly) with no network access to internal secrets?
## 2. OWASP LLM Top 10:2025 Checklist
The final 2025 rankings emphasize systemic supply chain and information disclosure risks.
### LLM01: Prompt Injection (Direct & Indirect)
- [ ] **Segregation of Duties:** Are system instructions clearly separated from user-provided data using structural markers (e.g., XML tags or specialized API roles)?
- [ ] **Indirect Injection:** Does the system process external data (webpages, emails) that could contain "hidden instructions" designed to hijack the agent?
### LLM02: Sensitive Information Disclosure
- [ ] **PII Scrubbing:** Does the system utilize a pre-processing layer to strip PII/Secrets before sending data to the model provider?
- [ ] **System Prompt Hardening (LLM07):** Is the system prompt protected from "Tell me your instructions" attacks via negative constraints and output filters?
### LLM03: AI Supply Chain Integrity
- [ ] **Slopsquatting Defense:** Are all AI-suggested dependencies verified? 
    - *Method:* Check registry date (>30 days), download count (>10k), and verify the package name isn't a "hallucination-friendly" typo.
- [ ] **Model Provenance:** Are we using a "Frontier" model (Claude 4.5, GPT-5) or a verified local weight? Flag any use of unvetted open-source models in production.
### LLM08: Vector & Embedding Weaknesses
- [ ] **RAG Isolation:** If using multi-tenant data, does the vector query include a strict `metadata.tenant_id` filter to prevent cross-context leakage?
- [ ] **Embedding Inversion:** Is sensitive text hashed or masked before being embedded to prevent "Inversion" attacks?
## 3. "Vibe Coding" Governance
"Vibe Coding" (AI-led development) creates 40-60% faster velocity but introduces **Over-reliance Bias**.
### The "Reasoning" Model Tiering (Dec 2025 Benchmarks)
| Model | Code Hallucination Rate | Review Requirement |
| :--- | :--- | :--- |
| **Claude 4.5 Sonnet** | ~48% | Mandatory human logic-check. |
| **GPT-5.1 (High)** | ~51% | Full audit for Tool-Calling logic. |
| **Opus 4.5** | ~58% | Senior-level architectural review. |
- [ ] **Audit Trail:** Are AI-generated commits clearly labeled `[AI-Generated]` to alert future reviewers of potential "Vibe Smells"?
- [ ] **Hallucinated Logic:** Check for "Ghost Functions"—APIs or library methods that look real but don't exist in the current version of the framework.
## 4. Prompt Engineering & Integrity
- [ ] **Self-Correction Logic:** Does the prompt instruct the model to "Check your work" or "Reflect on security" before outputting code?
- [ ] **Versioned Prompts:** Are system prompts stored in Git as "Code," with versioning and peer review, rather than hardcoded in the application?
- [ ] **Output Validation:** Is the LLM output treated as **Untrusted Input**? (Must be validated by a parser or Zod schema before being stored or used).
## 5. Security Guardrails
- [ ] **Semantic Guardrails:** Use tools (e.g., LlamaGuard, NeMo-Guardrails) to detect and block malicious intent in both user inputs and model outputs.
- [ ] **Token Quotas (LLM10):** Are there strict rate limits and token budgets per user/session to prevent "Denial of Wallet" or resource exhaustion?
