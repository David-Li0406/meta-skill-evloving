---
name: dsfr-component
description: Develops, styles, and tests DSFR-compliant React 19 components.
---

# DSFR Component Skill

This skill provides instructions and best practices for creating UI components for the Verseau frontend, based on the [Système de Design de l'État (DSFR)](https://www.systeme-de-design.gouv.fr/).

## Tech Stack
- **Framework**: React 19 (Vite)
- **UI Components**: `@codegouvfr/react-dsfr`
- **Testing**: `vitest` + `@testing-library/react`
- **Icons**: Remix Icon (integrated via `react-dsfr`)

## Core Principles

### 1. DSFR First
- **ALWAYS use DSFR components** whenever possible. Do not reinvent the wheel if a DSFR component exists.
- Check the [Official DSFR Component List](https://www.systeme-de-design.gouv.fr/elements-d-interface) and [React-DSFR documentation](https://components.react-dsfr.gouv.fr/).
- Use `react-dsfr` components (e.g., `Button`, `Input`, `Card`, `Badge`, `Alert`, `Accordion`).

### 2. Styling
- Use **DSFR utility classes** (e.g., `fr-m-2w`, `fr-text--bold`, `fr-container`, `fr-grid-row`) for layout and spacing.
- Avoid custom CSS unless absolutely necessary.
- Use the DSFR spacing system (e.g., `1w` = 4px, `2w` = 8px, `3w` = 12px, etc.).

### 3. Component Structure
- Keep components focused and small.
- Use functional components and TypeScript interfaces for props.
- Each component should be located in `apps/front/src/components`.

### 4. Testing
- Every component **MUST** have a `.spec.tsx` file in the same directory.
- Use `@testing-library/react` for functional testing.
- Test for:
    - Proper rendering of DSFR classes.
    - Accessibility (aria-labels, roles).
    - Interaction handling.
- Ensure tests pass by running `npm run test` in `apps/front`.

## Workflow

1. **Discovery**: Check if the required UI element exists in [React-DSFR documentation](https://components.react-dsfr.gouv.fr/).
2. **Implementation**: Create component in `src/components/MyComponent.tsx`.
3. **Tests**: Create `src/components/MyComponent.spec.tsx`.
4. **Validation**: Run `npm run test` and `npm run check` (TypeScript).

## Example Template

```tsx
import { ReactNode } from "react";
import { Button } from "@codegouvfr/react-dsfr/Button";
import { fr } from "@codegouvfr/react-dsfr";

interface MyComponentProps {
    title: string;
    description?: string;
    onConfirm: () => void;
}

export const MyComponent = ({ title, description, onConfirm }: MyComponentProps) => {
    return (
        <div className={fr.cx("fr-container", "fr-my-4w")}>
            <div className={fr.cx("fr-grid-row")}>
                <div className={fr.cx("fr-col-12")}>
                    <h1>{title}</h1>
                    {description && <p className={fr.cx("fr-text--lead")}>{description}</p>}
                    <Button onClick={onConfirm}>Confirmer</Button>
                </div>
            </div>
        </div>
    );
};
```
