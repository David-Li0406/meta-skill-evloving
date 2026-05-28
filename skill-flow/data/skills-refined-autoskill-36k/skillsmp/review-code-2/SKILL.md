---
name: review-code
description: Revisa código en documentos LaTeX para asegurar convenciones de nombrado. Usa cuando el usuario mencione revisar código, verificar nombres de variables/funciones, o validar estilo de código en documentos.
allowed-tools:
  - Read
  - Grep
  - Glob
---

# Revisión de Código en Documentos LaTeX

## Reglas de Estilo

### 1. Nombres de código en inglés
Todo el código (nombres de funciones, clases, variables, métodos) debe estar escrito en **inglés**.

**Correcto:**
- `TwoElementField`
- `approximate_sqrt`
- `verify_axioms`
- `RationalNumber`

**Incorrecto:**
- `CuerpoDosElementos`
- `aproximar_raiz`
- `verificar_axiomas`
- `NumeroRacional`

### 2. Comentarios en español
Los comentarios dentro del código deben estar en **español** para mantener consistencia con el texto del libro.

**Correcto:**
```python
# Calcula la aproximación de la raíz cuadrada
def approximate_sqrt(n, iterations):
    pass
```

**Incorrecto:**
```python
# Calculate the square root approximation
def approximate_sqrt(n, iterations):
    pass
```

### 3. Docstrings en español
La documentación de funciones (docstrings) debe estar en español.

```python
def verify_axioms(field):
    """
    Verifica que el cuerpo satisface todos los axiomas.

    Args:
        field: Instancia del cuerpo a verificar.

    Returns:
        True si todos los axiomas se cumplen.
    """
    pass
```

### 4. Código desde archivos externos
Los fragmentos de código en cajas de código (`lstlisting`, `minted`, etc.) deben insertarse desde archivos externos ubicados en el directorio `code/` de cada libro.

**Estructura de directorios:**
```
libro/
├── chapters/
│   └── chapter1.tex
├── code/
│   ├── zmod.py
│   ├── two_element_field.py
│   └── approximate_sqrt.py
└── main.tex
```

**Correcto** - Usar `\lstinputlisting`:
```latex
\lstinputlisting[language=Python, caption={Implementación de aritmética modular}]{code/zmod.py}
```

**Incorrecto** - Código embebido directamente:
```latex
\begin{lstlisting}[language=Python]
class Zmod:
    def __init__(self, value, modulus):
        ...
\end{lstlisting}
```

**Ventajas de usar archivos externos:**
- El código se puede probar y ejecutar de forma independiente
- Evita errores de sincronización entre el documento y el código real
- Facilita el mantenimiento y actualizaciones
- Permite usar herramientas de linting y formateo

**Convención de nombres para archivos:**
- Usar snake_case: `two_element_field.py`, `approximate_sqrt.py`
- Nombre descriptivo que refleje el contenido
- Extensión apropiada según el lenguaje (`.py`, `.js`, `.cpp`, etc.)

## Instrucciones

1. Busca archivos `.tex` en el directorio especificado
2. Identifica bloques de código:
   - Ambientes `lstlisting`, `verbatim`, `minted`
   - Referencias con `\texttt{}`
   - Código inline con backticks
3. Para cada bloque de código, verifica:
   - Nombres de identificadores (clases, funciones, variables) estén en inglés
   - Comentarios (`#`, `//`, `/* */`) estén en español
   - **El código se carga desde archivo externo** (`\lstinputlisting` o similar)
4. Verifica que existe el directorio `code/` en el libro
5. Si hay código embebido, sugiere:
   - Crear el archivo correspondiente en `code/`
   - Reemplazar el bloque por `\lstinputlisting`
6. Reporta inconsistencias con sugerencias de corrección

## Patrones a buscar

| Tipo | Patrón | Verificación |
|------|--------|--------------|
| Nombres de clase | `class NombreClase` | Debe estar en inglés |
| Nombres de función | `def nombre_funcion` | Debe estar en inglés |
| Variables | `variable = valor` | Debe estar en inglés |
| Comentarios | `# comentario` | Debe estar en español |
| Docstrings | `"""texto"""` | Debe estar en español |
| Bloques de código | `\begin{lstlisting}` | Debe usar `\lstinputlisting` |
| Archivos de código | `code/*.py` | Deben existir |

## Ejemplo de reporte

```
## Revisión de código: chapter1.tex

### Problemas encontrados:

1. Línea 118: `CuerpoDosElementos` → Sugerencia: `TwoElementField`
2. Línea 45: Comentario en inglés → Traducir a español
3. Línea 138-182: Código embebido en lstlisting
   → Crear archivo `code/zmod.py`
   → Reemplazar por: \lstinputlisting[language=Python, caption={...}]{code/zmod.py}

### Resumen:
- 1 nombre de clase en español (debe ser inglés)
- 1 comentario en inglés (debe ser español)
- 1 bloque de código embebido (debe estar en archivo externo)

### Acciones sugeridas:
1. Crear directorio `code/` si no existe
2. Extraer código a archivos separados
3. Verificar que los archivos de código sean ejecutables
```
