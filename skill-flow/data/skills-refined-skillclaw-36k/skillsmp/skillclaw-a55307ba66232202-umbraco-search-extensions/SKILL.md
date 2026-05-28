---
name: umbraco-search-extensions
description: Use this skill when implementing custom search functionality and result items in the Umbraco backoffice.
---

# Skill body

## What is it?
This skill encompasses the implementation of both search result items and search providers in the Umbraco backoffice, allowing for customized search functionality and display of results.

## Documentation
Always fetch the latest docs before implementing:

- **Extension Types**: [Extension Types Documentation](https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-types)
- **Foundation**: [Foundation Documentation](https://docs.umbraco.com/umbraco-cms/customizing/foundation)
- **Extension Registry**: [Extension Registry Documentation](https://docs.umbraco.com/umbraco-cms/customizing/extending-overview/extension-registry)

## Workflow

1. **Fetch docs** - Use WebFetch on the URLs above.
2. **Ask questions** - Determine what entity types to search, what additional info to display, and what fields to return.
3. **Generate files** - Create manifest and implementation files based on the latest docs.
4. **Explain** - Show what was created and how to test.

## Minimal Examples

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
          <span class="title">${this.item.title}</span>
          <span class="description">${this.item.description}</span>
        </div>
      </a>
    `;
  }
}
```

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
      total: results.length,
      items: results.map(result => this.#mapToSearchResultItem(result)),
    };
  }

  #fetchResults(query: string) {
    // Implement your data fetching logic here
  }

  #mapToSearchResultItem(result: any): UmbSearchResultItemModel {
    // Map your result to the UmbSearchResultItemModel structure
  }
}
```