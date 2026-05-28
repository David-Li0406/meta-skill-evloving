# CLI and TUI Development in Rust

Guide to building command-line interfaces and terminal user interfaces with Clap and Ratatui.

## CLI with Clap

### Basic Setup

```toml
[dependencies]
clap = { version = "4.5", features = ["derive"] }
```

### Simple CLI

```rust
use clap::Parser;

#[derive(Parser)]
#[command(name = "myapp")]
#[command(about = "A simple CLI application", long_about = None)]
struct Cli {
    /// Input file to process
    #[arg(short, long)]
    input: String,

    /// Output file
    #[arg(short, long)]
    output: Option<String>,

    /// Verbose output
    #[arg(short, long)]
    verbose: bool,
}

fn main() {
    let cli = Cli::parse();

    println!("Input: {}", cli.input);
    if let Some(output) = cli.output {
        println!("Output: {}", output);
    }
    if cli.verbose {
        println!("Verbose mode enabled");
    }
}
```

### Subcommands

```rust
use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "git-like")]
#[command(about = "A git-like CLI", long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Add files to staging
    Add {
        /// Files to add
        files: Vec<String>,
    },
    /// Commit staged changes
    Commit {
        /// Commit message
        #[arg(short, long)]
        message: String,

        /// Amend previous commit
        #[arg(long)]
        amend: bool,
    },
    /// Push commits to remote
    Push {
        /// Remote name
        remote: Option<String>,

        /// Branch name
        branch: Option<String>,
    },
}

fn main() {
    let cli = Cli::parse();

    match cli.command {
        Commands::Add { files } => {
            println!("Adding files: {:?}", files);
        }
        Commands::Commit { message, amend } => {
            println!("Committing: {}", message);
            if amend {
                println!("Amending previous commit");
            }
        }
        Commands::Push { remote, branch } => {
            println!("Pushing to {:?}/{:?}", remote, branch);
        }
    }
}
```

### Value Validation

```rust
use clap::Parser;

fn validate_port(s: &str) -> Result<u16, String> {
    let port: u16 = s.parse()
        .map_err(|_| format!("`{s}` isn't a valid port number"))?;

    if port < 1024 {
        return Err("Port must be >= 1024".to_string());
    }

    Ok(port)
}

#[derive(Parser)]
struct Cli {
    /// Port to listen on
    #[arg(short, long, value_parser = validate_port)]
    port: u16,

    /// Number of workers
    #[arg(short = 'w', long, default_value = "4")]
    workers: usize,

    /// Log level
    #[arg(long, value_enum)]
    log_level: LogLevel,
}

#[derive(clap::ValueEnum, Clone)]
enum LogLevel {
    Debug,
    Info,
    Warn,
    Error,
}
```

### Environment Variables

```rust
#[derive(Parser)]
struct Cli {
    /// Database URL
    #[arg(long, env = "DATABASE_URL")]
    database_url: String,

    /// API key
    #[arg(long, env = "API_KEY")]
    api_key: String,
}
```

### Argument Groups

```rust
use clap::{ArgGroup, Parser};

#[derive(Parser)]
#[command(group = ArgGroup::new("output").required(true).args(&["stdout", "file"]))]
struct Cli {
    /// Write to stdout
    #[arg(long)]
    stdout: bool,

    /// Write to file
    #[arg(long)]
    file: Option<String>,
}
```

### Rich Help Text

```rust
#[derive(Parser)]
#[command(author, version, about, long_about = None)]
#[command(next_line_help = true)]
struct Cli {
    /// Input files to process.
    ///
    /// Can be specified multiple times.
    /// Supports glob patterns.
    #[arg(short, long)]
    input: Vec<String>,

    /// Output format
    #[arg(short = 'f', long, default_value = "json")]
    #[arg(help = "Output format (json, yaml, toml)")]
    format: String,
}
```

## Advanced CLI Patterns

### Progress Bars

```toml
[dependencies]
indicatif = "0.17"
```

```rust
use indicatif::{ProgressBar, ProgressStyle};
use std::time::Duration;

fn process_files(files: Vec<String>) {
    let pb = ProgressBar::new(files.len() as u64);
    pb.set_style(
        ProgressStyle::default_bar()
            .template("{spinner:.green} [{elapsed_precise}] [{bar:40.cyan/blue}] {pos}/{len} ({eta})")
            .unwrap()
            .progress_chars("#>-"),
    );

    for file in files {
        process_file(&file);
        pb.inc(1);
    }

    pb.finish_with_message("Done!");
}
```

### Colored Output

```toml
[dependencies]
colored = "2.1"
```

```rust
use colored::*;

fn main() {
    println!("{}", "Success!".green());
    println!("{}", "Warning!".yellow());
    println!("{}", "Error!".red().bold());

    println!("{} {} {}",
        "Info:".cyan(),
        "Processing".white(),
        file.blue()
    );
}
```

### Interactive Prompts

```toml
[dependencies]
dialoguer = "0.11"
```

```rust
use dialoguer::{Input, Confirm, Select};

fn main() {
    // Text input
    let name: String = Input::new()
        .with_prompt("Your name")
        .interact()
        .unwrap();

    // Confirmation
    if Confirm::new()
        .with_prompt("Continue?")
        .interact()
        .unwrap()
    {
        println!("Continuing...");
    }

    // Selection
    let items = vec!["Option 1", "Option 2", "Option 3"];
    let selection = Select::new()
        .with_prompt("Choose an option")
        .items(&items)
        .interact()
        .unwrap();

    println!("You selected: {}", items[selection]);
}
```

## TUI with Ratatui

### Basic Setup

```toml
[dependencies]
ratatui = "0.26"
crossterm = "0.27"
```

### Hello World TUI

```rust
use std::io;
use ratatui::{
    backend::CrosstermBackend,
    widgets::{Block, Borders, Paragraph},
    Terminal,
};
use crossterm::{
    event::{self, Event, KeyCode},
    terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen},
    ExecutableCommand,
};

fn main() -> io::Result<()> {
    enable_raw_mode()?;
    let mut stdout = io::stdout();
    stdout.execute(EnterAlternateScreen)?;

    let backend = CrosstermBackend::new(stdout);
    let mut terminal = Terminal::new(backend)?;

    loop {
        terminal.draw(|f| {
            let size = f.size();
            let block = Block::default()
                .title("Hello, Ratatui!")
                .borders(Borders::ALL);
            let paragraph = Paragraph::new("Press 'q' to quit")
                .block(block);
            f.render_widget(paragraph, size);
        })?;

        if let Event::Key(key) = event::read()? {
            if key.code == KeyCode::Char('q') {
                break;
            }
        }
    }

    disable_raw_mode()?;
    io::stdout().execute(LeaveAlternateScreen)?;

    Ok(())
}
```

### Application State

```rust
struct App {
    counter: i32,
    should_quit: bool,
}

impl App {
    fn new() -> App {
        App {
            counter: 0,
            should_quit: false,
        }
    }

    fn on_tick(&mut self) {
        self.counter += 1;
    }

    fn on_key(&mut self, c: char) {
        match c {
            'q' => self.should_quit = true,
            'j' => self.counter += 1,
            'k' => self.counter -= 1,
            _ => {}
        }
    }
}

fn run_app(terminal: &mut Terminal<impl Backend>, mut app: App) -> io::Result<()> {
    loop {
        terminal.draw(|f| ui(f, &app))?;

        if let Event::Key(key) = event::read()? {
            if let KeyCode::Char(c) = key.code {
                app.on_key(c);
            }
        }

        if app.should_quit {
            return Ok(());
        }
    }
}

fn ui(f: &mut Frame, app: &App) {
    let size = f.size();

    let block = Block::default()
        .title("Counter")
        .borders(Borders::ALL);

    let text = format!("Count: {} (j/k to change, q to quit)", app.counter);
    let paragraph = Paragraph::new(text).block(block);

    f.render_widget(paragraph, size);
}
```

### Layouts

```rust
use ratatui::layout::{Layout, Constraint, Direction};

fn ui(f: &mut Frame, app: &App) {
    let chunks = Layout::default()
        .direction(Direction::Vertical)
        .constraints([
            Constraint::Length(3),      // Header
            Constraint::Min(0),          // Body
            Constraint::Length(3),       // Footer
        ])
        .split(f.size());

    let header = Paragraph::new("Header")
        .block(Block::default().borders(Borders::ALL));
    f.render_widget(header, chunks[0]);

    let body = Paragraph::new("Body")
        .block(Block::default().borders(Borders::ALL));
    f.render_widget(body, chunks[1]);

    let footer = Paragraph::new("Footer")
        .block(Block::default().borders(Borders::ALL));
    f.render_widget(footer, chunks[2]);
}
```

### Lists

```rust
use ratatui::widgets::{List, ListItem, ListState};

struct StatefulList {
    state: ListState,
    items: Vec<String>,
}

impl StatefulList {
    fn new(items: Vec<String>) -> StatefulList {
        StatefulList {
            state: ListState::default(),
            items,
        }
    }

    fn next(&mut self) {
        let i = match self.state.selected() {
            Some(i) => {
                if i >= self.items.len() - 1 {
                    0
                } else {
                    i + 1
                }
            }
            None => 0,
        };
        self.state.select(Some(i));
    }

    fn previous(&mut self) {
        let i = match self.state.selected() {
            Some(i) => {
                if i == 0 {
                    self.items.len() - 1
                } else {
                    i - 1
                }
            }
            None => 0,
        };
        self.state.select(Some(i));
    }
}

fn ui(f: &mut Frame, list: &mut StatefulList) {
    let items: Vec<ListItem> = list
        .items
        .iter()
        .map(|i| ListItem::new(i.as_str()))
        .collect();

    let list_widget = List::new(items)
        .block(Block::default().title("List").borders(Borders::ALL))
        .highlight_style(Style::default().bg(Color::Yellow))
        .highlight_symbol(">> ");

    f.render_stateful_widget(list_widget, f.size(), &mut list.state);
}
```

### Tables

```rust
use ratatui::widgets::{Table, Row, Cell};
use ratatui::style::{Style, Color, Modifier};

fn ui(f: &mut Frame) {
    let rows = vec![
        Row::new(vec!["Row1", "Data1", "Info1"]),
        Row::new(vec!["Row2", "Data2", "Info2"]),
        Row::new(vec!["Row3", "Data3", "Info3"]),
    ];

    let table = Table::new(rows, vec![
        Constraint::Percentage(33),
        Constraint::Percentage(33),
        Constraint::Percentage(33),
    ])
    .header(
        Row::new(vec!["Name", "Data", "Info"])
            .style(Style::default().fg(Color::Yellow))
            .bottom_margin(1),
    )
    .block(Block::default().title("Table").borders(Borders::ALL))
    .highlight_style(Style::default().add_modifier(Modifier::BOLD))
    .highlight_symbol(">> ");

    f.render_widget(table, f.size());
}
```

### Charts

```rust
use ratatui::widgets::{Chart, Axis, Dataset, GraphType};
use ratatui::symbols;

fn ui(f: &mut Frame, data: &[(f64, f64)]) {
    let datasets = vec![
        Dataset::default()
            .name("data")
            .marker(symbols::Marker::Dot)
            .graph_type(GraphType::Line)
            .style(Style::default().fg(Color::Cyan))
            .data(data),
    ];

    let chart = Chart::new(datasets)
        .block(Block::default().title("Chart").borders(Borders::ALL))
        .x_axis(
            Axis::default()
                .title("X Axis")
                .style(Style::default().fg(Color::Gray))
                .bounds([0.0, 100.0])
                .labels(vec!["0", "50", "100"]),
        )
        .y_axis(
            Axis::default()
                .title("Y Axis")
                .style(Style::default().fg(Color::Gray))
                .bounds([0.0, 100.0])
                .labels(vec!["0", "50", "100"]),
        );

    f.render_widget(chart, f.size());
}
```

## Common Patterns

### Config File Handling

```toml
[dependencies]
serde = { version = "1.0", features = ["derive"] }
toml = "0.8"
dirs = "5.0"
```

```rust
use serde::{Deserialize, Serialize};
use std::fs;
use std::path::PathBuf;

#[derive(Serialize, Deserialize)]
struct Config {
    database_url: String,
    log_level: String,
}

impl Config {
    fn load() -> Result<Self, Box<dyn std::error::Error>> {
        let config_path = dirs::config_dir()
            .ok_or("Could not find config directory")?
            .join("myapp")
            .join("config.toml");

        let contents = fs::read_to_string(config_path)?;
        let config: Config = toml::from_str(&contents)?;

        Ok(config)
    }

    fn save(&self) -> Result<(), Box<dyn std::error::Error>> {
        let config_dir = dirs::config_dir()
            .ok_or("Could not find config directory")?
            .join("myapp");

        fs::create_dir_all(&config_dir)?;

        let toml = toml::to_string_pretty(self)?;
        fs::write(config_dir.join("config.toml"), toml)?;

        Ok(())
    }
}
```

### Error Handling

```rust
use thiserror::Error;

#[derive(Error, Debug)]
enum CliError {
    #[error("File not found: {0}")]
    FileNotFound(String),

    #[error("Invalid format: {0}")]
    InvalidFormat(String),

    #[error(transparent)]
    IoError(#[from] std::io::Error),

    #[error(transparent)]
    ParseError(#[from] serde_json::Error),
}

fn main() -> Result<(), CliError> {
    let cli = Cli::parse();

    process_input(&cli.input)?;

    Ok(())
}
```

### File Operations

```rust
use std::fs;
use std::io::{BufRead, BufReader};
use std::path::Path;

fn read_lines(path: &Path) -> io::Result<Vec<String>> {
    let file = fs::File::open(path)?;
    let reader = BufReader::new(file);
    reader.lines().collect()
}

fn write_output(path: &Path, data: &str) -> io::Result<()> {
    fs::write(path, data)
}
```

## Testing CLI Applications

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use assert_cmd::Command;
    use predicates::prelude::*;

    #[test]
    fn test_basic_cli() {
        let mut cmd = Command::cargo_bin("myapp").unwrap();
        cmd.arg("--input").arg("test.txt")
            .assert()
            .success()
            .stdout(predicate::str::contains("Success"));
    }

    #[test]
    fn test_missing_arg() {
        let mut cmd = Command::cargo_bin("myapp").unwrap();
        cmd.assert()
            .failure()
            .stderr(predicate::str::contains("required"));
    }
}
```

## Best Practices

1. **Use clap derive**: Cleaner than builder API
2. **Provide help text**: Document all options
3. **Support --version**: Use `#[command(version)]`
4. **Use environment variables**: For secrets and config
5. **Implement --dry-run**: For destructive operations
6. **Add progress indicators**: For long-running tasks
7. **Handle SIGINT gracefully**: Clean shutdown
8. **Test with assert_cmd**: Automated CLI testing
9. **Support piping**: Read from stdin, write to stdout
10. **Follow Unix conventions**: Exit codes, stderr for errors
