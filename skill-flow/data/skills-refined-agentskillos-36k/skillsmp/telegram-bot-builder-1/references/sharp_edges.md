# Telegram Bot Builder - Sharp Edges

## Rate Limits

### **Id**
rate-limits
### **Summary**
Bot gets rate limited by Telegram
### **Severity**
high
### **Situation**
Bot stops responding or messages fail
### **Why**
  Too many messages per second.
  Bulk messaging without throttling.
  Not handling 429 errors.
  Webhook flooding.
  
### **Solution**
  ## Telegram Rate Limits
  
  ### Know the Limits
  | Action | Limit |
  |--------|-------|
  | Messages to user | 30/sec |
  | Messages to group | 20/min |
  | Bulk notifications | 30/sec total |
  | API calls | Varies |
  
  ### Throttling Implementation
  ```javascript
  import Bottleneck from 'bottleneck';
  
  const limiter = new Bottleneck({
    maxConcurrent: 1,
    minTime: 33, // ~30 per second
  });
  
  async function sendMessage(chatId, text) {
    return limiter.schedule(() =>
      bot.telegram.sendMessage(chatId, text)
    );
  }
  ```
  
  ### Handle 429 Errors
  ```javascript
  bot.catch((err, ctx) => {
    if (err.response?.error_code === 429) {
      const retryAfter = err.response.parameters?.retry_after || 30;
      console.log(`Rate limited. Retry after ${retryAfter}s`);
      // Queue for retry
    }
  });
  ```
  
  ### Bulk Messaging
  ```javascript
  async function broadcastMessage(userIds, message) {
    for (const userId of userIds) {
      try {
        await sendMessage(userId, message);
        await sleep(50); // 50ms between messages
      } catch (err) {
        if (err.response?.error_code === 403) {
          // User blocked bot
          await markUserInactive(userId);
        }
      }
    }
  }
  ```
  
### **Symptoms**
  - "Too Many Requests" errors
  - Messages not delivering
  - 429 error codes
  - Bot seems slow
### **Detection Pattern**
rate limit|429|too many|throttle

## Webhook Not Working

### **Id**
webhook-not-working
### **Summary**
Webhook not receiving updates
### **Severity**
high
### **Situation**
Bot works locally but not in production
### **Why**
  HTTPS required for webhooks.
  Wrong webhook URL.
  Certificate issues.
  Firewall blocking.
  
### **Solution**
  ## Webhook Troubleshooting
  
  ### Requirements
  - HTTPS only (no self-signed in prod)
  - Port 443, 80, 88, or 8443
  - Valid SSL certificate
  - Publicly accessible URL
  
  ### Check Webhook Status
  ```bash
  curl "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"
  ```
  
  ### Common Fixes
  ```javascript
  // 1. Set webhook explicitly
  bot.telegram.setWebhook('https://your-domain.com/webhook');
  
  // 2. Delete old webhook first
  bot.telegram.deleteWebhook();
  
  // 3. Check pending updates
  const info = await bot.telegram.getWebhookInfo();
  console.log(info);
  ```
  
  ### Local Development
  ```bash
  # Use ngrok for local testing
  ngrok http 3000
  
  # Then set webhook to ngrok URL
  ```
  
  ### Vercel/Serverless Issues
  - Ensure function is accessible
  - Check function logs
  - Verify environment variables
  - Test endpoint directly
  
### **Symptoms**
  - Works with polling, not webhook
  - No logs in production
  - getWebhookInfo shows errors
  - Updates not arriving
### **Detection Pattern**
webhook|not working|production|deploy

## User State Management

### **Id**
user-state-management
### **Summary**
Bot loses user context between messages
### **Severity**
medium
### **Situation**
Multi-step flows break, bot forgets user state
### **Why**
  No state persistence.
  Using in-memory storage.
  Serverless cold starts.
  Not tracking conversations.
  
### **Solution**
  ## User State Management
  
  ### State Storage Options
  | Storage | Best For |
  |---------|----------|
  | Redis | Fast, temporary state |
  | PostgreSQL | Persistent data |
  | SQLite | Simple bots |
  | Telegraf sessions | Development |
  
  ### Telegraf Sessions
  ```javascript
  import { session } from 'telegraf';
  
  // In-memory (development only)
  bot.use(session());
  
  // Redis (production)
  import { Redis } from '@telegraf/session/redis';
  
  bot.use(session({
    store: Redis({ url: process.env.REDIS_URL }),
  }));
  
  // Use session
  bot.command('start', (ctx) => {
    ctx.session.step = 'awaiting_name';
    ctx.reply('What is your name?');
  });
  
  bot.on('text', (ctx) => {
    if (ctx.session.step === 'awaiting_name') {
      ctx.session.name = ctx.message.text;
      ctx.session.step = 'awaiting_email';
      ctx.reply('What is your email?');
    }
  });
  ```
  
  ### Scene/Wizard Pattern
  ```javascript
  import { Scenes } from 'telegraf';
  
  const wizard = new Scenes.WizardScene(
    'onboarding',
    (ctx) => {
      ctx.reply('Step 1: Enter your name');
      return ctx.wizard.next();
    },
    (ctx) => {
      ctx.wizard.state.name = ctx.message.text;
      ctx.reply('Step 2: Enter your email');
      return ctx.wizard.next();
    },
    (ctx) => {
      const { name } = ctx.wizard.state;
      ctx.reply(`Done! Welcome ${name}`);
      return ctx.scene.leave();
    }
  );
  ```
  
### **Symptoms**
  - Multi-step flows fail
  - "Start over" needed frequently
  - User data lost
  - Inconsistent behavior
### **Detection Pattern**
state|session|forgot|lost|context

## Blocked Users

### **Id**
blocked-users
### **Summary**
Users block bot but you keep trying to message
### **Severity**
medium
### **Situation**
Error logs full of "bot blocked by user"
### **Why**
  Not tracking who blocked.
  Wasting API calls.
  Filling logs with errors.
  Affecting rate limits.
  
### **Solution**
  ## Handling Blocked Users
  
  ### Detect Block
  ```javascript
  async function sendSafe(chatId, message) {
    try {
      await bot.telegram.sendMessage(chatId, message);
      return { success: true };
    } catch (err) {
      if (err.response?.error_code === 403) {
        // User blocked bot or deleted account
        await markUserInactive(chatId);
        return { success: false, blocked: true };
      }
      throw err;
    }
  }
  ```
  
  ### Track Active Users
  ```sql
  -- Users table
  CREATE TABLE users (
    telegram_id BIGINT PRIMARY KEY,
    username TEXT,
    is_active BOOLEAN DEFAULT true,
    blocked_at TIMESTAMP
  );
  ```
  
  ### Clean Broadcast List
  ```javascript
  async function broadcast(message) {
    const activeUsers = await db.users.findMany({
      where: { is_active: true }
    });
  
    for (const user of activeUsers) {
      const result = await sendSafe(user.telegram_id, message);
      if (result.blocked) {
        // Already marked inactive in sendSafe
      }
    }
  }
  ```
  
### **Symptoms**
  - Lots of 403 errors
  - Broadcast failing silently
  - Wasted API calls
  - Inaccurate user counts
### **Detection Pattern**
403|blocked|forbidden|can't send