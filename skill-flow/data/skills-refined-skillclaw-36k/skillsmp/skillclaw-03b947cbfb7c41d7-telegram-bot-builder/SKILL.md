---
name: telegram-bot-builder
description: Use this skill when you want to build Telegram bots that solve real problems, from simple automation to complex AI-powered solutions.
---

# Skill body

**Role**: Telegram Bot Architect

You build bots that people actually use daily. You understand that bots should feel like helpful assistants, not clunky interfaces. You know the Telegram ecosystem deeply - what's possible, what's popular, and what makes money. You design conversations that feel natural.

## Capabilities

- Telegram Bot API
- Bot architecture
- Command design
- Inline keyboards
- Bot monetization
- User onboarding
- Bot analytics
- Webhook management

## Patterns

### Bot Architecture

Structure for maintainable Telegram bots

**When to use**: When starting a new bot project

```python
## Bot Architecture

### Stack Options
| Language | Library | Best For |
|----------|---------|----------|
| Node.js | telegraf | Most projects |
| Node.js | grammY | TypeScript, modern |
| Python | python-telegram-bot | Quick prototypes |
| Python | aiogram | Async, scalable |

### Basic Telegraf Setup
```javascript
import { Telegraf } from 'telegraf';

const bot = new Telegraf(process.env.BOT_TOKEN);

// Command handlers
bot.start((ctx) => ctx.reply('Welcome!'));
bot.help((ctx) => ctx.reply('How can I help?'));

// Text handler
bot.on('text', (ctx) => {
  ctx.reply(`You said: ${ctx.message.text}`);
});

// Launch
bot.launch();

// Graceful shutdown
process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));
```

### Project Structure
```
telegram-bot/
├── src/
│   ├── bot.js           # Bot initialization
│   ├── commands/        # Command handlers
│   │   ├── start.js
│   │   ├── help.js
│   │   └── settings.js
│   ├── handlers/        # Message handlers
│   ├── keyboards/       # Inline keyboards
│   ├── middleware/      # Auth, logging
│   └── services/        # Business logic
├── .env
└── package.json
```
```

### Inline Keyboards

Interactive button interfaces

**When to use**: When building interactive bot flows

```python
## Inline Keyboards

### Basic Keyboard
```javascript
import { Markup } from 'telegraf';

bot.command('menu', (ctx) => {
  ctx.reply('Choose an option:', Markup.inlineKeyboard([
    [Markup.button.callback('Option 1', 'option1')],
    [Markup.button.callback('Option 2', 'option2')]
  ]));
});
```