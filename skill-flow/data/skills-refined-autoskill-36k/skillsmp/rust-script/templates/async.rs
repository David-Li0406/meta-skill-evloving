#!/usr/bin/env rust-script
//! Async script using tokio runtime.
//!
//! ```cargo
//! [dependencies]
//! tokio = { version = "1", features = ["full"] }
//! reqwest = "0.11"
//! serde = { version = "1.0", features = ["derive"] }
//! serde_json = "1.0"
//! ```
//!
//! Run: rust-script async.rs

use serde::Deserialize;

#[derive(Debug, Deserialize)]
struct IpResponse {
    origin: String,
}

#[derive(Debug, Deserialize)]
struct UuidResponse {
    uuid: String,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("Fetching data asynchronously...\n");

    // Run multiple requests concurrently
    let (ip_result, uuid_result) = tokio::join!(
        fetch_ip(),
        fetch_uuid()
    );

    match ip_result {
        Ok(ip) => println!("Your IP: {}", ip.origin),
        Err(e) => eprintln!("Failed to fetch IP: {}", e),
    }

    match uuid_result {
        Ok(uuid) => println!("Random UUID: {}", uuid.uuid),
        Err(e) => eprintln!("Failed to fetch UUID: {}", e),
    }

    println!("\nDone!");
    Ok(())
}

async fn fetch_ip() -> Result<IpResponse, reqwest::Error> {
    reqwest::get("https://httpbin.org/ip")
        .await?
        .json()
        .await
}

async fn fetch_uuid() -> Result<UuidResponse, reqwest::Error> {
    reqwest::get("https://httpbin.org/uuid")
        .await?
        .json()
        .await
}
