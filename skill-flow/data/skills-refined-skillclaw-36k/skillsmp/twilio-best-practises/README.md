# Twilio Best Practices Skill

Skill para Claude Code con las mejores prácticas de integración de [Twilio](https://www.twilio.com/), la plataforma de comunicaciones en la nube.

## Instalación

```bash
npx skills add SK7zzz/skills-twilio-best-practises
```

## ¿Qué incluye?

### Productos cubiertos
- **Messaging** - SMS, MMS, WhatsApp, RCS
- **Voice** - Llamadas, IVR, conferencias, grabación
- **Verify** - OTP, 2FA, verificación de teléfono
- **Webhooks** - Manejo y validación de callbacks

### Contenido
- Autenticación con Account SID y Auth Token
- Envío y recepción de SMS/MMS
- Llamadas de voz y TwiML
- Verificación OTP con Verify API
- Validación de webhooks (X-Twilio-Signature)
- Integración con WhatsApp
- Manejo de errores y códigos comunes
- Rate limits y best practices

## Ejemplo rápido

```typescript
import twilio from 'twilio';

const client = twilio(
  process.env.TWILIO_ACCOUNT_SID,
  process.env.TWILIO_AUTH_TOKEN
);

// Enviar SMS
const message = await client.messages.create({
  body: 'Hello from Twilio!',
  from: '+15551234567',
  to: '+15559876543'
});
```

## Recursos

- [Documentación Twilio](https://www.twilio.com/docs)
- [Twilio Console](https://console.twilio.com/)
- [skills.sh](https://skills.sh/)

## Licencia

MIT
