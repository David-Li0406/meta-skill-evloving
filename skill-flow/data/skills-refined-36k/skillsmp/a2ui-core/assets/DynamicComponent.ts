/**
 * A2UI Dynamic Component Base Class
 * 
 * Extend this class for A2UI-compliant components that:
 * - Resolve literal or data-bound properties
 * - Dispatch user actions back to the agent
 * - React to data model changes via Lit Signals
 * 
 * @example
 * ```typescript
 * @customElement('agui-my-button')
 * export class MyButton extends DynamicComponent {
 *   render() {
 *     const label = this.resolve(this.componentDefinition.label);
 *     return html`<button @click=${() => this.dispatchUserAction('click')}>${label}</button>`;
 *   }
 * }
 * ```
 */

import { LitElement } from 'lit';
import { property } from 'lit/decorators.js';
// import { SignalWatcher } from '@lit-labs/signals';
// Uncomment above when @lit-labs/signals is added to dependencies

// For now, use standard LitElement. When signals are needed:
// export class DynamicComponent extends SignalWatcher(LitElement) {

/**
 * Component Definition structure from A2UI protocol
 */
interface A2UIPropertyValue {
    literalString?: string;
    literalNumber?: number;
    literalBoolean?: boolean;
    path?: string;  // JSON Pointer (RFC 6901)
}

interface A2UIComponentDefinition {
    id: string;
    component: Record<string, unknown>;
    [key: string]: unknown;
}

/**
 * Base class for all A2UI-compliant components.
 * Handles property resolution and user action dispatch.
 */
export class DynamicComponent extends LitElement {
    /**
     * The JSON component definition from the agent.
     * Contains all properties, including literal values and data paths.
     */
    @property({ type: Object })
    componentDefinition: A2UIComponentDefinition | null = null;

    /**
     * The surface ID this component belongs to.
     * Used for scoping data model access and action dispatch.
     */
    @property({ type: String })
    surfaceId: string = '';

    /**
     * Optional reference to a data store (implement in subclass or inject).
     * For signal-based reactivity, this would return a Signal.
     */
    protected dataStore: Map<string, unknown> = new Map();

    /**
     * Resolves a property value from the component definition.
     * 
     * Handles three cases:
     * 1. Literal values (literalString, literalNumber, literalBoolean)
     * 2. Data path bindings (subscribes to data model)
     * 3. Undefined (property not specified)
     * 
     * @param prop - The property value object from the component definition
     * @returns The resolved value, or undefined if not resolvable
     */
    protected resolve(prop: A2UIPropertyValue | undefined): string | number | boolean | undefined {
        if (!prop) return undefined;

        // Case 1: Literal String
        if (prop.literalString !== undefined) {
            return prop.literalString;
        }

        // Case 2: Literal Number
        if (prop.literalNumber !== undefined) {
            return prop.literalNumber;
        }

        // Case 3: Literal Boolean
        if (prop.literalBoolean !== undefined) {
            return prop.literalBoolean;
        }

        // Case 4: Data Path Binding
        if (prop.path) {
            return this.resolveDataPath(prop.path);
        }

        return undefined;
    }

    /**
     * Resolves a JSON Pointer path from the data model.
     * Override this method to integrate with your actual data store.
     * 
     * @param path - JSON Pointer (e.g., "/user/name")
     * @returns The value at that path, or undefined
     */
    protected resolveDataPath(path: string): unknown {
        // Default implementation uses a simple Map
        // In production, this would access a Signal-based reactive store
        return this.dataStore.get(path);
    }

    /**
     * Dispatches a user action event to the agent.
     * 
     * This is the standard way for A2UI components to communicate
     * user intent back to the agent. The event bubbles up through
     * Shadow DOM boundaries.
     * 
     * @param actionName - Semantic name of the action (e.g., "submit", "select_item")
     * @param contextData - Additional data needed by the agent (e.g., form values)
     */
    protected dispatchUserAction(actionName: string, contextData: Record<string, unknown> = {}): void {
        const detail = {
            surfaceId: this.surfaceId,
            componentId: this.componentDefinition?.id ?? 'unknown',
            action: actionName,
            context: contextData,
            timestamp: Date.now()
        };

        this.dispatchEvent(new CustomEvent('a2ui-action', {
            bubbles: true,
            composed: true,  // Crosses Shadow DOM boundary
            detail
        }));
    }

    /**
     * Helper to dispatch a value change action.
     * Common pattern for input components.
     * 
     * @param value - The new value
     * @param fieldPath - Optional path hint for the agent
     */
    protected dispatchValueChange(value: unknown, fieldPath?: string): void {
        this.dispatchUserAction('value_change', {
            value,
            fieldPath
        });
    }
}

export { A2UIPropertyValue, A2UIComponentDefinition };
