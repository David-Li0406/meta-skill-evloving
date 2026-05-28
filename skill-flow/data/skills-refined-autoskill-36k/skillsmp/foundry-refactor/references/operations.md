# Refactoring Operations

## Rename Operation

**With LSP:**
1. Collect all reference locations from `findReferences`
2. Sort files by dependency order (imports first, then usages)
3. For each file:
   - Read file content
   - Replace symbol at LSP-provided positions (precise, not text search)
   - Write updated file
4. Verify rename succeeded:
   ```
   findReferences(file="src/module.py", symbol="NewClassName")
   # Should return same count as before
   ```

**Without LSP (Manual):**
1. Use Grep to find all occurrences
2. Review each match for false positives
3. Edit files one at a time
4. Verify with Grep that old name no longer appears

## Extract Function/Method

1. **Identify code block** to extract (line range)
2. **Analyze variables:**
   - Inputs: referenced but not defined in block
   - Outputs: defined in block, used after
3. **Create new function** with appropriate signature
4. **Replace original code** with function call
5. **Verify structure:**
   ```
   documentSymbol(file="src/module.py")
   # Confirm new function appears in symbols
   ```

## Move Symbol

1. **Find all references** to the symbol
2. **Move definition** to new file
3. **Add export** in new location (if needed)
4. **Update all imports** across codebase
5. **Remove from original** file
6. **Verify no broken references:**
   ```
   findReferences(file="new/location.py", symbol="MovedSymbol")
   # All references should resolve
   ```

## Dead Code Cleanup

1. **Identify candidate** symbols for removal
2. **Check reference count:**
   ```
   references = findReferences(file="src/utils.py", symbol="unused_function")

   if references.count == 0:
       Safe to remove
   elif references.count == 1 and reference is definition:
       Safe to remove (only self-reference)
   else:
       NOT safe - has usages
   ```
3. **Remove symbol** if safe
4. **Clean up imports** that referenced removed symbol
