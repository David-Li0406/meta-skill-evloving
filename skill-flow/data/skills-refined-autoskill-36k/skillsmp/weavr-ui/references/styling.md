# Weavr UI Styling Reference

## Custom Fonts

Load custom fonts during initialization:

```javascript
window.OpcUxSecureClient.init("{{ui_key}}", {
  fonts: [
    { cssSrc: "https://fonts.googleapis.com/css2?family=Roboto" }
  ]
});
```

## Input Styling

Style input components using the `style` option:

```javascript
var input = form.input("p", "password", {
  placeholder: "Enter password",
  style: {
    // Base styles (always applied)
    base: {
      color: "#333333",
      fontSize: "16px",
      fontFamily: "Roboto, sans-serif",
      padding: "12px",
      margin: "0",
      textAlign: "left"
    },
    // Empty state
    empty: {
      color: "#999999"
    },
    // Valid input state
    valid: {
      color: "#28a745"
    },
    // Invalid input state
    invalid: {
      color: "#dc3545",
      borderColor: "#dc3545"
    }
  }
});
```

## Pseudo-class Styling

Apply styles to pseudo-classes:

```javascript
var input = form.input("p", "password", {
  style: {
    base: {
      color: "#333"
    },
    ":hover": {
      borderColor: "#007bff"
    },
    ":focus": {
      borderColor: "#0056b3",
      boxShadow: "0 0 0 2px rgba(0, 123, 255, 0.25)"
    },
    "::placeholder": {
      color: "#6c757d",
      fontStyle: "italic"
    },
    "::selection": {
      backgroundColor: "#007bff",
      color: "#ffffff"
    },
    ":-webkit-autofill": {
      backgroundColor: "#fff3cd"
    }
  }
});
```

## Available Style Properties

- `color` - Text color
- `fontSize` - Font size (e.g., "16px", "1rem")
- `fontFamily` - Font family
- `fontWeight` - Font weight
- `fontStyle` - Font style (normal, italic)
- `padding` - Internal spacing
- `margin` - External spacing
- `textAlign` - Text alignment
- `lineHeight` - Line height
- `letterSpacing` - Letter spacing
- `borderColor` - Border color
- `borderWidth` - Border width
- `borderStyle` - Border style
- `borderRadius` - Border radius
- `backgroundColor` - Background color
- `boxShadow` - Box shadow

## KYC/KYB Component Styling

Use external CSS or inline styles:

```javascript
// External CSS file
window.OpcUxSecureClient.kyc(
  "Bearer {{token}}",
  "{{reference}}",
  {
    selector: "kyc-container",
    customCss: "/assets/kyc-styles.css"
  },
  onMessage,
  onError
);

// Inline CSS string
window.OpcUxSecureClient.kyc(
  "Bearer {{token}}",
  "{{reference}}",
  {
    selector: "kyc-container",
    customCssStr: `
      .kyc-form { padding: 20px; }
      .kyc-button { background: #007bff; color: white; }
    `
  },
  onMessage,
  onError
);
```

## Language Configuration

Set UI language with ISO 639-1 codes:

```javascript
{
  lang: "en"  // English
  lang: "de"  // German
  lang: "fr"  // French
  lang: "es"  // Spanish
}
```
