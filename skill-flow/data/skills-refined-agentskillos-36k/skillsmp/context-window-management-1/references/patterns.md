# Context Window Management

## Patterns


---
  #### **Name**
Tiered Context Strategy
  #### **Description**
Different strategies based on context size
  #### **When**
Building any multi-turn conversation system
  #### **Example**
    interface ContextTier {
        maxTokens: number;
        strategy: 'full' | 'summarize' | 'rag';
        model: string;
    }
    
    const TIERS: ContextTier[] = [
        { maxTokens: 8000, strategy: 'full', model: 'claude-3-haiku' },
        { maxTokens: 32000, strategy: 'full', model: 'claude-3-5-sonnet' },
        { maxTokens: 100000, strategy: 'summarize', model: 'claude-3-5-sonnet' },
        { maxTokens: Infinity, strategy: 'rag', model: 'claude-3-5-sonnet' }
    ];
    
    async function selectStrategy(messages: Message[]): ContextTier {
        const tokens = await countTokens(messages);
    
        for (const tier of TIERS) {
            if (tokens <= tier.maxTokens) {
                return tier;
            }
        }
        return TIERS[TIERS.length - 1];
    }
    
    async function prepareContext(messages: Message[]): PreparedContext {
        const tier = await selectStrategy(messages);
    
        switch (tier.strategy) {
            case 'full':
                return { messages, model: tier.model };
    
            case 'summarize':
                const summary = await summarizeOldMessages(messages);
                return { messages: [summary, ...recentMessages(messages)], model: tier.model };
    
            case 'rag':
                const relevant = await retrieveRelevant(messages);
                return { messages: [...relevant, ...recentMessages(messages)], model: tier.model };
        }
    }
    

---
  #### **Name**
Serial Position Optimization
  #### **Description**
Place important content at start and end
  #### **When**
Constructing prompts with significant context
  #### **Example**
    // LLMs weight beginning and end more heavily
    // Structure prompts to leverage this
    
    function buildOptimalPrompt(components: {
        systemPrompt: string;
        criticalContext: string;
        conversationHistory: Message[];
        currentQuery: string;
    }): string {
        // START: System instructions (always first)
        const parts = [components.systemPrompt];
    
        // CRITICAL CONTEXT: Right after system (high primacy)
        if (components.criticalContext) {
            parts.push(`## Key Context\n${components.criticalContext}`);
        }
    
        // MIDDLE: Conversation history (lower weight)
        // Summarize if long, keep recent messages full
        const history = components.conversationHistory;
        if (history.length > 10) {
            const oldSummary = summarize(history.slice(0, -5));
            const recent = history.slice(-5);
            parts.push(`## Earlier Conversation (Summary)\n${oldSummary}`);
            parts.push(`## Recent Messages\n${formatMessages(recent)}`);
        } else {
            parts.push(`## Conversation\n${formatMessages(history)}`);
        }
    
        // END: Current query (high recency)
        // Restate critical requirements here
        parts.push(`## Current Request\n${components.currentQuery}`);
    
        // FINAL: Reminder of key constraints
        parts.push(`Remember: ${extractKeyConstraints(components.systemPrompt)}`);
    
        return parts.join('\n\n');
    }
    

---
  #### **Name**
Intelligent Summarization
  #### **Description**
Summarize by importance, not just recency
  #### **When**
Context exceeds optimal size
  #### **Example**
    interface MessageWithMetadata extends Message {
        importance: number;  // 0-1 score
        hasCriticalInfo: boolean;  // User preferences, decisions
        referenced: boolean;  // Was this referenced later?
    }
    
    async function smartSummarize(
        messages: MessageWithMetadata[],
        targetTokens: number
    ): Message[] {
        // Sort by importance, preserve order for tied scores
        const sorted = [...messages].sort((a, b) =>
            (b.importance + (b.hasCriticalInfo ? 0.5 : 0) + (b.referenced ? 0.3 : 0)) -
            (a.importance + (a.hasCriticalInfo ? 0.5 : 0) + (a.referenced ? 0.3 : 0))
        );
    
        const keep: Message[] = [];
        const summarizePool: Message[] = [];
        let currentTokens = 0;
    
        for (const msg of sorted) {
            const msgTokens = await countTokens([msg]);
            if (currentTokens + msgTokens < targetTokens * 0.7) {
                keep.push(msg);
                currentTokens += msgTokens;
            } else {
                summarizePool.push(msg);
            }
        }
    
        // Summarize the low-importance messages
        if (summarizePool.length > 0) {
            const summary = await llm.complete(`
                Summarize these messages, preserving:
                - Any user preferences or decisions
                - Key facts that might be referenced later
                - The overall flow of conversation
    
                Messages:
                ${formatMessages(summarizePool)}
            `);
    
            keep.unshift({ role: 'system', content: `[Earlier context: ${summary}]` });
        }
    
        // Restore original order
        return keep.sort((a, b) => a.timestamp - b.timestamp);
    }
    

---
  #### **Name**
Token Budget Allocation
  #### **Description**
Allocate token budget across context components
  #### **When**
Need predictable context management
  #### **Example**
    interface TokenBudget {
        system: number;      // System prompt
        criticalContext: number;  // User prefs, key info
        history: number;     // Conversation history
        query: number;       // Current query
        response: number;    // Reserved for response
    }
    
    function allocateBudget(totalTokens: number): TokenBudget {
        return {
            system: Math.floor(totalTokens * 0.10),      // 10%
            criticalContext: Math.floor(totalTokens * 0.15),  // 15%
            history: Math.floor(totalTokens * 0.40),     // 40%
            query: Math.floor(totalTokens * 0.10),       // 10%
            response: Math.floor(totalTokens * 0.25),    // 25%
        };
    }
    
    async function buildWithBudget(
        components: ContextComponents,
        modelMaxTokens: number
    ): PreparedContext {
        const budget = allocateBudget(modelMaxTokens);
    
        // Truncate/summarize each component to fit budget
        const prepared = {
            system: truncateToTokens(components.system, budget.system),
            criticalContext: truncateToTokens(
                components.criticalContext, budget.criticalContext
            ),
            history: await summarizeToTokens(components.history, budget.history),
            query: truncateToTokens(components.query, budget.query),
        };
    
        // Reallocate unused budget
        const used = await countTokens(Object.values(prepared).join('\n'));
        const remaining = modelMaxTokens - used - budget.response;
    
        if (remaining > 0) {
            // Give extra to history (most valuable for conversation)
            prepared.history = await summarizeToTokens(
                components.history,
                budget.history + remaining
            );
        }
    
        return prepared;
    }
    

## Anti-Patterns


---
  #### **Name**
Naive Truncation
  #### **Description**
Cutting off oldest messages when limit reached
  #### **Why**
Loses critical early context, breaks conversation flow
  #### **Instead**
Summarize old context, preserve critical information.

---
  #### **Name**
Ignoring Token Costs
  #### **Description**
Not tracking or optimizing token usage
  #### **Why**
Costs spiral, latency increases, context rot sets in
  #### **Instead**
Monitor tokens, set budgets, optimize continuously.

---
  #### **Name**
One-Size-Fits-All
  #### **Description**
Same context strategy for all conversations
  #### **Why**
Short conversations don't need RAG, long ones need summarization
  #### **Instead**
Adaptive strategies based on conversation characteristics.

---
  #### **Name**
Lost-in-Middle Placement
  #### **Description**
Putting critical info in middle of long prompts
  #### **Why**
LLMs underweight middle content (primacy/recency bias)
  #### **Instead**
Put critical info at start and end, summaries in middle.