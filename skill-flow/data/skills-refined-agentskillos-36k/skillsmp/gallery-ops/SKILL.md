---
name: gallery-ops
description: Governs the digital photo gallery, checkout flows, secure asset delivery, and Google Drive integrations.
---

# Gallery Operations & Delivery Standard

This skill defines the mandatory architecture for The Lost+Unfounds digital gallery, specifically regarding the purchase and delivery lifecycle.

## 1. Purchase Flow Architecture
The checkout process must ALWAYS follow this circular journey:

1.  **Origin**: User selects photos in a specific gallery (e.g., `/gallery/kattitude-tattoo`).
2.  **Checkout**: User hits "Secure Checkout".
    *   **Payload**: Must include `librarySlug` to identify the origin.
    *   **Return URL**: Backend MUST append `?library={slug}` to the PayPal return URL.
3.  **Payment**: User pays via PayPal.
4.  **Capture**: User returns to `/payment/success`.
5.  **Delivery Redirection (CRITICAL)**:
    *   The Success Page MUST read the `library` query parameter.
    *   It MUST redirect the user BACK to the specific gallery (e.g., `/gallery/kattitude-tattoo`), NOT the generic shop.
    *   **Redirect Time**: 3 seconds max transition.

## 2. Asset Delivery Mechanism
Delivery is dual-channel: **Instant Access** + **Email Backup**.

### A. Instant Access (The "Unlock")
*   Upon returning to the gallery, the frontend `PhotoGallery.tsx` checks `fetchPurchasedAssets` against Supabase.
*   **Visual Changes**:
    *   Watermarks are removed.
    *   "PROPRIETARY" badge (Green) is applied.
    *   Download buttons become available.
*   **Security**: Direct downloads use `/api/gallery/stream` to pipe content from Google Drive without exposing raw Drive links.

### B. Email Backup ("The Vault")
*   **Trigger**: Sent immediately by `local-server.js` upon successful capture.
*   **Subject**: "Your Photos Are Ready - THE LOST+UNFOUNDS"
*   **Content**:
    *   Primary link goes to the Gallery (`/gallery/{slug}`).
    *   Resend/Recovery links go to the Download Portal (`/downloads/{order_id}`).

## 3. Code Standards

### Backend (`local-server.js`)
*   **Return URL**: Always construct as: `http://localhost:3000/payment/success?library=${librarySlug}`
*   **Email Link**: Always check `librarySlug` existence before generating the CTA link.

### Frontend (`PaymentSuccess.tsx`)
*   **Navigation**: Never hardcode `/shop`. Always check for `searchParams.get('library')` first.
    ```typescript
    const librarySlug = searchParams.get('library');
    const redirectPath = librarySlug ? `/gallery/${librarySlug}` : '/shop';
    navigate(redirectPath);
    ```

## 4. Google Drive Integration
*   **Proxying**: All images are served via `/api/gallery/stream`.
*   **Privacy**: Images in Drive must be "Anyone with the link can view".
*   **CORS**: The proxy bypasses standard Drive CORS issues by piping the stream server-side.
