# Plaid Fintech - Sharp Edges

## Access Tokens Never Expire But Are Highly Sensitive

### **Id**
access-token-security
### **Severity**
critical
### **Description**
  Plaid access tokens provide full access to a user's financial data and
  never expire. They must be treated like passwords:
  - Encrypt at rest
  - Never log or expose
  - Use secrets manager in production
  - Rotate if compromised via /item/access_token/invalidate
  
### **Wrong Way**
  // Storing in plain text
  await db.user.update({
    where: { id: userId },
    data: { plaidAccessToken: access_token }  // Plain text!
  });
  
  // Logging the token
  console.log('Got access token:', access_token);
  
  // Exposing in API response
  res.json({ accessToken: access_token });  // Never!
  
### **Right Way**
  import { createCipheriv, createDecipheriv, randomBytes } from 'crypto';
  
  const ENCRYPTION_KEY = process.env.PLAID_TOKEN_ENCRYPTION_KEY;
  const ALGORITHM = 'aes-256-gcm';
  
  function encrypt(text: string): string {
    const iv = randomBytes(16);
    const cipher = createCipheriv(ALGORITHM, Buffer.from(ENCRYPTION_KEY, 'hex'), iv);
  
    let encrypted = cipher.update(text, 'utf8', 'hex');
    encrypted += cipher.final('hex');
  
    const authTag = cipher.getAuthTag();
  
    return `${iv.toString('hex')}:${authTag.toString('hex')}:${encrypted}`;
  }
  
  function decrypt(encryptedText: string): string {
    const [ivHex, authTagHex, encrypted] = encryptedText.split(':');
  
    const iv = Buffer.from(ivHex, 'hex');
    const authTag = Buffer.from(authTagHex, 'hex');
    const decipher = createDecipheriv(ALGORITHM, Buffer.from(ENCRYPTION_KEY, 'hex'), iv);
  
    decipher.setAuthTag(authTag);
  
    let decrypted = decipher.update(encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
  
    return decrypted;
  }
  
  // Store encrypted
  await db.plaidItem.create({
    data: {
      accessToken: encrypt(access_token),
    }
  });
  
### **Detection Patterns**
  - accessToken.*console\.log
  - access_token.*res\.json
  - plaidAccessToken:\s*access
### **References**
  - https://plaid.com/docs/api/tokens/

## accounts/get Returns Cached Balances, Not Real-Time

### **Id**
cached-vs-realtime-balance
### **Severity**
high
### **Description**
  The free /accounts/get endpoint returns cached data that may be hours
  or days old. For real-time balance checks before payments or transfers,
  you MUST use the paid /accounts/balance/get endpoint.
  
  Cached data updates:
  - Transactions-enabled items: ~1x per day
  - Auth/Identity-only items: May be much older
  
### **Wrong Way**
  // Checking balance for payment with cached data
  async function validatePaymentAmount(accessToken: string, amount: number) {
    // WRONG: This is cached, could be hours old!
    const response = await plaidClient.accountsGet({
      access_token: accessToken,
    });
  
    const balance = response.data.accounts[0].balances.available;
  
    if (balance >= amount) {
      // User might not actually have this much!
      await initiatePayment(amount);
    }
  }
  
### **Right Way**
  // Use real-time balance for payment decisions
  async function validatePaymentAmount(accessToken: string, amount: number) {
    // RIGHT: Real-time balance check
    const response = await plaidClient.accountsBalanceGet({
      access_token: accessToken,
    });
  
    const account = response.data.accounts[0];
    const realTimeBalance = account.balances.available ?? account.balances.current;
  
    if (realTimeBalance >= amount) {
      await initiatePayment(amount);
    } else {
      throw new InsufficientFundsError(realTimeBalance, amount);
    }
  }
  
  // Use cached data only for display
  async function displayAccountSummary(accessToken: string) {
    const response = await plaidClient.accountsGet({
      access_token: accessToken,
    });
  
    // Display with "as of" timestamp
    return response.data.accounts.map(acc => ({
      name: acc.name,
      balance: acc.balances.current,
      lastUpdated: acc.balances.last_updated_datetime || 'Unknown',
      isRealtime: false,
    }));
  }
  
### **Detection Patterns**
  - accountsGet.*payment|transfer
  - balances\.available.*initiatePayment
### **References**
  - https://plaid.com/docs/api/accounts/#accountsbalanceget

## Webhooks May Arrive Out of Order or Duplicated

### **Id**
webhook-order-duplicates
### **Severity**
high
### **Description**
  Plaid webhooks can:
  - Arrive out of order (HISTORICAL_UPDATE before INITIAL_UPDATE)
  - Be duplicated during retries
  - Be lost if your endpoint is down beyond retry period
  
  Design your handler to be idempotent and not rely on order.
  
### **Wrong Way**
  // Assuming webhooks arrive in order
  app.post('/webhooks', async (req, res) => {
    const { webhook_code, item_id } = req.body;
  
    if (webhook_code === 'INITIAL_UPDATE') {
      // Mark as ready for sync
      await db.plaidItem.update({
        where: { itemId: item_id },
        data: { syncReady: true },
      });
    }
  
    if (webhook_code === 'HISTORICAL_UPDATE') {
      // Assumes INITIAL_UPDATE already processed
      const item = await db.plaidItem.findUnique({
        where: { itemId: item_id },
      });
  
      if (!item.syncReady) {
        // WRONG: HISTORICAL_UPDATE can arrive first!
        throw new Error('Initial update not processed');
      }
    }
  
    res.sendStatus(200);
  });
  
### **Right Way**
  // Idempotent, order-independent webhook handler
  app.post('/webhooks', async (req, res) => {
    const { webhook_type, webhook_code, item_id } = req.body;
  
    // Create idempotency key
    const webhookId = crypto
      .createHash('sha256')
      .update(JSON.stringify(req.body))
      .digest('hex');
  
    // Check if already processed
    const existing = await db.webhookLog.findUnique({
      where: { id: webhookId },
    });
  
    if (existing) {
      return res.sendStatus(200);  // Already processed
    }
  
    // Record before processing
    await db.webhookLog.create({
      data: {
        id: webhookId,
        webhookType: webhook_type,
        webhookCode: webhook_code,
        itemId: item_id,
      },
    });
  
    // Handle any transaction-related webhook the same way
    if (webhook_type === 'TRANSACTIONS') {
      // Always just sync - sync handles its own state
      await queueTransactionSync(item_id);
    }
  
    res.sendStatus(200);
  });
  
### **Detection Patterns**
  - INITIAL_UPDATE.*HISTORICAL_UPDATE
  - webhook.*throw.*not.*processed
### **References**
  - https://plaid.com/docs/api/webhooks/

## Items Enter Error States That Require User Action

### **Id**
item-error-states
### **Severity**
high
### **Description**
  When users change passwords or banks require re-authentication, items
  enter ITEM_LOGIN_REQUIRED state. API calls will fail until the user
  goes through Link update mode. There is NO way to fix this automatically.
  
  Plaid does NOT send a webhook when an error is cleared - you must
  track this yourself.
  
### **Wrong Way**
  // Retrying on ITEM_LOGIN_REQUIRED
  async function syncWithRetry(accessToken: string) {
    for (let i = 0; i < 5; i++) {
      try {
        return await plaidClient.transactionsSync({
          access_token: accessToken,
        });
      } catch (error) {
        // WRONG: ITEM_LOGIN_REQUIRED won't resolve with retries!
        await sleep(1000 * Math.pow(2, i));
      }
    }
  }
  
### **Right Way**
  async function syncWithErrorHandling(accessToken: string, itemId: string) {
    try {
      return await plaidClient.transactionsSync({
        access_token: accessToken,
      });
    } catch (error) {
      const plaidError = error.response?.data;
  
      if (plaidError?.error_code === 'ITEM_LOGIN_REQUIRED') {
        // Mark item as needing update
        await db.plaidItem.update({
          where: { itemId },
          data: {
            status: 'NEEDS_UPDATE',
            errorCode: 'ITEM_LOGIN_REQUIRED',
          },
        });
  
        // Notify user (email, in-app, push)
        await notifyUserUpdateNeeded(itemId);
  
        // Return empty result, don't retry
        return { added: [], modified: [], removed: [] };
      }
  
      // Other errors might be transient, can retry
      throw error;
    }
  }
  
  // API to get update link token
  app.post('/api/plaid/update-link', async (req, res) => {
    const { itemId } = req.body;
  
    const item = await db.plaidItem.findUnique({
      where: { itemId },
    });
  
    const response = await plaidClient.linkTokenCreate({
      user: { client_user_id: item.userId },
      client_name: 'My App',
      country_codes: [CountryCode.Us],
      language: 'en',
      access_token: await decrypt(item.accessToken),  // Update mode
    });
  
    res.json({ link_token: response.data.link_token });
  });
  
  // After successful update, mark item as active
  app.post('/api/plaid/update-success', async (req, res) => {
    const { itemId } = req.body;
  
    await db.plaidItem.update({
      where: { itemId },
      data: {
        status: 'ACTIVE',
        errorCode: null,
      },
    });
  
    // Resume syncing
    await queueTransactionSync(itemId);
  
    res.json({ success: true });
  });
  
### **Detection Patterns**
  - ITEM_LOGIN_REQUIRED.*retry
  - catch.*sleep.*ITEM
### **References**
  - https://plaid.com/docs/link/update-mode/

## Sandbox Does Not Reflect Production Complexity

### **Id**
sandbox-vs-production
### **Severity**
medium
### **Description**
  Sandbox provides testing capabilities but doesn't reflect:
  - Real institution-specific behaviors
  - Actual data formats and edge cases
  - Real credential validation
  - True error scenarios
  
  Test in Production or Limited Production before launch.
  
### **Wrong Way**
  // Only testing in Sandbox
  const config = {
    basePath: PlaidEnvironments.sandbox,
    // Never testing in production!
  };
  
  // Assuming all institutions behave like sandbox
  const response = await plaidClient.transactionsSync({
    access_token: accessToken,
  });
  // Sandbox always returns clean data
  
### **Right Way**
  // Environment-based configuration
  const environment = process.env.PLAID_ENV || 'sandbox';
  
  const config = new Configuration({
    basePath: PlaidEnvironments[environment],
    baseOptions: {
      headers: {
        'PLAID-CLIENT-ID': process.env.PLAID_CLIENT_ID,
        'PLAID-SECRET': process.env[`PLAID_SECRET_${environment.toUpperCase()}`],
      },
    },
  });
  
  // Handle institution-specific edge cases
  async function syncTransactions(accessToken: string, itemId: string) {
    try {
      const response = await plaidClient.transactionsSync({
        access_token: accessToken,
      });
  
      // Handle missing/null fields that may occur in production
      for (const txn of response.data.added) {
        await db.transaction.create({
          data: {
            amount: txn.amount,
            date: txn.date,
            name: txn.name || txn.merchant_name || 'Unknown',
            // Some institutions don't provide category
            category: txn.personal_finance_category?.primary || 'UNCATEGORIZED',
            // merchant_name is often null
            merchantName: txn.merchant_name || null,
          },
        });
      }
    } catch (error) {
      // Production has more error types
      handlePlaidError(error, itemId);
    }
  }
  
### **Detection Patterns**
  - PlaidEnvironments\.sandbox(?!.*production)
  - PLAID_ENV.*sandbox
### **References**
  - https://plaid.com/docs/sandbox/

## TRANSACTIONS_SYNC_MUTATION_DURING_PAGINATION Requires Restart

### **Id**
transactions-sync-mutation
### **Severity**
medium
### **Description**
  If transactions change during pagination (user makes purchases while
  you're syncing), Plaid returns TRANSACTIONS_SYNC_MUTATION_DURING_PAGINATION.
  You must restart the sync from cursor=null.
  
### **Wrong Way**
  // Not handling mutation error
  async function syncAllTransactions(accessToken: string) {
    let cursor = lastCursor;
  
    while (true) {
      try {
        const response = await plaidClient.transactionsSync({
          access_token: accessToken,
          cursor,
        });
  
        // Process transactions...
        cursor = response.data.next_cursor;
  
        if (!response.data.has_more) break;
      } catch (error) {
        // WRONG: Just failing on mutation error
        throw error;
      }
    }
  }
  
### **Right Way**
  async function syncAllTransactions(accessToken: string, itemId: string) {
    let cursor = await getLastCursor(itemId);
    let attempts = 0;
    const MAX_MUTATION_RETRIES = 3;
  
    while (attempts < MAX_MUTATION_RETRIES) {
      try {
        while (true) {
          const response = await plaidClient.transactionsSync({
            access_token: accessToken,
            cursor: cursor || undefined,
          });
  
          // Process transactions...
  
          cursor = response.data.next_cursor;
          await saveCursor(itemId, cursor);
  
          if (!response.data.has_more) {
            return;  // Sync complete
          }
        }
      } catch (error) {
        const errorCode = error.response?.data?.error_code;
  
        if (errorCode === 'TRANSACTIONS_SYNC_MUTATION_DURING_PAGINATION') {
          // Data changed, restart from beginning
          console.log('Mutation during pagination, restarting sync');
          cursor = null;
          attempts++;
          continue;
        }
  
        throw error;
      }
    }
  
    throw new Error('Max mutation retries exceeded');
  }
  
### **Detection Patterns**
  - transactionsSync.*catch(?!.*MUTATION)
### **References**
  - https://plaid.com/docs/api/products/transactions/#transactionssync

## Link Tokens Are Short-Lived and Single-Use

### **Id**
link-token-expiry
### **Severity**
medium
### **Description**
  Link tokens expire after 4 hours and can only be used once.
  Don't create them far in advance or cache them for reuse.
  
### **Wrong Way**
  // Creating link token at app startup
  let cachedLinkToken = null;
  
  async function init() {
    // WRONG: Token created once and reused
    const response = await plaidClient.linkTokenCreate({...});
    cachedLinkToken = response.data.link_token;
  }
  
  app.get('/api/link-token', (req, res) => {
    res.json({ link_token: cachedLinkToken });  // May be expired or used!
  });
  
### **Right Way**
  // Create fresh link token on demand
  app.post('/api/plaid/link-token', async (req, res) => {
    const { userId } = req.body;
  
    // Create fresh token for each Link session
    const response = await plaidClient.linkTokenCreate({
      user: { client_user_id: userId },
      client_name: 'My App',
      products: [Products.Transactions],
      country_codes: [CountryCode.Us],
      language: 'en',
      webhook: process.env.PLAID_WEBHOOK_URL,
    });
  
    res.json({
      link_token: response.data.link_token,
      expiration: response.data.expiration,  // Tell client when it expires
    });
  });
  
  // Frontend: Create token when opening Link
  async function openPlaidLink() {
    // Create fresh token right before opening
    const { link_token } = await fetch('/api/plaid/link-token', {
      method: 'POST',
      body: JSON.stringify({ userId }),
    }).then(r => r.json());
  
    // Use immediately
    const { open } = usePlaidLink({ token: link_token });
    open();
  }
  
### **Detection Patterns**
  - linkToken.*cache
  - link_token.*global
### **References**
  - https://plaid.com/docs/api/link/#linktokencreate

## Recurring Transactions Need 180+ Days of History

### **Id**
recurring-transactions-history
### **Severity**
medium
### **Description**
  Recurring transaction detection requires sufficient history to identify
  patterns. Default 90 days may not be enough. Request 180+ days for
  optimal results.
  
### **Wrong Way**
  // Using default 90 days for recurring detection
  const response = await plaidClient.linkTokenCreate({
    user: { client_user_id: userId },
    products: [Products.Transactions],
    // Default: 90 days - not enough for recurring!
  });
  
### **Right Way**
  // Request 180+ days for recurring transactions
  const response = await plaidClient.linkTokenCreate({
    user: { client_user_id: userId },
    products: [Products.Transactions],
    transactions: {
      days_requested: 180,  // Or 365 for annual subscriptions
    },
  });
  
  // When using recurring transactions API
  const recurringResponse = await plaidClient.transactionsRecurringGet({
    access_token: accessToken,
    options: {
      include_personal_finance_category: true,
    },
  });
  
  // Check if enough history exists
  if (recurringResponse.data.updated_datetime) {
    const historyStart = new Date(recurringResponse.data.updated_datetime);
    const daysSinceStart = (Date.now() - historyStart.getTime()) / (1000 * 60 * 60 * 24);
  
    if (daysSinceStart < 90) {
      console.warn('Limited recurring detection due to short history');
    }
  }
  
### **Detection Patterns**
  - Recurring.*days_requested(?!.*180)
  - transactionsRecurringGet(?!.*180)
### **References**
  - https://plaid.com/docs/api/products/transactions/#transactionsrecurringget