---
name: telegram-mini-app
description: Use this skill when you want to build Telegram Mini Apps (TWA) that provide a native-like experience within Telegram, leveraging the TON ecosystem, Telegram Web App API, and monetization strategies.
---

# Skill body

## Role
**Telegram Mini App Architect**

You build apps where 800M+ Telegram users already are. You understand the Mini App ecosystem is exploding - games, DeFi, utilities, social apps. You know the TON blockchain and how to monetize with crypto. You design for the Telegram UX paradigm, not traditional web.

## Capabilities
- Telegram Web App API
- Mini App architecture
- TON Connect integration
- In-app payments
- User authentication via Telegram
- Mini App UX patterns
- Viral Mini App mechanics
- TON blockchain integration

## Patterns

### Mini App Setup
Getting started with Telegram Mini Apps.

**When to use**: When starting a new Mini App.

```html
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://telegram.org/js/telegram-web-app.js"></script>
</head>
<body>
  <script>
    const tg = window.Telegram.WebApp;
    tg.ready();
    tg.expand();

    // User data
    const user = tg.initDataUnsafe.user;
    console.log(user.first_name, user.id);
  </script>
</body>
</html>
```

### React Setup
```javascript
// hooks/useTelegram.js
export function useTelegram() {
  const tg = window.Telegram?.WebApp;

  return {
    tg,
    user: tg?.initDataUnsafe?.user,
    queryId: tg?.initDataUnsafe?.query_id,
    expand: () => tg?.expand(),
    close: () => tg?.close(),
    ready: () => tg?.ready(),
  };
}

// App.jsx
function App() {
  const { tg, user, expand, ready } = useTelegram();

  useEffect(() => {
    ready();
    expand();
  }, []);

  return <div>Hello, {user?.first_name}</div>;
}
```

### Bot Integration
```javascript
// Bot sends Mini App
bot.command('app', (ctx) => {
  ctx.reply('Open the app:', {
    reply_markup: {
      inline_keyboard: [[
        { text: '🚀 Open App', web_app: { url: 'https://your-app.com' } }
      ]]
    }
  });
});
```

### TON Connect Integration
Wallet connection for TON blockchain.

**When to use**: When building Web3 Mini Apps.

```bash
npm install @tonco
```