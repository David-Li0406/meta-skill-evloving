---
name: extend-app-schemas
description: Extend application schemas for enhanced functionality.
---

# Extend Application Schemas

This skill helps you extend the application schema to support new Kubernetes features. The application schema is a user-facing abstraction that gets converted to Kubernetes resource files (deployment.yaml, ingress.yaml, kustomization.yaml).

## Architecture Overview

The application uses a two-level schema system:

1. **Application Schema** (`app/(dashboard)/apps/formSchema.tsx`) - User-facing form validation using Zod
2. **Kubernetes Resource Schemas** (`app/api/schemas.ts`) - YAML output validation for deployment, ingress, and kustomization

The conversion happens in `app/api/applications.ts` via the `adaptAppToResources()` function, which transforms the application schema into Kubernetes resource specifications.

## Extension Workflow

When extending the application schema, follow these steps:

### Step 1: Add Field to Application Schema

Update `app/(dashboard)/apps/formSchema.tsx` to include your new field in the schema definition.

### Step 2: Update Resource Conversion

Modify the `adaptAppToResources()` function in `app/api/applications.ts` to map your new field to the appropriate Kubernetes resource.

### Step 3: Extend K8s Schema (If Needed)

If your extension requires fields not already defined in the Kubernetes schemas, update the appropriate schema in `app/api/schemas.ts`.

### Step 3.5: Verify Backend Before UI

Before making any UI changes, ensure:

- All backend API tests pass
- The API is functioning correctly
- The schema and resource conversion logic is fully tested

Once the backend tests are green and the API works as expected, you can proceed to update the UI.

### Step 4: Update Form UI

Modify the form component in `app/\(dashboard\)/apps/application-form.tsx` to include input fields for your new schema field. Use existing UI patterns (resource fields, environment variables) as templates:

### Step 5: Add Tests

Update the test files to cover your new functionality:

**API Tests** (`app/api/applications.test.ts`):

- Add tests to verify the new field is correctly reflected in the generated Kubernetes resources files
- Use the AAA pattern (Arrange, Act, Assert) with `produce()` for test data

**Form Tests** (`app/(dashboard)/apps/application-form.browser.test.tsx`):

- Add tests for form validation
- Test user interactions with new fields
- Verify form submission includes the new data

### Step 6: Verify Changes

Run the full test suite to ensure everything works:

```bash
pnpm run dance
```

This command runs linting, type checking, and all tests.

## Read the following files for reference:

`app/\(dashboard\)/apps/formSchema.tsx`
`app/api/applications.ts`
`app/api/schemas.ts`
`app/api/applications.test.ts`
`app/\(dashboard\)/apps/application-form.browser.test.tsx`

## Best Practices

1. **Use Existing Patterns**: Reference similar fields already in the `appFormSchema` to maintain consistency
2. **Field Path Consistency**: Field paths in the App Schema should match the same paths in Kubernetes resources for consistency. For example, if adding `spec.template.spec.containers[0].livenessProbe` to the deployment, structure the app schema field similarly (e.g., `deployment.spec.containers[0].livenessProbe`) unless specified otherwise
3. **Validation Alignment**: Validations in the App Schema should match or be a superset of Kubernetes validations for each field. Ensure user-facing validation is at least as strict as what Kubernetes will enforce.
4. **Test Thoroughly**: Both unit tests (applications.test.ts) and browser tests (application-form.browser.test.tsx)
5. **Run Type Checking**: Always run `pnpm run dance` to catch type errors
6. **Use Fixtures**: Leverage `test-utils/fixtures.ts` for base test data and `produce()` to create variations
7. **Follow Zod Patterns**: Use transforms and refinements for complex validation (see the CPU/memory field implementations in `appFormSchema`)
8. **Form Defaults**: Ensure default values are set in the form, not the schema.

## Plan

Before starting your implementation, outline your plan and give examples of the changes you will make to the app schema and how the Kubernetes resources will be affected. This helps clarify your approach and ensures alignment on the desired shape.
