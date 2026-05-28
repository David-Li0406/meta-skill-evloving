# Railil Skill 🚆

> The ultimate Israel Rail schedule assistant for your AI agents.

Welcome to the **Railil Skill**! This skill empowers your AI agents (like Clawdbot) to instantly access real-time train schedules, plan routes, and find upcoming trains for Israel Rail directly from the command line. Powered by the robust [railil](https://github.com/lirantal/railil) CLI, it's designed to be fast, flexible, and agent-friendly.

## 🌟 Features

*   **Smart Station Search:** Fuzzy matching for station names means you don't need to know the exact spelling.
*   **Flexible Scheduling:** Find trains for right now, or plan ahead for specific dates and times.
*   **Agent-Optimized Output:** Supports JSON output for easy parsing by AI agents, alongside human-readable text and tables.
*   **Zero Config:** Works out of the box with `npx` or global npm installation.

## 🚀 Quick Start

This skill is designed to work seamlessly with [Clawdbot](https://clawd.bot).

### Installation via ClawdHub

You can install this skill directly using the [ClawdHub](https://clawdhub.com) CLI:

```bash
clawdhub install railil
```

### Manual Installation

Clone this repository into your skills directory:

```bash
git clone https://github.com/lirantal/skill-railil.git ./skills/railil
```

## 🎮 Usage

Once installed, your agent can invoke the `railil` command to query train data.

### 📍 Find Next Trains
Need to get somewhere fast? Find the next available trains between two cities.

```bash
railil --from "Tel Aviv" --to "Haifa"
```

### 📅 Plan a Trip
Checking schedules for a future date? No problem.

```bash
railil --from "Beer Sheva" --to "Tel Aviv" --time 08:00 --date 2023-11-01
```

### 🤖 For Agents (JSON)
Get raw data for processing.

```bash
railil --from "Ben Gurion" --to "Jerusalem" --output json
```

## 🛠️ About Railil

This skill wraps the **railil** npm package. It's a community-driven project to make Israel Rail data accessible via the command line.

*   **NPM Package:** [railil](https://www.npmjs.com/package/railil)
*   **Source Code:** [GitHub](https://github.com/lirantal/railil)

## 👤 Author

**Liran Tal**

*   Website: [lirantal.com](https://lirantal.com)
*   GitHub: [@lirantal](https://github.com/lirantal)
*   Twitter: [@liran_tal](https://twitter.com/liran_tal)

## 🔗 Links

*   **ClawdHub:** Discover more skills at [clawdhub.com](https://clawdhub.com)
*   **Clawdbot:** The AI agent that runs this skill [clawd.bot](https://clawd.bot)

## 📄 License

This project is licensed under the **Apache-2.0 License**. See the [LICENSE](LICENSE) file for details.