# Email Template Color Schemes

Pre-defined color schemes for different email types in Authentik templates.

## Octopize Brand Colors

- **PRIMARY_GREEN**: `#3BD6B0` - Main brand color for headers, buttons, and accents
- **PRIMARY_GREY**: `dimgrey` (#696969) - Secondary color for text and subtle elements

## Available Schemes

### 1. Primary/Welcome (Octopize Green)
Used for: Account confirmation, welcome emails, successful actions, general communications

```css
.header {
    background: linear-gradient(135deg, #3BD6B0 0%, #2db89a 100%);
}
.button {
    background-color: #3BD6B0;
}
.button:hover {
    background-color: #2db89a;
}
```

### 2. Security/Password (Darker Green)
Used for: Password reset, security alerts, authentication

```css
.header {
    background: linear-gradient(135deg, #2db89a 0%, #259980 100%);
}
.button {
    background-color: #2db89a;
}
.button:hover {
    background-color: #259980;
}
```

### 3. Warning/Alert (Amber)
Used for: Account warnings, expiration notices, attention required

```css
.header {
    background: linear-gradient(135deg, #ffc107 0%, #ff9800 100%);
}
.button {
    background-color: #ffc107;
}
.button:hover {
    background-color: #ffb300;
}
```

### 4. Error/Critical (Red-Orange)
Used for: Critical alerts, account suspension, security warnings

```css
.header {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
}
.button {
    background-color: #ff6b6b;
}
.button:hover {
    background-color: #ff5252;
}
```

## Accent Elements

### Info Box (Teal - Brand Color)
```css
.info-box {
    background-color: #e0f7f4;
    border-left: 4px solid #38f9d7;
    padding: 15px;
    margin: 20px 0;
    border-radius: 4px;
}
.info-box p {
    margin: 0;
    color: #0d5c52;
}
```

### Warning Box (Amber)
```css
.warning-box {
    background-color: #fff8e1;
    border-left: 4px solid #ffc107;
    padding: 15px;
    margin: 20px 0;
    border-radius: 4px;
}
.warning-box p {
    margin: 0;
    color: #7a5c00;
}
```

### Success Box (Light Teal)
```css
.success-box {
    background-color: #d4f4e8;
    border-left: 4px solid #43e97b;
    padding: 15px;
    margin: 20px 0;
    border-radius: 4px;
}
.success-box p {
    margin: 0;
    color: #1a5c3e;
}
```

### Error Box (Red-Orange)
```css
.error-box {
    background-color: #ffe6e6;
    border-left: 4px solid #ff6b6b;
    padding: 15px;
    margin: 20px 0;
    border-radius: 4px;
}
.error-box p {
    margin: 0;
    color: #8b0000;
}
```

## Brand Consistency

All templates use the Octopize footer:
```html
<div class="footer">
    <p>This email was sent automatically, please do not reply.</p>
    <p>&copy; 2026 Octopize. All rights reserved.</p>
</div>
```
