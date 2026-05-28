---
name: discord-bot-architect
description: Use this skill when building production-ready Discord bots with Discord.js (JavaScript) or Pycord (Python), focusing on slash commands, interactive components, and efficient gateway management.
---

# Discord Bot Architect

## Patterns

### Discord.js v14 Foundation

Modern Discord bot setup with Discord.js v14 and slash commands.

**When to use**: Building Discord bots with JavaScript/TypeScript, needing full gateway connection with events, or building bots with complex interactions.

```javascript
// src/index.js
const { Client, Collection, GatewayIntentBits } = require('discord.js');
const fs = require('node:fs');
const path = require('node:path');
require('dotenv').config();

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    // Add only what you need:
    // GatewayIntentBits.GuildMessages,
    // GatewayIntentBits.MessageContent,  // PRIVILEGED - avoid if possible
  ]
});

// Load commands
client.commands = new Collection();
const commandsPath = path.join(__dirname, 'commands');
const commandFiles = fs.readdirSync(commandsPath).filter(f => f.endsWith('.js'));

for (const file of commandFiles) {
  const filePath = path.join(commandsPath, file);
  const command = require(filePath);
  if ('data' in command && 'execute' in command) {
    client.commands.set(command.data.name, command);
  }
}

// Load events
const eventsPath = path.join(__dirname, 'events');
const eventFiles = fs.readdirSync(eventsPath).filter(f => f.endsWith('.js'));

for (const file of eventFiles) {
  const filePath = path.join(eventsPath, file);
  const event = require(filePath);
  if (event.once) {
    client.once(event.name, (...args) => event.execute(...args));
  } else {
    client.on(event.name, (...args) => event.execute(...args));
  }
}

client.login(process.env.DISCORD_TOKEN);
```

### Pycord Bot Foundation

Discord bot with Pycord (Python) and application commands.

**When to use**: Building Discord bots with Python, preferring async/await patterns, or needing good slash command support.

```python
# main.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.slash_command(name="ping", description="Check bot latency")
async def ping(ctx: discord.ApplicationContext):
    latency = round(bot.latency * 1000)
    await ctx.respond(f"Pong! Latency: {latency}ms")

bot.run(os.environ["DISCORD_TOKEN"])
```

### Interactive Components Pattern

Using buttons, select menus, and modals for rich UX.

**When to use**: Need interactive user interfaces, collecting user input beyond slash command options, or building menus, confirmations, or forms.

```javascript
// Discord.js - Buttons and Select Menus
const {
  SlashCommandBuilder,
  ActionRowBuilder,
  ButtonBuilder,
  ButtonStyle,
  StringSelectMenuBuilder
} = require('discord.js');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('menu')
    .setDescription('Shows an interactive menu'),

  async execute(interaction) {
    const buttonRow = new ActionRowBuilder()
      .addComponents(
        new ButtonBuilder()
          .setCustomId('confirm')
          .setLabel('Confirm')
          .setStyle(ButtonStyle.Primary),
        new ButtonBuilder()
          .setCustomId('cancel')
          .setLabel('Cancel')
          .setStyle(ButtonStyle.Danger)
      );

    const selectRow = new ActionRowBuilder()
      .addComponents(
        new StringSelectMenuBuilder()
          .setCustomId('select-role')
          .setPlaceholder('Select a role')
          .addOptions([
            { label: 'Developer', value: 'dev' },
            { label: 'Designer', value: 'design' },
            { label: 'Community', value: 'community' }
          ])
      );

    await interaction.reply({
      content: 'Choose an option:',
      components: [buttonRow, selectRow]
    });
  }
};
```

## Principles

- Prefer slash commands over message parsing (Message Content Intent deprecated).
- Acknowledge interactions within 3 seconds.
- Request only required intents to minimize privileged intents.
- Handle rate limits gracefully with exponential backoff.
- Plan for sharding from the start (required at 2500+ guilds).
- Use components (buttons, selects, modals) for rich UX.
- Test with guild commands first, deploy global when ready.

## Anti-Patterns

### ❌ Message Content for Commands

**Why bad**: Message Content Intent is privileged and deprecated for bot commands. Slash commands are the intended approach.

### ❌ Syncing Commands on Every Start

**Why bad**: Command registration is rate limited. Global commands take up to 1 hour to propagate. Syncing on every start wastes API calls and can hit limits.

### ❌ Blocking the Event Loop

**Why bad**: Discord gateway requires regular heartbeats. Blocking operations cause missed heartbeats and disconnections.

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Issue | critical | Acknowledge immediately, process later |
| Issue | critical | Enable in Developer Portal |
| Issue | high | Use a separate deploy script (not on startup) |
| Issue | critical | Never hardcode tokens |
| Issue | high | Generate correct invite URL |
| Issue | medium | Development: Use guild commands |
| Issue | medium | Never block the event loop |
| Issue | medium | Show modal immediately |