---
name: business-logistics
description: Especialista en lógica de negocio de logística. Define reglas, flujos de trabajo y validaciones específicas de la app de delivery para Fusagasugá.
---

## Responsabilidad Única
Lógica de negocio y reglas específicas de la aplicación de logística. NO incluye stack técnico, arquitectura, UI/UX, ni detalles de implementación.

---

## Contexto de Negocio

### Región de Operación
- **Ciudad**: Fusagasugá, Cundinamarca, Colombia
- **Área de cobertura**: Zona urbana y rural cercana
- **Coordenadas aproximadas**: 4.3369° N, 74.3636° W

### Modelo de Operación
- Repartidores independientes con rutas diarias asignadas
- Múltiples paquetes por ruta (sin límite)
- Operación offline-first (conexión intermitente)
- Confirmación en tiempo real cuando hay conexión

---

## Gestión de Rutas

### Estados de Ruta
1. **Pending**: Ruta asignada, no iniciada
2. **Active**: Ruta en progreso
3. **Completed**: Todos los paquetes entregados o gestionados
4. **Cancelled**: Ruta cancelada (excepcional)

### Reglas de Negocio - Rutas
- Una ruta puede tener N paquetes (sin límite superior)
- Un repartidor solo puede tener **1 ruta activa** a la vez
- No se puede iniciar nueva ruta si hay una activa
- La ruta se completa automáticamente cuando todos los paquetes están en estado final (delivered/failed/returned)
- Fecha de ruta: Solo rutas del día actual pueden ser activadas

### Flujo de Trabajo - Ruta
1. Repartidor ve rutas asignadas del día
2. Selecciona ruta y la activa (estado → Active)
3. Sistema muestra paquetes ordenados por prioridad/ubicación
4. Repartidor gestiona paquetes uno por uno
5. Al completar todos los paquetes, ruta → Completed

---

## Gestión de Paquetes

### Estados de Paquete
1. **Pending**: Paquete en bodega, no asignado
2. **In Transit**: Asignado a ruta activa
3. **Out for Delivery**: Repartidor en camino a dirección
4. **Delivered**: Entregado exitosamente
5. **Failed**: Intento fallido (cliente ausente, dirección incorrecta, etc.)
6. **Returned**: Devuelto a bodega

### Reglas de Negocio - Paquetes
- **Tracking Number**: Único, alfanumérico, 8-20 caracteres
- **Dirección**: Obligatoria, debe ser validable en Fusagasugá
- **Teléfono**: Obligatorio, formato colombiano (10 dígitos)
- **Peso**: Opcional, en kilogramos
- **Notas**: Opcional, máximo 500 caracteres
- **Foto de entrega**: Obligatoria para estado Delivered
- **Firma/Nombre**: Obligatorio para estado Delivered
- **Razón de fallo**: Obligatoria para estado Failed

### Transiciones de Estado Válidas
```
Pending → In Transit (al asignar a ruta)
In Transit → Out for Delivery (repartidor en camino)
Out for Delivery → Delivered (entrega exitosa)
Out for Delivery → Failed (intento fallido)
Failed → Out for Delivery (reintento)
Failed → Returned (después de 3 intentos)
In Transit → Returned (cancelación)
```

### Validaciones de Negocio
- No se puede marcar como Delivered sin foto
- No se puede marcar como Failed sin razón
- Máximo 3 intentos de entrega antes de Returned
- No se puede modificar paquete en estado Delivered/Returned

---

## Scanner Inteligente (QR/Barcode)

### Propósito
Captura rápida de tracking numbers para agregar paquetes a ruta.

### Formatos Soportados
- **QR Code**: Tracking number codificado
- **Code 128**: Estándar de logística
- **Code 39**: Alternativa común
- **EAN-13**: Para paquetes con código de barras comercial

### Lógica de Negocio - Scanner
1. Abrir cámara en modo scanner
2. Detectar código automáticamente
3. Validar formato de tracking number
4. Buscar paquete en base de datos local
5. Si existe: Mostrar detalles y permitir agregar a ruta
6. Si no existe: Permitir entrada manual o crear nuevo paquete

### Fallback Manual
- Si código no escanea (dañado, borroso), permitir entrada manual
- Validar formato mientras se escribe
- Sugerir autocompletado si hay coincidencias parciales

### Reglas de Validación
- Tracking number debe ser único en el sistema
- No se puede agregar mismo paquete dos veces a una ruta
- Paquete debe estar en estado Pending o In Transit para agregarse

---

## Confirmación de Entregas

### Entrega Exitosa (Delivered)
**Datos requeridos**:
1. **Foto de entrega**: Captura de paquete en ubicación
2. **Nombre de quien recibe**: Texto libre, mínimo 3 caracteres
3. **Firma digital**: Opcional pero recomendada
4. **Coordenadas GPS**: Automáticas, para verificación
5. **Timestamp**: Automático

**Flujo**:
1. Repartidor llega a dirección
2. Presiona "Confirmar Entrega"
3. Toma foto del paquete
4. Ingresa nombre de quien recibe
5. Opcionalmente captura firma
6. Presiona botón "Hold to Confirm" (3 segundos)
7. Sistema guarda localmente y sincroniza cuando hay conexión

### Entrega Fallida (Failed)
**Datos requeridos**:
1. **Razón de fallo**: Selección de lista predefinida
2. **Foto de evidencia**: Opcional pero recomendada
3. **Notas adicionales**: Opcional
4. **Coordenadas GPS**: Automáticas
5. **Timestamp**: Automático

**Razones de Fallo Predefinidas**:
- Cliente ausente
- Dirección incorrecta
- Dirección incompleta
- Cliente rechaza paquete
- Zona insegura
- Otro (requiere nota)

**Flujo**:
1. Repartidor intenta entrega
2. Presiona "Reportar Fallo"
3. Selecciona razón de fallo
4. Opcionalmente toma foto de evidencia
5. Opcionalmente agrega notas
6. Confirma fallo
7. Sistema incrementa contador de intentos
8. Si intentos < 3: Paquete vuelve a In Transit
9. Si intentos >= 3: Paquete → Returned

---

## Botones de Seguridad (Safety Actions)

### Hold to Confirm
Para acciones críticas e irreversibles:
- Confirmar entrega
- Marcar como fallida
- Completar ruta

**Comportamiento**:
- Presionar y mantener por 3 segundos
- Mostrar progreso circular visual
- Feedback háptico al inicio y al completar
- Si se suelta antes de 3s, cancelar acción

### Propósito
Prevenir confirmaciones accidentales que afecten métricas de negocio.

---

## Priorización de Paquetes

### Criterios de Ordenamiento
1. **Prioridad manual**: Si fue marcado como urgente
2. **Intentos previos**: Paquetes con intentos fallidos primero
3. **Proximidad geográfica**: Más cercano al punto actual
4. **Hora de compromiso**: Si tiene ventana de entrega específica

### Reglas de Negocio
- Paquetes urgentes siempre al inicio de la lista
- Después de fallo, paquete sube en prioridad
- Repartidor puede reordenar manualmente si es necesario

---

## Notificaciones al Cliente (Futuro)

### Eventos que Generan Notificación
- Paquete asignado a ruta (In Transit)
- Repartidor en camino (Out for Delivery)
- Paquete entregado (Delivered)
- Intento fallido (Failed)

**Nota**: Implementación futura, definir canales (SMS, WhatsApp, Push).

---

## Métricas de Negocio

### KPIs del Repartidor
- **Tasa de entrega exitosa**: Delivered / Total paquetes
- **Promedio de intentos**: Total intentos / Total paquetes
- **Paquetes por hora**: Entregas / Horas trabajadas
- **Tiempo promedio por entrega**: Desde Out for Delivery hasta Delivered

### Reglas de Cálculo
- Solo contar paquetes en estado final (Delivered/Returned)
- Excluir paquetes cancelados de métricas
- Actualizar métricas en tiempo real cuando hay conexión

---

## Validaciones de Datos

### Tracking Number
```dart
bool isValidTrackingNumber(String value) {
  // Alfanumérico, 8-20 caracteres, sin espacios
  return RegExp(r'^[A-Z0-9]{8,20}$').hasMatch(value.toUpperCase());
}
```

### Teléfono Colombia
```dart
bool isValidColombianPhone(String value) {
  // 10 dígitos, puede empezar con 3 (móvil) o no
  return RegExp(r'^\d{10}$').hasMatch(value);
}
```

### Dirección Fusagasugá
```dart
bool isValidAddress(String value) {
  // Mínimo 10 caracteres, debe contener número
  return value.length >= 10 && RegExp(r'\d').hasMatch(value);
}
```

---

## Reglas de Sincronización (Lógica de Negocio)

### Prioridad de Sincronización
1. **Alta**: Confirmaciones de entrega (Delivered/Failed)
2. **Media**: Cambios de estado de paquetes
3. **Baja**: Actualización de datos de ruta

### Conflictos
- **Mismo paquete editado offline y online**: Última modificación gana
- **Ruta completada offline pero modificada online**: Notificar al repartidor
- **Paquete eliminado online pero editado offline**: Marcar como conflicto, requiere resolución manual

---

## Ejemplo de Flujo Completo

### Día del Repartidor
1. **Inicio de jornada**:
   - Abrir app
   - Ver rutas asignadas del día
   - Seleccionar ruta y activarla

2. **Durante la ruta**:
   - Ver lista de paquetes ordenados
   - Navegar al primer paquete
   - Intentar entrega
   - Si exitosa: Tomar foto, nombre, confirmar
   - Si fallida: Seleccionar razón, agregar notas
   - Repetir con siguiente paquete

3. **Fin de jornada**:
   - Completar todos los paquetes
   - Ruta se marca como Completed automáticamente
   - Sincronizar datos cuando haya WiFi
   - Revisar métricas del día