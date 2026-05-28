# Telegram Mini App

## Patterns


---
  #### **Name**
Mini App Setup
  #### **Description**
Getting started with Telegram Mini Apps
  #### **When To Use**
When starting a new Mini App
  #### **Implementation**
    ## Mini App Setup
    
    ### Basic Structure
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
    ```jsx
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
    

---
  #### **Name**
TON Connect Integration
  #### **Description**
Wallet connection for TON blockchain
  #### **When To Use**
When building Web3 Mini Apps
  #### **Implementation**
    ## TON Connect Integration
    
    ### Setup
    ```bash
    npm install @tonconnect/ui-react
    ```
    
    ### React Integration
    ```jsx
    import { TonConnectUIProvider, TonConnectButton } from '@tonconnect/ui-react';
    
    // Wrap app
    function App() {
      return (
        <TonConnectUIProvider manifestUrl="https://your-app.com/tonconnect-manifest.json">
          <MainApp />
        </TonConnectUIProvider>
      );
    }
    
    // Use in components
    function WalletSection() {
      return (
        <TonConnectButton />
      );
    }
    ```
    
    ### Manifest File
    ```json
    {
      "url": "https://your-app.com",
      "name": "Your Mini App",
      "iconUrl": "https://your-app.com/icon.png"
    }
    ```
    
    ### Send TON Transaction
    ```jsx
    import { useTonConnectUI } from '@tonconnect/ui-react';
    
    function PaymentButton({ amount, to }) {
      const [tonConnectUI] = useTonConnectUI();
    
      const handlePay = async () => {
        const transaction = {
          validUntil: Math.floor(Date.now() / 1000) + 60,
          messages: [{
            address: to,
            amount: (amount * 1e9).toString(), // TON to nanoton
          }]
        };
    
        await tonConnectUI.sendTransaction(transaction);
      };
    
      return <button onClick={handlePay}>Pay {amount} TON</button>;
    }
    ```
    

---
  #### **Name**
Mini App Monetization
  #### **Description**
Making money from Mini Apps
  #### **When To Use**
When planning Mini App revenue
  #### **Implementation**
    ## Mini App Monetization
    
    ### Revenue Streams
    | Model | Example | Potential |
    |-------|---------|-----------|
    | TON payments | Premium features | High |
    | In-app purchases | Virtual goods | High |
    | Ads (Telegram Ads) | Display ads | Medium |
    | Referral | Share to earn | Medium |
    | NFT sales | Digital collectibles | High |
    
    ### Telegram Stars (New!)
    ```javascript
    // In your bot
    bot.command('premium', (ctx) => {
      ctx.replyWithInvoice({
        title: 'Premium Access',
        description: 'Unlock all features',
        payload: 'premium',
        provider_token: '', // Empty for Stars
        currency: 'XTR', // Telegram Stars
        prices: [{ label: 'Premium', amount: 100 }], // 100 Stars
      });
    });
    ```
    
    ### Viral Mechanics
    ```jsx
    // Referral system
    function ReferralShare() {
      const { tg, user } = useTelegram();
      const referralLink = `https://t.me/your_bot?start=ref_${user.id}`;
    
      const share = () => {
        tg.openTelegramLink(
          `https://t.me/share/url?url=${encodeURIComponent(referralLink)}&text=Check this out!`
        );
      };
    
      return <button onClick={share}>Invite Friends (+10 coins)</button>;
    }
    ```
    
    ### Gamification for Retention
    - Daily rewards
    - Streak bonuses
    - Leaderboards
    - Achievement badges
    - Referral bonuses
    

---
  #### **Name**
Mini App UX Patterns
  #### **Description**
UX specific to Telegram Mini Apps
  #### **When To Use**
When designing Mini App interfaces
  #### **Implementation**
    ## Mini App UX
    
    ### Platform Conventions
    | Element | Implementation |
    |---------|----------------|
    | Main Button | tg.MainButton |
    | Back Button | tg.BackButton |
    | Theme | tg.themeParams |
    | Haptics | tg.HapticFeedback |
    
    ### Main Button
    ```javascript
    const tg = window.Telegram.WebApp;
    
    // Show main button
    tg.MainButton.setText('Continue');
    tg.MainButton.show();
    tg.MainButton.onClick(() => {
      // Handle click
      submitForm();
    });
    
    // Loading state
    tg.MainButton.showProgress();
    // ...
    tg.MainButton.hideProgress();
    ```
    
    ### Theme Adaptation
    ```css
    :root {
      --tg-theme-bg-color: var(--tg-theme-bg-color, #ffffff);
      --tg-theme-text-color: var(--tg-theme-text-color, #000000);
      --tg-theme-button-color: var(--tg-theme-button-color, #3390ec);
    }
    
    body {
      background: var(--tg-theme-bg-color);
      color: var(--tg-theme-text-color);
    }
    ```
    
    ### Haptic Feedback
    ```javascript
    // Light feedback
    tg.HapticFeedback.impactOccurred('light');
    
    // Success
    tg.HapticFeedback.notificationOccurred('success');
    
    // Selection
    tg.HapticFeedback.selectionChanged();
    ```
    

## Anti-Patterns


---
  #### **Name**
Ignoring Telegram Theme
  #### **Description**
App doesn't match Telegram look and feel
  #### **Why Bad**
    Feels foreign in Telegram.
    Bad user experience.
    Jarring transitions.
    Users don't trust it.
    
  #### **What To Do Instead**
    Use tg.themeParams.
    Match Telegram colors.
    Use native-feeling UI.
    Test in both light/dark.
    

---
  #### **Name**
Desktop-First Mini App
  #### **Description**
Designed for desktop, broken on mobile
  #### **Why Bad**
    95% of Telegram is mobile.
    Touch targets too small.
    Doesn't fit in Telegram UI.
    Scrolling issues.
    
  #### **What To Do Instead**
    Mobile-first always.
    Test on real phones.
    Touch-friendly buttons.
    Fit within Telegram frame.
    

---
  #### **Name**
No Loading States
  #### **Description**
Blank screen while loading
  #### **Why Bad**
    Users think it's broken.
    Poor perceived performance.
    High exit rate.
    Confusion.
    
  #### **What To Do Instead**
    Show skeleton UI.
    Loading indicators.
    Progressive loading.
    Optimistic updates.
    