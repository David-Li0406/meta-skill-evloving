---
name: TapPay Integration
description: TapPay 金流串接指南 - 前端 SDK 設定、後端 API 串接、測試與除錯
---

# TapPay 金流串接指南

本 Skill 提供 TapPay 金流系統的完整串接指南，包含前端 SDK 設定、後端 API 呼叫、測試卡號及除錯方法。

---

## 1. TapPay 基本概念

### 付款流程
```
使用者輸入卡號 → 前端取得 Prime → 後端呼叫 Pay by Prime API → 回傳交易結果
```

### 兩種付款方式

| 方式 | 說明 | 使用情境 |
|------|------|----------|
| **Pay by Prime** | 使用一次性的 prime 字串進行交易 | 一般單次付款 |
| **Pay by Token** | 使用 card_key + card_token 進行交易 | 訂閱制、定期扣款 |

### 環境 URL

| 環境 | URL |
|------|-----|
| Sandbox (測試) | `https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime` |
| Production (正式) | `https://prod.tappaysdk.com/tpc/payment/pay-by-prime` |

---

## 2. 取得串接金鑰

前往 [TapPay 廠商管理後台](https://portal.tappaysdk.com/dashboard):

1. **APP ID & APP Key**: 開發者 → 應用程式
2. **Partner Key**: 帳戶資訊
3. **Merchant ID**: 商家管理 → 商家設置 → 正式/測試環境

### Sandbox 測試金鑰 (本專案使用)
```javascript
// 前端 SDK
APP_ID: 166632
APP_KEY: 'app_eLtyNlnXhUY9PkZoJUw8wjU0o7Ts0iCe14YW6CND4AqYmi5hq8KR4PhKL9DA'

// 後端 API
PARTNER_KEY: 'partner_PHNbIt8d88834446583'
MERCHANT_ID: 'GlobalTesting_CTBC'
```

---

## 3. 前端設定 (React/TypeScript)

### Step 1: 載入 TapPay SDK

在 `index.html` 加入:
```html
<script src="https://js.tappaysdk.com/sdk/tpdirect/v5.18.0"></script>
```

### Step 2: 初始化 SDK

```typescript
declare const TPDirect: any;

// 設定 SDK
TPDirect.setupSDK(
    166632, // APP_ID
    'app_eLtyNlnXhUY9PkZoJUw8wjU0o7Ts0iCe14YW6CND4AqYmi5hq8KR4PhKL9DA', // APP_KEY
    'sandbox' // 'sandbox' 或 'production'
);
```

### Step 3: 設定信用卡輸入欄位

```typescript
TPDirect.card.setup({
    fields: {
        number: {
            element: '#card-number',
            placeholder: '**** **** **** ****'
        },
        expirationDate: {
            element: '#card-expiration-date',
            placeholder: 'MM / YY'
        },
        ccv: {
            element: '#card-ccv',
            placeholder: 'CCV'
        }
    },
    styles: {
        'input': { 'color': 'gray' },
        '.valid': { 'color': 'green' },
        '.invalid': { 'color': 'red' }
    }
});
```

### Step 4: 取得 Prime

```typescript
const onSubmit = () => {
    const tappayStatus = TPDirect.card.getTappayFieldsStatus();

    if (tappayStatus.canGetPrime === false) {
        console.error('卡片資訊不完整');
        return;
    }

    TPDirect.card.getPrime((result: any) => {
        if (result.status !== 0) {
            console.error('取得 Prime 失敗:', result.msg);
            return;
        }

        const prime = result.card.prime;
        // 將 prime 傳送至後端
        sendToBackend(prime);
    });
};
```

### HTML 結構
```html
<div id="card-number" class="tappay-field"></div>
<div id="card-expiration-date" class="tappay-field"></div>
<div id="card-ccv" class="tappay-field"></div>
```

---

## 4. 後端 API 串接 (Node.js/Express)

### Pay by Prime API

```typescript
import axios from 'axios';

const TAPPAY_PARTNER_KEY = process.env.TAPPAY_PARTNER_KEY;
const TAPPAY_MERCHANT_ID = process.env.TAPPAY_MERCHANT_ID;
const TAPPAY_URL = 'https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime';

export const payByPrime = async (req, res) => {
    const { prime, amount, orderId } = req.body;

    try {
        const response = await axios.post(TAPPAY_URL, {
            prime,
            partner_key: TAPPAY_PARTNER_KEY,
            merchant_id: TAPPAY_MERCHANT_ID,
            details: "商品描述",
            amount: amount,
            cardholder: {
                phone_number: "0912345678",
                name: "王小明",
                email: "test@example.com"
            },
            remember: false // 設為 true 可取得 card_key/card_token
        }, {
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': TAPPAY_PARTNER_KEY
            }
        });

        const data = response.data;

        if (data.status === 0) {
            // 交易成功
            return res.json({
                success: true,
                transactionId: data.rec_trade_id,
                bankTransactionId: data.bank_transaction_id
            });
        } else {
            // 交易失敗
            return res.status(400).json({
                success: false,
                error: data.msg,
                status: data.status
            });
        }
    } catch (error) {
        console.error('TapPay API Error:', error);
        return res.status(500).json({ error: 'Payment processing failed' });
    }
};
```

### API Request 參數

| 參數 | 類型 | 必填 | 說明 |
|------|------|------|------|
| `prime` | string | ✅ | 前端取得的一次性 token |
| `partner_key` | string | ✅ | 商戶金鑰 |
| `merchant_id` | string | ✅ | 商戶 ID |
| `amount` | number | ✅ | 交易金額 (TWD: 1-20,000,000) |
| `details` | string | ✅ | 商品描述 |
| `cardholder` | object | ✅ | 持卡人資訊 |
| `remember` | boolean | ❌ | 是否記憶卡片 (預設 false) |

### API Response 欄位

| 欄位 | 說明 |
|------|------|
| `status` | 0 = 成功, 其他 = 失敗 |
| `msg` | 錯誤訊息 |
| `rec_trade_id` | TapPay 交易編號 |
| `bank_transaction_id` | 銀行交易編號 |
| `card_key` | 卡片金鑰 (remember=true 時) |
| `card_token` | 卡片 token (remember=true 時) |

---

## 5. LINE Pay 整合

### 前端取得 LINE Pay Prime

```typescript
TPDirect.linePay.getPrime((result: any) => {
    if (result.status !== 0) {
        console.error('LINE Pay Prime 失敗:', result.msg);
        return;
    }

    const prime = result.prime;
    sendToBackend(prime, 'line_pay');
});
```

### 後端處理 (需額外設定)

LINE Pay 需要設定 `result_url` 用於付款完成後跳轉:

```typescript
const response = await axios.post(TAPPAY_URL, {
    prime,
    partner_key: TAPPAY_PARTNER_KEY,
    merchant_id: TAPPAY_MERCHANT_ID,
    amount: amount,
    details: "商品描述",
    cardholder: { /* ... */ },
    result_url: {
        frontend_redirect_url: "https://your-site.com/payment/result",
        backend_notify_url: "https://your-site.com/api/payment/notify"
    }
});
```

---

## 6. 測試卡號

### 信用卡測試號碼

| 卡別 | 卡號 | 有效期 | CCV |
|------|------|--------|-----|
| VISA (正常) | 4242-4242-4242-4242 | 任意未來日期 | 123 |
| VISA (3D驗證) | 4311-9522-2222-2222 | 任意未來日期 | 123 |
| MasterCard | 5425-2334-3010-9903 | 任意未來日期 | 123 |
| JCB | 3530-1113-3330-0000 | 任意未來日期 | 123 |

### 測試失敗情境

| 卡號 | 模擬情境 |
|------|----------|
| 4111-1111-1111-1111 | 餘額不足 |
| 4222-2222-2222-2222 | 拒絕交易 |

---

## 7. 錯誤代碼

### 常見 Status Code

| Status | 說明 | 處理方式 |
|--------|------|----------|
| 0 | 成功 | 正常處理 |
| -1 | 系統錯誤 | 重試或聯繫 TapPay |
| 10003 | Prime 已過期 (90秒) | 重新取得 Prime |
| 10009 | Prime 已使用 | 重新取得 Prime |
| 100 | 信用卡授權失敗 | 請用戶確認卡片資訊 |
| 10007 | Partner Key 無效 | 檢查金鑰設定 |

---

## 8. 本專案實作參考

### 相關檔案位置

| 檔案 | 說明 |
|------|------|
| `client/src/components/PaymentModal.tsx` | 前端支付彈窗 |
| `server/src/controllers/paymentController.ts` | 後端支付處理 |
| `server/src/routes/paymentRoutes.ts` | 支付路由定義 |

### 環境變數 (.env)

```bash
# TapPay 設定 (後端)
TAPPAY_PARTNER_KEY=partner_xxxxx
TAPPAY_MERCHANT_ID=your_merchant_id
```

### API 端點

```
POST /api/payment/pay
Content-Type: application/json
Authorization: Bearer <token>

{
    "prime": "prime_string_from_frontend",
    "paymentMethod": "credit_card",
    "details": {
        "amount": 90,
        "currency": "TWD"
    },
    "purchaseType": "PREMIUM"
}
```

---

## 9. 除錯指南

### 前端問題排查

```javascript
// 檢查 SDK 是否載入
console.log(typeof TPDirect); // 應為 'object'

// 檢查欄位狀態
const status = TPDirect.card.getTappayFieldsStatus();
console.log(status);
// {
//   canGetPrime: true/false,
//   hasError: true/false,
//   status: { number: 2, expiry: 2, ccv: 2 } // 2=valid, 0=empty, 1=invalid
// }
```

### 後端問題排查

```bash
# 測試 TapPay API 連線
curl -X POST https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime \
  -H "Content-Type: application/json" \
  -H "x-api-key: partner_PHNbIt8d88834446583" \
  -d '{
    "prime": "test_prime",
    "partner_key": "partner_PHNbIt8d88834446583",
    "merchant_id": "GlobalTesting_CTBC",
    "amount": 100,
    "details": "Test",
    "cardholder": {
      "phone_number": "0912345678",
      "name": "Test",
      "email": "test@test.com"
    }
  }'
```

### 常見問題

| 問題 | 原因 | 解決方式 |
|------|------|----------|
| TPDirect is undefined | SDK 未載入 | 確認 script tag 在 HTML head |
| canGetPrime = false | 欄位資訊不完整 | 檢查卡號、日期、CCV 格式 |
| Prime 過期 | 超過 90 秒 | 重新呼叫 getPrime |
| 401 Unauthorized | Partner Key 錯誤 | 檢查 x-api-key header |
| CORS Error | 前端直接呼叫 TapPay | Prime 要透過後端送出 |

---

## 10. 參考資源

- [TapPay 官方文件](https://docs.tappaysdk.com/tutorial/zh/home.html)
- [TapPay GitHub 範例](https://github.com/TapPay/tappay-web-example)
- [TapPay 管理後台](https://portal.tappaysdk.com/dashboard)
- [Backend API Reference](https://docs.tappaysdk.com/tutorial/zh/back.html)

---

**Last Updated**: 2026-01-19
**Maintainer**: Wishlist App Team
