#!/bin/bash

# DevContainer setup script for The Universal Axiom
# This script runs after the container is created

set -e

echo "🌟 Setting up The Universal Axiom development environment..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt-get update && sudo apt-get upgrade -y

# Install Julia (not included in universal image by default)
echo "📦 Installing Julia..."
sudo apt-get install -y julia

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install -e ".[dev]"

# Install Rust tools
echo "📦 Installing Rust tools..."
rustup component add rustfmt clippy

# Build TypeScript
echo "🔨 Building TypeScript..."
npm run build

# Build MCP Server
echo "🔨 Building MCP Server..."
npm run build:mcp

# Install Git hooks
echo "🪝 Installing Git hooks..."
npm run prepare

# Run verification
echo "✅ Running verification tests..."
python verify_outputs.py

# Set up git config (if not already set)
if [ -z "$(git config --global user.name)" ]; then
    echo "⚙️  Please configure git:"
    echo "  git config --global user.name 'Your Name'"
    echo "  git config --global user.email 'your.email@example.com'"
fi

echo ""
echo "✨ Setup complete! The Universal Axiom development environment is ready."
echo ""
echo "Quick start commands:"
echo "  make help          - Show all available commands"
echo "  make test          - Run all tests"
echo "  make verify        - Verify all implementations"
echo "  npm run example:js - Run JavaScript example"
echo "  python examples/python/basic_usage.py - Run Python example"
echo "  cargo run --example basic_usage --manifest-path src/rust/Cargo.toml - Run Rust example"
echo "  julia examples/julia/basic_usage.jl - Run Julia example"
echo ""
echo "📚 Documentation: https://github.com/TheUniversalAxiom/pointy-stick"
echo "🌐 Website: https://www.epiphanyengine.ai"
echo ""
