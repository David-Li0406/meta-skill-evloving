# MPG 交易完整參數說明

本文檔詳細說明藍新金流 MPG (Multiple Payment Gateway) 交易的所有請求參數和設定方式。

## 目錄

- [API 端點](#api-端點)
- [請求參數結構](#請求參數結構)
- [支付方式啟用參數](#支付方式啟用參數)
- [國民旅遊卡參數](#國民旅遊卡參數)
- [信用卡記憶卡號參數](#信用卡記憶卡號參數)
- [訂單細項參數 OrderDetail](#訂單細項參數-orderdetail)
- [重要注意事項](#重要注意事項)
- [完整PHP範例](#完整php範例)

---

## API 端點

**測試環境**: `https://ccore.newebpay.com/MPG/mpg_gateway`  
**正式環境**: `https://core.newebpay.com/MPG/mpg_gateway`

## HTTP Method

POST

## 請求參數結構

### 第一層參數 (Form Post)

| 參數名稱 | 必填 | 型態 | 說明 |
|---------|------|------|------|
| MerchantID | V | String(15) | 藍新金流商店代號 |
| TradeInfo | V | AES加密 | 將交易資料透過商店Key及IV進行AES256加密 |
| TradeSha | V | SHA256加密 | 將加密後的TradeInfo透過Key及IV進行SHA256加密 |
| Version | V | String(5) | 串接程式版本,目前為 `2.3` |
| EncryptType |  | Int(1) | 加密模式: `1`=AES/GCM, `0`或空=AES/CBC/PKCS7Padding |

### TradeInfo 內含參數

#### 基本必填參數

| 參數名稱 | 必填 | 型態 | 說明 |
|---------|------|------|------|
| MerchantID | V | String(15) | 藍新金流商店代號 |
| RespondType | V | String(6) | 回傳格式: `JSON` 或 `String` |
| TimeStamp | V | String(50) | Unix timestamp (秒數),容許誤差±120秒 |
| Version | V | String(5) | 串接程式版本 `2.3` |
| MerchantOrderNo | V | String(30) | 商店訂單編號,限英數字底線,不可重複 |
| Amt | V | Int(10) | 訂單金額(新台幣),純數字 |
| ItemDesc | V | String(50) | 商品資訊,UTF-8編碼,避免特殊符號 |

#### 選填基本參數

| 參數名稱 | 型態 | 說明 |
|---------|------|------|
| LangType | String(5) | 語系: `en`/`zh-tw`/`jp`,預設繁中 |
| TradeLimit | Int(3) | 交易有效秒數,60-900秒,0=不限制 |
| ExpireDate | String(10) | 繳費有效期限(非即時支付),格式Ymd,最長180天 |
| ExpireTime | String(6) | 繳費截止時間(超商代碼/ATM),格式His |
| OrderComment | String(300) | 商店備註,顯示於MPG頁面 |

#### 回傳URL設定

| 參數名稱 | 型態 | 說明 |
|---------|------|------|
| ReturnURL | String(200) | 支付完成後Form Post導回商店,限80/443 port |
| NotifyURL | String(200) | 幕後通知商店支付結果,限80/443 port |
| CustomerURL | String(200) | 取號完成後導回(非即時支付),限80/443 port |
| ClientBackURL | String(200) | MPG頁面返回鈕URL |

#### 付款人資訊

| 參數名稱 | 型態 | 說明 |
|---------|------|------|
| Email | String(50) | 付款人電子信箱 |
| EmailModify | Int(1) | 是否可修改Email: `1`=可修改 `0`=不可 |

## 支付方式啟用參數

### 信用卡相關

| 參數名稱 | 型態 | 說明 |
|---------|------|------|
| CREDIT | Int(1) | 信用卡一次付清: `1`=啟用 `0`=不啟用 |
| InstFlag | String(18) | 分期期數: `1`=全部, `3,6,12`=指定期數, `0`=不啟用 |
| CreditRed | Int(1) | 信用卡紅利: `1`=啟用 `0`=不啟用 |
| UNIONPAY | Int(1) | 銀聯卡: `1`=啟用 `0`=不啟用 |
| CREDITAE | Int(1) | 美國運通卡: `1`=啟用 `0`=不啟用 |

**分期期數說明**:
- 可用值: `3`, `6`, `8`(閘道商店), `12`, `18`, `24`, `30`
- 多期用逗號分隔,例: `3,6,12`

### 行動支付

| 參數名稱 | 型態 | 說明 |
|---------|------|------|
| APPLEPAY | Int(1) | Apple Pay: `1`=啟用 `0`=不啟用 |
| ANDROIDPAY | Int(1) | Google Pay: `1`=啟用 `0`=不啟用 |
| SAMSUNGPAY | Int(1) | Samsung Pay: `1`=啟用 `0`=不啟用 |

### 電子錢包

| 參數名稱 | 型態 | 說明 |
|---------|------|------|
| LINEPAY | Int(1) | LINE Pay: `1`=啟用 `0`=不啟用 |
| ImageUrl | String(200) | LINE Pay產品圖檔URL (84x84 jpg/png) |
| ESUNWALLET | Int(1) | 玉山Wallet: `1`=啟用 `0`=不啟用 |
| TAIWANPAY | Int(1) | 台灣Pay: `1`=啟用 `0`=不啟用 (限<50,000) |
| BITOPAY | Int(1) | BitoPay: `1`=啟用 `0`=不啟用 (100-49,999) |
| TWQR | Int(1) | TWQR/簡單付: `1`=啟用 `0`=不啟用 |
| TWQR_LifeTime | Int(7) | TWQR有效秒數,預設300秒,最長31天 |
| EZPWECHAT | Int(1) | 簡單付微信: `1`=啟用 `0`=不啟用 |
| EZPALIPAY | Int(1) | 簡單付支付寶: `1`=啟用 `0`=不啟用 |
| WalletDisplayMode | Int(1) | 電子支付模式: `1`=固定QR Code `0`=自動 |

### ATM轉帳

| 參數名稱 | 型態 | 說明 |
|---------|------|------|
| WEBATM | Int(1) | WebATM: `1`=啟用 (限<50,000且非手機) |
| VACC | Int(1) | ATM轉帳: `1`=啟用 (限<50,000) |
| BankType | String(26) | 指定銀行: `BOT`/`HNCB`/`KGI`,多個用逗號分隔 |
| SourceType | Int(1) | 智慧ATM2.0轉帳銀行設定 (0-4) |
| SourceBankId | String(3) | 指定轉帳銀行代碼(SourceType=1或3時必填) |
| SourceAccountNo | String(16) | 指定轉帳銀行帳號(SourceType=1或3時必填) |

**SourceType 說明**:
- `0`或空 = 關閉,支援台銀/華南/凱基
- `1` = 凱基,帳號必填且不可修改
- `2` = 凱基,帳號必填可修改
- `3` = 台銀/華南/凱基,選凱基時帳號必填不可修改
- `4` = 台銀/華南/凱基,選凱基時帳號必填可修改

### 超商支付

| 參數名稱 | 型態 | 說明 |
|---------|------|------|
| CVS | Int(1) | 超商代碼: `1`=啟用 (30-20,000元) |
| BARCODE | Int(1) | 超商條碼: `1`=啟用 (20-40,000元) |
| CVSCOM | Int(1) | 超商取貨: `1`=不付款 `2`=付款 `3`=兩者 (限<20,000) |
| LgsType | String(3) | 物流型態: `B2C`=大宗寄倉(7-11) `C2C`=店到店 |

## 國民旅遊卡參數

| 參數名稱 | 型態 | 說明 |
|---------|------|------|
| NTCB | Int(1) | 是否為國旅卡: `1`=是 `0`=否 |
| NTCBLocate | String(3) | 旅遊地區代號 (001-029) |
| NTCBStartDate | String(10) | 起始日期 YYYY-MM-DD |
| NTCBEndDate | String(10) | 結束日期 YYYY-MM-DD |

## 信用卡記憶卡號參數

| 參數名稱 | 型態 | 說明 |
|---------|------|------|
| TokenTerm | String(20) | 付款人綁定資料(會員編號/Email) |
| TokenTermDemand | Int(1) | 必填欄位: `1`=到期+CVV `2`=到期 `3`=CVV `4`=非必填 |

## 訂單細項參數 OrderDetail

訂單細項為 JSON 陣列,每個品項包含:

| 參數名稱 | 必填 | 型態 | 說明 |
|---------|------|------|------|
| ItemName | V | String(20) | 品項名稱 |
| ItemAmt | V | Int(10) | 品項金額(需總和等於訂單金額) |
| ItemType | V | Int(1) | 品項性質: `1`=一般 `2`=票券 `3`=儲值 |
| ItemOrderNo | V | String(20) | 品項編號(不可重複) |

範例:
```json
[
  {
    "ItemName": "商品A",
    "ItemAmt": 500,
    "ItemType": 1,
    "ItemOrderNo": "ITEM001"
  },
  {
    "ItemName": "商品B",
    "ItemAmt": 500,
    "ItemType": 1,
    "ItemOrderNo": "ITEM002"
  }
]
```

## 重要注意事項

1. **支付方式預設值**: 當所有支付方式參數都未設定時,以商店設定值為準
2. **URL設定優先順序**: API參數 > 商店後台設定
3. **ReturnURL vs NotifyURL**: 
   - 兩者會分別收到回應,不可設為同一URL
   - ReturnURL 在前端顯示給消費者
   - NotifyURL 在後端更新訂單狀態
4. **Port限制**: 所有回傳URL只接受 80 和 443 port

## 完整PHP範例

```php
<?php
$key = "你的HashKey";
$iv = "你的HashIV";
$mid = "你的商店代號";

$data = http_build_query([
    'MerchantID' => $mid,
    'TimeStamp' => time(),
    'Version' => '2.3',
    'RespondType' => 'JSON',
    'MerchantOrderNo' => "ORDER_" . time(),
    'Amt' => '1000',
    'ItemDesc' => '測試商品',
    'Email' => 'buyer@example.com',
    // 啟用支付方式
    'CREDIT' => '1',
    'LINEPAY' => '1',
    'VACC' => '1',
    'CVS' => '1',
    // 回傳URL
    'ReturnURL' => 'https://yourdomain.com/return',
    'NotifyURL' => 'https://yourdomain.com/notify',
]);

// AES加密
$encrypted = bin2hex(openssl_encrypt(
    $data, 
    "AES-256-CBC", 
    $key, 
    OPENSSL_RAW_DATA, 
    $iv
));

// SHA256簽章
$hash_str = "HashKey={$key}&{$encrypted}&HashIV={$iv}";
$trade_sha = strtoupper(hash("sha256", $hash_str));
?>

<form method="post" action="https://ccore.newebpay.com/MPG/mpg_gateway">
    <input name="MerchantID" value="<?= $mid ?>" />
    <input name="Version" value="2.3" />
    <input name="TradeInfo" value="<?= $encrypted ?>" />
    <input name="TradeSha" value="<?= $trade_sha ?>" />
    <button type="submit">前往付款</button>
</form>
```
