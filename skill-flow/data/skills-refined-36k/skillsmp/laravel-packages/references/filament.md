# Filament v4 Advanced

> **v4 Key Changes:**
>
> - `Schema` replaces `Form` in method signatures
> - `->components()` instead of `->schema()` in some contexts
> - Badge colors use closures: `->color(fn ($state) => match...)`
> - TailwindCSS v4 required for custom themes
> - Built-in MFA support
> - Nested resources support

## Custom Actions

```php
use Filament\Tables\Actions\Action;

Action::make('approve')
    ->label('Approve')
    ->icon('heroicon-o-check')
    ->color('success')
    ->requiresConfirmation()
    ->action(fn (Order $record) => $record->approve())
    ->visible(fn (Order $record) => $record->status === 'pending');
```

## v4 Form Field Types

```php
use Filament\Forms\Components;

// Text with live JS updates (reduces network requests)
Components\TextInput::make('name')
    ->required()
    ->maxLength(255)
    ->live()
    ->afterStateUpdatedJs('
        $set("slug", $state.toLowerCase().replace(/ /g, "-"));
    ');

// Slider (NEW in v4)
Components\Slider::make('rating')
    ->min(1)
    ->max(5)
    ->step(0.5);

// Code Editor (NEW in v4)
Components\CodeEditor::make('custom_css')
    ->language('css')
    ->minHeight('200px');

// Table Repeater (NEW in v4)
Components\TableRepeater::make('line_items')
    ->schema([
        Components\TextInput::make('description')->required(),
        Components\TextInput::make('quantity')->numeric()->required(),
        Components\TextInput::make('unit_price')->numeric()->prefix('£'),
    ])
    ->defaultItems(1);

// Rich Editor (TipTap in v4)
Components\RichEditor::make('content')
    ->toolbarButtons(['bold', 'italic', 'link', 'bulletList', 'orderedList'])
    ->fileAttachmentsDisk('public')
    ->fileAttachmentsDirectory('attachments');

// File Upload with Image Editor
Components\FileUpload::make('avatar')
    ->image()
    ->imageEditor()
    ->imageEditorAspectRatios(['1:1', '4:3', '16:9'])
    ->circleCropper()
    ->directory('avatars');

// Relationship with Create Option
Components\Select::make('category_id')
    ->relationship('category', 'name')
    ->searchable()
    ->preload()
    ->createOptionForm([
        Components\TextInput::make('name')->required(),
        Components\TextInput::make('slug')->required(),
    ]);
```

## JS-Based Visibility (No Server Round-Trip)

```php
// v4: Use hiddenJs to hide without server request
Forms\Components\Toggle::make('is_featured');

Forms\Components\TextInput::make('featured_until')
    ->hiddenJs('!$get("is_featured")');

// Multiple conditions
Forms\Components\Select::make('discount_type')
    ->options(['percentage' => '%', 'fixed' => '£']);

Forms\Components\TextInput::make('discount_value')
    ->suffix(fn ($get) => $get('discount_type') === 'percentage' ? '%' : '£')
    ->visibleJs('$get("discount_type") !== null');
```

## Custom Pages

```php
<?php

namespace App\Filament\Pages;

use Filament\Pages\Page;
use Filament\Schemas\Schema;
use Filament\Forms\Components\TextInput;
use Filament\Actions\Action;

class Settings extends Page
{
    protected static ?string $navigationIcon = 'heroicon-o-cog';

    protected static string $view = 'filament.pages.settings';

    public ?array $data = [];

    public function mount(): void
    {
        $this->form->fill([
            'site_name' => config('app.name'),
        ]);
    }

    public function form(Schema $schema): Schema
    {
        return $schema
            ->components([
                TextInput::make('site_name')->required(),
            ])
            ->statePath('data');
    }

    protected function getFormActions(): array
    {
        return [
            Action::make('save')
                ->label('Save')
                ->submit('save'),
        ];
    }

    public function save(): void
    {
        // Save settings
    }
}
```

## Notifications

```php
use Filament\Notifications\Notification;

Notification::make()
    ->title('Order Saved')
    ->success()
    ->send();

Notification::make()
    ->title('Error')
    ->body('Something went wrong')
    ->danger()
    ->persistent()
    ->send();
```

## Global Search

```php
// In Resource
public static function getGloballySearchableAttributes(): array
{
    return ['name', 'email', 'order_number'];
}

public static function getGlobalSearchResultDetails(Model $record): array
{
    return [
        'Email' => $record->email,
    ];
}
```

## Authorization

```php
// In Resource
public static function canCreate(): bool
{
    return auth()->user()->can('create orders');
}

public static function canEdit(Model $record): bool
{
    return auth()->user()->can('update', $record);
}

public static function canDelete(Model $record): bool
{
    return auth()->user()->can('delete', $record);
}
```

## Nested Resources (NEW in v4)

```php
// Resources can now be deeply nested
// URL: /admin/categories/1/products/5/variants/2

class VariantResource extends Resource
{
    protected static ?string $model = Variant::class;

    // Parent relationship
    public static function getParentResource(): ?string
    {
        return ProductResource::class;
    }
}
```

## Multi-Factor Authentication (NEW in v4)

```php
// Built-in MFA support
// config/filament.php
'mfa' => [
    'enabled' => true,
    'methods' => [
        'totp' => true,  // Time-based OTP
        'backup_codes' => true,
    ],
],
```
