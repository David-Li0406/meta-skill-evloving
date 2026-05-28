/**
 * Template for src/data/extensions.ts
 * 
 * This file defines all CMS collections for your Wix CLI app.
 * All collections are defined in a single file using extensions.genericExtension().
 * 
 * Replace the example collection with your actual collections.
 */

import { extensions } from '@wix/astro/builders';

export const dataExtension = extensions.genericExtension({
  // IMPORTANT: Replace with a freshly generated UUID v4 string
  // Format: xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx
  // Do NOT use randomUUID() - the UUID must be a static string
  compId: '{{GENERATE_UUID}}',
  
  // Always 'data-extension' for CMS collections
  compName: 'data-extension',
  
  // Always 'DATA_COMPONENT' for CMS collections
  compType: 'DATA_COMPONENT',
  
  compData: {
    dataComponent: {
      // Array of all collections
      collections: [
        {
          // Legacy field - will be removed in future
          schemaUrl: 'https://www.wix.com/',
          
          // Collection identifier (lower-kebab-case or lower_underscore)
          // This will be scoped with app namespace automatically
          idSuffix: 'example-collection',
          
          // Human-readable name shown in CMS
          displayName: 'Example Collection',
          
          // Field used for display (optional)
          displayField: 'title',
          
          // Array of field definitions
          fields: [
            {
              // Field identifier (lowerCamelCase, ASCII only)
              key: 'title',
              
              // Human-readable label
              displayName: 'Title',
              
              // Field type - see FIELD_TYPES.md for all types
              type: 'TEXT',
              
              // Optional: Help text
              description: 'The title of the item'
            },
            {
              key: 'amount',
              displayName: 'Amount',
              type: 'NUMBER'
            },
            {
              key: 'isActive',
              displayName: 'Is Active',
              type: 'BOOLEAN'
            }
            // Add more fields as needed
          ],
          
          // Permission configuration
          // See PERMISSIONS.md for all access levels
          dataPermissions: {
            // Who can read items
            itemRead: 'ANYONE',
            
            // Who can create items
            itemInsert: 'PRIVILEGED',
            
            // Who can update items
            itemUpdate: 'PRIVILEGED',
            
            // Who can delete items
            itemRemove: 'PRIVILEGED'
          },
          
          // Optional: Initial seed data
          // Only include if blueprint mentions example data
          initialData: [
            {
              // Must match field keys exactly (lowerCamelCase)
              title: 'Example Item 1',
              amount: 10,
              isActive: true
            },
            {
              title: 'Example Item 2',
              amount: 20,
              isActive: false
            }
            // Add more initial items as needed
          ]
        }
        // Add more collections as needed
      ]
    }
  }
});

/**
 * Example: Collection with REFERENCE field
 * 
 * To create a reference relationship, define both collections in the same file:
 * 
 * collections: [
 *   {
 *     idSuffix: 'categories',
 *     displayName: 'Categories',
 *     fields: [
 *       { key: 'name', displayName: 'Name', type: 'TEXT' }
 *     ],
 *     dataPermissions: { ... }
 *   },
 *   {
 *     idSuffix: 'products',
 *     displayName: 'Products',
 *     fields: [
 *       { key: 'name', displayName: 'Name', type: 'TEXT' },
 *       {
 *         key: 'category',
 *         displayName: 'Category',
 *         type: 'REFERENCE',
 *         referenceOptions: {
 *           // Use idSuffix of referenced collection
 *           referencedCollectionId: 'categories'
 *         }
 *       }
 *     ],
 *     dataPermissions: { ... }
 *   }
 * ]
 * 
 * IMPORTANT: REFERENCE fields can ONLY link to other custom collections
 * in your app. NEVER use REFERENCE to link to Wix business entities
 * (Products, Orders, Contacts, Members, etc.).
 */

/**
 * Example: Collection with MULTI_REFERENCE field
 * 
 * For many-to-many relationships:
 * 
 * {
 *   key: 'tags',
 *   displayName: 'Tags',
 *   type: 'MULTI_REFERENCE',
 *   multiReferenceOptions: {
 *     referencedCollectionId: 'tags'
 *   }
 * }
 */

/**
 * Field Types Available:
 * 
 * Basic: TEXT, NUMBER, BOOLEAN, DATE, DATETIME, TIME
 * Media: IMAGE, VIDEO, AUDIO, DOCUMENT, MEDIA_GALLERY
 * Rich: RICH_TEXT, RICH_CONTENT
 * Arrays: ARRAY, ARRAY_STRING, ARRAY_DOCUMENT
 * References: REFERENCE, MULTI_REFERENCE
 * Special: URL, ADDRESS, PAGE_LINK, LANGUAGE, OBJECT, ANY
 * 
 * See references/FIELD_TYPES.md for complete documentation.
 */

/**
 * Access Levels Available:
 * 
 * UNDEFINED, ANYONE, SITE_MEMBER, SITE_MEMBER_AUTHOR, 
 * CMS_EDITOR, PRIVILEGED
 * 
 * See references/PERMISSIONS.md for complete documentation.
 */

/**
 * Wix CLI-Specific Constraints:
 * 
 * - NEVER create collections for embedded script configuration
 *   → Use embedded script parameters instead
 * 
 * - NEVER create collections for site widget configuration
 *   → Use widget settings panel instead
 * 
 * - REFERENCE fields can ONLY link to custom collections in your app
 *   → NEVER link to Wix business entities
 * 
 * See wix-cli-cms-collection/references/CODEGEN_PATTERNS.md for complete guidelines.
 */
