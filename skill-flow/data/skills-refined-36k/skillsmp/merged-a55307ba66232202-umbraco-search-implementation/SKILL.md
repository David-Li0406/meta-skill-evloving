---
name: umbraco-search-implementation
description: Use this skill when implementing custom search functionality and result items in the Umbraco backoffice.
---

# Umbraco Search Implementation

## What is it?
This skill encompasses the implementation of custom search providers and search result items in the Umbraco backoffice. It allows you to integrate custom search functionality and control how individual search results are displayed.

## Documentation
Always fetch the latest docs before implementing:

- **Extension Types**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types
- **Foundation**: https://docs.umbraco.com/umbraco-cms/customizing/foundation
- **Extension Registry**: https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry

## Related Foundation Skills

- **Umbraco Element**: For implementing the result item element
  - Reference skill: `umbraco-umbraco-element`

- **Repository Pattern**: For data access in search providers
  - Reference skill: `umbraco-repository-pattern`

- **Context API**: For accessing contexts within the provider
  - Reference skill: `umbraco-context-api`

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above.
2. **Ask questions** - What data to search? What fields to return? What additional info to display?
3. **Generate files** - Create manifest + provider class and result item based on latest docs.
4. **Explain** - Show what was created and how to test.

## Minimal Examples

### Search Provider Manifest (manifests.ts)
```typescript
import type { ManifestSearchProvider } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestSearchProvider = {
  type: 'searchProvider',
  alias: 'My.SearchProvider',
  name: 'My Search Provider',
  api: () => import('./my-search-provider.js'),
  meta: {
    label: 'My Items',
  },
};

export const manifests = [manifest];
```

### Search Provider Implementation (my-search-provider.ts)
```typescript
import type { UmbSearchProvider, UmbSearchResultItemModel, UmbSearchRequestArgs } from '@umbraco-cms/backoffice/search';
import type { UmbControllerHost } from '@umbraco-cms/backoffice/controller-api';
import { UmbControllerBase } from '@umbraco-cms/backoffice/class-api';

export class MySearchProvider extends UmbControllerBase implements UmbSearchProvider {
  constructor(host: UmbControllerHost) {
    super(host);
  }

  async search(args: UmbSearchRequestArgs) {
    const { query } = args;

    // Fetch results from your data source
    const results = await this.#fetchResults(query);

    return {
      data: {
        items: results,
        total: results.length,
      },
    };
  }

  async #fetchResults(query: string): Promise<UmbSearchResultItemModel[]> {
    // Your search logic here - API call, local filtering, etc.
    const response = await fetch(`/api/my-items/search?q=${encodeURIComponent(query)}`);
    const data = await response.json();

    return data.items.map((item: any) => ({
      entityType: 'my-entity',
      unique: item.id,
      name: item.name,
      icon: 'icon-document',
      href: `/section/my-section/workspace/my-workspace/edit/${item.id}`,
    }));
  }
}

export default MySearchProvider;
```

### Search Result Item Manifest (manifests.ts)
```typescript
import type { ManifestSearchResultItem } from '@umbraco-cms/backoffice/extension-registry';

const manifest: ManifestSearchResultItem = {
  type: 'searchResultItem',
  alias: 'My.SearchResultItem',
  name: 'My Search Result Item',
  element: () => import('./my-search-result-item.element.js'),
  forEntityTypes: ['my-entity'],
};

export const manifests = [manifest];
```

### Search Result Item Implementation (my-search-result-item.element.ts)
```typescript
import { html, css, customElement, property } from '@umbraco-cms/backoffice/external/lit';
import { UmbLitElement } from '@umbraco-cms/backoffice/lit-element';
import type { UmbSearchResultItemModel } from '@umbraco-cms/backoffice/search';

@customElement('my-search-result-item')
export class MySearchResultItemElement extends UmbLitElement {
  @property({ type: Object })
  item?: UmbSearchResultItemModel;

  render() {
    if (!this.item) return html``;

    return html`
      <a href=${this.item.href} class="result-item">
        <umb-icon name=${this.item.icon ?? 'icon-document'}></umb-icon>
        <div class="content">
          <span class="name">${this.item.name}</span>
          <span class="type">${this.item.entityType}</span>
        </div>
      </a>
    `;
  }

  static styles = css`
    .result-item {
      display: flex;
      align-items: center;
      gap: var(--uui-size-space-3);
      padding: var(--uui-size-space-3);
      text-decoration: none;
      color: inherit;
    }

    .result-item:hover {
      background: var(--uui-color-surface-alt);
    }

    .content {
      display: flex;
      flex-direction: column;
    }

    .name {
      font-weight: 500;
    }

    .type {
      font-size: var(--uui-type-small-size);
      color: var(--uui-color-text-alt);
    }
  `;
}

export default MySearchResultItemElement;
```

## Item Model Properties

| Property | Description |
|----------|-------------|
| `entityType` | The entity type identifier |
| `unique` | Unique identifier for the item |
| `name` | Display name |
| `icon` | Icon name (optional) |
| `href` | URL to navigate when clicked |

That's it! Always fetch fresh docs, keep examples minimal, generate complete working code.