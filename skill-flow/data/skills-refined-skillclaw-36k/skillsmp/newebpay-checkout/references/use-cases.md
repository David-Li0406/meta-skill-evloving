# 常見使用情境

本文檔提供藍新金流整合的常見使用情境和完整程式碼範例。

## 目錄

- [情境 1: 建立基本的信用卡支付](#情境-1-建立基本的信用卡支付)
- [情境 2: 多元支付 (信用卡 + ATM + 超商)](#情境-2-多元支付-信用卡--atm--超商)
- [情境 3: 信用卡分期付款](#情境-3-信用卡分期付款)
- [情境 4: LINE Pay 整合](#情境-4-line-pay-整合)
- [情境 5: 超商取貨付款](#情境-5-超商取貨付款)
- [情境 6: Apple Pay / Google Pay](#情境-6-apple-pay--google-pay)
- [情境 7: 信用卡記憶卡號 (快速結帳)](#情境-7-信用卡記憶卡號-快速結帳)
- [情境 8: 智慧ATM 2.0 (指定轉帳帳號)](#情境-8-智慧atm-20-指定轉帳帳號)
- [情境 9: 國民旅遊卡交易](#情境-9-國民旅遊卡交易)
- [情境 10: 電子支付 (台灣Pay / TWQR)](#情境-10-電子支付-台灣pay--twqr)
- [情境 11: 處理 NotifyURL 回傳](#情境-11-處理-notifyurl-回傳)
- [情境 12: 訂單細項參數](#情境-12-訂單細項參數)
- [完整的購物車結帳流程](#完整的購物車結帳流程)

---

## 情境 1: 建立基本的信用卡支付

最簡單的實作,只啟用信用卡一次付清功能。

```php
<?php
require_once 'encryption.php';

// 初始化加密工具
$crypto = new NewebPayCrypto(
    "你的HashKey",
    "你的HashIV"
);

// 準備訂單資料
$order_data = [
    'MerchantID' => 'MS12345678',
    'TimeStamp' => time(),
    'Version' => '2.3',
    'RespondType' => 'JSON',
    'MerchantOrderNo' => 'ORDER_' . time(),
    'Amt' => '1000',
    'ItemDesc' => '商品名稱',
    'Email' => 'buyer@example.com',
    
    // 啟用信用卡
    'CREDIT' => '1',
    
    // 回傳URL
    'ReturnURL' => 'https://yourdomain.com/return',
    'NotifyURL' => 'https://yourdomain.com/notify',
];

// 加密並產生表單
$trade_info_raw = http_build_query($order_data);
$trade_info = $crypto->encrypt($trade_info_raw);
$trade_sha = $crypto->generateTradeSha($trade_info);
?>

<form method="post" action="https://ccore.newebpay.com/MPG/mpg_gateway">
    <input type="hidden" name="MerchantID" value="MS12345678">
    <input type="hidden" name="Version" value="2.3">
    <input type="hidden" name="TradeInfo" value="<?= htmlspecialchars($trade_info) ?>">
    <input type="hidden" name="TradeSha" value="<?= $trade_sha ?>">
    <button type="submit">前往付款</button>
</form>
```

## 情境 2: 多元支付 (信用卡 + ATM + 超商)

讓消費者可以選擇多種支付方式。

```php
<?php
$order_data = [
    'MerchantID' => 'MS12345678',
    'TimeStamp' => time(),
    'Version' => '2.3',
    'RespondType' => 'JSON',
    'MerchantOrderNo' => 'ORDER_' . time(),
    'Amt' => '1500',
    'ItemDesc' => '多元支付商品',
    'Email' => 'buyer@example.com',
    'TradeLimit' => 600,  // 10分鐘交易時間
    
    // 啟用多種支付方式
    'CREDIT' => '1',           // 信用卡
    'VACC' => '1',             // ATM轉帳
    'CVS' => '1',              // 超商代碼
    'BARCODE' => '1',          // 超商條碼
    
    // 非即時支付設定
    'ExpireDate' => date('Ymd', strtotime('+7 days')),  // 7天繳費期限
    
    // 回傳URL
    'ReturnURL' => 'https://yourdomain.com/return',
    'NotifyURL' => 'https://yourdomain.com/notify',
    'CustomerURL' => 'https://yourdomain.com/cvs_notify',  // 取號通知
];
```

## 情境 3: 信用卡分期付款

提供3期、6期、12期分期選項。

```php
<?php
$order_data = [
    'MerchantID' => 'MS12345678',
    'TimeStamp' => time(),
    'Version' => '2.3',
    'RespondType' => 'JSON',
    'MerchantOrderNo' => 'ORDER_' . time(),
    'Amt' => '12000',  // 分期通常需要較高金額
    'ItemDesc' => '筆記型電腦',
    'Email' => 'buyer@example.com',
    
    // 啟用信用卡和分期
    'CREDIT' => '1',
    'InstFlag' => '3,6,12',  // 開啟3期、6期、12期
    
    'ReturnURL' => 'https://yourdomain.com/return',
    'NotifyURL' => 'https://yourdomain.com/notify',
];
```

## 情境 4: LINE Pay 整合

啟用 LINE Pay 支付並設定商品圖片。

```php
<?php
$order_data = [
    'MerchantID' => 'MS12345678',
    'TimeStamp' => time(),
    'Version' => '2.3',
    'RespondType' => 'JSON',
    'MerchantOrderNo' => 'ORDER_' . time(),
    'Amt' => '800',
    'ItemDesc' => 'LINE貼圖組合包',
    'Email' => 'buyer@example.com',
    
    // 啟用 LINE Pay
    'LINEPAY' => '1',
    'ImageUrl' => 'https://yourdomain.com/product/image.jpg',  // 84x84 jpg/png
    
    // 信用卡作為備選
    'CREDIT' => '1',
    
    'ReturnURL' => 'https://yourdomain.com/return',
    'NotifyURL' => 'https://yourdomain.com/notify',
];
```

## 情境 5: 超商取貨付款

整合超商物流和取貨付款功能。

```php
<?php
$order_data = [
    'MerchantID' => 'MS12345678',
    'TimeStamp' => time(),
    'Version' => '2.3',
    'RespondType' => 'JSON',
    'MerchantOrderNo' => 'ORDER_' . time(),
    'Amt' => '1200',  // 需小於20,000
    'ItemDesc' => '電子配件',
    'Email' => 'buyer@example.com',
    
    // 超商取貨付款
    'CVSCOM' => '2',        // 2=取貨付款
    'LgsType' => 'C2C',     // C2C=店到店, B2C=大宗寄倉
    
    // 取號完成通知
    'CustomerURL' => 'https://yourdomain.com/cvs_result',
    // 付款完成通知
    'NotifyURL' => 'https://yourdomain.com/notify',
];

// 處理取號回傳
// CustomerURL 會收到門市資訊: StoreCode, StoreName, StoreAddr 等
```

## 情境 6: Apple Pay / Google Pay

啟用行動支付方式。

```php
<?php
$order_data = [
    'MerchantID' => 'MS12345678',
    'TimeStamp' => time(),
    'Version' => '2.3',
    'RespondType' => 'JSON',
    'MerchantOrderNo' => 'ORDER_' . time(),
    'Amt' => '2500',
    'ItemDesc' => '線上課程',
    'Email' => 'buyer@example.com',
    
    // 行動支付
    'APPLEPAY' => '1',      // Apple Pay
    'ANDROIDPAY' => '1',    // Google Pay
    'SAMSUNGPAY' => '1',    // Samsung Pay
    
    // 傳統信用卡作為備選
    'CREDIT' => '1',
    
    'ReturnURL' => 'https://yourdomain.com/return',
    'NotifyURL' => 'https://yourdomain.com/notify',
];
```

## 情境 7: 信用卡記憶卡號 (快速結帳)

讓熟客可以快速完成付款。

```php
<?php
// 首次購買: 設定記憶卡號
$order_data = [
    'MerchantID' => 'MS12345678',
    'TimeStamp' => time(),
    'Version' => '2.3',
    'RespondType' => 'JSON',
    'MerchantOrderNo' => 'ORDER_' . time(),
    'Amt' => '500',
    'ItemDesc' => '會員訂閱',
    'Email' => 'member@example.com',
    
    'CREDIT' => '1',
    
    // 記憶卡號設定
    'TokenTerm' => 'MEMBER_12345',        // 會員編號
    'TokenTermDemand' => '1',             // 1=到期日+CVV都要填
    
    'ReturnURL' => 'https://yourdomain.com/return',
    'NotifyURL' => 'https://yourdomain.com/notify',
];

// 第二次購買: 使用記憶卡號
// 只需再次傳送相同的 TokenTerm
// 系統會自動帶入卡號前六後四碼
$order_data_2 = [
    // ... 其他參數相同 ...
    'TokenTerm' => 'MEMBER_12345',  // 相同的會員編號
    'TokenTermDemand' => '4',       // 4=到期日和CVV都非必填 (最快速)
];
```

## 情境 8: 智慧ATM 2.0 (指定轉帳帳號)

要求消費者從特定銀行帳戶轉帳。

```php
<?php
$order_data = [
    'MerchantID' => 'MS12345678',
    'TimeStamp' => time(),
    'Version' => '2.3',
    'RespondType' => 'JSON',
    'MerchantOrderNo' => 'ORDER_' . time(),
    'Amt' => '3000',
    'ItemDesc' => '企業訂單',
    'Email' => 'company@example.com',
    
    // ATM轉帳
    'VACC' => '1',
    'BankType' => 'KGI',  // 僅凱基銀行
    
    // 智慧ATM 2.0 - 指定轉帳帳號
    'SourceType' => '1',              // 1=帳號必填且不可修改
    'SourceBankId' => '822',          // 銀行代碼 (822=凱基)
    'SourceAccountNo' => '1234567890123456',  // 指定帳號
    
    'ExpireDate' => date('Ymd', strtotime('+3 days')),
    
    'CustomerURL' => 'https://yourdomain.com/atm_result',
    'NotifyURL' => 'https://yourdomain.com/notify',
];
```

## 情境 9: 國民旅遊卡交易

處理國旅卡特殊需求。

```php
<?php
$order_data = [
    'MerchantID' => 'MS12345678',
    'TimeStamp' => time(),
    'Version' => '2.3',
    'RespondType' => 'JSON',
    'MerchantOrderNo' => 'ORDER_' . time(),
    'Amt' => '5000',
    'ItemDesc' => '花蓮旅遊套裝行程',
    'Email' => 'traveler@example.com',
    
    'CREDIT' => '1',
    
    // 國民旅遊卡參數
    'NTCB' => '1',                    // 啟用國旅卡
    'NTCBLocate' => '022',            // 旅遊地區: 022=花蓮縣
    'NTCBStartDate' => '2025-02-01',  // 起始日期
    'NTCBEndDate' => '2025-02-03',    // 結束日期
    
    'ReturnURL' => 'https://yourdomain.com/return',
    'NotifyURL' => 'https://yourdomain.com/notify',
];
```

## 情境 10: 電子支付 (台灣Pay / TWQR)

使用台灣Pay和TWQR支付。

```php
<?php
$order_data = [
    'MerchantID' => 'MS12345678',
    'TimeStamp' => time(),
    'Version' => '2.3',
    'RespondType' => 'JSON',
    'MerchantOrderNo' => 'ORDER_' . time(),
    'Amt' => '999',
    'ItemDesc' => '行動支付商品',
    'Email' => 'buyer@example.com',
    
    // 電子支付
    'TAIWANPAY' => '1',               // 台灣Pay (限<50,000)
    'TWQR' => '1',                    // TWQR
    'TWQR_LifeTime' => '600',         // TWQR有效時間600秒
    
    // 顯示模式
    'WalletDisplayMode' => '0',       // 0=自動, 1=固定顯示QR Code
    
    'ReturnURL' => 'https://yourdomain.com/return',
    'NotifyURL' => 'https://yourdomain.com/notify',
];
```

## 情境 11: 處理 NotifyURL 回傳

接收並驗證藍新金流的付款通知。

```php
<?php
// notify.php - 處理付款通知
require_once 'encryption.php';

$crypto = new NewebPayCrypto("你的HashKey", "你的HashIV");

// 1. 驗證簽章
if (!$crypto->verifyTradeSha($_POST['TradeInfo'], $_POST['TradeSha'])) {
    http_response_code(400);
    exit("Invalid signature");
}

// 2. 解密資料
$decrypted = $crypto->decrypt($_POST['TradeInfo']);
parse_str($decrypted, $result);

// 3. 處理結果
if ($result['Status'] === 'SUCCESS') {
    // 更新訂單狀態
    $order_no = $result['MerchantOrderNo'];
    $trade_no = $result['TradeNo'];
    $amount = $result['Amt'];
    $payment_type = $result['PaymentType'];
    
    // 寫入資料庫
    $db = new PDO(/* ... */);
    $stmt = $db->prepare("
        UPDATE orders 
        SET status = 'paid', 
            trade_no = ?, 
            payment_type = ?,
            paid_at = NOW()
        WHERE order_no = ? AND amount = ?
    ");
    $stmt->execute([$trade_no, $payment_type, $order_no, $amount]);
    
    // 發送確認信
    send_order_confirmation_email($order_no);
    
    // 回應 SUCCESS
    echo "SUCCESS";
} else {
    // 交易失敗
    log_error("訂單 {$result['MerchantOrderNo']} 付款失敗: {$result['Status']}");
    echo "FAIL";
}
```

## 情境 12: 訂單細項參數

傳送詳細的訂單品項資訊。

```php
<?php
// 訂單明細
$items = [
    [
        'ItemName' => '智慧型手機',
        'ItemAmt' => 15000,
        'ItemType' => 1,  // 1=一般商品
        'ItemOrderNo' => 'ITEM001'
    ],
    [
        'ItemName' => '手機保護殼',
        'ItemAmt' => 500,
        'ItemType' => 1,
        'ItemOrderNo' => 'ITEM002'
    ],
    [
        'ItemName' => '運費',
        'ItemAmt' => 100,
        'ItemType' => 1,
        'ItemOrderNo' => 'ITEM003'
    ]
];

$total_amount = array_sum(array_column($items, 'ItemAmt'));

$order_data = [
    'MerchantID' => 'MS12345678',
    'TimeStamp' => time(),
    'Version' => '2.3',
    'RespondType' => 'JSON',
    'MerchantOrderNo' => 'ORDER_' . time(),
    'Amt' => $total_amount,  // 必須等於所有品項金額總和
    'ItemDesc' => '多品項訂單',
    'Email' => 'buyer@example.com',
    
    'CREDIT' => '1',
    
    // 訂單細項 (JSON格式)
    'OrderDetail' => json_encode($items),
    
    'ReturnURL' => 'https://yourdomain.com/return',
    'NotifyURL' => 'https://yourdomain.com/notify',
];
```

## 完整的購物車結帳流程

```php
<?php
// checkout.php - 結帳頁面

// 1. 從購物車取得訂單資訊
$cart_items = get_cart_items($user_id);
$total = calculate_total($cart_items);

// 2. 建立訂單
$order_no = create_order($user_id, $cart_items, $total);

// 3. 準備付款資料
$crypto = new NewebPayCrypto("你的HashKey", "你的HashIV");

$payment_data = [
    'MerchantID' => 'MS12345678',
    'TimeStamp' => time(),
    'Version' => '2.3',
    'RespondType' => 'JSON',
    'MerchantOrderNo' => $order_no,
    'Amt' => $total,
    'ItemDesc' => get_cart_description($cart_items),
    'Email' => $user_email,
    'TradeLimit' => 900,  // 15分鐘
    
    // 多元支付
    'CREDIT' => '1',
    'LINEPAY' => '1',
    'VACC' => '1',
    'CVS' => '1',
    
    'ReturnURL' => 'https://yourdomain.com/payment/return',
    'NotifyURL' => 'https://yourdomain.com/payment/notify',
    'ClientBackURL' => 'https://yourdomain.com/orders',
];

// 4. 加密並導向
$trade_info_raw = http_build_query($payment_data);
$trade_info = $crypto->encrypt($trade_info_raw);
$trade_sha = $crypto->generateTradeSha($trade_info);
?>

<!DOCTYPE html>
<html>
<head>
    <title>前往付款</title>
</head>
<body>
    <h1>正在導向付款頁面...</h1>
    
    <form id="payment-form" method="post" action="https://ccore.newebpay.com/MPG/mpg_gateway">
        <input type="hidden" name="MerchantID" value="MS12345678">
        <input type="hidden" name="Version" value="2.3">
        <input type="hidden" name="TradeInfo" value="<?= htmlspecialchars($trade_info) ?>">
        <input type="hidden" name="TradeSha" value="<?= $trade_sha ?>">
    </form>
    
    <script>
        // 自動提交表單
        document.getElementById('payment-form').submit();
    </script>
</body>
</html>
```

## 注意事項

1. **安全性**
   - HashKey 和 HashIV 絕不可暴露在前端
   - 所有加密操作必須在後端進行
   - NotifyURL 必須驗證 TradeSha

2. **訂單編號**
   - 確保 MerchantOrderNo 唯一性
   - 建議格式: `ORDER_` + timestamp + random
   - 長度限制30字元

3. **金額計算**
   - 使用 OrderDetail 時,總金額必須相符
   - 注意各支付方式的金額限制
   - ATM/超商代碼有金額上下限

4. **非即時支付**
   - 需設定 CustomerURL 接收取號通知
   - NotifyURL 接收實際付款通知
   - 兩者時間可能相差數天

5. **測試建議**
   - 先在測試環境完整測試
   - 測試各種支付方式
   - 測試錯誤處理邏輯
   - 確認 NotifyURL 正確運作
