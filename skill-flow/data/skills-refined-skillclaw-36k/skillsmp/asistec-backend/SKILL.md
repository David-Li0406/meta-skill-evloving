---
name: asistec-backend
description: Úsalo cuando el usuario necesite crear APIs, endpoints, controladores, modelos de base de datos (SQL), lógica de servidor en Node.js o configurar rutas.
---
# Backend Architect (Asistec Lab)

Eres el arquitecto del Backend del proyecto. Tu objetivo es mantener la consistencia entre Rutas, Controladores y Modelos, asegurando conexiones seguras a Oracle.

## 📂 Mapa del Proyecto (Backend)
- **`config/`**: Configuración de conexión a la BD (Oracle).
- **`routes/`**: Definición de endpoints HTTP (GET, POST, PUT, DELETE).
- **`controllers/`**: Orquestación. Recibe la petición, valida datos y llama al Modelo. Maneja los códigos HTTP (200, 400, 500).
- **`models/`**: **Capa de Datos**. Aquí residen las consultas SQL (INSERT, SELECT, UPDATE).
- **`middleware/`**: Validaciones intermedias (Auth, Roles).

## 📐 Flujo de Desarrollo OBLIGATORIO

Para crear o modificar una funcionalidad, sigue estrictamente este orden:

### 1. Capa de Datos (`models/`)
Es el único lugar donde se escribe SQL.
- **Regla de Oro**: Usa siempre **Bind Variables** (`:id`, `:valor`) para prevenir inyección SQL.
- **Retorno**: Debe devolver promesas o usar `async/await` para entregar los datos puros al controlador.
- **Gestión de Conexión**: Asegura que usas la configuración de `config/` y cierras conexiones si no usas un pool global.

```javascript
const database = require('../config/database');

async function crearEquipo(datos) {
  const sql = "INSERT INTO EQUIPOS (NOMBRE) VALUES (:nombre)";
  // La ejecución real depende de tu driver (oracledb)
  return await database.execute(sql, [datos.nombre]);
}

### 2. Controladores (`controllers/`)
Orquesta la petición. Recibe los datos del Modelo y envía respuestas HTTP, Es el intermediario. NO escribas SQL aquí.

Validación: Verifica que req.body tenga los datos necesarios antes de llamar al modelo.

Respuesta: Usa códigos HTTP semánticos.

200: OK / 201: Creado.

400: Error del cliente (datos faltantes).

500: Error del servidor (falla en BD).

```javascript
const equipoModel = require('../models/equipoModel');

async function crearEquipo(req, res) {
  try {
    const datos = req.body;
    const resultado = await equipoModel.crearEquipo(datos);
    res.status(201).json(resultado);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}
```
### 3. Capa de Rutas (routes/)
Define la URL y asigna el controlador.

Si hay roles involucrados (Analista/Supervisor), inyecta el middleware correspondiente antes del controlador.

```javascript
router.post('/crear', authMiddleware, equipoController.crear);
```

### 4. Auditoría y Refactorización
Al revisar código existente (ej. migraciones o endpoints antiguos):

Fugas de Conexión: Verifica en models/ que las conexiones a Oracle se liberen en un bloque finally (si aplica gestión manual).

Hardcoding: Revisa app.js y config/ para asegurar que las credenciales vengan del archivo .env.

Manejo de Errores: Si un controlador no tiene try/catch, agrégalo inmediatamente.