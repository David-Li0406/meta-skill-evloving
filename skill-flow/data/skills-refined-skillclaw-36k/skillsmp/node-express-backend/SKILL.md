---
name: node-express-backend
description: Gestione del backend Node.js (Express, Firebase, Middleware).
---

# Node.js Express Backend

Usa questa skill quando modifichi il codice nella cartella `backend/`.
Lo stack è **Node.js + Express + Firebase Admin + Postgres (opzionale)**.

## Struttura Backend

```text
backend/src/
├── middleware/   # Auth check, Error handling, Logging
├── routes/       # Definizioni degli endpoint (Router)
├── services/     # Business logic (interazione con DB/Firebase)
├── utils/        # Helper functions
└── index.js      # Server entry point
```

## Regole di Sviluppo

1. **Separazione Routes/Controllers**:
   Non mettere logica nel file di route.
   - `routes/user.js`: Definisce solo i path e i middleware.
   - `services/userService.js`: Contiene la logica vera e propria.

2. **Gestione Errori**:
   Non usare `console.log` per gli errori.
   Passa gli errori al middleware di gestione errori di Express usando `next(err)`.

   ```javascript
   // Esempio Route Handler
   app.get('/users/:id', async (req, res, next) => {
     try {
       const user = await userService.getById(req.params.id);
       res.json(user);
     } catch (err) {
       next(err); // Passa al global error handler
     }
   });
   ```

3. **Autenticazione**:
   Usa il middleware di Firebase Auth per proteggere le route private.
   Verifica sempre il token `Bearer` nell'header `Authorization`.

   ```javascript
   // middleware/auth.js
   const verifyToken = async (req, res, next) => {
     const token = req.headers.authorization?.split('Bearer ')[1];
     if (!token) return res.status(401).send('Unauthorized');
     
     try {
       const decodedToken = await admin.auth().verifyIdToken(token);
       req.user = decodedToken;
       next();
     } catch (e) {
       res.status(403).send('Invalid Token');
     }
   };
   ```

4. **Variabili d'Ambiente**:
   Non hardcodare mai chiavi API o stringhe di connessione. Usa `process.env` e il file `.env`.
