#!/usr/bin/env rust-script
//! Script with dependencies specified in a cargo manifest block.
//!
//! The ```cargo code block in doc comments defines the Cargo.toml content.
//! This is the preferred method for complex dependency specifications.
//!
//! ```cargo
//! [dependencies]
//! serde = { version = "1.0", features = ["derive"] }
//! serde_json = "1.0"
//! chrono = "0.4"
//!
//! # You can also specify other Cargo.toml sections:
//! # [features]
//! # default = []
//! ```
//!
//! Run: rust-script script.rs

use serde::{Deserialize, Serialize};
use chrono::Local;

#[derive(Debug, Serialize, Deserialize)]
struct Message {
    text: String,
    timestamp: String,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let msg = Message {
        text: "Hello from rust-script!".to_string(),
        timestamp: Local::now().format("%Y-%m-%d %H:%M:%S").to_string(),
    };

    let json = serde_json::to_string_pretty(&msg)?;
    println!("{}", json);

    Ok(())
}
