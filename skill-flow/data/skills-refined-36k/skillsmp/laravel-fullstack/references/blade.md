# Advanced Blade Patterns

## Named Slots

```blade
{{-- resources/views/components/card.blade.php --}}
<div class="bg-white rounded-lg shadow">
    @if(isset($header))
        <div class="px-4 py-3 border-b">
            {{ $header }}
        </div>
    @endif
    
    <div class="p-4">
        {{ $slot }}
    </div>
    
    @if(isset($footer))
        <div class="px-4 py-3 border-t bg-gray-50">
            {{ $footer }}
        </div>
    @endif
</div>

{{-- Usage --}}
<x-card>
    <x-slot:header>
        <h2 class="font-semibold">Card Title</h2>
    </x-slot:header>
    
    <p>Card content here</p>
    
    <x-slot:footer>
        <button>Action</button>
    </x-slot:footer>
</x-card>
```

## Stacks

```blade
{{-- Layout --}}
<head>
    @vite(['resources/css/app.css'])
    @stack('styles')
</head>
<body>
    {{ $slot }}
    
    @vite(['resources/js/app.js'])
    @stack('scripts')
</body>

{{-- Page --}}
@push('styles')
    <link rel="stylesheet" href="/custom.css">
@endpush

@push('scripts')
    <script src="/custom.js"></script>
@endpush
```

## Conditional Classes

```blade
@php
    $isActive = true;
    $isDisabled = false;
@endphp

<button @class([
    'px-4 py-2 rounded',
    'bg-blue-600 text-white' => $isActive,
    'bg-gray-300 text-gray-500' => $isDisabled,
    'cursor-not-allowed' => $isDisabled,
])>
    Button
</button>
```

## Inline Blade Components

```blade
{{-- resources/views/components/icon.blade.php --}}
@props(['name', 'class' => 'w-5 h-5'])

@switch($name)
    @case('check')
        <svg {{ $attributes->merge(['class' => $class]) }} fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
        </svg>
        @break
    @case('x')
        <svg {{ $attributes->merge(['class' => $class]) }} fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
        @break
@endswitch

{{-- Usage --}}
<x-icon name="check" class="w-6 h-6 text-green-500" />
```

## Form Components

```blade
{{-- resources/views/components/form/input.blade.php --}}
@props([
    'name',
    'label' => null,
    'type' => 'text',
])

<div>
    @if($label)
        <label for="{{ $name }}" class="block text-sm font-medium text-gray-700 mb-1">
            {{ $label }}
        </label>
    @endif
    
    <input 
        type="{{ $type }}"
        name="{{ $name }}"
        id="{{ $name }}"
        value="{{ old($name) }}"
        {{ $attributes->class([
            'w-full rounded-lg border-gray-300 shadow-sm',
            'border-red-500' => $errors->has($name),
        ]) }}
    >
    
    @error($name)
        <p class="mt-1 text-sm text-red-600">{{ $message }}</p>
    @enderror
</div>

{{-- Usage --}}
<x-form.input name="email" label="Email Address" type="email" required />
```

## Loops with @forelse

```blade
<ul>
    @forelse($items as $item)
        <li>{{ $item->name }}</li>
    @empty
        <li class="text-gray-500">No items found.</li>
    @endforelse
</ul>
```
