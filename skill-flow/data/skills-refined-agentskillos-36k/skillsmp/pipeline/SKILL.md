---
name: pipeline
description: Gestiona el pipeline de flujo controlado. Usa para ver estado, avanzar, resetear o ir a un step específico del pipeline.
user-invocable: true
---

# Pipeline Management

Gestiona el pipeline de flujo controlado para este proyecto.

## Subcomandos

Parsea `$ARGUMENTS` para determinar la acción:

- **vacío o "status"** → Mostrar estado actual
- **"advance"** → Avanzar al siguiente step
- **"reset"** → Resetear a step 0
- **"set N"** → Ir directamente al step N

## Ejecución

El `project_dir` para este proyecto es: `/Users/juanpablodiaz/my_projects/agentcockpit`

### Para status (default):
Llama a `mcp__pipeline-manager__pipeline_status` con `project_dir="/Users/juanpablodiaz/my_projects/agentcockpit"`.

Muestra el resultado en formato tabla:
```
Pipeline: Step {current_step} - {step_name}

| # | Nombre | Estado | Bloqueados |
|---|--------|--------|------------|
```

### Para advance:
Llama a `mcp__pipeline-manager__pipeline_advance` con `project_dir="/Users/juanpablodiaz/my_projects/agentcockpit"`.
Confirma: "Avanzado a Step N - {nombre}"

### Para reset:
Llama a `mcp__pipeline-manager__pipeline_reset` con `project_dir="/Users/juanpablodiaz/my_projects/agentcockpit"`.
Confirma: "Pipeline reseteado a Step 0"

### Para set N:
Llama a `mcp__pipeline-manager__pipeline_set_step` con `project_dir="/Users/juanpablodiaz/my_projects/agentcockpit"` y `step_index=N`.
Confirma: "Pipeline en Step N - {nombre}"

## Notas

- Write/Edit están bloqueados en steps 0 y 1
- Usa `/pipeline advance` o `/pipeline set 2` para desbloquear
