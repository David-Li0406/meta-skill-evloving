# Weavr UI Components Reference

## Script Installation

```html
<!-- Sandbox (testing) -->
<script src="https://sandbox.weavr.io/app/secure/static/client.1.js"></script>

<!-- Production (live) -->
<script src="https://secure.weavr.io/app/secure/static/client.1.js"></script>
```

## Password Component

Securely collect passwords during onboarding/login. Tokenizes passwords so your app never sees raw credentials.

```javascript
window.OpcUxSecureClient.init("{{ui_key}}");
var form = window.OpcUxSecureClient.form();
var input = form.input("p", "password", {
  placeholder: "Password",
  maxlength: 30
});
input.mount(document.getElementById("password"));

input.on("submit", () => {
  form.tokenize(function(tokens) {
    // Send tokens.password to your server
    // Server calls POST /login_with_password
  });
});
```

## Confirm Password Component

For password confirmation during registration:

```javascript
var confirmInput = form.input("cp", "confirmPassword", {
  placeholder: "Confirm Password"
});
confirmInput.mount(document.getElementById("confirm-password"));
```

## PassCode Component

Alternative to password authentication:

```javascript
var passcodeInput = form.input("pc", "passCode", {
  placeholder: "Enter Passcode"
});
passcodeInput.mount(document.getElementById("passcode"));
```

## Confirm PassCode Component

For passcode confirmation:

```javascript
var confirmPasscodeInput = form.input("cpc", "confirmPassCode", {
  placeholder: "Confirm Passcode"
});
confirmPasscodeInput.mount(document.getElementById("confirm-passcode"));
```

## Card Number Display

Display tokenized card numbers. Requires stepped-up authentication.

```javascript
// Server retrieves tokenized card number from GET /managed_cards/{id}
window.OpcUxSecureClient.init("{{ui_key}}");

window.OpcUxSecureClient.associate(
  "Bearer {{stepped_up_auth_token}}",
  function() {
    var span = window.OpcUxSecureClient.span("cardNumber", "{{cardnumber_token}}");
    span.mount(document.getElementById("cardNumber"));
  },
  function(error) {
    console.error("Association failed:", error);
  }
);
```

## CVV Display

Display tokenized CVV. Requires stepped-up authentication.

```javascript
window.OpcUxSecureClient.associate(
  "Bearer {{stepped_up_auth_token}}",
  function() {
    var span = window.OpcUxSecureClient.span("cvv", "{{cvv_token}}");
    span.mount(document.getElementById("cvv"));
  },
  function(error) {
    console.error(error);
  }
);
```

## Capture Card PIN

Capture PIN for physical card issuance:

```javascript
window.OpcUxSecureClient.init("{{ui_key}}");
var form = window.OpcUxSecureClient.form();

window.OpcUxSecureClient.associate(
  "Bearer {{stepped_up_auth_token}}",
  function() {
    var input = form.input("cardPin", "cardPin");
    input.mount(document.getElementById("cardpin"));

    input.on("submit", () => {
      form.tokenize(function(tokens) {
        // Send tokens.cardPin to server
        // Server calls POST /managed_cards/{id}/physical
      });
    });
  }
);
```

## Show Card PIN

Display existing card PIN:

```javascript
window.OpcUxSecureClient.associate(
  "Bearer {{stepped_up_auth_token}}",
  function() {
    var span = window.OpcUxSecureClient.span("pin", "{{pin_token}}");
    span.mount(document.getElementById("pin"));
  },
  function(error) {
    console.error(error);
  }
);
```

## Consumer KYC

For consumer identity verification. Requires the user to be authenticated via `associate()` first.

```html
<div id="kyc-container"></div>
```

```javascript
window.OpcUxSecureClient.init("{{ui_key}}");

// Must associate first
window.OpcUxSecureClient.associate(
  "Bearer {{auth_token}}",
  function() {
    // Then initialize consumer KYC
    window.OpcUxSecureClient.consumer_kyc().init({
      selector: document.getElementById("kyc-container"),
      reference: "{{kyc_reference}}", // From POST /consumers/{id}/kyc/start
      lang: "en",
      customCss: "/path/to/custom.css",
      customCssStr: "body { font-family: Arial; }",
      onMessage: function(message) {
        if (message.type === "kycSubmitted") {
          console.log("KYC documentation submitted");
        }
      },
      onError: function(error) {
        console.error("KYC error:", error);
      }
    });
  },
  function(error) {
    console.error("Association failed:", error);
  }
);
```

## Director KYC

For corporate director/representative identity verification. Directors receive email links with a reference parameter.

```javascript
window.OpcUxSecureClient.init("{{ui_key}}");

// Must associate first
window.OpcUxSecureClient.associate(
  "Bearer {{auth_token}}",
  function() {
    window.OpcUxSecureClient.kyc().init(
      document.getElementById("kyc-container"),
      { accessToken: "{{auth_token}}", reference: "{{director_reference}}" },
      function(messageType, payload) {
        // messageType: 'complete', 'close', 'error', 'step_change'
        console.log(messageType, payload);
      },
      { lang: "en", hideSteps: false }
    );
  },
  function(error) {
    console.error("Association failed:", error);
  }
);
```

## KYB (Business Verification)

For corporate business verification.

```javascript
window.OpcUxSecureClient.init("{{ui_key}}");

// Must associate first
window.OpcUxSecureClient.associate(
  "Bearer {{auth_token}}",
  function() {
    window.OpcUxSecureClient.kyb().init(
      document.getElementById("kyb-container"),
      { accessToken: "{{auth_token}}", reference: "{{kyb_reference}}" }, // From POST /corporates/{id}/kyb/start
      function(messageType, payload) {
        // messageType: 'complete', 'close', 'error', 'step_change'
        console.log(messageType, payload);
      },
      { lang: "en", hideSteps: false }
    );
  },
  function(error) {
    console.error("Association failed:", error);
  }
);
```
