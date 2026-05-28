---
name: security_auditor
description: "Revisa cada línea de código buscando vulnerabilidades de ciberseguridad (basado en Dot Dager)."
---

# 🛡️ Habilidad: Auditor de Seguridad

Esta habilidad permite al agente realizar auditorías de seguridad profundas siguiendo los principios de ciberseguridad de Dot Dager y las mejores prácticas de la industria.

## 🎯 Objetivo
Identificar, documentar y proponer soluciones para vulnerabilidades en el código fuente, asegurando la integridad de los datos y la privacidad del usuario.

## 📋 Lista de Verificación (Checklist)

### 1. Secretos y Credenciales
- [ ] **Secrets Hardcodeados**: Buscar API Keys, contraseñas, tokens de Firebase o secretos de Netlify escritos directamente en el código.
- [ ] **Manejo de `.env`**: Verificar que no se suban archivos sensibles al repositorio (aunque aquí es local, se debe usar una estructura segura).

### 2. Inyecciones
- [ ] **SQL Injection**: Buscar concatenaciones directas en consultas de base de datos (especialmente en `data.js` con Firebase).
- [ ] **NoSQL Injection**: Validar que los objetos pasados a las consultas de Firestore no contengan operadores maliciosos.

### 3. Cross-Site Scripting (XSS)
- [ ] **innerHTML / dangerouslySetInnerHTML**: Identificar cualquier uso de estas propiedades que renderice datos del usuario sin sanitizar.
- [ ] **Sanitización de Inputs**: Revisar que los inputs del POS y Configuración escapen caracteres especiales.

### 4. Autenticación y Autorización
- [ ] **Bypass de Login**: Verificar que no existan parches temporales que permitan saltarse el login de Dueño/Vendedor.
- [ ] **Permisos de Rol**: Asegurar que las funciones críticas (borrar ventas, editar inventario) verifiquen el rol del usuario en el lado del "servidor" (o lógica centralizada).

### 5. Gestión de Datos y Logs
- [ ] **Fuga de Información**: Revisar `console.log` que impriman objetos `user` completos o datos sensibles de transacciones.
- [ ] **Criptografía Débil**: Verificar el uso de algoritmos de hashing modernos para PINs o contraseñas (ej. Bcrypt vs MD5).

## 🛠️ Procedimiento de Auditoría

1.  **Escaneo de Superficie**: Usa `grep_search` para buscar palabras clave como `API_KEY`, `secret`, `password`, `innerHTML`, `+ " '`.
2.  **Análisis por Archivo**: Lee `app.js` y `data.js` bloque por bloque, evaluando el flujo de datos.
3.  **Reporte de Hallazgos**: Genera un reporte detallando:
    -   **Ubicación**: Archivo y línea.
    -   **Nivel de Riesgo**: (Crítico, Alto, Medio, Bajo).
    -   **Descripción**: Qué está mal.
    -   **Remediación**: Cómo arreglarlo.

## ⚠️ Regla de Oro (Dot Dager)
> "No confíes en nada que venga del cliente (frontend). Valida todo, sanitiza todo, y nunca, NUNCA subas una API Key al repositorio."
