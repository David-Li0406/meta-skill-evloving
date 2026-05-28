---
name: muebleria-integrations
description: >
  External API integrations (MercadoPago, emails, etc.) for MuebleriaIris.
  Trigger: When integrating external APIs, payment gateways, or third-party services.
license: Apache-2.0
metadata:
  author: muebleria-iris
  version: "1.0"
  scope: [root]
  auto_invoke:
    - "Integrating MercadoPago"
    - "Sending emails"
    - "Working with external APIs"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## When to Use

Use this skill when:

- Integrating MercadoPago for payments
- Sending transactional emails
- Consuming external APIs
- Implementing webhooks
- Handling API errors and retries

---

## Critical Patterns

### Pattern 1: MercadoPago Integration

```python
# backend/app/integrations/mercadopago.py
import mercadopago
import os

sdk = mercadopago.SDK(os.environ.get('MERCADOPAGO_ACCESS_TOKEN'))

def create_payment_preference(order_id: int, items: list, total: float):
    """Create MercadoPago payment preference"""
    preference_data = {
        "items": [
            {
                "title": item['nombre'],
                "quantity": item['cantidad'],
                "unit_price": float(item['precio'])
            }
            for item in items
        ],
        "back_urls": {
            "success": f"{os.environ.get('FRONTEND_URL')}/pago/success",
            "failure": f"{os.environ.get('FRONTEND_URL')}/pago/failure",
            "pending": f"{os.environ.get('FRONTEND_URL')}/pago/pending"
        },
        "auto_return": "approved",
        "external_reference": str(order_id),
        "notification_url": f"{os.environ.get('BACKEND_URL')}/api/webhooks/mercadopago"
    }
    
    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    
    return preference

# Usage in route
@main.route('/api/ordenes/<int:id>/pagar', methods=['POST'])
@jwt_required()
def create_payment(id):
    orden = Orden.query.get_or_404(id)
    
    # Get order items
    items = [{
        'nombre': d.producto.nombre,
        'cantidad': d.cantidad,
        'precio': d.precio_unitario
    } for d in orden.detalles]
    
    # Create preference
    preference = create_payment_preference(
        orden.id_orden,
        items,
        float(orden.monto_total)
    )
    
    # Save preference ID
    pago = Pago(
        id_orden=orden.id_orden,
        mp_preference_id=preference['id']
    )
    db.session.add(pago)
    db.session.commit()
    
    return jsonify({
        'preference_id': preference['id'],
        'init_point': preference['init_point']  # URL for checkout
    }), 200
```

### Pattern 2: MercadoPago Webhook

```python
# backend/app/routes.py
@main.route('/api/webhooks/mercadopago', methods=['POST'])
def mercadopago_webhook():
    """Handle MercadoPago notifications"""
    data = request.get_json()
    
    if data.get('type') == 'payment':
        payment_id = data['data']['id']
        
        # Get payment info from MercadoPago
        payment_info = sdk.payment().get(payment_id)
        payment = payment_info['response']
        
        # Update order
        external_ref = payment.get('external_reference')
        if external_ref:
            orden = Orden.query.get(int(external_ref))
            
            if payment['status'] == 'approved':
                orden.estado = 'pagada'
                
                # Update payment record
                pago = Pago.query.filter_by(id_orden=orden.id_orden).first()
                pago.mp_payment_id = payment_id
                pago.mp_estado = 'approved'
                pago.mp_tipo_pago = payment['payment_type_id']
                pago.monto_cobrado_mp = payment['transaction_amount']
                
                db.session.commit()
                
                app.logger.info(f'Payment approved for order {orden.id_orden}')
    
    return jsonify({'status': 'ok'}), 200
```

---

## Email Integration

### Pattern 3: Sending Emails

```python
# backend/app/integrations/email.py
from flask_mail import Mail, Message
import os

mail = Mail()

def send_order_confirmation(order_id: int, customer_email: str):
    """Send order confirmation email"""
    orden = Orden.query.get(order_id)
    
    msg = Message(
        subject=f'Confirmación de Orden #{orden.id_orden}',
        sender=os.environ.get('MAIL_DEFAULT_SENDER'),
        recipients=[customer_email]
    )
    
    msg.html = f"""
    <h1>¡Gracias por tu compra!</h1>
    <p>Tu orden #{orden.id_orden} ha sido recibida.</p>
    <p>Total: ${orden.monto_total}</p>
    <p>Estado: {orden.estado}</p>
    """
    
    mail.send(msg)

# backend/app/__init__.py
from flask_mail import Mail

mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    
    mail.init_app(app)
    return app
```

---

## External API Patterns

### Pattern 4: API Client with Retry

```python
# backend/app/integrations/api_client.py
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session_with_retry():
    """Create session with automatic retries"""
    session = requests.Session()
    
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

def call_external_api(endpoint: str, data: dict = None):
    """Call external API with error handling"""
    session = create_session_with_retry()
    
    try:
        response = session.get(
            endpoint,
            json=data,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.Timeout:
        app.logger.error(f'Timeout calling {endpoint}')
        raise
        
    except requests.exceptions.RequestException as e:
        app.logger.error(f'Error calling {endpoint}: {str(e)}')
        raise
```

---

## Frontend Integration

### Pattern 5: MercadoPago Checkout

```tsx
// src/components/CheckoutButton.tsx
"use client";
import { useState } from 'react';

interface CheckoutButtonProps {
  orderId: number;
}

export function CheckoutButton({ orderId }: CheckoutButtonProps) {
  const [loading, setLoading] = useState(false);
  
  const handleCheckout = async () => {
    setLoading(true);
    
    try {
      const response = await fetch(
        `http://localhost:5000/api/ordenes/${orderId}/pagar`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json'
          }
        }
      );
      
      const data = await response.json();
      
      // Redirect to MercadoPago
      window.location.href = data.init_point;
      
    } catch (error) {
      alert('Error al procesar el pago');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <button
      onClick={handleCheckout}
      disabled={loading}
      className="bg-blue-600 text-white px-6 py-3 rounded hover:bg-blue-700 disabled:bg-gray-400"
    >
      {loading ? 'Procesando...' : 'Pagar con MercadoPago'}
    </button>
  );
}
```

---

## Environment Variables

```bash
# backend/.env

# MercadoPago
MERCADOPAGO_ACCESS_TOKEN=your-access-token
MERCADOPAGO_PUBLIC_KEY=your-public-key

# Email (Gmail example)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@muebleriairis.com

# URLs
FRONTEND_URL=http://localhost:4321
BACKEND_URL=http://localhost:5000
```

---

## Best Practices

### DO:
- Use environment variables for credentials
- Implement retry logic for transient errors
- Log all external API calls
- Validate webhook signatures
- Handle timeouts gracefully
- Use async for non-blocking operations
- Cache responses when appropriate

### DON'T:
- Hardcode API keys
- Expose webhook URLs publicly without verification
- Make synchronous calls for slow APIs
- Ignore API rate limits
- Store sensitive data in logs
- Trust external data without validation

---

## Commands

```bash
# Install dependencies
pip install mercadopago flask-mail requests

# Test webhook locally (ngrok)
ngrok http 5000
# Use ngrok URL for notification_url
```

---

## QA Checklist

- [ ] API keys in environment variables
- [ ] Retry logic for transient errors
- [ ] Timeouts configured
- [ ] Errors logged with context
- [ ] Webhook signature validation
- [ ] External data validated
- [ ] Rate limiting respected
- [ ] Fallbacks for failed calls

---

## Resources

- **MercadoPago SDK**: https://www.mercadopago.com.ar/developers
- **Flask-Mail**: https://pythonhosted.org/Flask-Mail/
- **Requests**: https://requests.readthedocs.io
