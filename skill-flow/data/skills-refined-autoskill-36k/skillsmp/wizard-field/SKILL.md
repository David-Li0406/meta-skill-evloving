---
name: wizard-field
description: Guide for adding new fields to application or property wizards. Uses Laravel Precognition with FormRequest rules as single source of truth. Auto-triggers on "add field to wizard", "new wizard field", "add to application form", "add to property form", "wizard validation".
---

# Adding Wizard Fields Guide

You are helping add new fields to RentPath's multi-step wizard forms (Application Wizard or Property Wizard).

## Arguments

This skill accepts optional arguments to specify the field and wizard:

| Usage                                            | Behavior                               |
| ------------------------------------------------ | -------------------------------------- |
| `/wizard-field`                                  | Interactive - ask for field details    |
| `/wizard-field emergency_contact`                | Add field named emergency_contact      |
| `/wizard-field application emergency_contact`    | Add to application wizard specifically |
| `/wizard-field property energy_rating`           | Add to property wizard specifically    |
| `/wizard-field application.identity nationality` | Add to specific step                   |
| `/wizard-field --step=financial`                 | Focus on the financial step            |

**Argument interpretation:**

- **Field name** - The database/form field to add
- **Wizard type** (`application`, `property`) - Which wizard to modify
- **Step** (`identity`, `financial`, `specs`, etc.) - Which step the field belongs to
- **wizard.step** format - Explicit wizard and step specification

## Before You Start

1. **Read the validation pattern**: `docs/patterns/validation.md`
2. **Read the wizard pattern**: `docs/patterns/wizard.md`
3. **Identify which wizard**: Application (tenant) or Property (manager)

## Validation Architecture

RentPath uses **Laravel Precognition** for real-time validation:

- Backend FormRequest rules are the **single source of truth**
- Frontend uses Precognition requests to validate against backend rules
- No Zod schemas - validation is not duplicated

```
Frontend (Precognition) → Backend (FormRequest) → Database
```

## Tools to Use

| Task                   | Tool   | Command/Action                                                             |
| ---------------------- | ------ | -------------------------------------------------------------------------- |
| Check Step FormRequest | `Read` | `app/Http/Requests/Property/Steps/` or `Application/Steps/`                |
| Check model            | `Read` | `app/Models/Application.php` or `Property.php`                             |
| Create migration       | `Bash` | `php artisan make:migration add_[field]_to_[table]`                        |
| Check types            | `Read` | `resources/js/types/index.d.ts`                                            |
| Check wizard hook      | `Read` | `resources/js/hooks/use-property-wizard.ts` or `use-application-wizard.ts` |
| Run validation         | `Bash` | `php artisan test --filter=Validation`                                     |

## Step-by-Step Implementation

### 1. Create Database Migration

```bash
php artisan make:migration add_[field_name]_to_[table_name] --no-interaction
```

```php
public function up(): void
{
    Schema::table('applications', function (Blueprint $table) {
        $table->string('new_field')->nullable();
    });
}
```

Run migration:

```bash
php artisan migrate
```

### 2. Update Model

**Add to fillable:**

```php
// app/Models/Application.php
protected $fillable = [
    // ... existing fields
    'new_field',
];
```

**Add casts if needed:**

```php
protected function casts(): array
{
    return [
        'flag_field' => 'boolean',
        'complex_field' => 'array',
    ];
}
```

### 3. Update Step FormRequest (Backend Validation)

Find the appropriate step FormRequest and add the field:

```php
// app/Http/Requests/Application/Steps/IdentityStepRequest.php

public function rules(): array
{
    return [
        // ... existing rules
        'new_field' => ['required', 'string', 'max:255'],
    ];
}

public function messages(): array
{
    return [
        // ... existing messages
        'new_field.required' => 'New field is required',
        'new_field.max' => 'New field must be less than 255 characters',
    ];
}
```

### 4. Update TypeScript Types

```typescript
// resources/js/types/index.d.ts

interface Application {
    // ... existing fields
    new_field: string | null;
}
```

### 5. Update Wizard Hook Step Config

Add the field to the step's `fields` array for Precognition targeting:

```typescript
// resources/js/hooks/use-application-wizard.ts or use-property-wizard.ts

export const APPLICATION_STEPS: WizardStepConfig<ApplicationStep>[] = [
    {
        id: 'identity',
        title: 'Identity & Legal Eligibility',
        shortTitle: 'Identity',
        fields: [
            // ... existing fields
            'new_field', // Add here - IMPORTANT for step validation
        ],
    },
    // ...
];
```

**Why fields array matters:**

- Precognition uses `Precognition-Validate-Only` header with these field names
- `validateFieldAndRecalculateMaxStep` uses this to know which step a field belongs to
- If field is missing from array, validation won't target it correctly

Also add to initial data:

```typescript
function getInitialData(draft?: DraftApplication): ApplicationWizardData {
    return {
        // ... existing fields
        new_field: draft?.new_field || '',
    };
}
```

### 6. Update Wizard Step Component

```tsx
// resources/js/components/application-wizard/steps/[Step]Step.tsx

interface StepProps {
    data: ApplicationWizardData;
    errors: Record<string, string>;
    touchedFields: Record<string, boolean>;
    updateField: (field: string, value: any) => void;
    markFieldTouched: (field: string) => void;
    onFieldBlur: (field: string) => void; // Validates + recalculates maxStepReached
}

export function IdentityStep({ data, errors, touchedFields, updateField, markFieldTouched, onFieldBlur }: StepProps) {
    return (
        <div className="space-y-4">
            {/* New field */}
            <div className="space-y-2">
                <Label htmlFor="new_field">
                    New Field <span className="text-error">*</span>
                </Label>
                <Input
                    id="new_field"
                    value={data.new_field}
                    onChange={(e) => updateField('new_field', e.target.value)}
                    onBlur={() => onFieldBlur('new_field')}
                    aria-invalid={touchedFields.new_field && !!errors.new_field}
                    className={touchedFields.new_field && errors.new_field ? 'border-error' : ''}
                />
                {touchedFields.new_field && errors.new_field && <p className="text-sm text-error">{errors.new_field}</p>}
            </div>
        </div>
    );
}
```

**Key patterns:**

- `updateField` clears the error for that field
- `onFieldBlur` validates the field AND recalculates maxStepReached if field is from a previous step
- Errors only show when field is touched (prevents cascade errors on mount)
- `aria-invalid` must be set for scroll-to-first-error to work

### 7. Update Controller/Service (if needed)

If the field requires special handling:

```php
// app/Services/ApplicationService.php

// In the publish/submit method, ensure field is handled
$application->update([
    // ... existing fields
    'new_field' => $data['new_field'],
]);
```

### 8. Add Translations (i18n)

Translations are organized by route/domain. Add to the appropriate wizard file:

```php
// For Application Wizard: resources/lang/en/wizard/application.php
// For Property Wizard: resources/lang/en/wizard/property.php

return [
    'steps' => [
        'identity' => [
            // ... existing fields
            'newField' => [
                'label' => 'New Field',
                'placeholder' => 'Enter value...',
            ],
        ],
    ],
];
```

Remember to add translations for all 4 locales (en, de, fr, nl). See `docs/architecture/i18n.md` for the full translation structure.

### 9. Update Tests

```php
// tests/Feature/ApplicationWizardValidationTest.php

test('application requires new_field', function () {
    $user = User::factory()->withTenantProfile()->create();

    $response = $this->actingAs($user)
        ->post('/applications', [
            // ... other required fields
            'new_field' => '',  // Empty
        ]);

    $response->assertSessionHasErrors('new_field');
});
```

### 10. Update Factory (for tests)

```php
// database/factories/ApplicationFactory.php

public function definition(): array
{
    return [
        // ... existing fields
        'new_field' => fake()->sentence(),
    ];
}
```

## Which Step Does the Field Belong To?

### Application Wizard Steps

| Step          | FormRequest           | Fields                               |
| ------------- | --------------------- | ------------------------------------ |
| 1. Identity   | IdentityStepRequest   | Name, DOB, nationality, ID documents |
| 2. Household  | HouseholdStepRequest  | Move-in, occupants, pets             |
| 3. Financial  | FinancialStepRequest  | Employment, income, proof            |
| 4. Support    | SupportStepRequest    | Co-signers, guarantors, insurance    |
| 5. History    | HistoryStepRequest    | Address, references, credit          |
| 6. Additional | AdditionalStepRequest | Extra documents, notes               |
| 7. Consent    | ConsentStepRequest    | Declarations, signature              |

### Property Wizard Steps

| Step         | FormRequest          | Fields                       |
| ------------ | -------------------- | ---------------------------- |
| 1. Type      | TypeStepRequest      | Property type, subtype       |
| 2. Location  | LocationStepRequest  | Address, country             |
| 3. Specs     | SpecsStepRequest     | Bedrooms, bathrooms, size    |
| 4. Amenities | AmenitiesStepRequest | Kitchen, amenities           |
| 5. Energy    | EnergyStepRequest    | Energy class, heating        |
| 6. Pricing   | PricingStepRequest   | Rent, currency, availability |
| 7. Media     | MediaStepRequest     | Title, description, images   |

## Documentation References

- `docs/patterns/validation.md` - Precognition validation strategy
- `docs/patterns/wizard.md` - Wizard architecture
- `docs/modules/applications.md` - Application fields
- `docs/modules/properties.md` - Property fields

## Checklist

- [ ] Migration created and run
- [ ] Model updated (fillable, casts)
- [ ] Step FormRequest updated with rules and messages
- [ ] TypeScript types updated
- [ ] Wizard hook step config updated (fields array)
- [ ] Wizard hook initial data updated
- [ ] Step component updated with UI and onBlur handler
- [ ] Service/Controller updated (if needed)
- [ ] Translations added
- [ ] Tests written
- [ ] Factory updated
- [ ] Manual testing in browser
