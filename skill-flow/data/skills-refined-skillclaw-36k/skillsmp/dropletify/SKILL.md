---
name: dropletify
description: Esta skill debe usarse cuando el usuario pide "desplegar en DigitalOcean", "configurar droplet", "deploy a droplet", "CI/CD para DigitalOcean", "GitHub Actions para droplet", o quiere preparar un proyecto para despliegue con Docker en DigitalOcean.
user-invocable: true
---

# Despliegue de proyecto dentro de un droplet de DigitalOcean

El objetivo a alcanzar es configurar el proyecto para poder desplegarlo dentro de un droplet de DigitalOcean
mediante GitHub Actions.

## Requisitos previos - Docker

Todas las aplicaciones desplegadas en DigitalOcean deben estar contenidas dentro de contenedores Docker.

Hay que comprobar que existan archivos de Docker dentro del proyecto y un docker compose file para orquestarlo.
Hay dos posibles escenarios:

### Archivos de Docker existentes

Corroborar que existan los siguientes archivos:

- `Dockerfile` en la raíz del proyecto
- `docker-compose.yml` en la raíz del proyecto

Evaluar si están actualizados y alineados con las necesidades del proyecto mediante agentes de exploración.

Con base en eso, evaluar: ¿Se puede reusar el Dockerfile y docker-compose.yml existentes para el despliegue en DigitalOcean?

- **Sí**: Usar esos mismos archivos.
- **No**: Invocar el agente `dockerify` para crear versiones optimizadas para producción.

### Archivos de Docker inexistentes

**Invocar el agente `dockerify`** para analizar el proyecto y generar los archivos Docker necesarios.

El agente `dockerify` se encarga de:

- Detectar runtime, framework y dependencias del proyecto
- Crear `Dockerfile` optimizado con multi-stage builds y mejores prácticas
- Generar `.dockerignore` apropiado
- Usar imágenes Alpine por defecto (con fallback a Debian si hay incompatibilidades)
- Aplicar hardening de seguridad (usuario non-root, permisos correctos)

Después de que `dockerify` complete su trabajo, crear manualmente el `docker-compose.yml` si el proyecto lo requiere para orquestación local.

## Archivo de workflow para GitHub Actions

Seguir los siguientes pasos:

- Crear un archivo de workflow de GitHub Actions en `.github/workflows/deploy.yml` tomando como referencia [este](./reference.yml) ejemplo.
- Crear los scripts necesarios en el directorio `scripts/`:
  - `scripts/docker-cleanup.sh` - Limpieza automática de recursos Docker ([copiar este archivo](./docker-cleanup.sh))
  - `scripts/rollback.sh` - Rollback automático en caso de fallo ([copiar este archivo](./rollback.sh))
- En el campo `env` del workflow, agregar los secretos necesarios para el despliegue.
  - Ya hay algunos por defecto en el ejemplo que son para configurar el registro de contenedores y droplet de DigitalOcean.
- Dentro del step `Deploy to DigitalOcean Droplet` atender la indicación de crear el archivo .env correspondiente para producción usando los valores de `env` del workflow.

### Configuración del cleanup automático

El workflow incluye un job `setup-cleanup-cron` que:

1. Verifica si el script de limpieza ya existe en el droplet (idempotente)
2. Si no existe:
   - Copia `scripts/docker-cleanup.sh` desde el repositorio al droplet
   - Lo instala en `/usr/local/bin/docker-cleanup.sh`
   - Configura un cron job para ejecutarlo diariamente a las 3 AM
   - Ejecuta una limpieza inicial para verificar funcionamiento
3. Si ya existe: termina sin hacer nada

El script de cleanup mantiene el droplet limpio automáticamente:
- Retiene solo las 5 imágenes Docker más recientes por repositorio
- Elimina contenedores detenidos, imágenes dangling, redes y volúmenes no usados
- Registra todas las operaciones en `/var/log/docker-cleanup.log`

### Configuración del rollback automático

El workflow incluye lógica de rollback automático en el job `deploy`:

1. **Instalación del script**: En el primer deployment, copia e instala `scripts/rollback.sh` en `/usr/local/bin/rollback.sh`
2. **Tracking de versiones**: Mantiene un archivo `.rollback-<image-name>.env` en el home del usuario del droplet que guarda el `LAST_WORKING_TAG` (último tag que funcionó correctamente)
3. **Verificación post-deployment**: Después de iniciar el contenedor, verifica que esté corriendo
4. **Rollback automático**: Si el contenedor falla al iniciar:
   - Lee el `LAST_WORKING_TAG` del archivo de rollback
   - Extrae la configuración del contenedor fallido (env vars, ports, volumes, network)
   - Despliega un nuevo contenedor usando el tag anterior con la misma configuración
   - Si el rollback tiene éxito, el deployment termina exitosamente
   - Si el rollback falla, requiere intervención manual
5. **Actualización del tag**: Solo actualiza `LAST_WORKING_TAG` cuando un deployment es exitoso

El script de rollback puede ejecutarse manualmente:
```bash
/usr/local/bin/rollback.sh <container-name> <image-name> <registry-path>
```

### Notas sobre el despliegue

El workflow usa `docker run` directamente en lugar de `docker-compose` para simplificar el despliegue:
- No requiere clonar el repositorio en el droplet
- Las variables de entorno se manejan mediante archivo `.env` temporal
- Para múltiples puertos, agrega más flags `-p` en el comando `docker run`
