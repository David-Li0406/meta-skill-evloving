# Weavr UI Styling Reference

## Script URLs

```html
<!-- Sandbox -->
<script src="https://sandbox.weavr.io/app/secure/static/client.1.js"></script>

<!-- Production -->
<script src="https://secure.weavr.io/app/secure/static/client.1.js"></script>
```

## Custom Fonts

Load fonts during initialization:

```javascript
window.OpcUxSecureClient.init("{{ui_key}}", {
  fonts: [
    { cssSrc: "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600" }
  ]
});
```

## Input Component Styling

### Full Style Configuration

```javascript
var input = form.input("p", "password", {
  placeholder: "Enter password",
  maxlength: 30,
  style: {
    // Base styles (always applied)
    base: {
      color: "#333333",
      fontSize: "16px",
      fontFamily: "Inter, sans-serif",
      fontWeight: "400",
      padding: "12px 16px",
      margin: "0",
      textAlign: "left",
      lineHeight: "1.5",
      letterSpacing: "normal",
      borderColor: "#d1d5db",
      borderWidth: "1px",
      borderStyle: "solid",
      borderRadius: "8px",
      backgroundColor: "#ffffff"
    },

    // Empty state
    empty: {
      color: "#9ca3af"
    },

    // Valid input
    valid: {
      color: "#059669",
      borderColor: "#10b981"
    },

    // Invalid input
    invalid: {
      color: "#dc2626",
      borderColor: "#ef4444"
    },

    // Pseudo-classes
    ":hover": {
      borderColor: "#3b82f6"
    },

    ":focus": {
      borderColor: "#2563eb",
      boxShadow: "0 0 0 3px rgba(59, 130, 246, 0.1)"
    },

    "::placeholder": {
      color: "#9ca3af",
      fontStyle: "normal"
    },

    "::selection": {
      backgroundColor: "#3b82f6",
      color: "#ffffff"
    },

    ":-webkit-autofill": {
      backgroundColor: "#fef3c7"
    }
  }
});
```

### Available Style Properties

| Property | Example | Description |
|----------|---------|-------------|
| `color` | `"#333"` | Text color |
| `fontSize` | `"16px"`, `"1rem"` | Font size |
| `fontFamily` | `"Inter, sans-serif"` | Font family |
| `fontWeight` | `"400"`, `"bold"` | Font weight |
| `fontStyle` | `"normal"`, `"italic"` | Font style |
| `padding` | `"12px"`, `"12px 16px"` | Internal spacing |
| `margin` | `"0"`, `"8px 0"` | External spacing |
| `textAlign` | `"left"`, `"center"` | Text alignment |
| `lineHeight` | `"1.5"`, `"24px"` | Line height |
| `letterSpacing` | `"0.5px"` | Letter spacing |
| `borderColor` | `"#d1d5db"` | Border color |
| `borderWidth` | `"1px"`, `"2px"` | Border width |
| `borderStyle` | `"solid"`, `"none"` | Border style |
| `borderRadius` | `"8px"`, `"4px"` | Border radius |
| `backgroundColor` | `"#fff"` | Background color |
| `boxShadow` | `"0 1px 2px rgba(0,0,0,0.1)"` | Box shadow |

### State Classes

| State | When Applied |
|-------|--------------|
| `base` | Always applied |
| `empty` | Input has no value |
| `valid` | Input passes validation |
| `invalid` | Input fails validation |

### Pseudo-classes

| Pseudo-class | Description |
|--------------|-------------|
| `:hover` | Mouse over input |
| `:focus` | Input is focused |
| `::placeholder` | Placeholder text |
| `::selection` | Selected text |
| `:-webkit-autofill` | Browser autofilled |

## KYC/KYB Component Styling

### External CSS File

```javascript
window.OpcUxSecureClient.kyc().init(
  document.getElementById("kyc-container"),
  { accessToken: token, reference: ref },
  callback,
  {
    lang: "en",
    customCss: "/assets/kyc-theme.css"
  }
);
```

### Inline CSS

```javascript
window.OpcUxSecureClient.consumer_kyc().init({
  selector: document.getElementById("kyc-container"),
  reference: ref,
  customCssStr: `
    .kyc-container {
      font-family: Inter, sans-serif;
    }
    .kyc-form {
      padding: 24px;
      background: #f9fafb;
      border-radius: 12px;
    }
    .kyc-button {
      background: #3b82f6;
      color: white;
      border: none;
      border-radius: 8px;
      padding: 12px 24px;
      font-weight: 500;
    }
    .kyc-button:hover {
      background: #2563eb;
    }
    .kyc-input {
      border: 1px solid #d1d5db;
      border-radius: 8px;
      padding: 12px;
    }
  `
});
```

## Display Component Styling

Card number, CVV, and PIN spans inherit styles from their container:

```html
<style>
  #card-number {
    font-family: 'SF Mono', Monaco, monospace;
    font-size: 18px;
    letter-spacing: 2px;
    color: #1f2937;
  }

  #cvv {
    font-family: 'SF Mono', Monaco, monospace;
    font-size: 16px;
    color: #374151;
  }
</style>

<div id="card-number"></div>
<div id="cvv"></div>
```

```javascript
var cardSpan = window.OpcUxSecureClient.span("cardNumber", token);
cardSpan.mount(document.getElementById("card-number"));
```

## Language Configuration

Set UI language with ISO 639-1 codes:

```javascript
{
  lang: "en"  // English (default)
  lang: "de"  // German
  lang: "fr"  // French
  lang: "es"  // Spanish
  lang: "it"  // Italian
  lang: "nl"  // Dutch
  lang: "pt"  // Portuguese
}
```

## Design System Integration Example

### Tailwind-style Theme

```javascript
const weavrInputStyle = {
  base: {
    color: "#111827",           // gray-900
    fontSize: "14px",           // text-sm
    fontFamily: "Inter, ui-sans-serif, system-ui, sans-serif",
    padding: "10px 14px",       // px-3.5 py-2.5
    borderColor: "#d1d5db",     // gray-300
    borderWidth: "1px",
    borderRadius: "8px",        // rounded-lg
    backgroundColor: "#ffffff"
  },
  empty: { color: "#6b7280" },  // gray-500
  valid: { borderColor: "#10b981" },  // green-500
  invalid: { borderColor: "#ef4444" }, // red-500
  ":focus": {
    borderColor: "#3b82f6",     // blue-500
    boxShadow: "0 0 0 2px rgba(59, 130, 246, 0.2)"
  },
  "::placeholder": { color: "#9ca3af" }  // gray-400
};

var input = form.input("p", "password", {
  placeholder: "Password",
  style: weavrInputStyle
});
```
