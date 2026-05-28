# Context Window Management - Sharp Edges

## Context Rot

### **Id**
context-rot
### **Summary**
Long context degrades model accuracy and coherence
### **Severity**
high
### **Situation**
Model gives inconsistent or incorrect answers with large context
### **Why**
  Studies show accuracy drops after ~50K tokens.
  "Needle in a haystack" performance degrades.
  Models lose focus with too much context.
  
### **Solution**
  // Monitor context effectiveness, not just size
  
  class ContextHealthMonitor {
      // Track accuracy by context size
      private metrics: Map<string, { size: number; accuracy: number }[]> = new Map();
  
      async evaluate(
          context: string,
          query: string,
          expectedAnswer: string
      ): Promise<ContextHealth> {
          const tokens = await countTokens(context);
          const response = await llm.complete(context + '\n' + query);
          const accuracy = calculateAccuracy(response, expectedAnswer);
  
          // Store for analysis
          this.trackMetric(tokens, accuracy);
  
          // Alert if accuracy drops with size
          const trend = this.getAccuracyTrend();
          if (trend.degradation > 0.1) {
              console.warn(`Context rot detected: ${trend.degradation * 100}% accuracy drop`);
          }
  
          return {
              tokens,
              accuracy,
              recommendation: tokens > 50000 && accuracy < 0.8
                  ? 'Consider summarizing or using RAG'
                  : 'Context size appropriate'
          };
      }
  }
  
  // Set context size limits based on task
  const CONTEXT_LIMITS = {
      qa: 32000,       // Q&A works well with moderate context
      coding: 100000,  // Code benefits from more context
      chat: 16000,     // Casual chat needs less
      analysis: 50000, // Analysis benefits from focus
  };
  
### **Symptoms**
  - Answers become less accurate with more context
  - Model ignores earlier parts of context
  - Inconsistent responses to same questions
### **Detection Pattern**
context|token|length

## Lost In Middle

### **Id**
lost-in-middle
### **Summary**
Critical information in middle of context is ignored
### **Severity**
high
### **Situation**
Model misses important context placed in middle
### **Why**
  Primacy and recency bias in transformer attention.
  Beginning and end of context weighted more heavily.
  Long middle sections get underweighted.
  
### **Solution**
  // Structure context with position awareness
  
  function structureForAttention(components: {
      criticalFacts: string[];
      conversationHistory: Message[];
      currentTask: string;
  }): string {
      const parts: string[] = [];
  
      // START: Critical facts (high primacy)
      parts.push('## Key Information');
      for (const fact of components.criticalFacts) {
          parts.push(`- ${fact}`);
      }
  
      // MIDDLE: Less critical, summarized history
      if (components.conversationHistory.length > 0) {
          parts.push('\n## Conversation Context');
          // Summarize middle to reduce volume
          const summary = summarizeConversation(components.conversationHistory);
          parts.push(summary);
      }
  
      // END: Current task + repeat critical facts
      parts.push('\n## Current Task');
      parts.push(components.currentTask);
  
      // FINAL: Repeat most critical facts (high recency)
      parts.push('\n## Remember');
      for (const fact of components.criticalFacts.slice(0, 3)) {
          parts.push(`- ${fact}`);
      }
  
      return parts.join('\n');
  }
  
### **Symptoms**
  - Model ignores specific instructions
  - Critical context not reflected in responses
  - Works with short context, fails with long
### **Detection Pattern**
prompt|context|instruction

## Token Count Mismatch

### **Id**
token-count-mismatch
### **Summary**
Token count differs between tokenizers
### **Severity**
medium
### **Situation**
Context fits in testing but exceeds limit in production
### **Why**
  Different models use different tokenizers.
  Approximate counting leads to overflow.
  Special tokens not accounted for.
  
### **Solution**
  import { get_encoding } from 'tiktoken';
  
  // Use the CORRECT tokenizer for your model
  const TOKENIZERS = {
      'gpt-4': 'cl100k_base',
      'gpt-3.5-turbo': 'cl100k_base',
      'claude-3': 'claude',  // Anthropic tokenizer
  };
  
  async function countTokensAccurately(
      text: string,
      model: string
  ): Promise<number> {
      // For Claude, use the API's token counting
      if (model.startsWith('claude')) {
          const response = await anthropic.messages.count_tokens({
              model,
              messages: [{ role: 'user', content: text }]
          });
          return response.input_tokens;
      }
  
      // For OpenAI models
      const encoding = get_encoding(TOKENIZERS[model] || 'cl100k_base');
      const tokens = encoding.encode(text);
      return tokens.length;
  }
  
  // Add safety margin
  function maxSafeContext(modelLimit: number): number {
      // Leave 5% buffer for special tokens and counting variance
      return Math.floor(modelLimit * 0.95);
  }
  
### **Symptoms**
  - "Context too long" errors in production
  - Works with some inputs, fails with others
  - Token counts don't match API responses
### **Detection Pattern**
count.*token|token.*count|encoding

## Summarization Loss

### **Id**
summarization-loss
### **Summary**
Summarization loses critical details
### **Severity**
medium
### **Situation**
Important information lost when summarizing context
### **Why**
  Generic summarization prioritizes brevity over specifics.
  User-specific details often dropped.
  Numbers and names frequently lost.
  
### **Solution**
  // Preserve critical information during summarization
  
  async function summarizeWithPreservation(
      messages: Message[],
      preservePatterns: string[]
  ): Promise<string> {
      // Extract must-keep information
      const preserved: string[] = [];
      for (const msg of messages) {
          for (const pattern of preservePatterns) {
              const regex = new RegExp(pattern, 'gi');
              const matches = msg.content.match(regex);
              if (matches) {
                  preserved.push(...matches);
              }
          }
      }
  
      // Summarize with explicit preservation
      const summary = await llm.complete(`
          Summarize this conversation, but you MUST preserve these exact details:
          ${preserved.map(p => `- "${p}"`).join('\n')}
  
          Conversation:
          ${formatMessages(messages)}
  
          Preserve all:
          - Names and identifiers
          - Numbers and dates
          - User preferences and decisions
          - Technical specifications
      `);
  
      return summary;
  }
  
  // Common preservation patterns
  const PRESERVE_PATTERNS = [
      /\$[\d,]+/g,           // Money amounts
      /\d{4}-\d{2}-\d{2}/g,  // Dates
      /@\w+/g,               // Usernames
      /#\w+/g,               // IDs/hashtags
      /"\w+"/g,              // Quoted terms
  ];
  
### **Symptoms**
  - User has to repeat information
  - Numbers/names wrong after summarization
  - Context feels "lost" after compression
### **Detection Pattern**
summarize|compress|reduce