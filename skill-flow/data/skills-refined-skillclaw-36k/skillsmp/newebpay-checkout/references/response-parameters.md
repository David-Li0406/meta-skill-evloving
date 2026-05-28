# 回應參數詳細說明

本文檔說明藍新金流 MPG 交易的所有回應參數,包括支付完成和取號完成兩種情境。

## 目錄

- [回應方式](#回應方式)
- [回應參數結構](#回應參數結構)
- [支付完成回傳參數](#422-回應參數---支付完成)
- [取號完成回傳參數](#423-回應參數---取號完成)
- [解密與驗證流程](#解密與驗證流程)
- [完整處理範例](#完整處理範例)
- [注意事項](#注意事項)

---

## 回應方式

藍新金流會透過以下方式回傳結果:

1. **NotifyURL (幕後通知)**: 以 POST 方式將加密後的交易結果回傳到商店的後端
2. **ReturnURL (支付完成導回)**: 以 Form POST 方式將加密後的結果導回商店前端頁面
3. **CustomerURL (取號完成導回)**: 非即時支付取號完成後導回商店頁面

## 回應參數結構

### 外層參數 (Form Post)

| 參數名稱 | 型態 | 說明 |
|---------|------|------|
| Status | String(10) | `SUCCESS`=成功, 其他=錯誤代碼 |
| MerchantID | String(20) | 商店代號 |
| TradeInfo | AES加密 | 加密的交易資料 |
| TradeSha | SHA256加密 | TradeInfo的SHA256簽章 |
| Version | String(5) | 串接程式版本 |
| EncryptType | Int(1) | 若使用AES/GCM則回傳 |

## 4.2.2 回應參數 - 支付完成

適用於:
- **即時支付**: 信用卡、Apple Pay、Google Pay、Samsung Pay、WebATM、電子錢包、LINE Pay、台灣Pay、BitoPay
- **非即時支付**: 超商代碼、超商條碼、超商取貨付款、ATM (付款完成後)

### TradeInfo 解密後的內層參數

#### 所有支付方式共同參數

| 參數名稱 | 型態 | 說明 |
|---------|------|------|
| Status | String(10) | `SUCCESS`=成功, 其他=錯誤代碼 |
| Message | String(50) | 交易狀態描述訊息 |
| Result | Object | 當RespondType為JSON時,回傳參數放在此陣列 |
| MerchantID | String(15) | 商店代號 |
| Amt | Int(10) | 交易金額(新台幣) |
| TradeNo | String(20) | 藍新金流交易序號 |
| MerchantOrderNo | String(30) | 商店訂單編號 |
| PaymentType | String(10) | 支付方式代碼 |
| RespondType | String(10) | 回傳格式 (JSON/String) |
| PayTime | DateTime | 支付完成時間 YYYY-MM-DD HH:mm:ss |
| IP | String(15) | 付款人IP位址 |
| EscrowBank | String(10) | 款項保管銀行 (HNCB=華南銀行) |

### 信用卡支付回傳參數

適用於: 一次付清、分期、紅利、DCC、Apple Pay、Google Pay、Samsung Pay、國民旅遊卡、銀聯、美國運通卡

| 參數名稱 | 型態 | 說明 |
|---------|------|------|
| AuthBank | String(10) | 收單金融機構代碼 |
| CardBank | String(10) | 發卡金融機構 (若非台灣銀行則空白) |
| RespondCode | String(5) | 金融機構回應碼 |
| Auth | String(6) | 授權碼 |
| Card6No | String(6) | 卡號前六碼 |
| Card4No | String(4) | 卡號後四碼 |
| Inst | Int(10) | 分期期別 |
| InstFirst | Int(10) | 分期首期金額 |
| InstEach | Int(10) | 分期每期金額 |
| ECI | String(2) | ECI值 (1,2,5,6=3D交易) |
| TokenUseStatus | Int(1) | 快速結帳狀態: 0=未使用 1=首次設定 2=使用 9=取消 |
| RedAmt | Int(5) | 紅利折抵後實際金額 |
| PaymentMethod | String(15) | 交易類別 (詳見下方說明) |

#### PaymentMethod 交易類別對應

```
CREDIT = 台灣發卡機構信用卡
FOREIGN = 國外發卡機構信用卡
UNIONPAY = 銀聯卡
APPLEPAY = Apple Pay
GOOGLEPAY = Google Pay
SAMSUNGPAY = Samsung Pay
DCC = 動態貨幣轉換
GOOGLEPAY_FOREIGN = Google Pay (國外卡)
SAMSUNGPAY_FOREIGN = Samsung Pay (國外卡)
APPLEPAY_FOREIGN = Apple Pay (國外卡)
```

#### AuthBank 收單金融機構對應

```
Esun = 玉山銀行
Taishin = 台新銀行
CTBC = 中國信託銀行
NCCC = 聯合信用卡中心
CathayBK = 國泰世華銀行
Citibank = 花旗銀行
UBOT = 聯邦銀行
SKBank = 新光銀行
Fubon = 富邦銀行
FirstBank = 第一銀行
LINEBank = 連線商業銀行
SinoPac = 永豐銀行
KGI = 凱基銀行
```

### DCC 動態貨幣轉換回傳參數

僅支援台新銀行一次付清代收商店:

| 參數名稱 | 型態 | 說明 |
|---------|------|------|
| DCC_Amt | Float | 外幣金額 |
| DCC_Rate | Float | 匯率 |
| DCC_Markup | Float | 風險匯率 |
| DCC_Currency | String(4) | 幣別代碼 (USD/JPY/MOP等) |
| DCC_Currency_Code | Int(4) | 幣別數字代碼 (如MOP=446) |

### WebATM/ATM 繳費回傳參數

| 參數名稱 | 型態 | 說明 |
|---------|------|------|
| PayBankCode | String(10) | 付款人金融機構代碼 |
| PayerAccount5Code | String(5) | 付款人帳號末五碼 |

### 超商代碼繳費回傳參數

| 參數名稱 | 型態 | 說明 |
|---------|------|------|
| CodeNo | String(30) | 繳費代碼 |
| StoreType | Int(1) | 繳費門市: 1=7-11 2=全家 3=OK 4=萊爾富 |
| StoreID | String(10) | 繳費門市代號 |

### 超商條碼繳費回傳參數

| 參數名稱 | 型態 | 說明 |
|---------|------|------|
| Barcode_1 | String(20) | 第一段條碼 |
| Barcode_2 | String(20) | 第二段條碼 |
| Barcode_3 | String(20) | 第三段條碼 |
| RepayTimes | Int(3) | 付款次數 |
| PayStore | String(8) | 繳費超商: SEVEN/FAMILY/OK/HILIFE |

### 超商物流回傳參數

| 參數名稱 | 型態 | 說明 |
|---------|------|------|
| StoreCode | String(10) | 超商門市編號 |
| StoreName | String(15) | 超商門市名稱 |
| StoreType | String(10) | 超商類別: 全家/7-ELEVEN/萊爾富/OK mart |
| StoreAddr | String(100) | 超商門市地址 |
| TradeType | Int(1) | 取件方式: 1=取貨付款 3=取貨不付款 |
| CVSCOMName | String(20) | 取貨人姓名 |
| CVSCOMPhone | String(10) | 取貨人手機 |
| LgsNo | String(20) | 物流寄件單號 |
| LgsType | String(3) | 物流型態: B2C/C2C |

### 跨境支付回傳參數

適用於: 簡單付電子錢包、簡單付微信、簡單付支付寶

| 參數名稱 | 型態 | 說明 |
|---------|------|------|
| ChannelID | String(15) | 跨境通路類型 (詳見下方) |
| ChannelNo | String(32) | 跨境通路交易序號 |

#### ChannelID 跨境通路類型

```
ALIPAY = 支付寶
WECHATPAY = 微信支付
ACCLINK = 約定連結帳戶
CREDIT = 信用卡
CVS = 超商代碼
P2GEACC = 簡單付電子帳戶轉帳
VACC = ATM轉帳
WEBATM = WebATM轉帳
TWQR = TWQR跨機構
```

### 玉山 Wallet 回傳參數

| 參數名稱 | 型態 | 說明 |
|---------|------|------|
| PayAmt | Int(10) | 實際付款金額 |
| RedDisAmt | Int(5) | 紅利折抵金額 |

### 台灣Pay 回傳參數

| 參數名稱 | 型態 | 說明 |
|---------|------|------|
| PayAmt | Int(10) | 實際付款金額 |

### BitoPay 回傳參數

| 參數名稱 | 型態 | 說明 |
|---------|------|------|
| PayAmt | Int(10) | 實際付款金額 |
| CryptoCurrency | String(10) | 加密貨幣代號: BTC/ETH/USDT |
| CryptoAmount | String(60) | 加密貨幣數量 (如 1.123456) |
| CryptoRate | String(60) | 加密貨幣匯率 |

## 4.2.3 回應參數 - 取號完成

適用於: 超商代碼、超商條碼、超商取貨付款、ATM (取號完成時)

### TradeInfo 解密後的參數

#### 共同回傳參數

| 參數名稱 | 型態 | 說明 |
|---------|------|------|
| Status | String(10) | `SUCCESS`=取號成功, 其他=錯誤代碼 |
| Message | String(50) | 取號狀態描述 |
| Result | Object | JSON格式時的參數陣列 |
| MerchantID | String(15) | 商店代號 |
| Amt | Int(10) | 支付金額 |
| TradeNo | String(20) | 藍新金流交易序號 |
| MerchantOrderNo | String(30) | 商店訂單編號 |
| PaymentType | String(10) | 支付方式 |
| ExpireDate | DateTime | 繳費截止日期 YYYY-MM-DD |
| ExpireTime | String(6) | 繳費截止時間 His格式 (超商取貨不回傳) |

#### ATM 回傳參數

| 參數名稱 | 型態 | 說明 |
|---------|------|------|
| BankCode | String(10) | 金融機構代碼 |
| CodeNo | String(30) | 繳費代碼(虛擬帳號) |

#### 超商代碼回傳參數

| 參數名稱 | 型態 | 說明 |
|---------|------|------|
| CodeNo | String(30) | 繳費代碼 |
| StoreType | Int(1) | 門市類別: 1=7-11 2=全家 3=OK 4=萊爾富 |
| StoreID | String(10) | 門市代號 |

#### 超商條碼回傳參數

| 參數名稱 | 型態 | 說明 |
|---------|------|------|
| Barcode_1 | String(20) | 第一段條碼 |
| Barcode_2 | String(20) | 第二段條碼 |
| Barcode_3 | String(20) | 第三段條碼 |

#### 超商取貨付款回傳參數

| 參數名稱 | 型態 | 說明 |
|---------|------|------|
| StoreCode | String(10) | 門市編號 |
| StoreName | String(15) | 門市名稱 |
| StoreType | String(10) | 超商類別 |
| StoreAddr | String(100) | 門市地址 |
| TradeType | Int(1) | 1=取貨付款 3=取貨不付款 |
| CVSCOMName | String(20) | 取貨人姓名 |
| CVSCOMPhone | String(10) | 取貨人手機 |
| LgsNo | String(20) | 物流寄件單號 |
| LgsType | String(3) | B2C/C2C |

## 解密與驗證流程

### Step 1: 解密 TradeInfo

```php
<?php
function decrypt_trade_info($encrypted_data, $key, $iv) {
    // 解密
    $decrypted = openssl_decrypt(
        hex2bin($encrypted_data), 
        "AES-256-CBC", 
        $key, 
        OPENSSL_RAW_DATA|OPENSSL_ZERO_PADDING, 
        $iv
    );
    
    // 移除 PKCS7 padding
    $slast = ord(substr($decrypted, -1));
    $slastc = chr($slast);
    if (preg_match("/$slastc{" . $slast . "}/", $decrypted)) {
        $decrypted = substr($decrypted, 0, strlen($decrypted) - $slast);
    }
    
    return $decrypted;
}

$key = "你的HashKey";
$iv = "你的HashIV";
$trade_info = $_POST['TradeInfo'];

$decrypted = decrypt_trade_info($trade_info, $key, $iv);
parse_str($decrypted, $result);
?>
```

### Step 2: 驗證 TradeSha

```php
<?php
function verify_trade_sha($trade_info, $trade_sha, $key, $iv) {
    $check_string = "HashKey={$key}&{$trade_info}&HashIV={$iv}";
    $check_value = strtoupper(hash("sha256", $check_string));
    
    return $check_value === $trade_sha;
}

$is_valid = verify_trade_sha(
    $_POST['TradeInfo'], 
    $_POST['TradeSha'], 
    $key, 
    $iv
);

if ($is_valid) {
    // 驗證成功,處理訂單
} else {
    // 驗證失敗,記錄異常
}
?>
```

### Step 3: 驗證 CheckCode (選用)

```php
<?php
function create_check_code($result, $key, $iv) {
    $check_arr = [
        'Amt' => $result['Amt'],
        'MerchantID' => $result['MerchantID'],
        'MerchantOrderNo' => $result['MerchantOrderNo'],
        'TradeNo' => $result['TradeNo']
    ];
    
    ksort($check_arr);
    $check_str = http_build_query($check_arr);
    $check_code = "HashIV={$iv}&{$check_str}&HashKey={$key}";
    
    return strtoupper(hash("sha256", $check_code));
}

// 若回應中有 CheckCode,可進行二次驗證
if (isset($result['CheckCode'])) {
    $calculated_code = create_check_code($result, $key, $iv);
    if ($calculated_code === $result['CheckCode']) {
        // CheckCode 驗證成功
    }
}
?>
```

## 完整處理範例

```php
<?php
// 接收藍新金流回傳
$key = "你的HashKey";
$iv = "你的HashIV";

// 1. 驗證 TradeSha
if (!verify_trade_sha($_POST['TradeInfo'], $_POST['TradeSha'], $key, $iv)) {
    http_response_code(400);
    exit("Invalid signature");
}

// 2. 解密 TradeInfo
$decrypted = decrypt_trade_info($_POST['TradeInfo'], $key, $iv);
parse_str($decrypted, $result);

// 3. 檢查交易狀態
if ($result['Status'] === 'SUCCESS') {
    // 交易成功
    $trade_no = $result['TradeNo'];
    $order_no = $result['MerchantOrderNo'];
    $amount = $result['Amt'];
    $payment_type = $result['PaymentType'];
    
    // 更新訂單狀態
    update_order_status($order_no, 'paid', $trade_no);
    
    // 根據不同支付方式做額外處理
    if ($payment_type === 'CREDIT') {
        // 信用卡支付
        $auth = $result['Auth'];
        $card4no = $result['Card4No'];
        log_payment("信用卡 {$card4no}, 授權碼: {$auth}");
    } elseif ($payment_type === 'VACC') {
        // ATM 轉帳
        $bank_code = $result['PayBankCode'];
        log_payment("ATM 轉帳, 銀行代碼: {$bank_code}");
    }
    
    echo "SUCCESS";
} else {
    // 交易失敗
    $error_code = $result['Status'];
    $message = $result['Message'];
    log_error("訂單 {$result['MerchantOrderNo']} 失敗: {$error_code} - {$message}");
    
    echo "FAIL";
}
?>
```

## 注意事項

1. **安全性**
   - 務必驗證 TradeSha 確保資料來自藍新金流
   - 解密後的資料不可直接信任,需再次驗證
   - CheckCode 提供額外的驗證機制

2. **NotifyURL vs ReturnURL**
   - NotifyURL: 後端處理,更新訂單狀態,回應 "SUCCESS"
   - ReturnURL: 前端顯示,給消費者看結果
   - 兩者可能時間不同步,以 NotifyURL 為準

3. **非即時支付**
   - 取號完成時會先收到 CustomerURL 回傳
   - 實際付款完成後才會收到 NotifyURL 回傳
   - 需分別處理兩種回傳

4. **超商取貨**
   - PayTime 會是空值
   - 需等待物流通知才能出貨
   - LgsNo 是物流單號,用於追蹤貨物

5. **回應格式**
   - NotifyURL 必須回應 "SUCCESS" 表示接收成功
   - 若未正確回應,藍新金流會重複通知
   - 建議實作冪等性機制避免重複處理
