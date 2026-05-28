---
name: blog-management
description: Manage blog posts including creating, editing, viewing, and troubleshooting blog-related features. Use when working with blog posts, articles, post forms, rich text editor, tags, thumbnails, or publishing workflows.
---

# Blog Management

## Overview
This skill helps you work with blog post management features in the admin_side application. It includes creating new posts, editing existing posts, managing tags, handling thumbnails, and working with the Quill rich text editor.

## Key Files and Components

### Blog Pages
- `src/app/admin/blogs/page.tsx` - Blog listing page
- `src/app/admin/blogs/create/page.tsx` - Create new blog page
- `src/app/admin/blogs/edit/page.tsx` - Edit existing blog page
- `src/app/admin/blogs/blog-form.tsx` - Main blog form component

### Related Components
- `src/app/admin/components/inputs/rich-text-editor/` - Quill editor components
- `src/app/admin/components/inputs/multi-chip-input.tsx` - Tag input component
- `src/app/admin/components/inputs/thumbnail-input.tsx` - Image upload component

### Domain Models
- `src/domains/post.ts` - Blog post model and types
- `src/domains/tag.ts` - Tag model and types

## Common Tasks

### Working with Blog Posts

When creating or editing blog posts:

1. **Read the blog form** to understand the current structure:
   ```bash
   Read src/app/admin/blogs/blog-form.tsx
   ```

2. **Check the post domain model** for data structure:
   ```bash
   Read src/domains/post.ts
   ```

3. **Review API integration** in `src/config/api.config.ts`

### Blog Post Fields

A blog post typically includes:
- **title**: Post title
- **previewContent**: Short preview/excerpt
- **content**: Full HTML content from Quill editor
- **thumbnailPaths**: Array of image URLs
- **published**: Boolean status (draft/published)
- **postTags**: Array of tags with name and color
- **categoryId**: Selected category ID
- **rowVersion**: For optimistic locking

### Rich Text Editor

The project uses Quill 2.0 with plugins:
- quill-html-edit-button
- quill-resize-image
- quill-table-better
- quill-toggle-fullscreen-button
- highlight.js for code syntax

When working with the editor:
1. Check `RichTextEditorWrapper` component for setup
2. Verify plugin initialization
3. Test content saving and loading

### Tag Management

Tags use the MultiChipInput component with:
- Random color assignment
- Add/remove functionality
- Label-based storage

### Thumbnail Management

Images are handled by ThumbnailsInput:
- Accepts image uploads
- Returns array of paths
- Displays preview thumbnails

## API Endpoints

Blog posts use REST API endpoints:
- `GET /posts` - List all posts
- `GET /posts/:id` - Get single post
- `POST /posts` - Create new post
- `PUT /posts/:id` - Update existing post
- `DELETE /posts/:id` - Delete post

All endpoints require Bearer token authentication via `authenticatedFetch`.

## Best Practices

1. **Always validate data** before submission
2. **Handle loading states** with appropriate UI feedback
3. **Preserve rowVersion** for optimistic locking on updates
4. **Test rich text content** for proper HTML rendering
5. **Check authentication** before API calls
6. **Handle errors gracefully** with user-friendly messages
7. **Use TypeScript types** from domain models

## Debugging Tips

If you encounter issues:
1. Check browser console for API errors
2. Verify authentication token is valid
3. Check network tab for failed requests
4. Validate form data matches API expectations
5. Test Quill editor initialization
6. Verify image upload paths are correct

## Example Workflow

When implementing a new blog feature:

1. Read relevant domain model
2. Review existing blog-form.tsx implementation
3. Check API configuration
4. Test with existing data
5. Implement changes following established patterns
6. Validate with TypeScript
7. Test in development server
