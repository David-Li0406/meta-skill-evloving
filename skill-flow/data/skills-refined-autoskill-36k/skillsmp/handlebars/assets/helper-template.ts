/**
 * Template for creating a new Handlebars helper
 *
 * Steps:
 * 1. Copy this file to src/@cliter/handlebars/helpers/
 * 2. Rename to your-helper-name.ts (kebab-case)
 * 3. Update the helper name (camelCase)
 * 4. Add import to src/@cliter/handlebars/helpers/index.ts
 */
import * as handlebars from 'handlebars';

// Option 1: Simple helper (returns a value)
handlebars.registerHelper('mySimpleHelper', function(
    value: string,
    options?: any,
)
{
    // Transform and return the value
    return value.toUpperCase();
});

// Option 2: Helper with multiple parameters
handlebars.registerHelper('myMultiParamHelper', function(
    param1: string,
    param2: number,
    param3: boolean,
)
{
    if (param3)
    {
        return `${param1}-${param2}`;
    }
    return param1;
});

// Option 3: Block helper (with content)
handlebars.registerHelper('myBlockHelper', function(
    condition: any,
    options: any,
)
{
    // options.fn(this) - renders the block content
    // options.inverse(this) - renders the else block
    // options.data.root - access to root context
    // options.hash - named parameters {{ helper key=value }}

    if (condition)
    {
        return options.fn(this);
    }
    return options.inverse(this);
});

// Option 4: Helper that modifies context
handlebars.registerHelper('myContextHelper', function(
    varName: string,
    varValue: any,
    options: any,
)
{
    // Set variable in root context for later use
    options.data.root[varName] = varValue;
    // Return empty string (side-effect only helper)
    return '';
});

// Option 5: Helper with typed parameters (Aurora CLI pattern)
import { Property } from '../../types';

handlebars.registerHelper('myTypedHelper', function(
    properties: Property[],
    config?: any,
)
{
    return properties
        .filter(prop => !prop.nullable)
        .map(prop => prop.name)
        .join(', ');
});
