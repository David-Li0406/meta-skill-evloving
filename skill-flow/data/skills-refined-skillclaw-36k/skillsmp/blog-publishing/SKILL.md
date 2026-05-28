---
name: blog-publishing
description: Handles the end-to-end workflow for publishing blog posts on THE LOST+UNFOUNDS. Use this when creating new posts or updating existing ones via SQL scripts.
---

# Blog Publishing & Styling Skill

This skill ensures that every blog post is published correctly and adheres to the strict "Noir" aesthetic and styling rules.

## Part 1: The 6-Step Publishing Workflow

1. **Create SQL File**: Create `sql/create-blog-post-[slug].sql` and `public/sql/create-blog-post-[slug].sql`.
    - **Pattern**: Must use `DECLARE existing_post_id UUID;` and a check-and-insert/update block.
    - **Critical**: Never use `ON CONFLICT (slug)`.
2. **Update SQL.tsx**: Add fetch code and register in the `allScripts` array in `src/pages/SQL.tsx`.
3. **Update API Endpoint**: Add the new SQL file path to `SQL_FILES` in `api/sql/latest.ts`.
4. **Commit Changes**: Stage and commit with a descriptive message.
5. **Merge to Production**: Checkout `main`, pull, merge the branch, and push.
6. **Verify Deployment**:
    - URL: `https://www.thelostandunfounds.com/sql/create-blog-post-[slug].sql`
    - Page: `https://www.thelostandunfounds.com/sql`

## Part 2: Content Styling & Formatting

### 1. Text Alignment (Critical)
- **NEVER** use `text-center` or `text-justify` for body content.
- **ALWAYS** use `text-left`. Applies to paragraphs, analysis components, and headers.

### 2. Book Title Formatting
- **Bolding**: All book titles must be **bold**.
- **Case Preservation**: Titles must preserve the author's original case.
- **Linking**: Max 2 links per book. Linked titles must be **underlined**.

### 3. Disclosure & Special Characters
- **Disclosure**: Author names must be **UPPERCASE BOLD**. Disclosure text can be justified.
- **Remove "⸻"**: Do not use the long dash character. Use proper paragraph spacing.

## SQL Template Pattern
```sql
DO $$
DECLARE
    existing_post_id UUID;
BEGIN
    SELECT id INTO existing_post_id FROM blog_posts WHERE slug = '[slug]' LIMIT 1;
    IF existing_post_id IS NOT NULL THEN
        UPDATE blog_posts SET ... WHERE id = existing_post_id;
    ELSE
        INSERT INTO blog_posts (...) VALUES (...);
    END IF;
END $$;
```
