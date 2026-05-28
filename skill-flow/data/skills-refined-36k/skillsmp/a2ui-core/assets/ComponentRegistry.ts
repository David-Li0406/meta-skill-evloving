/**
 * A2UI Component Registry (The Trusted Catalog)
 * 
 * This singleton maps abstract component names (used by agents) to
 * concrete Lit element constructors. It enforces the "Trusted Catalog"
 * security model: only explicitly registered components can be rendered.
 * 
 * @example
 * ```typescript
 * // During app initialization
 * import { componentRegistry } from './ComponentRegistry';
 * import { MyButton } from './components/MyButton';
 * 
 * componentRegistry.register('Button', MyButton, 'agui-button');
 * 
 * // Later, when rendering A2UI payloads
 * const ctor = componentRegistry.get('Button');
 * if (ctor) {
 *   // Safe to instantiate
 * } else {
 *   // Agent requested unknown component - ignore safely
 * }
 * ```
 */

import { LitElement } from 'lit';

/**
 * Type for Lit element constructors
 */
type ComponentConstructor = new () => LitElement;

/**
 * Registry entry containing constructor and metadata
 */
interface RegistryEntry {
    constructor: ComponentConstructor;
    tagName: string;
    category?: 'layout' | 'input' | 'display' | 'smart-wrapper' | 'custom';
    description?: string;
}

/**
 * The Trusted Catalog for A2UI components.
 * Prevents UI injection attacks by only allowing registered components.
 */
class ComponentRegistry {
    private registry = new Map<string, RegistryEntry>();

    /**
     * Register a component for use by agents.
     * 
     * @param type - The key agents use (e.g., "Button", "Chart")
     * @param constructor - The LitElement class
     * @param tagName - The HTML custom element tag (e.g., "agui-button")
     * @param options - Optional metadata (category, description)
     */
    register(
        type: string,
        constructor: ComponentConstructor,
        tagName: string,
        options: { category?: RegistryEntry['category']; description?: string } = {}
    ): void {
        // Register with custom elements if not already defined
        if (!customElements.get(tagName)) {
            customElements.define(tagName, constructor);
        }

        this.registry.set(type, {
            constructor,
            tagName,
            category: options.category,
            description: options.description
        });
    }

    /**
     * Retrieve a component constructor by its type key.
     * Returns undefined if not registered (safe failure).
     * 
     * @param type - The component type requested by the agent
     * @returns The constructor, or undefined if not in catalog
     */
    get(type: string): ComponentConstructor | undefined {
        return this.registry.get(type)?.constructor;
    }

    /**
     * Get the HTML tag name for a component type.
     * 
     * @param type - The component type
     * @returns The tag name, or undefined
     */
    getTagName(type: string): string | undefined {
        return this.registry.get(type)?.tagName;
    }

    /**
     * Check if a component type is registered.
     * 
     * @param type - The component type to check
     * @returns True if registered in the catalog
     */
    has(type: string): boolean {
        return this.registry.has(type);
    }

    /**
     * Get all registered component types.
     * Useful for advertising capabilities to agents.
     * 
     * @returns Array of registered type names
     */
    getRegisteredTypes(): string[] {
        return Array.from(this.registry.keys());
    }

    /**
     * Get capability manifest for agent handshake.
     * Describes what components this client supports.
     */
    getCapabilityManifest(): Record<string, { tagName: string; category?: string }> {
        const manifest: Record<string, { tagName: string; category?: string }> = {};

        for (const [type, entry] of this.registry.entries()) {
            manifest[type] = {
                tagName: entry.tagName,
                category: entry.category
            };
        }

        return manifest;
    }

    /**
     * Clear the registry. Useful for testing.
     */
    clear(): void {
        this.registry.clear();
    }
}

/**
 * Singleton instance of the Component Registry.
 * Import this to register or retrieve components.
 */
export const componentRegistry = new ComponentRegistry();

/**
 * Convenience function to register multiple components at once.
 * 
 * @example
 * ```typescript
 * registerComponents([
 *   ['Button', MyButton, 'agui-button', { category: 'input' }],
 *   ['Text', MyText, 'agui-text', { category: 'display' }]
 * ]);
 * ```
 */
export function registerComponents(
    components: Array<[string, ComponentConstructor, string, { category?: RegistryEntry['category'] }?]>
): void {
    for (const [type, ctor, tagName, options] of components) {
        componentRegistry.register(type, ctor, tagName, options);
    }
}

export { ComponentConstructor, RegistryEntry };
