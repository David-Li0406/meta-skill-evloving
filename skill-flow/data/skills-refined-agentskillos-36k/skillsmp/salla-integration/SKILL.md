---
name: salla_integration
description: Manage and test Salla e-commerce webhooks and API integrations.
---

# Salla Integration Skill

This skill handles the connection between RIBH and the Salla platform.

## 🔗 Key Endpoints
- **Webhook Listener**: `/webhooks/salla`
- **Events**: `cart.abandoned`, `order.created`, `app.installed`.

## 🚀 Execution Instructions

### 1. Simulate a Webhook
Use this to test the recovery flow without a real store:
```bash
# Example curl command (requires local server running)
curl -X POST http://localhost:3000/webhooks/salla \
     -H "Content-Type: application/json" \
     -d '{"event":"cart.abandoned", "data": {"customer": {"email": "test@example.com", "mobile": "966500000000"}, "cart": {"total": 500}}}'
```

### 2. Verify API Keys
Ensure `SALLA_ACCESS_TOKEN` is set in `.env` or Firebase config.

### 3. Salla Portal Text
When updating the app listing:
- **Brief**: تطبيق استرداد العربات المتروكة عبر الواتساب والرسائل النصية.
- **Description**: نظام ذكي يستخدم الذكاء الاصطناعي لاسترداد المبيعات الضائعة تلقائياً.

## 📁 Resources
- `PROJECT_CONTEXT.md`: Overview of the integration.
