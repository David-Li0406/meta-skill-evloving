---
name: muebleria-forms
description: >
  Forms and validation patterns with react-hook-form + Zod for MuebleriaIris.
  Trigger: When creating forms, validation schemas, or handling form submissions.
license: Apache-2.0
metadata:
  author: muebleria-iris
  version: "1.0"
  scope: [root]
  auto_invoke:
    - "Creating forms"
    - "Implementing form validation"
    - "Using react-hook-form"
    - "Working with Zod schemas"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## When to Use

Use this skill when:

- Creating forms (login, register, CRUD)
- Implementing validation (client + server)
- Using react-hook-form + Zod
- Handling form submissions
- Managing form state

---

## Tech Stack

```
react-hook-form 7.62+ | Zod 4+ | TypeScript
Server validation: Python (backend)
```

---

## Critical Patterns

### Pattern 1: Form with Zod Validation

```tsx
// src/components/forms/ProductForm.tsx
"use client";
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// Zod schema
const productSchema = z.object({
  sku: z.string().min(1, 'SKU requerido').max(50),
  nombre: z.string().min(1, 'Nombre requerido').max(100),
  precio: z.number().positive('Precio debe ser positivo'),
  material: z.string().min(1, 'Material requerido'),
  id_categoria: z.number().int().positive()
});

type ProductFormData = z.infer<typeof productSchema>;

export function ProductForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset
  } = useForm<ProductFormData>({
    resolver: zodResolver(productSchema)
  });
  
  const onSubmit = async (data: ProductFormData) => {
    try {
      const response = await fetch('http://localhost:5000/api/productos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      
      if (!response.ok) {
        const error = await response.json();
        alert(error.error || 'Error al crear producto');
        return;
      }
      
      alert('Producto creado exitosamente');
      reset();
      
    } catch (error) {
      alert('Error de conexión');
    }
  };
  
  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label className="block text-sm font-medium mb-1">SKU</label>
        <input
          {...register('sku')}
          className="w-full p-2 border rounded"
        />
        {errors.sku && (
          <p className="text-red-600 text-sm mt-1">{errors.sku.message}</p>
        )}
      </div>
      
      <div>
        <label className="block text-sm font-medium mb-1">Nombre</label>
        <input
          {...register('nombre')}
          className="w-full p-2 border rounded"
        />
        {errors.nombre && (
          <p className="text-red-600 text-sm mt-1">{errors.nombre.message}</p>
        )}
      </div>
      
      <div>
        <label className="block text-sm font-medium mb-1">Precio</label>
        <input
          type="number"
          step="0.01"
          {...register('precio', { valueAsNumber: true })}
          className="w-full p-2 border rounded"
        />
        {errors.precio && (
          <p className="text-red-600 text-sm mt-1">{errors.precio.message}</p>
        )}
      </div>
      
      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
      >
        {isSubmitting ? 'Guardando...' : 'Crear Producto'}
      </button>
    </form>
  );
}
```

---

## Zod Validation Patterns

```typescript
import { z } from 'zod';

// String validations
z.string().min(1, 'Campo requerido')
z.string().max(100, 'Máximo 100 caracteres')
z.string().email('Email inválido')
z.string().regex(/^[A-Z]{3}\d{3}$/, 'Formato: ABC123')

// Number validations
z.number().int('Debe ser entero')
z.number().positive('Debe ser positivo')
z.number().min(0, 'Mínimo 0')
z.number().max(9999, 'Máximo 9999')

// Custom validations
z.string().refine(val => val.length >= 8, {
  message: 'Mínimo 8 caracteres'
})

// Optional fields
z.string().optional()
z.number().nullable()

// Enums
z.enum(['Madera', 'Metal', 'Tela'])

// Objects
z.object({
  nombre: z.string(),
  edad: z.number()
})

// Arrays
z.array(z.string())
z.array(z.object({ id: z.number() }))

// Unions
z.union([z.string(), z.number()])

// Transformations
z.string().transform(val => val.trim())
z.string().transform(val => val.toLowerCase())
```

---

## Server-Side Validation (Backend)

```python
# backend/app/validators.py
from typing import Dict, Any, List

def validate_producto(data: Dict[str, Any]) -> List[str]:
    """Validate producto data, return list of errors"""
    errors = []
    
    # Required fields
    if not data.get('sku'):
        errors.append('SKU es requerido')
    elif len(data['sku']) > 50:
        errors.append('SKU máximo 50 caracteres')
    
    if not data.get('nombre'):
        errors.append('Nombre es requerido')
    
    if not data.get('precio'):
        errors.append('Precio es requerido')
    elif data['precio'] <= 0:
        errors.append('Precio debe ser positivo')
    
    return errors

# Usage in route
@main.route('/api/productos', methods=['POST'])
def create_producto():
    data = request.get_json()
    
    # Validate
    errors = validate_producto(data)
    if errors:
        return jsonify({'error': ', '.join(errors)}), 400
    
    # Process...
```

---

## Complex Form Example (Order Creation)

```tsx
// src/components/forms/OrderForm.tsx
"use client";
import { useForm, useFieldArray } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const orderItemSchema = z.object({
  id_producto: z.number().int().positive(),
  cantidad: z.number().int().positive('Cantidad debe ser mayor a 0')
});

const orderSchema = z.object({
  id_cliente: z.number().int().positive('Cliente requerido'),
  items: z.array(orderItemSchema).min(1, 'Agregue al menos un producto')
});

type OrderFormData = z.infer<typeof orderSchema>;

export function OrderForm() {
  const {
    register,
    control,
    handleSubmit,
    formState: { errors }
  } = useForm<OrderFormData>({
    resolver: zodResolver(orderSchema),
    defaultValues: {
      items: [{ id_producto: 0, cantidad: 1 }]
    }
  });
  
  const { fields, append, remove } = useFieldArray({
    control,
    name: 'items'
  });
  
  const onSubmit = async (data: OrderFormData) => {
    // Submit to API...
  };
  
  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label>Cliente</label>
        <select {...register('id_cliente', { valueAsNumber: true })}>
          <option value="">Seleccione cliente</option>
          {/* Options... */}
        </select>
        {errors.id_cliente && <p className="text-red-600">{errors.id_cliente.message}</p>}
      </div>
      
      <div>
        <h3>Productos</h3>
        {fields.map((field, index) => (
          <div key={field.id} className="flex gap-2 mb-2">
            <select {...register(`items.${index}.id_producto`, { valueAsNumber: true })}>
              <option value="">Producto</option>
            </select>
            
            <input
              type="number"
              {...register(`items.${index}.cantidad`, { valueAsNumber: true })}
              className="w-20"
            />
            
            <button
              type="button"
              onClick={() => remove(index)}
              className="text-red-600"
            >
              Eliminar
            </button>
          </div>
        ))}
        
        <button
          type="button"
          onClick={() => append({ id_producto: 0, cantidad: 1 })}
          className="text-blue-600"
        >
          + Agregar Producto
        </button>
      </div>
      
      <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">
        Crear Orden
      </button>
    </form>
  );
}
```

---

## Form Component Structure

```
src/components/forms/
├── ProductForm.tsx          # CRUD producto
├── OrderForm.tsx            # Crear orden
├── ClienteForm.tsx          # Registro cliente
├── LoginForm.tsx            # Autenticación
└── schemas/
    ├── productSchema.ts     # Shared Zod schemas
    ├── orderSchema.ts
    └── clienteSchema.ts
```

---

## Best Practices

### DO:
- Validate on client AND server
- Use Zod for TypeScript type inference
- Show clear error messages
- Disable submit button while submitting
- Reset form after successful submission
- Use `valueAsNumber` for number inputs
- Handle API errors gracefully

### DON'T:
- Trust client-side validation only
- Submit without checking isSubmitting
- Ignore error state
- Use uncontrolled inputs for complex forms
- Forget to handle network errors

---

## Commands

```bash
# Install dependencies
npm install react-hook-form @hookform/resolvers zod
```

---

## QA Checklist

- [ ] Schema defined with Zod
- [ ] Client-side validation present
- [ ] Server-side validation matches
- [ ] Error messages are user-friendly
- [ ] Submit button disabled while submitting
- [ ] Form resets after success
- [ ] Loading states shown
- [ ] Network errors handled

---

## Resources

- **react-hook-form**: https://react-hook-form.com
- **Zod**: https://zod.dev
