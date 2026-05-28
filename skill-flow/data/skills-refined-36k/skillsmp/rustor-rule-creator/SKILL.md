---
name: rustor-rule-creator
description: Create PHP refactoring rules for the rustor Rust project. Use when implementing new rules, converting PHP patterns to array_find/array_any/array_all, modernizing PHP syntax, or adding refactoring transformations. Automatically generates Rust code, tests, registers rules, and validates with cargo test.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
  - Edit
---

# Rustor Rule Creator

Efficiently implement PHP refactoring rules in the rustor project.

## Overview

Rustor is a PHP refactoring tool written in Rust. This skill helps you:
1. Design rule patterns from PHP code examples
2. Generate the Rust rule implementation
3. Register the rule in the system
4. Create comprehensive tests
5. Validate everything compiles and passes

## Workflow

### Step 1: Understand the Pattern

When given a PHP transformation, identify:
- **Before pattern**: The PHP code to match
- **After pattern**: The replacement PHP code
- **AST nodes involved**: FuncCall, Expression, Statement, etc.
- **Variables to capture**: Expressions that vary between instances

### Step 2: Generate Rule File

Create `crates/rustor-rules/src/{rule_name}.rs` with this structure:

```rust
//! Rule: {description}
//!
//! Pattern:
//! ```php
//! // Before
//! {before_php}
//!
//! // After
//! {after_php}
//! ```

use mago_span::{HasSpan, Span};
use mago_syntax::ast::*;
use rustor_core::Edit;

use crate::registry::{Category, PhpVersion, Rule};

pub fn check_{rule_name}<'a>(program: &Program<'a>, source: &str) -> Vec<Edit> {
    let mut checker = {RuleName}Checker {
        source,
        edits: Vec::new(),
    };
    checker.check_program(program);
    checker.edits
}

struct {RuleName}Checker<'s> {
    source: &'s str,
    edits: Vec<Edit>,
}

impl<'s> {RuleName}Checker<'s> {
    fn get_text(&self, span: Span) -> &str {
        &self.source[span.start.offset as usize..span.end.offset as usize]
    }

    fn check_program(&mut self, program: &Program<'_>) {
        self.check_statement_sequence(program.statements.as_slice());
    }

    fn check_statement(&mut self, stmt: &Statement<'_>) {
        // Recurse into nested structures
        match stmt {
            Statement::Function(func) => self.check_block(&func.body),
            Statement::Class(class) => {
                for member in class.members.iter() {
                    if let ClassLikeMember::Method(method) = member {
                        if let MethodBody::Concrete(ref body) = method.body {
                            self.check_block(body);
                        }
                    }
                }
            }
            Statement::Namespace(ns) => {
                let statements = match &ns.body {
                    NamespaceBody::Implicit(body) => &body.statements,
                    NamespaceBody::BraceDelimited(body) => &body.statements,
                };
                self.check_statement_sequence(statements.as_slice());
            }
            Statement::Block(block) => self.check_block(block),
            Statement::If(if_stmt) => self.check_if_body(&if_stmt.body),
            Statement::While(while_stmt) => self.check_while_body(&while_stmt.body),
            Statement::For(for_stmt) => self.check_for_body(&for_stmt.body),
            Statement::Foreach(foreach_stmt) => self.check_foreach_body(&foreach_stmt.body),
            Statement::Try(try_stmt) => {
                self.check_block(&try_stmt.block);
                for catch in try_stmt.catch_clauses.iter() {
                    self.check_block(&catch.block);
                }
                if let Some(finally) = &try_stmt.finally_clause {
                    self.check_block(&finally.block);
                }
            }
            _ => {}
        }
    }

    fn check_block(&mut self, block: &Block<'_>) {
        self.check_statement_sequence(block.statements.as_slice());
    }

    fn check_statement_sequence(&mut self, statements: &[Statement<'_>]) {
        for stmt in statements.iter() {
            self.check_statement(stmt);
        }
        // Add pattern detection across adjacent statements here
    }

    // Helper methods for control flow bodies
    fn check_if_body(&mut self, body: &IfBody<'_>) {
        match body {
            IfBody::Statement(stmt_body) => {
                self.check_statement(stmt_body.statement);
                for else_if in stmt_body.else_if_clauses.iter() {
                    self.check_statement(else_if.statement);
                }
                if let Some(else_clause) = &stmt_body.else_clause {
                    self.check_statement(else_clause.statement);
                }
            }
            IfBody::ColonDelimited(block) => {
                self.check_statement_sequence(block.statements.as_slice());
            }
        }
    }

    fn check_while_body(&mut self, body: &WhileBody<'_>) {
        match body {
            WhileBody::Statement(stmt) => self.check_statement(stmt),
            WhileBody::ColonDelimited(block) => self.check_statement_sequence(block.statements.as_slice()),
        }
    }

    fn check_for_body(&mut self, body: &ForBody<'_>) {
        match body {
            ForBody::Statement(stmt) => self.check_statement(stmt),
            ForBody::ColonDelimited(block) => self.check_statement_sequence(block.statements.as_slice()),
        }
    }

    fn check_foreach_body(&mut self, body: &ForeachBody<'_>) {
        match body {
            ForeachBody::Statement(stmt) => self.check_statement(stmt),
            ForeachBody::ColonDelimited(block) => self.check_statement_sequence(block.statements.as_slice()),
        }
    }
}

pub struct {RuleName}Rule;

impl Rule for {RuleName}Rule {
    fn name(&self) -> &'static str {
        "{rule_name}"
    }

    fn description(&self) -> &'static str {
        "{description}"
    }

    fn check<'a>(&self, program: &Program<'a>, source: &str) -> Vec<Edit> {
        check_{rule_name}(program, source)
    }

    fn category(&self) -> Category {
        Category::{category}
    }

    fn min_php_version(&self) -> Option<PhpVersion> {
        Some(PhpVersion::{php_version})
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use bumpalo::Bump;
    use mago_database::file::FileId;
    use rustor_core::apply_edits;

    fn check_php(source: &str) -> Vec<Edit> {
        let arena = Bump::new();
        let file_id = FileId::new("test.php");
        let (program, _) = mago_syntax::parser::parse_file_content(&arena, file_id, source);
        check_{rule_name}(program, source)
    }

    fn transform(source: &str) -> String {
        let edits = check_php(source);
        apply_edits(source, &edits).unwrap()
    }

    #[test]
    fn test_basic_pattern() {
        let source = r#"<?php
{test_before}
"#;
        let edits = check_php(source);
        assert_eq!(edits.len(), 1);
        let result = transform(source);
        assert!(result.contains("{test_after}"));
    }

    // Add skip cases for patterns that should NOT match
    #[test]
    fn test_skip_wrong_pattern() {
        let source = r#"<?php
{skip_case}
"#;
        let edits = check_php(source);
        assert_eq!(edits.len(), 0);
    }
}
```

### Step 3: Register the Rule

1. Add to `lib.rs`:
```rust
pub mod {rule_name};
pub use {rule_name}::check_{rule_name};
```

2. Add to `registry.rs`:
```rust
registry.register(Box::new(super::{rule_name}::{RuleName}Rule));
```

### Step 4: Run Tests

```bash
cargo test -p rustor-rules {rule_name} -- --nocapture
```

## AST Reference

### Common AST Patterns

| PHP Pattern | AST Node | Access |
|-------------|----------|--------|
| `func()` | `Expression::Call(Call::Function)` | `call.argument.arguments` |
| `$obj->method()` | `Expression::Call(Call::Method)` | `call.object`, `call.method` |
| `$var` | `Expression::Variable(Variable::Direct)` | `var.name` |
| `if (cond) {}` | `Statement::If` | `if_stmt.condition`, `if_stmt.body` |
| `foreach ($a as $v)` | `Statement::Foreach` | `foreach.expression`, `foreach.target` |
| `$a = $b` | `Expression::Assignment` | `assign.lhs`, `assign.rhs`, `assign.operator` |
| `true/false` | `Expression::Literal(Literal::True/False)` | direct match |
| `null` | `Expression::Literal(Literal::Null)` | direct match |

### Foreach Target

```rust
// Value only: foreach ($arr as $val)
let ForeachTarget::Value(value) = &foreach.target;

// Key-value: foreach ($arr as $key => $val)
let ForeachTarget::KeyValue(kv) = &foreach.target;
let key = &kv.key;    // Expression
let value = &kv.value; // Expression
```

### If Body Statements

```rust
fn get_if_body_statements<'a>(&self, body: &'a IfBody<'a>) -> Option<&'a [Statement<'a>]> {
    match body {
        IfBody::Statement(stmt_body) => {
            match stmt_body.statement {
                Statement::Block(ref block) => Some(block.statements.as_slice()),
                _ => None,
            }
        }
        IfBody::ColonDelimited(block) => Some(block.statements.as_slice()),
    }
}
```

### Helper Functions

```rust
// Get variable name without $
fn get_simple_variable_name(&self, expr: &Expression<'_>) -> Option<String> {
    if let Expression::Variable(Variable::Direct(var)) = expr {
        return Some(var.name.trim_start_matches('$').to_string());
    }
    None
}

// Check for literals
fn is_true_literal(&self, expr: &Expression<'_>) -> bool {
    matches!(expr, Expression::Literal(Literal::True(_)))
}

fn is_false_literal(&self, expr: &Expression<'_>) -> bool {
    matches!(expr, Expression::Literal(Literal::False(_)))
}

fn is_null_literal(&self, expr: &Expression<'_>) -> bool {
    matches!(expr, Expression::Literal(Literal::Null(_)))
}
```

## Categories and PHP Versions

| Category | Use For |
|----------|---------|
| `Performance` | Runtime optimizations |
| `Modernization` | New PHP syntax features |
| `Simplification` | Cleaner code |
| `Compatibility` | Best practices |

| PHP Version | Constant |
|-------------|----------|
| 5.4 | `Php54` |
| 7.0-7.4 | `Php70` - `Php74` |
| 8.0-8.4 | `Php80` - `Php84` |
| 8.5 | `Php85` |

## Multi-Statement Pattern Detection

For patterns spanning multiple statements (like foreach loops):

```rust
fn check_statement_sequence(&mut self, statements: &[Statement<'_>]) {
    // First, recurse into each statement
    for stmt in statements.iter() {
        self.check_statement(stmt);
    }

    // Then check patterns across adjacent statements
    for i in 0..statements.len() {
        // Pattern: prev_stmt + current_stmt
        if i > 0 {
            if let Some(edit) = self.check_pattern(&statements[i - 1], &statements[i]) {
                self.edits.push(edit);
            }
        }

        // Pattern: current_stmt + next_stmt
        if i + 1 < statements.len() {
            if let Some(edit) = self.check_pattern(&statements[i], &statements[i + 1]) {
                self.edits.push(edit);
            }
        }
    }
}
```

## Example: Foreach to Array Function

See these implemented rules for reference:
- `foreach_to_array_any.rs` - Boolean assignment + early return patterns
- `foreach_to_array_all.rs` - Negation handling
- `foreach_to_array_find.rs` - Null assignment pattern
- `foreach_to_array_find_key.rs` - Key-value iteration

## Execution Checklist

1. [ ] Create rule file in `crates/rustor-rules/src/`
2. [ ] Add `pub mod {name};` to `lib.rs`
3. [ ] Add `pub use {name}::check_{name};` to `lib.rs`
4. [ ] Register in `registry.rs`
5. [ ] Run `cargo test -p rustor-rules {name}`
6. [ ] Run `cargo build --release`
