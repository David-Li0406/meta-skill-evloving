# Telegram Bot Builder

## Patterns


---
  #### **Name**
Bot Architecture
  #### **Description**
Structure for maintainable Telegram bots
  #### **When To Use**
When starting a new bot project
  #### **Implementation**
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
    

---
  #### **Name**
Inline Keyboards
  #### **Description**
Interactive button interfaces
  #### **When To Use**
When building interactive bot flows
  #### **Implementation**
    ## Inline Keyboards
    
    ### Basic Keyboard
    ```javascript
    import { Markup } from 'telegraf';
    
    bot.command('menu', (ctx) => {
      ctx.reply('Choose an option:', Markup.inlineKeyboard([
        [Markup.button.callback('Option 1', 'opt_1')],
        [Markup.button.callback('Option 2', 'opt_2')],
        [
          Markup.button.callback('Yes', 'yes'),
          Markup.button.callback('No', 'no'),
        ],
      ]));
    });
    
    // Handle button clicks
    bot.action('opt_1', (ctx) => {
      ctx.answerCbQuery('You chose Option 1');
      ctx.editMessageText('You selected Option 1');
    });
    ```
    
    ### Keyboard Patterns
    | Pattern | Use Case |
    |---------|----------|
    | Single column | Simple menus |
    | Multi column | Yes/No, pagination |
    | Grid | Category selection |
    | URL buttons | Links, payments |
    
    ### Pagination
    ```javascript
    function getPaginatedKeyboard(items, page, perPage = 5) {
      const start = page * perPage;
      const pageItems = items.slice(start, start + perPage);
    
      const buttons = pageItems.map(item =>
        [Markup.button.callback(item.name, `item_${item.id}`)]
      );
    
      const nav = [];
      if (page > 0) nav.push(Markup.button.callback('◀️', `page_${page-1}`));
      if (start + perPage < items.length) nav.push(Markup.button.callback('▶️', `page_${page+1}`));
    
      return Markup.inlineKeyboard([...buttons, nav]);
    }
    ```
    

---
  #### **Name**
Bot Monetization
  #### **Description**
Making money from Telegram bots
  #### **When To Use**
When planning bot revenue
  #### **Implementation**
    ## Bot Monetization
    
    ### Revenue Models
    | Model | Example | Complexity |
    |-------|---------|------------|
    | Freemium | Free basic, paid premium | Medium |
    | Subscription | Monthly access | Medium |
    | Per-use | Pay per action | Low |
    | Ads | Sponsored messages | Low |
    | Affiliate | Product recommendations | Low |
    
    ### Telegram Payments
    ```javascript
    // Create invoice
    bot.command('buy', (ctx) => {
      ctx.replyWithInvoice({
        title: 'Premium Access',
        description: 'Unlock all features',
        payload: 'premium_monthly',
        provider_token: process.env.PAYMENT_TOKEN,
        currency: 'USD',
        prices: [{ label: 'Premium', amount: 999 }], // $9.99
      });
    });
    
    // Handle successful payment
    bot.on('successful_payment', (ctx) => {
      const payment = ctx.message.successful_payment;
      // Activate premium for user
      await activatePremium(ctx.from.id);
      ctx.reply('🎉 Premium activated!');
    });
    ```
    
    ### Freemium Strategy
    ```
    Free tier:
    - 10 uses per day
    - Basic features
    - Ads shown
    
    Premium ($5/month):
    - Unlimited uses
    - Advanced features
    - No ads
    - Priority support
    ```
    
    ### Usage Limits
    ```javascript
    async function checkUsage(userId) {
      const usage = await getUsage(userId);
      const isPremium = await checkPremium(userId);
    
      if (!isPremium && usage >= 10) {
        return { allowed: false, message: 'Daily limit reached. Upgrade?' };
      }
      return { allowed: true };
    }
    ```
    

---
  #### **Name**
Webhook Deployment
  #### **Description**
Production bot deployment
  #### **When To Use**
When deploying bot to production
  #### **Implementation**
    ## Webhook Deployment
    
    ### Polling vs Webhooks
    | Method | Best For |
    |--------|----------|
    | Polling | Development, simple bots |
    | Webhooks | Production, scalable |
    
    ### Express + Webhook
    ```javascript
    import express from 'express';
    import { Telegraf } from 'telegraf';
    
    const bot = new Telegraf(process.env.BOT_TOKEN);
    const app = express();
    
    app.use(express.json());
    app.use(bot.webhookCallback('/webhook'));
    
    // Set webhook
    const WEBHOOK_URL = 'https://your-domain.com/webhook';
    bot.telegram.setWebhook(WEBHOOK_URL);
    
    app.listen(3000);
    ```
    
    ### Vercel Deployment
    ```javascript
    // api/webhook.js
    import { Telegraf } from 'telegraf';
    
    const bot = new Telegraf(process.env.BOT_TOKEN);
    // ... bot setup
    
    export default async (req, res) => {
      await bot.handleUpdate(req.body);
      res.status(200).send('OK');
    };
    ```
    
    ### Railway/Render Deployment
    ```dockerfile
    FROM node:18-alpine
    WORKDIR /app
    COPY package*.json ./
    RUN npm install
    COPY . .
    CMD ["node", "src/bot.js"]
    ```
    

## Anti-Patterns


---
  #### **Name**
Blocking Operations
  #### **Description**
Long operations blocking bot responses
  #### **Why Bad**
    Telegram has timeout limits.
    Users think bot is dead.
    Poor experience.
    Requests pile up.
    
  #### **What To Do Instead**
    Acknowledge immediately.
    Process in background.
    Send update when done.
    Use typing indicator.
    

---
  #### **Name**
No Error Handling
  #### **Description**
Bot crashes on unexpected input
  #### **Why Bad**
    Users get no response.
    Bot appears broken.
    Debugging nightmare.
    Lost trust.
    
  #### **What To Do Instead**
    Global error handler.
    Graceful error messages.
    Log errors for debugging.
    Rate limiting.
    

---
  #### **Name**
Spammy Bot
  #### **Description**
Sending too many messages
  #### **Why Bad**
    Users block the bot.
    Telegram may ban.
    Annoying experience.
    Low retention.
    
  #### **What To Do Instead**
    Respect user attention.
    Consolidate messages.
    Allow notification control.
    Quality over quantity.
    