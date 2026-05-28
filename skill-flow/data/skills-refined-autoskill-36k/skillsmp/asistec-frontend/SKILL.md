---
name: asistec-frontend
description: Úsalo cuando el usuario necesite crear pantallas, componentes visuales, lógica de cliente (Angular), rutas en Ionic, aplicar estilos SCSS o modificar el frontend.
---
# Frontend Expert (Asistec Lab)

Eres el especialista Frontend del proyecto Asistec. Tu objetivo es crear interfaces móviles limpias, rápidas, modulares y expansibles.

## 🛠️ Stack Tecnológico
- **Framework**: Angular 17+ (Arquitectura basada en **NgModules**, NO Standalone).
- **UI Toolkit**: Ionic 7+ (Componentes nativos móviles).
- **Estilos**: Tailwind CSS (Utility-first con patrón @apply).

## 📐 Reglas de Arquitectura & Código

### 1. Estructura del TS de las Páginas (Standalone: false)
Los componentes **NO** son standalone. Deben ser parte de un módulo.
```typescript
@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  standalone: false,
})
export class HomePage { ... }


## 📐 Reglas de Arquitectura (CRÍTICO)

### 1. Gestión de Componentes Compartidos (ComponentsModule)
**NO** generes componentes con `standalone: true`. Todos los componentes reutilizables (Botones, Headers, Cards) deben ser declarados y exportados en el `ComponentsModule`.

**Flujo de creación de un componente:**
1. Generar el componente (ej: `ng g c components/mi-nuevo-comp`).
2. Ir a `src/app/components/components.module.ts`.
3. Importarlo, Declararlo y Exportarlo.

**Ejemplo de Referencia (`components.module.ts`):**
```typescript
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';
import { FormsModule } from '@angular/forms';
// Importaciones de tus componentes
import { HeaderComponent } from '../header/header.component';
import { ALIItemAccordeonComponent } from '../ali-item-accordeon/ali-item-accordeon.component';

@NgModule({
    declarations: [
        HeaderComponent,
        ALIItemAccordeonComponent,
        // ... agrega aquí los nuevos
    ],
    imports: [
        CommonModule,
        IonicModule,
        FormsModule
    ],
    exports: [
        HeaderComponent,
        ALIItemAccordeonComponent,
        // ... expórtalos para usarlos en las Pages
    ]
})
export class ComponentsModule { }
```

### 2. Estandarización HTML & SCSS (Patrón @apply)
Buscamos limpiar el HTML de largas cadenas de utilidades. Agrupa elementos visuales bajo clases semánticas y aplica estilos en el SCSS.

**Reglas de HTML:**
- Usa nombres de clase descriptivos y estandarizados para agrupar bloques (ej: `.label-contenedor`, `.card-usuario`, `.input-group`).
- Mantén el HTML legible.

**Reglas de SCSS:**
- Usa **siempre** la directiva `@apply` de Tailwind para definir los estilos de esas clases.
- No escribas CSS puro (hexadecimales o medidas en px) si existe una clase de Tailwind para ello.

#### ✅ Ejemplo Correcto:

**HTML (`mi-componente.component.html`):**
```html
<div class="label-contenedor">
  <ion-label>Nombre del Equipo</ion-label>
  <ion-input placeholder="Ej: Osciloscopio"></ion-input>
</div>
```

**SCSS (`mi-componente.component.scss`):**
```scss
.label-contenedor {
  @apply flex flex-col gap-2;
}
```
### 3. Uso de componentes en paginas
Para usar estos componentes en una página (ej: HomePage), NO importes el componente individualmente. Debes importar el ComponentsModule en el módulo de la página.

```TypeScript
import { ComponentsModule } from '../../components/components.module';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    ComponentsModule, // <--- Obligatorio para usar <app-header>
    HomePageRoutingModule
  ],
  declarations: [HomePage]
})
export class HomePageModule {}
```


### 4. Buenas Prácticas Generales
Interfaces: Define modelos de datos en src/app/interfaces/ antes de codificar la vista.

Logica: La lógica compleja va en Servicios, no en el componente.

### 5. Nuevas Páginas y Routing
Al crear una página nueva (ej: `ionic generate page pages/nueva-funcionalidad`):
1. Asegúrate de configurar la ruta en `app-routing.module.ts`.
2. Recuerda importar `ComponentsModule` en el `nueva-funcionalidad.module.ts`.
3. Usa la estructura HTML/SCSS con `@apply` definida arriba.