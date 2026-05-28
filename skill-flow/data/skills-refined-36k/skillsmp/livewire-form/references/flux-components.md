# Flux UI Component Examples

Complete reference for Flux UI form components with Livewire integration.

## Text Input

```blade
<flux:field>
    <flux:label>Name</flux:label>
    <flux:input
        wire:model.blur="title"
        placeholder="Enter title"
        required
    />
    <flux:error name="title" />
</flux:field>
```

## Email Input

```blade
<flux:field>
    <flux:label>Email</flux:label>
    <flux:input
        type="email"
        wire:model.blur="email"
        placeholder="user@example.com"
    />
    <flux:error name="email" />
</flux:field>
```

## Textarea

```blade
<flux:field>
    <flux:label>Description</flux:label>
    <flux:textarea
        wire:model.blur="content"
        rows="4"
        placeholder="Enter content"
    />
    <flux:error name="content" />
</flux:field>
```

## Select Dropdown

```blade
<flux:field>
    <flux:label>Category</flux:label>
    <flux:select wire:model.live="categoryId" placeholder="Choose category...">
        @foreach($categories as $category)
            <flux:option value="{{ $category->id }}">{{ $category->name }}</flux:option>
        @endforeach
    </flux:select>
    <flux:error name="categoryId" />
</flux:field>
```

## Checkbox

```blade
<flux:field>
    <flux:checkbox wire:model.boolean="published">
        <flux:label>Published</flux:label>
    </flux:checkbox>
    <flux:error name="published" />
</flux:field>
```

## Radio Buttons

```blade
<flux:field>
    <flux:label>Status</flux:label>
    <div class="flex gap-4">
        <flux:radio wire:model="status" value="draft">Draft</flux:radio>
        <flux:radio wire:model="status" value="published">Published</flux:radio>
    </div>
    <flux:error name="status" />
</flux:field>
```

## Date Picker (Pro)

```blade
<flux:field>
    <flux:label>Start Date</flux:label>
    <flux:date-picker wire:model="startDate" />
    <flux:error name="startDate" />
</flux:field>
```

## File Upload (Pro)

```blade
<flux:field>
    <flux:label>Avatar</flux:label>
    <flux:file-upload wire:model="avatar" accept="image/*" />
    <flux:error name="avatar" />
</flux:field>
```

## Multiple Select

```blade
<flux:select wire:model="tagIds" multiple>
    @foreach ($tags as $tag)
        <flux:option value="{{ $tag->id }}">{{ $tag->name }}</flux:option>
    @endforeach
</flux:select>
```
