# Conversation Memory

## Patterns


---
  #### **Name**
Tiered Memory System
  #### **Description**
Different memory tiers for different purposes
  #### **When**
Building any conversational AI
  #### **Example**
    interface MemorySystem {
        // Buffer: Current conversation (in context)
        buffer: ConversationBuffer;
    
        // Short-term: Recent interactions (session)
        shortTerm: ShortTermMemory;
    
        // Long-term: Persistent across sessions
        longTerm: LongTermMemory;
    
        // Entity: Facts about people, places, things
        entity: EntityMemory;
    }
    
    class TieredMemory implements MemorySystem {
        async addMessage(message: Message): Promise<void> {
            // Always add to buffer
            this.buffer.add(message);
    
            // Extract entities
            const entities = await extractEntities(message);
            for (const entity of entities) {
                await this.entity.upsert(entity);
            }
    
            // Check for memorable content
            if (await isMemoryWorthy(message)) {
                await this.shortTerm.add({
                    content: message.content,
                    timestamp: Date.now(),
                    importance: await scoreImportance(message)
                });
            }
        }
    
        async consolidate(): Promise<void> {
            // Move important short-term to long-term
            const memories = await this.shortTerm.getOld(24 * 60 * 60 * 1000);
            for (const memory of memories) {
                if (memory.importance > 0.7 || memory.referenced > 2) {
                    await this.longTerm.add(memory);
                }
                await this.shortTerm.remove(memory.id);
            }
        }
    
        async buildContext(query: string): Promise<string> {
            const parts: string[] = [];
    
            // Relevant long-term memories
            const longTermRelevant = await this.longTerm.search(query, 3);
            if (longTermRelevant.length) {
                parts.push('## Relevant Memories\n' +
                    longTermRelevant.map(m => `- ${m.content}`).join('\n'));
            }
    
            // Relevant entities
            const entities = await this.entity.getRelevant(query);
            if (entities.length) {
                parts.push('## Known Entities\n' +
                    entities.map(e => `- ${e.name}: ${e.facts.join(', ')}`).join('\n'));
            }
    
            // Recent conversation
            const recent = this.buffer.getRecent(10);
            parts.push('## Recent Conversation\n' + formatMessages(recent));
    
            return parts.join('\n\n');
        }
    }
    

---
  #### **Name**
Entity Memory
  #### **Description**
Store and update facts about entities
  #### **When**
Need to remember details about people, places, things
  #### **Example**
    interface Entity {
        id: string;
        name: string;
        type: 'person' | 'place' | 'thing' | 'concept';
        facts: Fact[];
        lastMentioned: number;
        mentionCount: number;
    }
    
    interface Fact {
        content: string;
        confidence: number;
        source: string;  // Which message this came from
        timestamp: number;
    }
    
    class EntityMemory {
        async extractAndStore(message: Message): Promise<void> {
            // Use LLM to extract entities and facts
            const extraction = await llm.complete(`
                Extract entities and facts from this message.
                Return JSON: { "entities": [
                    { "name": "...", "type": "...", "facts": ["..."] }
                ]}
    
                Message: "${message.content}"
            `);
    
            const { entities } = JSON.parse(extraction);
            for (const entity of entities) {
                await this.upsert(entity, message.id);
            }
        }
    
        async upsert(entity: ExtractedEntity, sourceId: string): Promise<void> {
            const existing = await this.store.get(entity.name.toLowerCase());
    
            if (existing) {
                // Merge facts, avoiding duplicates
                for (const fact of entity.facts) {
                    if (!this.hasSimilarFact(existing.facts, fact)) {
                        existing.facts.push({
                            content: fact,
                            confidence: 0.9,
                            source: sourceId,
                            timestamp: Date.now()
                        });
                    }
                }
                existing.lastMentioned = Date.now();
                existing.mentionCount++;
                await this.store.set(existing.id, existing);
            } else {
                // Create new entity
                await this.store.set(entity.name.toLowerCase(), {
                    id: generateId(),
                    name: entity.name,
                    type: entity.type,
                    facts: entity.facts.map(f => ({
                        content: f,
                        confidence: 0.9,
                        source: sourceId,
                        timestamp: Date.now()
                    })),
                    lastMentioned: Date.now(),
                    mentionCount: 1
                });
            }
        }
    }
    

---
  #### **Name**
Memory-Aware Prompting
  #### **Description**
Include relevant memories in prompts
  #### **When**
Making LLM calls with memory context
  #### **Example**
    async function promptWithMemory(
        query: string,
        memory: MemorySystem,
        systemPrompt: string
    ): Promise<string> {
        // Retrieve relevant memories
        const relevantMemories = await memory.longTerm.search(query, 5);
        const entities = await memory.entity.getRelevant(query);
        const recentContext = memory.buffer.getRecent(5);
    
        // Build memory-augmented prompt
        const prompt = `
    ${systemPrompt}
    
    ## User Context
    ${entities.length ? `Known about user:\n${entities.map(e =>
        `- ${e.name}: ${e.facts.map(f => f.content).join('; ')}`
    ).join('\n')}` : ''}
    
    ${relevantMemories.length ? `Relevant past interactions:\n${relevantMemories.map(m =>
        `- [${formatDate(m.timestamp)}] ${m.content}`
    ).join('\n')}` : ''}
    
    ## Recent Conversation
    ${formatMessages(recentContext)}
    
    ## Current Query
    ${query}
        `.trim();
    
        const response = await llm.complete(prompt);
    
        // Extract any new memories from response
        await memory.addMessage({ role: 'assistant', content: response });
    
        return response;
    }
    

## Anti-Patterns


---
  #### **Name**
Remember Everything
  #### **Description**
Storing every message as a memory
  #### **Why**
Overwhelms context, increases costs, reduces relevance
  #### **Instead**
Filter for memorable content based on importance scoring.

---
  #### **Name**
No Memory Retrieval
  #### **Description**
Storing memories but not surfacing them
  #### **Why**
Stored memories useless if never retrieved
  #### **Instead**
Search and include relevant memories in every prompt.

---
  #### **Name**
Single Memory Store
  #### **Description**
One flat list for all memories
  #### **Why**
Can't distinguish importance, type, or recency
  #### **Instead**
Tiered memory with different stores for different purposes.

---
  #### **Name**
No Consolidation
  #### **Description**
Never processing short-term into long-term
  #### **Why**
Short-term overflows, important memories lost
  #### **Instead**
Regular consolidation based on importance and age.