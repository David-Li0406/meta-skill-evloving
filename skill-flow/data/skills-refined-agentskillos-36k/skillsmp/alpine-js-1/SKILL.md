---
name: alpine-js
description: Implementação de interatividade leve com Alpine.js em projetos Laravel/Blade incluindo componentes reativos, modais, dropdowns, tabs, e formulários dinâmicos. Usar para adicionar comportamentos interativos sem necessidade de Vue/React, criar componentes Blade interativos, e implementar UX moderna em aplicações server-side.
---

# Alpine.js

Skill para interatividade frontend leve em projetos Laravel.

## Setup

```html
<!-- Via CDN -->
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>

<!-- Via NPM -->
npm install alpinejs

// resources/js/app.js
import Alpine from 'alpinejs'
window.Alpine = Alpine
Alpine.start()
```

## Sintaxe Básica

### Diretivas Principais

```html
<!-- x-data: Define estado reativo -->
<div x-data="{ open: false, count: 0, name: '' }">

<!-- x-show: Mostra/esconde (display) -->
<div x-show="open">Conteúdo visível</div>

<!-- x-if: Renderiza condicionalmente (remove do DOM) -->
<template x-if="open">
    <div>Conteúdo renderizado</div>
</template>

<!-- x-for: Loop -->
<template x-for="item in items" :key="item.id">
    <div x-text="item.name"></div>
</template>

<!-- x-bind: Bind de atributos -->
<button :class="{ 'bg-blue-500': active }" :disabled="loading">

<!-- x-on: Event listeners -->
<button @click="open = !open">Toggle</button>
<button @click.prevent="submit()">Submit</button>
<input @keyup.enter="search()">

<!-- x-model: Two-way binding -->
<input type="text" x-model="name">
<p>Olá, <span x-text="name"></span></p>

<!-- x-text: Define texto -->
<span x-text="message"></span>

<!-- x-html: Define HTML (cuidado com XSS) -->
<div x-html="htmlContent"></div>

<!-- x-ref: Referência a elementos -->
<input x-ref="input">
<button @click="$refs.input.focus()">Focus</button>

<!-- x-init: Código de inicialização -->
<div x-data="{ items: [] }" x-init="items = await fetchItems()">
```

## Componentes Comuns

### Dropdown

```html
<div x-data="{ open: false }" class="relative">
    <button @click="open = !open" 
            @click.away="open = false"
            class="px-4 py-2 bg-white border rounded-lg flex items-center gap-2">
        Opções
        <svg :class="{ 'rotate-180': open }" class="w-4 h-4 transition-transform" 
             fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
        </svg>
    </button>
    
    <div x-show="open"
         x-transition:enter="transition ease-out duration-200"
         x-transition:enter-start="opacity-0 scale-95"
         x-transition:enter-end="opacity-100 scale-100"
         x-transition:leave="transition ease-in duration-100"
         x-transition:leave-start="opacity-100 scale-100"
         x-transition:leave-end="opacity-0 scale-95"
         class="absolute mt-2 w-48 bg-white border rounded-lg shadow-lg z-10">
        <a href="#" class="block px-4 py-2 hover:bg-gray-100">Opção 1</a>
        <a href="#" class="block px-4 py-2 hover:bg-gray-100">Opção 2</a>
        <a href="#" class="block px-4 py-2 hover:bg-gray-100">Opção 3</a>
    </div>
</div>
```

### Modal

```html
<div x-data="{ showModal: false }">
    <!-- Trigger -->
    <button @click="showModal = true" class="px-4 py-2 bg-blue-600 text-white rounded-lg">
        Abrir Modal
    </button>
    
    <!-- Modal -->
    <div x-show="showModal" 
         x-transition:enter="transition ease-out duration-300"
         x-transition:enter-start="opacity-0"
         x-transition:enter-end="opacity-100"
         x-transition:leave="transition ease-in duration-200"
         x-transition:leave-start="opacity-100"
         x-transition:leave-end="opacity-0"
         class="fixed inset-0 z-50 flex items-center justify-center"
         @keydown.escape.window="showModal = false">
        
        <!-- Overlay -->
        <div class="fixed inset-0 bg-black bg-opacity-50" @click="showModal = false"></div>
        
        <!-- Content -->
        <div x-show="showModal"
             x-transition:enter="transition ease-out duration-300"
             x-transition:enter-start="opacity-0 scale-90"
             x-transition:enter-end="opacity-100 scale-100"
             class="relative bg-white rounded-lg shadow-xl max-w-md w-full mx-4 z-10">
            <div class="p-6">
                <h3 class="text-lg font-semibold mb-4">Título do Modal</h3>
                <p class="text-gray-600">Conteúdo do modal aqui.</p>
            </div>
            <div class="flex justify-end gap-2 p-4 border-t">
                <button @click="showModal = false" class="px-4 py-2 text-gray-600">
                    Cancelar
                </button>
                <button @click="showModal = false" class="px-4 py-2 bg-blue-600 text-white rounded-lg">
                    Confirmar
                </button>
            </div>
        </div>
    </div>
</div>
```

### Tabs

```html
<div x-data="{ activeTab: 'tab1' }">
    <!-- Tab Headers -->
    <div class="flex border-b">
        <button @click="activeTab = 'tab1'"
                :class="{ 'border-b-2 border-blue-500 text-blue-600': activeTab === 'tab1' }"
                class="px-4 py-2 font-medium">
            Tab 1
        </button>
        <button @click="activeTab = 'tab2'"
                :class="{ 'border-b-2 border-blue-500 text-blue-600': activeTab === 'tab2' }"
                class="px-4 py-2 font-medium">
            Tab 2
        </button>
        <button @click="activeTab = 'tab3'"
                :class="{ 'border-b-2 border-blue-500 text-blue-600': activeTab === 'tab3' }"
                class="px-4 py-2 font-medium">
            Tab 3
        </button>
    </div>
    
    <!-- Tab Content -->
    <div class="p-4">
        <div x-show="activeTab === 'tab1'">Conteúdo da Tab 1</div>
        <div x-show="activeTab === 'tab2'">Conteúdo da Tab 2</div>
        <div x-show="activeTab === 'tab3'">Conteúdo da Tab 3</div>
    </div>
</div>
```

### Accordion

```html
<div x-data="{ active: null }" class="space-y-2">
    <div class="border rounded-lg">
        <button @click="active = active === 1 ? null : 1"
                class="w-full px-4 py-3 text-left flex justify-between items-center">
            <span>Seção 1</span>
            <svg :class="{ 'rotate-180': active === 1 }" class="w-5 h-5 transition-transform"
                 fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
        </button>
        <div x-show="active === 1" x-collapse class="px-4 pb-4">
            Conteúdo da seção 1
        </div>
    </div>
    
    <div class="border rounded-lg">
        <button @click="active = active === 2 ? null : 2"
                class="w-full px-4 py-3 text-left flex justify-between items-center">
            <span>Seção 2</span>
            <svg :class="{ 'rotate-180': active === 2 }" class="w-5 h-5 transition-transform"
                 fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
            </svg>
        </button>
        <div x-show="active === 2" x-collapse class="px-4 pb-4">
            Conteúdo da seção 2
        </div>
    </div>
</div>
```

### Formulário com Validação

```html
<form x-data="{
    form: { name: '', email: '', message: '' },
    errors: {},
    loading: false,
    success: false,
    
    validate() {
        this.errors = {};
        if (!this.form.name) this.errors.name = 'Nome é obrigatório';
        if (!this.form.email) this.errors.email = 'Email é obrigatório';
        else if (!/^\S+@\S+\.\S+$/.test(this.form.email)) this.errors.email = 'Email inválido';
        if (!this.form.message) this.errors.message = 'Mensagem é obrigatória';
        return Object.keys(this.errors).length === 0;
    },
    
    async submit() {
        if (!this.validate()) return;
        
        this.loading = true;
        try {
            const response = await fetch('/api/contact', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN': document.querySelector('meta[name=csrf-token]').content
                },
                body: JSON.stringify(this.form)
            });
            
            if (response.ok) {
                this.success = true;
                this.form = { name: '', email: '', message: '' };
            }
        } finally {
            this.loading = false;
        }
    }
}" @submit.prevent="submit" class="space-y-4">

    <div x-show="success" class="p-4 bg-green-100 text-green-800 rounded-lg">
        Mensagem enviada com sucesso!
    </div>

    <div>
        <label class="block text-sm font-medium mb-1">Nome</label>
        <input type="text" x-model="form.name"
               :class="{ 'border-red-500': errors.name }"
               class="w-full px-3 py-2 border rounded-lg">
        <p x-show="errors.name" x-text="errors.name" class="text-sm text-red-600 mt-1"></p>
    </div>

    <div>
        <label class="block text-sm font-medium mb-1">Email</label>
        <input type="email" x-model="form.email"
               :class="{ 'border-red-500': errors.email }"
               class="w-full px-3 py-2 border rounded-lg">
        <p x-show="errors.email" x-text="errors.email" class="text-sm text-red-600 mt-1"></p>
    </div>

    <div>
        <label class="block text-sm font-medium mb-1">Mensagem</label>
        <textarea x-model="form.message" rows="4"
                  :class="{ 'border-red-500': errors.message }"
                  class="w-full px-3 py-2 border rounded-lg"></textarea>
        <p x-show="errors.message" x-text="errors.message" class="text-sm text-red-600 mt-1"></p>
    </div>

    <button type="submit" :disabled="loading"
            class="w-full px-4 py-2 bg-blue-600 text-white rounded-lg disabled:opacity-50">
        <span x-show="!loading">Enviar</span>
        <span x-show="loading">Enviando...</span>
    </button>
</form>
```

### Delete com Confirmação

```html
<div x-data="{ confirmDelete: false, deleting: false }">
    <button @click="confirmDelete = true" 
            class="text-red-600 hover:text-red-800">
        Excluir
    </button>
    
    <!-- Confirm Dialog -->
    <div x-show="confirmDelete" class="fixed inset-0 z-50 flex items-center justify-center">
        <div class="fixed inset-0 bg-black bg-opacity-50" @click="confirmDelete = false"></div>
        <div class="relative bg-white rounded-lg p-6 max-w-sm mx-4">
            <h3 class="text-lg font-semibold mb-2">Confirmar exclusão</h3>
            <p class="text-gray-600 mb-4">Tem certeza que deseja excluir este item?</p>
            <div class="flex justify-end gap-2">
                <button @click="confirmDelete = false" class="px-4 py-2 text-gray-600">
                    Cancelar
                </button>
                <button @click="
                    deleting = true;
                    fetch('/api/items/{{ $item->id }}', { 
                        method: 'DELETE',
                        headers: { 'X-CSRF-TOKEN': '{{ csrf_token() }}' }
                    }).then(() => location.reload());
                " :disabled="deleting"
                   class="px-4 py-2 bg-red-600 text-white rounded-lg disabled:opacity-50">
                    <span x-show="!deleting">Excluir</span>
                    <span x-show="deleting">Excluindo...</span>
                </button>
            </div>
        </div>
    </div>
</div>
```

## Plugins Úteis

```javascript
// Collapse (animação de altura)
import collapse from '@alpinejs/collapse'
Alpine.plugin(collapse)

// Uso: <div x-show="open" x-collapse>

// Focus (trap focus em modais)
import focus from '@alpinejs/focus'
Alpine.plugin(focus)

// Uso: <div x-trap="showModal">
```
