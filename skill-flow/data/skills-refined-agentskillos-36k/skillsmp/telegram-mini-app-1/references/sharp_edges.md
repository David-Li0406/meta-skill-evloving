# Telegram Mini App - Sharp Edges

## Init Data Validation

### **Id**
init-data-validation
### **Summary**
Not validating initData from Telegram
### **Severity**
high
### **Situation**
Backend trusts user data without verification
### **Why**
  initData can be spoofed.
  Security vulnerability.
  Users can impersonate others.
  Data tampering possible.
  
### **Solution**
  ## Validating initData
  
  ### Why Validate
  - initData contains user info
  - Must verify it came from Telegram
  - Prevent spoofing/tampering
  
  ### Node.js Validation
  ```javascript
  import crypto from 'crypto';
  
  function validateInitData(initData, botToken) {
    const params = new URLSearchParams(initData);
    const hash = params.get('hash');
    params.delete('hash');
  
    // Sort and join
    const dataCheckString = Array.from(params.entries())
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([k, v]) => `${k}=${v}`)
      .join('\n');
  
    // Create secret key
    const secretKey = crypto
      .createHmac('sha256', 'WebAppData')
      .update(botToken)
      .digest();
  
    // Calculate hash
    const calculatedHash = crypto
      .createHmac('sha256', secretKey)
      .update(dataCheckString)
      .digest('hex');
  
    return calculatedHash === hash;
  }
  ```
  
  ### Using in API
  ```javascript
  app.post('/api/action', (req, res) => {
    const { initData } = req.body;
  
    if (!validateInitData(initData, process.env.BOT_TOKEN)) {
      return res.status(401).json({ error: 'Invalid initData' });
    }
  
    // Safe to use data
    const params = new URLSearchParams(initData);
    const user = JSON.parse(params.get('user'));
    // ...
  });
  ```
  
### **Symptoms**
  - Trusting client data blindly
  - No server-side validation
  - Using initDataUnsafe directly
  - Security audit failures
### **Detection Pattern**
initData|validate|security|spoof

## Ton Connect Mobile

### **Id**
ton-connect-mobile
### **Summary**
TON Connect not working on mobile
### **Severity**
high
### **Situation**
Wallet connection fails on mobile Telegram
### **Why**
  Deep linking issues.
  Wallet app not opening.
  Return URL problems.
  Different behavior iOS vs Android.
  
### **Solution**
  ## TON Connect Mobile Issues
  
  ### Common Problems
  1. Wallet doesn't open
  2. Return to Mini App fails
  3. Transaction confirmation lost
  
  ### Fixes
  ```jsx
  // Use correct manifest
  const manifestUrl = 'https://your-domain.com/tonconnect-manifest.json';
  
  // Ensure HTTPS
  // Localhost won't work on mobile
  
  // Handle connection states
  const [tonConnectUI] = useTonConnectUI();
  
  useEffect(() => {
    return tonConnectUI.onStatusChange((wallet) => {
      if (wallet) {
        console.log('Connected:', wallet.account.address);
      }
    });
  }, []);
  ```
  
  ### Testing
  - Test on real devices
  - Test with multiple wallets (Tonkeeper, OpenMask)
  - Test both iOS and Android
  - Use ngrok for local dev + mobile test
  
  ### Fallback
  ```jsx
  // Show QR for desktop
  // Show wallet list for mobile
  <TonConnectButton />
  // Automatically handles this
  ```
  
### **Symptoms**
  - Works on desktop, fails mobile
  - Wallet app doesn't open
  - Connection stuck
  - Users can't pay
### **Detection Pattern**
TON.*mobile|wallet.*open|connect.*fail

## Mini App Performance

### **Id**
mini-app-performance
### **Summary**
Mini App feels slow and janky
### **Severity**
medium
### **Situation**
App lags, slow transitions, poor UX
### **Why**
  Too much JavaScript.
  No code splitting.
  Large bundle size.
  No loading optimization.
  
### **Solution**
  ## Mini App Performance
  
  ### Bundle Size
  - Target < 200KB gzipped
  - Use code splitting
  - Lazy load routes
  - Tree shake dependencies
  
  ### Quick Wins
  ```jsx
  // Lazy load heavy components
  const HeavyChart = lazy(() => import('./HeavyChart'));
  
  // Optimize images
  <img loading="lazy" src="..." />
  
  // Use CSS instead of JS animations
  ```
  
  ### Loading Strategy
  ```jsx
  function App() {
    const [ready, setReady] = useState(false);
  
    useEffect(() => {
      // Show skeleton immediately
      // Load data in background
      Promise.all([
        loadUserData(),
        loadAppConfig(),
      ]).then(() => setReady(true));
    }, []);
  
    if (!ready) return <Skeleton />;
    return <MainApp />;
  }
  ```
  
  ### Vite Optimization
  ```javascript
  // vite.config.js
  export default {
    build: {
      rollupOptions: {
        output: {
          manualChunks: {
            vendor: ['react', 'react-dom'],
          }
        }
      }
    }
  };
  ```
  
### **Symptoms**
  - Slow initial load
  - Laggy interactions
  - Users complaining about speed
  - High bounce rate
### **Detection Pattern**
slow|lag|performance|loading

## Not Using Main Button

### **Id**
not-using-main-button
### **Summary**
Custom buttons instead of MainButton
### **Severity**
medium
### **Situation**
App has custom submit buttons that feel non-native
### **Why**
  MainButton is expected UX.
  Custom buttons feel foreign.
  Inconsistent with Telegram.
  Users don't know what to tap.
  
### **Solution**
  ## Using MainButton Properly
  
  ### When to Use MainButton
  - Form submission
  - Primary actions
  - Continue/Next flows
  - Checkout/Payment
  
  ### Implementation
  ```javascript
  const tg = window.Telegram.WebApp;
  
  // Show for forms
  function showMainButton(text, onClick) {
    tg.MainButton.setText(text);
    tg.MainButton.onClick(onClick);
    tg.MainButton.show();
  }
  
  // Hide when not needed
  function hideMainButton() {
    tg.MainButton.hide();
    tg.MainButton.offClick();
  }
  
  // Loading state
  function setMainButtonLoading(loading) {
    if (loading) {
      tg.MainButton.showProgress();
      tg.MainButton.disable();
    } else {
      tg.MainButton.hideProgress();
      tg.MainButton.enable();
    }
  }
  ```
  
  ### React Hook
  ```jsx
  function useMainButton(text, onClick, visible = true) {
    const tg = window.Telegram?.WebApp;
  
    useEffect(() => {
      if (!tg) return;
  
      if (visible) {
        tg.MainButton.setText(text);
        tg.MainButton.onClick(onClick);
        tg.MainButton.show();
      } else {
        tg.MainButton.hide();
      }
  
      return () => {
        tg.MainButton.offClick(onClick);
      };
    }, [text, onClick, visible]);
  }
  ```
  
### **Symptoms**
  - Custom submit buttons
  - MainButton never used
  - Inconsistent UX
  - Users confused about actions
### **Detection Pattern**
MainButton|button|submit|action