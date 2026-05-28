# Alpine.js Advanced Patterns

## Data with Fetch

```blade
<div 
    x-data="{
        items: [],
        loading: true,
        async init() {
            const response = await fetch('/api/items');
            this.items = await response.json();
            this.loading = false;
        }
    }"
>
    <template x-if="loading">
        <div>Loading...</div>
    </template>
    
    <template x-for="item in items" :key="item.id">
        <div x-text="item.name"></div>
    </template>
</div>
```

## Form Submission with Fetch

```blade
<form 
    x-data="{
        form: { name: '', email: '' },
        errors: {},
        loading: false,
        async submit() {
            this.loading = true;
            this.errors = {};
            
            try {
                const response = await fetch('/api/users', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRF-TOKEN': document.querySelector('meta[name=csrf-token]').content,
                    },
                    body: JSON.stringify(this.form),
                });
                
                if (!response.ok) {
                    const data = await response.json();
                    this.errors = data.errors || {};
                    return;
                }
                
                window.location.href = '/users';
            } finally {
                this.loading = false;
            }
        }
    }"
    @submit.prevent="submit"
>
    <input type="text" x-model="form.name">
    <template x-if="errors.name">
        <span x-text="errors.name[0]" class="text-red-500"></span>
    </template>
    
    <input type="email" x-model="form.email">
    
    <button type="submit" :disabled="loading">
        <span x-show="!loading">Submit</span>
        <span x-show="loading">Saving...</span>
    </button>
</form>
```

## Tabs Component

```blade
<div x-data="{ activeTab: 'general' }">
    <div class="flex border-b">
        <button 
            @click="activeTab = 'general'"
            :class="{ 'border-b-2 border-blue-500': activeTab === 'general' }"
            class="px-4 py-2"
        >
            General
        </button>
        <button 
            @click="activeTab = 'settings'"
            :class="{ 'border-b-2 border-blue-500': activeTab === 'settings' }"
            class="px-4 py-2"
        >
            Settings
        </button>
    </div>
    
    <div x-show="activeTab === 'general'" class="p-4">
        General content
    </div>
    
    <div x-show="activeTab === 'settings'" class="p-4">
        Settings content
    </div>
</div>
```

## Confirm Delete

```blade
<button 
    x-data
    @click="if(confirm('Are you sure?')) $refs.deleteForm.submit()"
>
    Delete
</button>

<form x-ref="deleteForm" method="POST" action="{{ route('items.destroy', $item) }}">
    @csrf
    @method('DELETE')
</form>
```

## Magic Properties

```blade
<div x-data="{ items: ['a', 'b', 'c'] }">
    {{-- $el - Current DOM element --}}
    <button @click="$el.classList.toggle('active')">Toggle</button>
    
    {{-- $refs - Named references --}}
    <input x-ref="search" type="text">
    <button @click="$refs.search.focus()">Focus</button>
    
    {{-- $watch - Watch for changes --}}
    <div x-init="$watch('items', value => console.log(value))">
        <button @click="items.push('d')">Add</button>
    </div>
    
    {{-- $dispatch - Dispatch custom events --}}
    <button @click="$dispatch('notify', { message: 'Hello' })">Notify</button>
</div>
```

## Global State with Alpine.store

```blade
{{-- In app.js or inline --}}
<script>
    document.addEventListener('alpine:init', () => {
        Alpine.store('notifications', {
            items: [],
            add(message) {
                this.items.push({ id: Date.now(), message });
                setTimeout(() => this.items.shift(), 3000);
            }
        });
    });
</script>

{{-- Usage anywhere --}}
<button @click="$store.notifications.add('Saved!')">Save</button>

<div x-data>
    <template x-for="notification in $store.notifications.items" :key="notification.id">
        <div x-text="notification.message" class="toast"></div>
    </template>
</div>
```
