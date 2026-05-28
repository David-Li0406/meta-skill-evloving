# Common Rule Patterns

This file contains concrete examples of pattern detection from implemented rules.

## Pattern 1: Boolean Assignment with Break

**PHP Pattern:**
```php
// Before
$found = false;
foreach ($items as $item) {
    if ($item > 10) {
        $found = true;
        break;
    }
}

// After
$found = array_any($items, fn($item) => $item > 10);
```

**Detection Logic:**
```rust
fn check_boolean_assignment_pattern(
    &self,
    prev_stmt: &Statement<'_>,
    foreach_stmt: &Statement<'_>,
) -> Option<Edit> {
    // 1. Previous statement must be: $var = false;
    let Statement::Expression(prev_expr_stmt) = prev_stmt else {
        return None;
    };
    let Expression::Assignment(prev_assign) = prev_expr_stmt.expression else {
        return None;
    };
    if !matches!(prev_assign.operator, AssignmentOperator::Assign(_)) {
        return None;
    }
    if !self.is_false_literal(&prev_assign.rhs) {
        return None;
    }
    let var_name = self.get_simple_variable_name(&prev_assign.lhs)?;

    // 2. Current statement must be foreach
    let Statement::Foreach(foreach) = foreach_stmt else {
        return None;
    };

    // 3. Foreach body must have exactly one statement (an if)
    let body_stmts = foreach.body.statements();
    if body_stmts.len() != 1 {
        return None;
    }

    // 4. Get the if statement (handle nested block)
    let if_stmt = self.get_if_from_statement(&body_stmts[0])?;

    // 5. If body must have: $var = true; break;
    let if_body_stmts = self.get_if_body_statements(&if_stmt.body)?;
    if if_body_stmts.len() != 2 {
        return None;
    }

    // Check assignment
    let Statement::Expression(assign_stmt) = &if_body_stmts[0] else {
        return None;
    };
    let Expression::Assignment(assign) = assign_stmt.expression else {
        return None;
    };
    if !self.is_true_literal(&assign.rhs) {
        return None;
    }
    let assigned_var = self.get_simple_variable_name(&assign.lhs)?;
    if assigned_var != var_name {
        return None;
    }

    // Check break
    let Statement::Break(break_stmt) = &if_body_stmts[1] else {
        return None;
    };

    // 6. Generate replacement
    let condition_source = self.get_text(if_stmt.condition.span());
    let value_var = self.get_foreach_value_var(foreach)?;
    let array_source = self.get_text(foreach.expression.span());

    let replacement = format!(
        "${} = array_any({}, fn({}) => {})",
        var_name, array_source, value_var, condition_source
    );

    // 7. Create span covering both statements
    let span = Span::new(
        prev_stmt.span().file_id,
        prev_stmt.span().start,
        foreach.span().end,
    );

    Some(Edit::new(span, replacement, "Convert foreach to array_any()"))
}
```

## Pattern 2: Early Return

**PHP Pattern:**
```php
// Before
foreach ($items as $item) {
    if ($item > 10) {
        return true;
    }
}
return false;

// After
return array_any($items, fn($item) => $item > 10);
```

**Detection Logic:**
```rust
fn check_early_return_pattern(
    &self,
    foreach_stmt: &Statement<'_>,
    next_stmt: &Statement<'_>,
) -> Option<Edit> {
    let Statement::Foreach(foreach) = foreach_stmt else {
        return None;
    };

    // Next statement must be return false;
    let Statement::Return(return_stmt) = next_stmt else {
        return None;
    };
    let return_value = return_stmt.value.as_ref()?;
    if !self.is_false_literal(return_value) {
        return None;
    }

    // Foreach body must have: if (cond) { return true; }
    let body_stmts = foreach.body.statements();
    if body_stmts.len() != 1 {
        return None;
    }

    let if_stmt = self.get_if_from_statement(&body_stmts[0])?;
    let if_body_stmts = self.get_if_body_statements(&if_stmt.body)?;
    if if_body_stmts.len() != 1 {
        return None;
    }

    let Statement::Return(inner_return) = &if_body_stmts[0] else {
        return None;
    };
    let inner_return_value = inner_return.value.as_ref()?;
    if !self.is_true_literal(inner_return_value) {
        return None;
    }

    // Generate replacement
    let condition_source = self.get_text(if_stmt.condition.span());
    let value_var = self.get_foreach_value_var(foreach)?;
    let array_source = self.get_text(foreach.expression.span());

    let replacement = format!(
        "return array_any({}, fn({}) => {})",
        array_source, value_var, condition_source
    );

    let span = Span::new(
        foreach.span().file_id,
        foreach.span().start,
        next_stmt.span().end,
    );

    Some(Edit::new(span, replacement, "Convert foreach to array_any()"))
}
```

## Pattern 3: Condition Negation (for array_all)

**PHP Pattern:**
```php
// Before - the condition is negated
$allMatch = true;
foreach ($items as $item) {
    if (!($item > 10)) {  // Negated condition
        $allMatch = false;
        break;
    }
}

// After - remove negation for array_all
$allMatch = array_all($items, fn($item) => $item > 10);
```

**Negation Handling:**
```rust
/// Negate a condition - if it starts with !, remove it; otherwise add !
fn negate_condition_source(&self, condition: &Expression<'_>) -> String {
    if let Expression::UnaryPrefix(unary) = condition {
        if let UnaryPrefixOperator::Not(_) = unary.operator {
            // Already negated, just return the inner expression
            return self.get_text(unary.operand.span()).to_string();
        }
    }
    // Not negated, add !
    format!("!({})", self.get_text(condition.span()))
}
```

## Pattern 4: Key-Value Foreach

**PHP Pattern:**
```php
// Before
$foundKey = null;
foreach ($items as $key => $item) {
    if ($item > 10) {
        $foundKey = $key;
        break;
    }
}

// After
$foundKey = array_find_key($items, fn($item) => $item > 10);
```

**Key-Value Detection:**
```rust
// Must have both key and value in foreach
let ForeachTarget::KeyValue(key_value) = &foreach.target else {
    return None;  // Skip if no key
};

// Get key variable name
let foreach_key_name = self.get_simple_variable_name(&key_value.key)?;

// Check that assignment uses the KEY (not value)
let assigned_value_name = self.get_simple_variable_name(&assign.rhs)?;
if assigned_value_name != foreach_key_name {
    return None;  // Assigns value, not key
}

// For the callback, use the VALUE variable
let value_var = self.get_variable_text(&key_value.value)?;
```

## Pattern 5: Function Call Replacement

**PHP Pattern:**
```php
// Before
is_null($x)

// After
$x === null
```

**Detection Logic:**
```rust
fn visit_expression(&mut self, expr: &Expression<'a>, _source: &str) -> bool {
    if let Expression::Call(Call::Function(call)) = expr {
        // Get function name
        let Expression::Identifier(ident) = call.function else {
            return true;
        };

        if ident.value.eq_ignore_ascii_case("is_null") {
            // Must have exactly 1 argument
            if call.argument.arguments.len() != 1 {
                return true;
            }

            let arg = &call.argument.arguments.as_slice()[0];
            let Argument::Positional(pos_arg) = arg else {
                return true;
            };

            let arg_text = self.get_text(pos_arg.value.span());
            let replacement = format!("{} === null", arg_text);

            self.edits.push(Edit::new(
                expr.span(),
                replacement,
                "Replace is_null() with === null comparison",
            ));
        }
    }
    true
}
```

## Helper: Get If from Statement (Handle Nested Blocks)

```rust
fn get_if_from_statement<'a>(&self, stmt: &'a Statement<'a>) -> Option<&'a If<'a>> {
    match stmt {
        Statement::If(if_stmt) => Some(if_stmt),
        Statement::Block(block) => {
            let stmts = block.statements.as_slice();
            if stmts.len() == 1 {
                if let Statement::If(if_stmt) = &stmts[0] {
                    return Some(if_stmt);
                }
            }
            None
        }
        _ => None,
    }
}
```

## Helper: Get Variable Text with $ prefix

```rust
fn get_variable_text(&self, expr: &Expression<'_>) -> Option<String> {
    if let Expression::Variable(Variable::Direct(var)) = expr {
        return Some(format!("${}", var.name.trim_start_matches('$')));
    }
    None
}
```
