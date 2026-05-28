# SearchOnline Skill

A powerful, multi-source web search skill designed for AI agents like **Claude Code**, **OpenCode**, or **Codex**. This tool serves as a superior replacement or enhancement for built-in WebSearch tools by aggregating results from multiple premium sources and synthesizing them using Gemini AI.

## 🚀 Key Features

- **Multi-Source Aggregation**: Concurrently fetches search results from **Tavily**, **WebSearchAPI**, and **Gemini Google Search Grounding**.
- **AI-Powered Summarization**: Uses Gemini models (Flash/Pro) to synthesize aggregated data into structured, actionable Markdown.
- **Optimized for Agents**: Output is specifically formatted for AI consumption—concise for simple facts, structured for research.
- **Robustness**:
    - Concurrent execution using `ThreadPoolExecutor` for speed.
    - Automatic retry logic with exponential backoff.
    - Graceful fallback: If AI summarization fails, it returns formatted raw results.
- **Highly Configurable**: Control result depth per source (1-10) and manage API rate limits with automatic model switching.

## 🛠 Installation

### 1. Requirements
- Python 3.8+
- `requests` library

```bash
pip install requests
```

### 2. Environment Variables
Create a `.env` file in the project root or set these variables in your environment:

| Variable | Required | Purpose | Get API Key |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | **Yes** | AI summarization and Google Search Grounding | [Google AI Studio](https://aistudio.google.com/) |
| `TAVILY_API_KEY` | Optional | Premium search results via Tavily | [Tavily](https://www.tavily.com) |
| `WEBSEARCHAPI_KEY` | Optional | Additional search coverage via WebSearchAPI | [WebSearchAPI](https://websearchapi.ai) |

## 📖 Usage

### Command Line Interface (CLI)

```bash
python3 SearchOnline.py "<your search query>" [max_results]
```

- `max_results`: (Optional) Results per source (1-10, default: 5).

**Example:**
```bash
python3 SearchOnline.py "latest features in Python 3.13" 3
```

### As a Claude Code Skill

This project is structured as a Claude Code skill. When integrated, the agent will prioritize `SearchOnline` over its built-in search tool for:
- Current events and news.
- Real-time data (weather, stocks, trending repos).
- Information beyond the model's knowledge cutoff.

## ⚙️ How it Works

1. **Parallel Search**: The script launches concurrent requests to all configured search providers.
2. **Context Synthesis**: It aggregates all successful responses, removes duplicates, and filters for relevance.
3. **Smart Summarization**: Gemini processes the data based on the query type (e.g., tables for lists, paragraphs for research).
4. **Adaptive Rate Limiting**: If one Gemini model hits a rate limit, the script automatically tries the next available model (`gemini-3-flash-preview`, `gemini-flash-latest`, etc.).

## 📂 Project Structure

- `SearchOnline.py`: The core implementation logic.
- `SKILL.md`: Configuration and instructions for Claude Code integration.
- `.env.example`: Template for environment variables.
- `.gitignore`: Pre-configured to keep your API keys safe.

## 📄 License

MIT License - feel free to use and modify!

---
*Created with [Claude Code](https://claude.com/claude-code)*
