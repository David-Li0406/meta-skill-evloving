/**
 * Template for creating a new Handlebars partial
 *
 * Steps:
 * 1. Copy this file to src/@cliter/handlebars/partials/
 * 2. Rename to your-partial-name.ts (kebab-case)
 * 3. Add import to src/@cliter/handlebars/partials/index.ts
 *
 * Usage in templates:
 *   {{> myPartial }}
 *   {{> myPartial param1="value" param2=variable }}
 */
import * as handlebars from 'handlebars';

// Option 1: Simple partial (static content)
handlebars.registerPartial('simplePartial', `
// This is static content that will be inserted
// wherever {{> simplePartial }} is used
`);

// Option 2: Partial with parameters
handlebars.registerPartial('paramPartial', `
{{! Access parameters directly }}
import { {{ className }} } from '{{ importPath }}';
`);

// Option 3: Complex partial with logic
handlebars.registerPartial('complexPartial', `
{{#each items}}
{{#if (isAllowProperty ../moduleName this)}}
    {{ toCamelCase name }}: {{ getDtoTypeProperty this ../config }};
{{/if}}
{{/each}}
`);

// Option 4: Partial for relationships (Aurora CLI pattern)
handlebars.registerPartial('relationshipPartial', `
{{#eq relationship.type ../relationshipType.ONE_TO_ONE}}
    // One-to-One relationship
    {{ toCamelCase relationship.field }}?: {{ relationship.aggregateName }};
{{/eq}}
{{#eq relationship.type ../relationshipType.ONE_TO_MANY}}
    // One-to-Many relationship
    {{ toCamelCase name }}?: {{ relationship.aggregateName }}[];
{{/eq}}
{{#eq relationship.type ../relationshipType.MANY_TO_ONE}}
    // Many-to-One relationship
    {{ toCamelCase relationship.field }}?: {{ relationship.aggregateName }};
{{/eq}}
{{#eq relationship.type ../relationshipType.MANY_TO_MANY}}
    // Many-to-Many relationship
    {{ toCamelCase name }}?: {{ relationship.aggregateName }}[];
{{/eq}}
`);

// Option 5: Partial for import generation
handlebars.registerPartial('importPartial', `
{{~#each imports}}
import { {{ items }} } from '{{ path }}';
{{/each~}}
`);
