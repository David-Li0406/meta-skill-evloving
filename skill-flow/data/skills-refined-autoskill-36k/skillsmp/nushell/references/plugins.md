# Nushell Plugin Development

Nushell plugins are standalone Rust executables that extend Nushell with custom commands.

## Quick Start

### 1. Create Plugin Project

```bash
# Use template script
python3 scripts/init_plugin.py <plugin-name>

# OR manually
cargo new nu_plugin_<name>
cd nu_plugin_<name>
cargo add nu-plugin nu-protocol
```

### 2. Basic Plugin Structure

```rust
use nu_plugin::{EvaluatedCall, MsgPackSerializer, serve_plugin};
use nu_plugin::{EngineInterface, Plugin, PluginCommand, SimplePluginCommand};
use nu_protocol::{LabeledError, Signature, Type, Value};

struct MyPlugin;

impl Plugin for MyPlugin {
    fn version(&self) -> String {
        env!("CARGO_PKG_VERSION").into()
    }

    fn commands(&self) -> Vec<Box<dyn PluginCommand<Plugin = Self>>> {
        vec![Box::new(MyCommand)]
    }
}

struct MyCommand;

impl SimplePluginCommand for MyCommand {
    type Plugin = MyPlugin;

    fn name(&self) -> &str { "my-command" }

    fn signature(&self) -> Signature {
        Signature::build("my-command")
            .input_output_type(Type::String, Type::Int)
    }

    fn run(
        &self,
        _plugin: &MyPlugin,
        _engine: &EngineInterface,
        call: &EvaluatedCall,
        input: &Value,
    ) -> Result<Value, LabeledError> {
        match input {
            Value::String { val, .. } => {
                Ok(Value::int(val.len() as i64, call.head))
            }
            _ => Err(LabeledError::new("Expected string input")
                .with_label("requires string", call.head))
        }
    }
}

fn main() {
    serve_plugin(&MyPlugin, MsgPackSerializer)
}
```

### 3. Build and Install

```bash
cargo build --release
cargo install --path . --locked
plugin add ~/.cargo/bin/nu_plugin_<name>  # .exe on Windows
plugin use <name>
"hello" | my-command
```

______________________________________________________________________

## Command Types

### SimplePluginCommand

For commands that operate on single values:

- Input: `&Value`
- Output: `Result<Value, LabeledError>`
- Use for: transformations, simple filters, single value operations

### PluginCommand

For commands that handle streams:

- Input: `PipelineData`
- Output: `Result<PipelineData, LabeledError>`
- Use for: streaming transformations, lazy processing, large datasets

______________________________________________________________________

## Defining Command Signatures

### Input-Output Types

```rust
use nu_protocol::{Signature, Type};

Signature::build("my-command")
    .input_output_type(Type::String, Type::Int)
```

Common types: `String`, `Int`, `Float`, `Bool`, `List(Box<Type>)`, `Record(...)`, `Any`

### Parameters

```rust
Signature::build("my-command")
    .named("output", SyntaxShape::Filepath, "output file", Some('o'))
    .switch("verbose", "enable verbose output", Some('v'))
    .required("input", SyntaxShape::String, "input value")
    .optional("count", SyntaxShape::Int, "repeat count")
    .rest("files", SyntaxShape::Filepath, "files to process")
```

### Accessing Arguments

```rust
fn run(&self, call: &EvaluatedCall, ...) -> Result<Value, LabeledError> {
    let output: Option<String> = call.get_flag("output")?;
    let verbose: bool = call.has_flag("verbose")?;
    let input: String = call.req(0)?;
    let count: Option<i64> = call.opt(1)?;
    let files: Vec<String> = call.rest(2)?;
}
```

______________________________________________________________________

## Error Handling

Always return `LabeledError` with span information:

```rust
Err(LabeledError::new("Error message")
    .with_label("specific issue", call.head))
```

______________________________________________________________________

## Serialization

`MsgPackSerializer` (Recommended) - Binary format, faster, use for production.

`JsonSerializer` - Text-based, useful for debugging.

```rust
serve_plugin(&MyPlugin, MsgPackSerializer)  // Production
// serve_plugin(&MyPlugin, JsonSerializer)  // Debug
```

______________________________________________________________________

## Common Patterns

### String Transformation

```rust
Value::String { val, .. } => {
    Ok(Value::string(val.to_uppercase(), call.head))
}
```

### List Generation

```rust
let items = vec![
    Value::string("a", call.head),
    Value::string("b", call.head),
];
Ok(Value::list(items, call.head))
```

### Record (Table Row)

```rust
use nu_protocol::record;

Ok(Value::record(
    record! {
        "name" => Value::string("example", call.head),
        "size" => Value::int(42, call.head),
    },
    call.head,
))
```

### Table (List of Records)

```rust
let records = vec![
    Value::record(record! { "name" => Value::string("a", span) }, span),
    Value::record(record! { "name" => Value::string("b", span) }, span),
];
Ok(Value::list(records, call.head))
```

______________________________________________________________________

## Streaming with PipelineData

```rust
use nu_plugin::PluginCommand;
use nu_protocol::{PipelineData, ListStream};

impl PluginCommand for MyStreamingCommand {
    type Plugin = MyPlugin;

    fn run(
        &self,
        plugin: &MyPlugin,
        engine: &EngineInterface,
        call: &EvaluatedCall,
        input: PipelineData,
    ) -> Result<PipelineData, LabeledError> {
        let result = input.into_iter().map(|value| {
            process_value(value, call.head)
        });

        Ok(PipelineData::ListStream(
            ListStream::new(result, call.head, None),
            None
        ))
    }
}
```

### PipelineData Variants

- `PipelineData::Empty` - No data
- `PipelineData::Value(value, None)` - Single value
- `PipelineData::ListStream(stream, None)` - Stream of values (lazy)
- `PipelineData::ByteStream(stream, None)` - Raw byte stream

______________________________________________________________________

## Engine Interface

```rust
// Environment variables
engine.add_env_var("MY_VAR", Value::string("value", span))?;
let home = engine.get_env_var("HOME")?;

// Configuration
let config = engine.get_config()?;
let plugin_config = engine.get_plugin_config()?;  // $env.config.plugins.PLUGIN_NAME

// Current directory
let current_dir = engine.get_current_dir()?;

// Evaluation
let result = engine.eval("ls | length")?;
```

______________________________________________________________________

## Custom Values

Define custom data types with `#[typetag::serde]`:

```rust
use nu_protocol::{CustomValue, ShellError, Span, Value};
use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, Serialize, Deserialize)]
struct MyCustomValue { data: String }

#[typetag::serde]  // Required for plugin serialization
impl CustomValue for MyCustomValue {
    fn clone_value(&self, span: Span) -> Value {
        Value::custom(Box::new(self.clone()), span)
    }
    fn type_name(&self) -> String { "MyCustomType".to_string() }
    fn to_base_value(&self, span: Span) -> Result<Value, ShellError> {
        Ok(Value::string(&self.data, span))
    }
    fn as_any(&self) -> &dyn std::any::Any { self }
    fn as_mut_any(&mut self) -> &mut dyn std::any::Any { self }
}
```

Add `typetag = "0.2"` to Cargo.toml.

______________________________________________________________________

## Development Workflow

### Iterative Development

```bash
cargo build
plugin add target/debug/nu_plugin_<name>
plugin use <name>
"test" | my-command

# After changes
plugin rm <name>
plugin add target/debug/nu_plugin_<name>
plugin use <name>
```

### Automated Testing

```toml
[dev-dependencies]
nu-plugin-test-support = "0.109.1"
```

```rust
#[cfg(test)]
mod tests {
    use nu_plugin_test_support::PluginTest;

    #[test]
    fn test_command() -> Result<(), nu_protocol::ShellError> {
        PluginTest::new("myplugin", MyPlugin.into())?
            .test_examples(&MyCommand)
    }
}
```

______________________________________________________________________

## Debugging

1. Use `JsonSerializer` temporarily to inspect protocol messages
2. Log to file (plugins can't use stdout/stderr):
   ```rust
   fn debug_log(msg: &str) {
       std::fs::OpenOptions::new()
           .create(true).append(true)
           .open("/tmp/myplugin.log").unwrap()
           .write_all(format!("{}\n", msg).as_bytes()).ok();
   }
   ```
3. Run with backtrace: `RUST_BACKTRACE=1 nu`
4. Check registration: `plugin list | where name == myplugin`

______________________________________________________________________

## Common Issues

| Problem               | Solution                                              |
| --------------------- | ----------------------------------------------------- |
| Plugin not found      | Use absolute path, check binary name is `nu_plugin_*` |
| Changes not reflected | `plugin rm` then `plugin add` again, or restart nu    |
| "Plugin panicked"     | Add file logging, check for unwrap() calls            |
| Path not found        | Use `engine.get_current_dir()?.join(path)`            |

______________________________________________________________________

## Important Constraints

- Stdio reserved: Plugins can't use stdin/stdout (protocol uses them)
- Path handling: Always resolve relative to `engine.get_current_dir()`
- Version match: `nu-plugin` and `nu-protocol` versions must match target Nushell

______________________________________________________________________

## Multi-Command Plugin

```rust
impl Plugin for MathPlugin {
    fn commands(&self) -> Vec<Box<dyn PluginCommand<Plugin = Self>>> {
        vec![
            Box::new(Add),
            Box::new(Multiply),
            Box::new(Power),
        ]
    }
}

struct Add;
impl SimplePluginCommand for Add {
    fn name(&self) -> &str { "math add" }
    // ...
}
```

______________________________________________________________________

## External Resources

- [Official Plugin Guide](https://www.nushell.sh/contributor-book/plugins.html)
- [nu-plugin API Docs](https://docs.rs/nu-plugin/latest/nu_plugin/)
- [Plugin Examples Repository](https://github.com/nushell/plugin-examples)
- [Awesome Nu](https://github.com/nushell/awesome-nu) - Community plugins
- [nushellWith](https://github.com/YPares/nushellWith) - Nix flake for reproducible plugin environments
