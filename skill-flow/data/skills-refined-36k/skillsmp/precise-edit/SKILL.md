---
name: precise-edit
description: Edit code at symbol level using AG4ONE Serena integration
argument-hint: "<symbol> <action>"
allowed-tools: [Read, Write, serena_insert_after_symbol, serena_replace_symbol_body, serena_find_symbol]
platforms: [opencode,claude,gemini]
---

<objective>
Perform precise, symbol-level code edits using AG4ONE Serena integration for targeted modifications without full file rewrites.

</objective>

<execution_context>
@ag4one/serena/semantic-analysis.md
@AG4-STYLE.md
@.planning/STATE.md
</execution_context>

<context>
Target symbol: $ARGUMENT_1
Edit action: $ARGUMENT_2
Platform: $PLATFORM
Available tools: Serena symbol manipulation suite
</context>

<process>
1. **Symbol Identification**
   - Use Serena to locate exact symbol and its context
   - Verify symbol type (class, function, method, variable)
   - Understand current implementation and relationships

2. **Precise Edit Execution**
   - For insertions: Use serena_insert_after_symbol
   - For replacements: Use serena_replace_symbol_body
   - For additions: Use appropriate Serena tool
   - Preserve surrounding code context

3. **Impact Validation**
   - Use Serena to find all symbol references
   - Verify no broken dependencies after edit
   - Update related components if needed

4. **Quality Assurance**
   - Validate syntax and semantics after edit
   - Run type checking if applicable
   - Update documentation and comments
</process>

<success_criteria>
- [ ] Symbol located and context understood
- [ ] Precise edit completed with Serena tools
- [ ] All symbol references remain valid
- [ ] No broken dependencies introduced
- [ ] Code quality checks pass
- [ ] Changes documented appropriately
</success_criteria>