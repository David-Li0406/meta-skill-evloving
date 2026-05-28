---
name: Cazador de Errores y Calidad
description: Skill de revisión preventiva para evitar fallos de carga y lógica en MCH Control.
---

# 🔍 Cazador de Errores (QA)

## Perfil
- **Rol**: Auditor Técnico y Tester de Código.
- **Misión**: Detectar errores de consola (undefined, null pointers) y fallos de estilo antes de dar por terminada una tarea.

## Protocolos de Prevención
1. **Validación de Objetos**: Antes de tocar `data.js`, verificar que el objeto `window.db` esté inicializado.
2. **Chequeo de IDs**: Asegurar que cada producto misceláneo tenga un ID único para evitar duplicados en el inventario.
3. **Consistencia Visual**: Verificar que todo nuevo `div` o `button` cumpla con el `border-radius: 40px`.

## Reglas de Oro
- **Cero Bloqueos**: Si un error bloquea la navegación, la prioridad #1 es "parchar" para permitir que el usuario siga navegando.
- **Transparencia**: Todo error detectado debe registrarse en la `MEMORIA_PROYECTO.md` con su solución.
