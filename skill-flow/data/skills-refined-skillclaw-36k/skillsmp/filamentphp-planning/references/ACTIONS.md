# FilamentPHP Actions

## Overview

Actions are interactive elements in FilamentPHP that enable users to perform operations like creating, editing, deleting records, triggering custom logic, and managing relationships. Actions can appear in multiple contexts: table rows, table headers, page headers, modals, and custom components.

**When to Use Actions:**
- Record operations (view, edit, delete)
- Bulk operations on multiple records
- Relationship management (attach, detach, associate, dissociate)
- Custom workflows with forms and modals
- Triggering external API calls or background jobs
- Opening modals for user confirmation or data collection

**Key Concepts:**
- Actions can have modals with forms for data collection
- Authorization via policies and the `visible()`/`hidden()` methods
- Bulk actions operate on multiple selected records
- Actions can be grouped into dropdowns for clean UI
- Notifications provide feedback on action success/failure
- Custom action classes promote code reusability

## Table of Contents

1. [Basic Actions](#basic-actions)
2. [Table Actions](#table-actions)
3. [Bulk Actions](#bulk-actions)
4. [Relationship Actions](#relationship-actions)
5. [Action Modals](#action-modals)
6. [Action Forms](#action-forms)
7. [Action Authorization](#action-authorization)
8. [Action Notifications](#action-notifications)
9. [Action Grouping](#action-grouping)
10. [Pre-built Actions](#pre-built-actions)
11. [Custom Action Classes](#custom-action-classes)
12. [Action Positioning](#action-positioning)
13. [External Data Actions](#external-data-actions)
14. [Testing Actions](#testing-actions)
15. [Advanced Patterns](#advanced-patterns)
16. [Troubleshooting](#troubleshooting)

---

## Basic Actions

### Create a Simple Action

```php
use Filament\Actions\Action;

Action::make('sendEmail')
    ->action(function () {
        // Logic to send email
    })
```

### Action with Confirmation

```php
Action::make('delete')
    ->requiresConfirmation()
    ->action(fn () => $this->client->delete())
```

### Action with URL

```php
Action::make('edit')
    ->url(fn (Post $record): string => route('posts.edit', $record))
    ->openUrlInNewTab()
```

### Action with Form Schema

Collect data before executing:

```php
use Filament\Forms\Components\RichEditor;
use Filament\Forms\Components\TextInput;

Action::make('sendEmail')
    ->schema([
        TextInput::make('subject')->required(),
        RichEditor::make('body')->required(),
    ])
    ->action(function (array $data) {
        Mail::to($this->client)
            ->send(new GenericEmail(
                subject: $data['subject'],
                body: $data['body'],
            ));
    })
```

---

## Table Actions

### Record Actions (Row Actions)

Actions that appear for individual table rows:

```php
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->recordActions([
            // ...
        ]);
}
```

### Header Actions

Actions in the table header:

```php
public function table(Table $table): Table
{
    return $table
        ->headerActions([
            // ...
        ]);
}
```

### Toolbar Actions

Actions in the table toolbar (usually bulk actions):

```php
public function table(Table $table): Table
{
    return $table
        ->toolbarActions([
            // ...
        ]);
}
```

### Action with Record Access

```php
use App\Models\Post;
use Filament\Actions\Action;

Action::make('feature')
    ->action(function (Post $record) {
        $record->is_featured = true;
        $record->save();
    })
    ->hidden(fn (Post $record): bool => $record->is_featured)
```

### Multiple Record Actions

```php
use App\Models\Post;
use Filament\Actions\Action;

public function table(Table $table): Table
{
    return $table
        ->columns([
            // ...
        ])
        ->recordActions([
            Action::make('feature')
                ->action(function (Post $record) {
                    $record->is_featured = true;
                    $record->save();
                })
                ->hidden(fn (Post $record): bool => $record->is_featured),
            Action::make('unfeature')
                ->action(function (Post $record) {
                    $record->is_featured = false;
                    $record->save();
                })
                ->visible(fn (Post $record): bool => $record->is_featured),
        ]);
}
```

### Action on Cell Click

Trigger action when clicking a table cell:

```php
use Filament\Actions\Action;
use Filament\Tables\Columns\TextColumn;

TextColumn::make('title')
    ->action(function (Post $record): void {
        $this->dispatch('open-post-edit-modal', post: $record->getKey());
    })
```

Or with modal confirmation:

```php
TextColumn::make('title')
    ->action(
        Action::make('select')
            ->requiresConfirmation()
            ->action(function (Post $record): void {
                $this->dispatch('select-post', post: $record->getKey());
            }),
    )
```

---

## Bulk Actions

### Basic Bulk Action

```php
use Filament\Actions\BulkAction;
use Illuminate\Database\Eloquent\Collection;

BulkAction::make('delete')
    ->requiresConfirmation()
    ->action(fn (Collection $records) => $records->each->delete())
```

### Bulk Action with Authorization

Check policy for each record:

```php
BulkAction::make('delete')
    ->requiresConfirmation()
    ->authorizeIndividualRecords('delete')
    ->action(fn (Collection $records) => $records->each->delete())
```

Records that fail authorization are excluded from `$records`.

### Group Bulk Actions

```php
use Filament\Actions\BulkAction;
use Filament\Actions\BulkActionGroup;

public function table(Table $table): Table
{
    return $table
        ->toolbarActions([
            BulkActionGroup::make([
                BulkAction::make('delete')
                    ->requiresConfirmation()
                    ->action(fn (Collection $records) => $records->each->delete()),
                BulkAction::make('forceDelete')
                    ->requiresConfirmation()
                    ->action(fn (Collection $records) => $records->each->forceDelete()),
            ]),
            BulkAction::make('export')
                ->button()
                ->action(fn (Collection $records) => ...),
        ]);
}
```

### Grouped Bulk Actions Shorthand

When all bulk actions are grouped:

```php
use Filament\Actions\BulkAction;

public function table(Table $table): Table
{
    return $table
        ->groupedBulkActions([
            BulkAction::make('delete')
                ->requiresConfirmation()
                ->action(fn (Collection $records) => $records->each->delete()),
            BulkAction::make('forceDelete')
                ->requiresConfirmation()
                ->action(fn (Collection $records) => $records->each->forceDelete()),
        ]);
}
```

### Bulk Action Notifications

```php
BulkAction::make('delete')
    ->requiresConfirmation()
    ->authorizeIndividualRecords('delete')
    ->action(fn (Collection $records) => $records->each->delete())
    ->successNotificationTitle('Deleted users')
    ->failureNotificationTitle(function (int $successCount, int $totalCount): string {
        if ($successCount) {
            return "{$successCount} of {$totalCount} users deleted";
        }

        return 'Failed to delete any users';
    })
```

### Report Individual Failures

```php
BulkAction::make('delete')
    ->requiresConfirmation()
    ->authorizeIndividualRecords('delete')
    ->action(function (BulkAction $action, Collection $records) {
        $records->each(function (Model $record) use ($action) {
            $record->delete() || $action->reportBulkProcessingFailure(
                'deletion_failed',
                message: function (int $failureCount, int $totalCount): string {
                    if (($failureCount === 1) && ($totalCount === 1)) {
                        return 'One user failed to delete.';
                    }
        
                    if ($failureCount === $totalCount) {
                        return 'All users failed to delete.';
                    }
        
                    if ($failureCount === 1) {
                        return 'One of the selected users failed to delete.';
                    }
        
                    return "{$failureCount} of the selected users failed to delete.";
                },
            );
        });
    })
    ->successNotificationTitle('Deleted users')
    ->failureNotificationTitle(function (int $successCount, int $totalCount): string {
        if ($successCount) {
            return "{$successCount} of {$totalCount} users deleted";
        }

        return 'Failed to delete any users';
    })
```

### Deselect After Completion

```php
BulkAction::make('delete')
    ->action(fn (Collection $records) => $records->each->delete())
    ->deselectRecordsAfterCompletion()
```

### Conditional Record Selection

Disable bulk actions for specific records:

```php
use Illuminate\Database\Eloquent\Model;

public function table(Table $table): Table
{
    return $table
        ->toolbarActions([
            // ...
        ])
        ->checkIfRecordIsSelectableUsing(
            fn (Model $record): bool => $record->status === Status::Enabled,
        );
}
```

### Select Groups Only

Restrict bulk selection to within groups:

```php
public function table(Table $table): Table
{
    return $table
        ->toolbarActions([
            // ...
        ])
        ->selectGroupsOnly();
}
```

---

## Relationship Actions

### Attach Action

For many-to-many relationships:

```php
use Filament\Actions\AttachAction;

public function table(Table $table): Table
{
    return $table
        ->headerActions([
            AttachAction::make(),
        ]);
}
```

### Attach with Pivot Data

```php
use Filament\Forms;

AttachAction::make()
    ->schema(fn (AttachAction $action): array => [
        $action->getRecordSelect(),
        Forms\Components\TextInput::make('role')->required(),
    ])
```

### Attach Multiple Records

```php
AttachAction::make()
    ->multiple()
```

### Attach with Table Select

Use full table instead of dropdown:

```php
use App\Filament\Resources\Products\Tables\ProductsTable;

AttachAction::make()
    ->tableSelect(ProductsTable::class)
```

### Configure Table for Attach Action

```php
use Filament\Tables\Columns\TextColumn;
use Filament\Tables\Table;

public static function configure(Table $table): Table
{
    return $table
        ->columns([
            TextColumn::make('name'),
            TextColumn::make('sku'),
            // ...
        ])
        ->filters([
            // ...
        ]);
}
```

### Search Multiple Columns in Attach

```php
AttachAction::make()
    ->recordSelectSearchColumns(['title', 'description'])
```

### Detach Action

```php
use Filament\Actions\DetachAction;

public function table(Table $table): Table
{
    return $table
        ->recordActions([
            DetachAction::make(),
        ]);
}
```

### Detach Bulk Action

```php
use Filament\Actions\BulkActionGroup;
use Filament\Actions\DetachBulkAction;

public function table(Table $table): Table
{
    return $table
        ->toolbarActions([
            BulkActionGroup::make([
                DetachBulkAction::make(),
            ]),
        ]);
}
```

### Associate Action

For one-to-many relationships:

```php
use Filament\Actions\AssociateAction;

public function table(Table $table): Table
{
    return $table
        ->headerActions([
            AssociateAction::make(),
        ]);
}
```

### Customize Associate Select

```php
use Filament\Forms\Components\Select;

AssociateAction::make()
    ->recordSelect(
        fn (Select $select) => $select->placeholder('Select a post'),
    )
```

### Associate with Search Columns

```php
AssociateAction::make()
    ->recordSelectSearchColumns(['title', 'id'])
```

### Dissociate Action

```php
use Filament\Actions\DissociateAction;

public function table(Table $table): Table
{
    return $table
        ->recordActions([
            DissociateAction::make(),
        ]);
}
```

### Dissociate Bulk Action

```php
use Filament\Actions\BulkActionGroup;
use Filament\Actions\DissociateBulkAction;

public function table(Table $table): Table
{
    return $table
        ->toolbarActions([
            BulkActionGroup::make([
                DissociateBulkAction::make(),
            ]),
        ]);
}
```

---

## Action Modals

### Basic Modal Action

```php
use App\Models\Post;
use Filament\Actions\Action;

Action::make('delete')
    ->action(fn (Post $record) => $record->delete())
    ->requiresConfirmation()
    ->modalHeading('Delete post')
    ->modalDescription('Are you sure you\'d like to delete this post? This cannot be undone.')
    ->modalSubmitActionLabel('Yes, delete it')
```

### Custom Modal Content

Using a Blade view:

```php
Action::make('advance')
    ->action(fn (Post $record) => $record->advance())
    ->modalContent(view('filament.pages.actions.advance'))
```

Dynamic content with data:

```php
use Illuminate\Contracts\View\View;

Action::make('advance')
    ->action(fn (Contract $record) => $record->advance())
    ->modalContent(fn (Contract $record): View => view(
        'filament.pages.actions.advance',
        ['record' => $record],
    ))
```

### Modal Footer Content

```php
Action::make('advance')
    ->action(fn (Post $record) => $record->advance())
    ->modalContentFooter(view('filament.pages.actions.advance'))
```

### Register Modal Actions

For custom modal content:

```php
use Illuminate\Contracts\View\View;

Action::make('advance')
    ->registerModalActions([
        Action::make('report')
            ->requiresConfirmation()
            ->action(fn (Post $record) => $record->report()),
    ])
    ->action(fn (Post $record) => $record->advance())
    ->modalContent(fn (Action $action): View => view(
        'filament.pages.actions.advance',
        ['action' => $action],
    ))
```

### Extra Modal Footer Actions

```php
Action::make('create')
    ->schema([
        // ...
    ])
    ->extraModalFooterActions(fn (Action $action): array => [
        $action->makeModalSubmitAction('createAnother', arguments: ['another' => true]),
    ])
    ->action(function (array $data, array $arguments): void {
        // Create

        if ($arguments['another'] ?? false) {
            // Reset the form and don't close the modal
        }
    })
```

### Sticky Modal Header

```php
Action::make('updateAuthor')
    ->schema([
        // ...
    ])
    ->action(function (array $data): void {
        // ...
    })
    ->stickyModalHeader()
```

### Remove Modal Submit Button

```php
Action::make('help')
    ->modalContent(view('actions.help'))
    ->modalSubmitAction(false)
```

### Multistep Wizard in Modal

```php
use Filament\Forms\Components\MarkdownEditor;
use Filament\Forms\Components\TextInput;
use Filament\Forms\Components\Toggle;
use Filament\Schemas\Components\Wizard\Step;

Action::make('create')
    ->steps([
        Step::make('Name')
            ->description('Give the category a unique name')
            ->schema([
                TextInput::make('name')
                    ->required()
                    ->live()
                    ->afterStateUpdated(fn ($state, callable $set) => $set('slug', Str::slug($state))),
                TextInput::make('slug')
                    ->disabled()
                    ->required()
                    ->unique(Category::class, 'slug'),
            ])
            ->columns(2),
        Step::make('Description')
            ->description('Add some extra details')
            ->schema([
                MarkdownEditor::make('description'),
            ]),
        Step::make('Visibility')
            ->description('Control who can view it')
            ->schema([
                Toggle::make('is_visible')
                    ->label('Visible to customers.')
                    ->default(true),
            ]),
    ])
```

---

## Action Forms

### Form Schema in Action

```php
use App\Models\Post;
use App\Models\User;
use Filament\Forms\Components\Select;

Action::make('updateAuthor')
    ->schema([
        Select::make('authorId')
            ->label('Author')
            ->options(User::query()->pluck('name', 'id'))
            ->required(),
    ])
    ->action(function (array $data, Post $record): void {
        $record->author()->associate($data['authorId']);
        $record->save();
    })
```

### Complex Schema in Modal

```php
use Filament\Forms\Components\Checkbox;
use Filament\Forms\Components\Select;
use Filament\Forms\Components\TextInput;
use Filament\Infolists\Components\TextEntry;
use Filament\Schemas\Components\Grid;
use Filament\Schemas\Components\Section;

Action::make('viewUser')
    ->schema([
        Grid::make(2)
            ->schema([
                Section::make('Details')
                    ->schema([
                        TextInput::make('name'),
                        Select::make('position')
                            ->options([
                                'developer' => 'Developer',
                                'designer' => 'Designer',
                            ]),
                        Checkbox::make('is_admin'),
                    ]),
                Section::make('Auditing')
                    ->schema([
                        TextEntry::make('created_at')
                            ->dateTime(),
                        TextEntry::make('updated_at')
                            ->dateTime(),
                    ]),
            ]),
    ])
```

### Accessing Form Data

```php
function (array $data) {
    // $data contains submitted form values
}
```

**Note:** `$data` is empty until the modal form is submitted.

---

## Action Authorization

### Visible/Hidden Methods

```php
Action::make('edit')
    ->url(fn (): string => route('posts.edit', ['post' => $this->post]))
    ->visible(auth()->user()->can('update', $this->post))
```

```php
Action::make('edit')
    ->url(fn (): string => route('posts.edit', ['post' => $this->post]))
    ->hidden(! auth()->user()->can('update', $this->post))
```

### Authorize Individual Records

For bulk actions:

```php
BulkAction::make('delete')
    ->requiresConfirmation()
    ->authorizeIndividualRecords('delete')
    ->action(fn (Collection $records) => $records->each->delete())
```

Pass policy method name to check against each record. Unauthorized records are filtered out.

---

## Action Notifications

### Success Notification

```php
use Filament\Notifications\Notification;

Action::make('delete')
    ->action(fn (Post $record) => $record->delete())
    ->successNotification(
       Notification::make()
            ->success()
            ->title('Post deleted')
            ->body('The post has been deleted successfully.'),
    )
```

### Failure Notification

```php
BulkAction::make('delete')
    ->successNotificationTitle('Deleted users')
    ->failureNotificationTitle(function (int $successCount, int $totalCount): string {
        if ($successCount) {
            return "{$successCount} of {$totalCount} users deleted";
        }

        return 'Failed to delete any users';
    })
```

---

## Action Grouping

### Basic Action Group

```php
use Filament\Actions\Action;
use Filament\Actions\ActionGroup;

ActionGroup::make([
    Action::make('view'),
    Action::make('edit'),
    Action::make('delete'),
])
```

### Table with Grouped Actions

```php
use Filament\Actions\ActionGroup;
use Filament\Actions\DeleteAction;
use Filament\Actions\EditAction;
use Filament\Actions\ViewAction;

public function table(Table $table): Table
{
    return $table
        ->recordActions([
            ActionGroup::make([
                ViewAction::make(),
                EditAction::make(),
                DeleteAction::make(),
            ]),
            // ...
        ]);
}
```

### Button Group

Render as inline buttons instead of dropdown:

```php
use Filament\Support\Icons\Heroicon;

ActionGroup::make([
    Action::make('edit')
        ->color('gray')
        ->icon(Heroicon::PencilSquare)
        ->hiddenLabel(),
    Action::make('delete')
        ->color('gray')
        ->icon(Heroicon::Trash)
        ->hiddenLabel(),
])
    ->buttonGroup()
```

### Nested Action Groups with Dividers

```php
ActionGroup::make([
    ActionGroup::make([
        // First group of actions
    ])->dropdown(false),
    // Second group of actions (divider automatically added)
])
```

---

## Pre-built Actions

### CreateAction

```php
use Filament\Actions\CreateAction;
use Filament\Forms\Components\TextInput;

CreateAction::make()
    ->schema([
        TextInput::make('title')
            ->required()
            ->maxLength(255),
        // ...
    ])
```

### EditAction

```php
use Filament\Actions\EditAction;

EditAction::make()
```

### ViewAction

```php
use Filament\Actions\ViewAction;
use Filament\Forms\Components\TextInput;

ViewAction::make()
    ->schema([
        TextInput::make('title')
            ->required()
            ->maxLength(255),
        // ...
    ])
```

### DeleteAction

```php
use Filament\Actions\DeleteAction;

DeleteAction::make()
```

### DeleteBulkAction

```php
use Filament\Actions\DeleteBulkAction;

public function table(Table $table): Table
{
    return $table
        ->toolbarActions([
            DeleteBulkAction::make(),
        ]);
}
```

### ForceDeleteAction

```php
use Filament\Actions\ForceDeleteAction;

ForceDeleteAction::make()
    ->successNotification(
       Notification::make()
            ->success()
            ->title('User force-deleted')
            ->body('The user has been force-deleted successfully.'),
    )
```

### ForceDeleteBulkAction

```php
use Filament\Actions\ForceDeleteBulkAction;

public function table(Table $table): Table
{
    return $table
        ->toolbarActions([
            ForceDeleteBulkAction::make(),
        ]);
}
```

### ExportAction

```php
use App\Filament\Exports\ProductExporter;
use Filament\Actions\ExportAction;

public function table(Table $table): Table
{
    return $table
        ->headerActions([
            ExportAction::make()
                ->exporter(ProductExporter::class),
        ]);
}
```

### ExportBulkAction

```php
use App\Filament\Exports\ProductExporter;
use Filament\Actions\ExportBulkAction;

public function table(Table $table): Table
{
    return $table
        ->toolbarActions([
            ExportBulkAction::make()
                ->exporter(ProductExporter::class),
        ]);
}
```

### ImportAction

```php
use App\Filament\Imports\ProductImporter;
use Filament\Actions\ImportAction;

public function table(Table $table): Table
{
    return $table
        ->headerActions([
            ImportAction::make()
                ->importer(ProductImporter::class)
        ]);
}
```

---

## Custom Action Classes

### Define Reusable Action Class

```php
namespace App\Filament\Resources\Customers\Actions;

use App\Models\Customer;
use Filament\Actions\Action;
use Filament\Forms\Components\Textarea;
use Filament\Forms\Components\TextInput;
use Filament\Support\Icons\Heroicon;

class EmailCustomerAction
{
    public static function make(): Action
    {
        return Action::make('email')
            ->label('Send email')
            ->icon(Heroicon::Envelope)
            ->schema([
                TextInput::make('subject')
                    ->required()
                    ->maxLength(255),
                Textarea::make('body')
                    ->autosize()
                    ->required(),
            ])
            ->action(function (Customer $customer, array $data) {
                // Send email logic
            });
    }
}
```

### Use Custom Action in Table

```php
use App\Filament\Resources\Customers\Actions\EmailCustomerAction;

public static function configure(Table $table): Table
{
    return $table
        ->columns([
            // ...
        ])
        ->recordActions([
            EmailCustomerAction::make(),
        ]);
}
```

### Use Custom Action in Page Header

```php
use App\Filament\Resources\Customers\Actions\EmailCustomerAction;

protected function getHeaderActions(): array
{
    return [
        EmailCustomerAction::make(),
    ];
}
```

### Action with Default Name

```php
use Filament\Actions\Action;

class SendInvoiceAction extends Action
{
    public static function getDefaultName(): string
    {
        return 'send';
    }

    protected function setUp(): void
    {
        parent::setUp();
        
        $this
            ->requiresConfirmation()
            ->action(function () {
                // ...
            });
    }
}
```

### Action with ActionName Attribute

```php
use Filament\Actions\Action;
use Filament\Actions\ActionName;

#[ActionName('send')]
class SendInvoiceAction
{
    public static function make(): Action
    {
        return Action::make('send')
            ->requiresConfirmation()
            ->action(function () {
                // ...
            });
    }
}
```

---

## Action Positioning

### Record Actions Position

#### Default (After Columns)

```php
use Filament\Tables\Table;

public function table(Table $table): Table
{
    return $table
        ->recordActions([
            // Actions appear in the last cell
        ]);
}
```

#### Before Columns

```php
use Filament\Tables\Enums\RecordActionsPosition;

public function table(Table $table): Table
{
    return $table
        ->recordActions([
            // ...
        ], position: RecordActionsPosition::BeforeColumns);
}
```

#### Before Checkbox

```php
use Filament\Tables\Enums\RecordActionsPosition;

public function table(Table $table): Table
{
    return $table
        ->recordActions([
            // ...
        ], position: RecordActionsPosition::BeforeCells);
}
```

### Globally Configure Ungrouped Actions

```php
use Filament\Actions\Action;
use Filament\Tables\Table;

Table::configureUsing(function (Table $table): void {
    $table
        ->modifyUngroupedRecordActionsUsing(fn (Action $action) => $action->iconButton());
});
```

---

## External Data Actions

### Create via External API

```php
use Filament\Actions\Action;
use Filament\Forms\Components\Select;
use Filament\Forms\Components\TextInput;
use Filament\Notifications\Notification;
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\Http;

Action::make('create')
    ->modalHeading('Create product')
    ->schema([
        TextInput::make('title')
            ->required(),
        Select::make('category')
            ->options(fn (): Collection => Http::get("{$baseUrl}/products/categories")
                ->collect()
                ->pluck('name', 'slug')
            )
            ->required(),
    ])
    ->action(function (array $data) use ($baseUrl) {
        $response = Http::post("{$baseUrl}/products/add", [
            'title' => $data['title'],
            'category' => $data['category'],
        ]);

        if ($response->failed()) {
            Notification::make()
                ->title('Product failed to create')
                ->danger()
                ->send();
                
            return;
        }
        
        Notification::make()
            ->title('Product created')
            ->success()
            ->send();
    })
```

### Edit via External API

```php
Action::make('edit')
    ->icon(Heroicon::PencilSquare)
    ->modalHeading('Edit product')
    ->fillForm(fn (array $record) => $record)
    ->schema([
        TextInput::make('title')
            ->required(),
        Select::make('category')
            ->options(fn (): Collection => Http::get("{$baseUrl}/products/categories")
                ->collect()
                ->pluck('name', 'slug')
            )
            ->required(),
    ])
    ->action(function (array $data, array $record) use ($baseUrl) {
        $response = Http::put("{$baseUrl}/products/{$record['id']}", [
            'title' => $data['title'],
            'category' => $data['category'],
        ]);

        if ($response->failed()) {
            Notification::make()
                ->title('Product failed to save')
                ->danger()
                ->send();
                
            return;
        }
        
        Notification::make()
            ->title('Product saved')
            ->success()
            ->send();
    })
```

### Delete via External API

```php
Action::make('delete')
    ->color('danger')
    ->icon(Heroicon::Trash)
    ->modalIcon(Heroicon::OutlinedTrash)
    ->modalHeading('Delete Product')
    ->requiresConfirmation()
    ->action(function (array $record) use ($baseUrl) {
        $response = Http::baseUrl($baseUrl)
            ->delete("products/{$record['id']}");

        if ($response->failed()) {
            Notification::make()
                ->title('Product failed to delete')
                ->danger()
                ->send();
                
            return;
        }
        
        Notification::make()
            ->title('Product deleted')
            ->success()
            ->send();
    })
```

### View with External API Data

```php
use Filament\Infolists\Components\ImageEntry;
use Filament\Infolists\Components\TextEntry;
use Filament\Schemas\Components\Flex;
use Filament\Schemas\Components\Grid;
use Filament\Schemas\Components\Section;

Action::make('view')
    ->color('gray')
    ->icon(Heroicon::Eye)
    ->modalHeading('View product')
    ->schema([
        Section::make()
            ->schema([
                Flex::make([
                    Grid::make(2)
                        ->schema([
                            TextEntry::make('title'),
                            TextEntry::make('category'),
                            TextEntry::make('brand'),
                            TextEntry::make('price')
                                ->money(),
                        ]),
                    ImageEntry::make('thumbnail')
                        ->hiddenLabel()
                        ->grow(false),
                ])->from('md'),
                TextEntry::make('description')
                    ->prose(),
            ]),
    ])
    ->modalSubmitAction(false)
    ->modalCancelActionLabel('Close')
```

### Bulk Actions with Custom Data

```php
use Illuminate\Support\Arr;
use Illuminate\Support\Collection;

public function table(Table $table): Table
{
    return $table
        ->records(function (): array {
            // Return custom array data
        })
        ->resolveSelectedRecordsUsing(function (array $keys): array {
            return Arr::only([
                1 => ['title' => 'First item', 'slug' => 'first-item'],
                2 => ['title' => 'Second item', 'slug' => 'second-item'],
                3 => ['title' => 'Third item', 'slug' => 'third-item'],
            ], $keys);
        })
        ->toolbarActions([
            BulkAction::make('feature')
                ->requiresConfirmation()
                ->action(function (Collection $records): void {
                    // Do something with collection of array data
                }),
        ]);
}
```

### Handle Deselected Records

```php
->resolveSelectedRecordsUsing(function (
    array $keys,
    bool $isTrackingDeselectedKeys,
    array $deselectedKeys
): array {
    $records = [
        1 => ['title' => 'First item'],
        2 => ['title' => 'Second item'],
        3 => ['title' => 'Third item'],
    ];
    
    if ($isTrackingDeselectedKeys) {
        return Arr::except($records, $deselectedKeys);
    }
    
    return Arr::only($records, $keys);
})
```

---

## Testing Actions

### Test Table Row Action

```php
use Filament\Actions\Testing\TestAction;
use function Pest\Livewire\livewire;

$invoice = Invoice::factory()->create();

livewire(ListInvoices::class)
    ->callAction(TestAction::make('send')->table($invoice));

livewire(ListInvoices::class)
    ->assertActionVisible(TestAction::make('send')->table($invoice));

livewire(ListInvoices::class)
    ->assertActionExists(TestAction::make('send')->table($invoice));
```

### Test Table Header Action

```php
livewire(ListInvoices::class)
    ->callAction(TestAction::make('create')->table());

livewire(ListInvoices::class)
    ->assertActionVisible(TestAction::make('create')->table());
```

### Test Bulk Action

```php
$invoices = Invoice::factory()->count(3)->create();

livewire(ListInvoices::class)
    ->selectTableRecords($invoices->pluck('id')->toArray())
    ->callAction(TestAction::make('send')->table()->bulk());
```

### Test Nested Actions

```php
$invoice = Invoice::factory()->create();

livewire(ManageInvoices::class)
    ->callAction([
        TestAction::make('view')->table($invoice),
        TestAction::make('send')->schemaComponent('customer.name'),
    ]);
```

### Test Custom Action Class

```php
use App\Filament\Resources\Invoices\Actions\SendInvoiceAction;

$invoice = Invoice::factory()->create();

livewire(ManageInvoices::class)
    ->callAction(TestAction::make(SendInvoiceAction::class)->table($invoice));
```

### Pre-fill Action Form

```php
$invoice = Invoice::factory()->create();

livewire(EditInvoice::class, [
    'invoice' => $invoice,
])
    ->mountAction('send')
    ->fillForm([
        'email' => $email = fake()->email(),
    ]);
```

### Test Bulk Delete

```php
use Filament\Actions\Testing\TestAction;
use function Pest\Laravel\assertDatabaseMissing;

it('can bulk delete users', function () {
    $users = User::factory()->count(5)->create();

    livewire(ListUsers::class)
        ->assertCanSeeTableRecords($users)
        ->selectTableRecords($users)
        ->callAction(TestAction::make(DeleteBulkAction::class)->table()->bulk())
        ->assertNotified()
        ->assertCanNotSeeTableRecords($users);

    $users->each(fn (User $user) => assertDatabaseMissing($user));
});
```

---

## Advanced Patterns

### Access Selected Records in Row Action

```php
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Database\Eloquent\Model;

public function table(Table $table): Table
{
    return $table
        ->selectable()
        ->recordActions([
            Action::make('copyToSelected')
                ->accessSelectedRecords()
                ->action(function (Model $record, Collection $selectedRecords) {
                    $selectedRecords->each(
                        fn (Model $selectedRecord) => $selectedRecord->update([
                            'is_active' => $record->is_active,
                        ]),
                    );
                }),
        ]);
}
```

### Nested Modal Actions

```php
Action::make('edit')
    ->schema([
        // ...
    ])
    ->extraModalFooterActions([
        Action::make('delete')
            ->requiresConfirmation()
            ->action(function () {
                // ...
            }),
    ])
```

### Cancel Parent Actions

```php
Action::make('delete')
    ->requiresConfirmation()
    ->action(function () {
        // ...
    })
    ->cancelParentActions()
```

Selectively cancel specific parents:

```php
Action::make('first')
    ->requiresConfirmation()
    ->action(function () {
        // ...
    })
    ->extraModalFooterActions([
        Action::make('second')
            ->requiresConfirmation()
            ->action(function () {
                // ...
            })
            ->extraModalFooterActions([
                Action::make('third')
                    ->requiresConfirmation()
                    ->action(function () {
                        // ...
                    })
                    ->extraModalFooterActions([
                        Action::make('fourth')
                            ->requiresConfirmation()
                            ->action(function () {
                                // ...
                            })
                            ->cancelParentActions('second'),
                    ]),
            ]),
    ])
```

This cancels 'second' and 'third', but 'first' remains active.

### Access Parent Action Data

```php
use Filament\Forms\Components\TextInput;

Action::make('first')
    ->schema([
        TextInput::make('foo'),
    ])
    ->action(function () {
        // ...
    })
    ->extraModalFooterActions([
        Action::make('second')
            ->requiresConfirmation()
            ->action(function (array $mountedActions) {
                dd($mountedActions[0]->getRawData());
            
                // ...
            }),
    ])
```

### Access Multiple Parent Actions

```php
Action::make('first')
    ->schema([TextInput::make('foo')])
    ->action(function () { /* ... */ })
    ->extraModalFooterActions([
        Action::make('second')
            ->schema([TextInput::make('bar')])
            ->arguments(['number' => 2])
            ->action(function () { /* ... */ })
            ->extraModalFooterActions([
                Action::make('third')
                    ->schema([TextInput::make('baz')])
                    ->arguments(['number' => 3])
                    ->action(function () { /* ... */ })
                    ->extraModalFooterActions([
                        Action::make('fourth')
                            ->requiresConfirmation()
                            ->action(function (array $mountedActions) {
                                dd(
                                    $mountedActions[0]->getRawData(),
                                    $mountedActions[0]->getArguments(),
                                    $mountedActions[1]->getRawData(),
                                    $mountedActions[1]->getArguments(),
                                    $mountedActions[2]->getRawData(),
                                    $mountedActions[2]->getArguments()
                                );
                            }),
                    ]),
            ]),
    ])
```

### Default Action on Page Load

```php
use Filament\Actions\Action;

public $defaultAction = 'onboarding';

public function onboardingAction(): Action
{
    return Action::make('onboarding')
        ->modalHeading('Welcome')
        ->visible(fn (): bool => ! auth()->user()->isOnBoarded());
}
```

### Custom Form Actions

Add custom buttons to form footer:

```php
use Filament\Actions\Action;

protected function getFormActions(): array
{
    return [
        ...parent::getFormActions(),
        Action::make('close')->action('createAndClose'),
    ];
}

public function createAndClose(): void
{
    // ...
}
```

Remove all form actions:

```php
protected function getFormActions(): array
{
    return [];
}
```

### Move Save Action to Header

```php
protected function getHeaderActions(): array
{
    return [
        $this->getSaveFormAction()
            ->formId('form'),
    ];
}
```

### Extra Repeater Item Actions

```php
use Filament\Forms\Components\Repeater;
use Filament\Forms\Components\TextInput;
use Filament\Support\Icons\Heroicon;

Repeater::make('members')
    ->schema([
        TextInput::make('email')
            ->label('Email address')
            ->email(),
        // ...
    ])
    ->extraItemActions([
        Action::make('sendEmail')
            ->icon(Heroicon::Envelope)
            ->action(function (array $arguments, Repeater $component): void {
                $itemData = $component->getItemState($arguments['item']);

                Mail::to($itemData['email'])
                    ->send(
                        // ...
                    );
            }),
    ])
```

### Dashboard Filter Action Modal

```php
use Filament\Forms\Components\DatePicker;
use Filament\Pages\Dashboard as BaseDashboard;
use Filament\Pages\Dashboard\Actions\FilterAction;
use Filament\Pages\Dashboard\Concerns\HasFiltersAction;

class Dashboard extends BaseDashboard
{
    use HasFiltersAction;
    
    protected function getHeaderActions(): array
    {
        return [
            FilterAction::make()
                ->schema([
                    DatePicker::make('startDate'),
                    DatePicker::make('endDate'),
                    // ...
                ]),
        ];
    }
}
```

### Customize Filters Trigger

```php
use Filament\Actions\Action;

public function table(Table $table): Table
{
    return $table
        ->filters([
            // ...
        ])
        ->filtersTriggerAction(
            fn (Action $action) => $action
                ->button()
                ->label('Filter'),
        );
}
```

### Customize Apply Filters Action

```php
public function table(Table $table): Table
{
    return $table
        ->filters([
            // ...
        ])
        ->filtersApplyAction(
            fn (Action $action) => $action
                ->link()
                ->label('Save filters to table'),
        );
}
```

---

## Troubleshooting

### Issue: Action Not Visible

**Causes:**
- Authorization check failing
- `visible(false)` or `hidden(true)` set
- Missing permissions

**Solutions:**

Check authorization:
```php
Action::make('edit')
    ->visible(auth()->user()->can('update', $this->post))
```

Debug visibility:
```php
Action::make('test')
    ->visible(fn () => dd('Checking visibility'))
```

### Issue: Bulk Action Not Working

**Problem:** Bulk action doesn't receive records.

**Checklist:**
- Table has `->selectable()` enabled
- Records are actually selected
- `authorizeIndividualRecords()` not filtering all records out
- Correct parameter type hint (`Collection $records`)

**Solution:**
```php
public function table(Table $table): Table
{
    return $table
        ->selectable()  // Enable checkboxes
        ->toolbarActions([
            BulkAction::make('delete')
                ->action(fn (Collection $records) => $records->each->delete()),
        ]);
}
```

### Issue: Modal Form Data Not Submitted

**Problem:** `$data` is empty in action callback.

**Cause:** Form hasn't been submitted yet or action runs before submission.

**Solution:**
```php
Action::make('update')
    ->schema([
        TextInput::make('name')->required(),
    ])
    ->action(function (array $data) {
        // $data will have values AFTER modal is submitted
        dd($data);  // ['name' => 'submitted value']
    })
```

### Issue: Attach Action Not Searchable

**Problem:** Can't search records in attach modal.

**Solution:** Define search columns:
```php
AttachAction::make()
    ->recordSelectSearchColumns(['title', 'id', 'email'])
```

### Issue: Relationship Action Fails

**Problem:** Attach/Associate/Detach/Dissociate not working.

**Checklist:**
1. Relationship properly defined on model
2. Foreign key exists in database
3. Pivot table exists (for many-to-many)
4. User has permission to modify relationship

**Debug:**
```php
AttachAction::make()
    ->before(function () {
        dd('Attaching...');
    })
    ->after(function ($record) {
        dd('Attached', $record);
    })
```

### Issue: Action Notification Not Showing

**Problem:** Success/failure notification doesn't appear.

**Solutions:**

Ensure notification is configured:
```php
Action::make('delete')
    ->action(fn () => ...)
    ->successNotification(
        Notification::make()
            ->success()
            ->title('Deleted!')
            ->send()
    )
```

Or manually trigger:
```php
->action(function () {
    // Do work
    
    Notification::make()
        ->success()
        ->title('Done!')
        ->send();
})
```

### Issue: Custom Action Class Not Found

**Problem:** `TestAction::make(MyAction::class)` fails in tests.

**Solutions:**

Use `#[ActionName]` attribute:
```php
use Filament\Actions\ActionName;

#[ActionName('myAction')]
class MyAction
{
    public static function make(): Action
    {
        return Action::make('myAction')
            // ...
    }
}
```

Or implement `getDefaultName()`:
```php
class MyAction extends Action
{
    public static function getDefaultName(): string
    {
        return 'myAction';
    }
}
```

### Issue: Bulk Action Deselects Records Prematurely

**Problem:** Records deselected before seeing results.

**Solution:** Remove auto-deselect or delay it:
```php
BulkAction::make('process')
    ->action(fn (Collection $records) => ...)
    // Don't use ->deselectRecordsAfterCompletion()
```

Or keep deselection but show notification:
```php
->deselectRecordsAfterCompletion()
->successNotificationTitle('Processed records')
```

### Issue: Action Icons Not Showing

**Problem:** Icon not visible on action button.

**Solutions:**

Use Heroicon enum:
```php
use Filament\Support\Icons\Heroicon;

Action::make('edit')
    ->icon(Heroicon::PencilSquare)
```

Or string:
```php
->icon('heroicon-o-pencil-square')
```

Check icon aliases:
```php
use Filament\Actions\View\ActionsIconAlias;

// Use predefined aliases
->icon(ActionsIconAlias::EDIT_ACTION)
```

---

## Cross-References

### Related Topics

- **[FORMS.md](FORMS.md)** - Form components used in action modals
- **[TABLES.md](TABLES.md)** - Table integration with actions
- **[NOTIFICATIONS.md](NOTIFICATIONS.md)** - Action feedback via notifications
- **[RESOURCES.md](RESOURCES.md)** - Resource-level actions
- **[PANEL_CONFIGURATION.md](PANEL_CONFIGURATION.md)** - Global action configuration
- **[TESTING.md](TESTING.md)** - Testing action behavior
- **[CODE_QUALITY.md](CODE_QUALITY.md)** - Organizing action classes

### Action Integration

**Actions work with:**
- Resource pages (Create, Edit, List, View)
- Relation managers
- Custom Livewire pages
- Table columns (click actions)
- Dashboard widgets
- Custom components

### Best Practices

1. **Use Custom Action Classes** - Extract complex actions into reusable classes
2. **Authorization First** - Always check permissions before showing/executing
3. **Clear Feedback** - Use notifications to inform users of results
4. **Confirmation for Destructive Actions** - Always require confirmation for deletes
5. **Group Related Actions** - Use ActionGroup for cleaner UI
6. **Test Actions Thoroughly** - Write tests for critical action workflows
7. **Handle Failures Gracefully** - Provide clear error messages
8. **Optimize Bulk Actions** - Use `authorizeIndividualRecords()` for security
9. **Document Complex Actions** - Add comments for multi-step workflows
10. **Consistent Naming** - Use clear, action-oriented names (sendEmail, deleteUser)

---

## FilamentPHP 4.x Documentation

- [Official Actions Documentation](https://filamentphp.com/docs/4.x/actions/overview)
- [Table Actions](https://filamentphp.com/docs/4.x/tables/actions)
- [Bulk Actions](https://filamentphp.com/docs/4.x/tables/actions)
- [Relationship Actions](https://filamentphp.com/docs/4.x/resources/managing-relationships)
- [Action Modals](https://filamentphp.com/docs/4.x/actions/modals)
- [Action Authorization](https://filamentphp.com/docs/4.x/actions/overview#authorization)
- [Testing Actions](https://filamentphp.com/docs/4.x/testing/testing-actions)
- [Pre-built Actions](https://filamentphp.com/docs/4.x/actions/create)

---

**Version:** 1.0.0  
**Last Updated:** January 18, 2026  
**FilamentPHP Version:** 4.x  
**Status:** Complete
