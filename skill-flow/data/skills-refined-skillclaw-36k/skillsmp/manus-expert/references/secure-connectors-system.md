# Secure Connectors System (2026)

Manus Connectors provide a safe way to give agents access to external services without exposing credentials in the system prompt.

## 1. How Connectors Work

Instead of saying "My password is X," you register a connector with Manus.
-   **Registration**: Encrypted credentials stored in the Manus vault.
-   **Usage**: Agent requests tool use; Manus injects credentials at the API layer.

## 2. Types of Connectors

-   **Service Connectors**: GitHub, Slack, Notion, Salesforce.
-   **Custom Web Connectors**: Using OAuth 2.1 to bridge your private APIs.
-   **Database Connectors**: Secure, read-only access to specific tables.

## 3. Least Privilege for Agents

Limit the connector scope to the minimum required for the mission.
-   *Bad*: `Full GitHub Admin`.
-   *Good*: `Read-only access to 'squaads/core' repository`.

## 4. Connector Lifecycle

-   **Rotation**: Rotate connector secrets every 30 days.
-   **Revocation**: Instantly revoke access if an agent shows anomalous behavior.

## 5. Security: RSA Verification

All connector-driven events from Manus must be verified using the RSA-SHA256 signature protocol.

---
*Updated: January 22, 2026 - 21:10*
