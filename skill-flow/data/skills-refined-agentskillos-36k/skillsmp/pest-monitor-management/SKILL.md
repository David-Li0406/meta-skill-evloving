---
name: Pest Monitor Management
description: Comprehensive guide for maintaining and extending the National Rice Pest Monitoring Network.
---

# Pest Monitor Management Skill

This skill provides the necessary context and instructions for developers or agents working on the **PestMonitor TH** project.

## 🏗 Core Architecture

The project is built with **Next.js (App Router)** and **Supabase**. It follows a community-driven data integrity model where public reports are verified by agricultural experts.

## 🗄 Database Management (Supabase)

The database consist of several tables in the `public` schema. When making changes, reference the existing SQL files in the `supabase/` directory.

### Key Tables

- `profiles`: Extends auth users with `user_role` (admin, expert, general).
- `reports`: Stores pest sightings. Includes `verification_status` (pending, verified, rejected).
- `articles`: Stores Alerts and News content.
- `expert_applications`: Manages the workflow for users applying for expert status.

### RLS Policies

- `profiles`: Users can view/update only their own profile.
- `reports`: Publicly readable (`SELECT`). Anyone can `INSERT` (anonymous allowed). Only owner can `UPDATE`/`DELETE`.
- `articles`: Only published articles are public. Drafts/Creation restricted to `expert` or `admin`.

## 👮 Role-Based Access Control (RBAC)

- **General User**: Can view maps, news, and submit reports.
- **Expert**: Can verify pending reports and publish Alerts/News.
- **Admin**: Can manage users and approve Expert applications.

## 📱 Mobile-First Development

The application prioritizes field usage.

- **Testing**: Use Browser DevTools (`F12` -> Toggle Device Toolbar) or test on a physical device using the local network IP (e.g., `http://192.168.1.119:3001`).
- **UI Patterns**: Use the blue stacked-menu drawer for mobile navigation and user icons instead of text for login/profile.

## 🚦 Key Development Workflows

1. **Adding a New Page**: Ensure the page is added to the `DashboardLayout` sidebar and follows the `globals.css` design system.
2. **Database Updates**:
   - Write migrations in `supabase/*.sql`.
   - Apply migrations using `supabase-mcp-server`.
   - Update types if necessary.
3. **Internal Testing**: Always verify build status using `npm run build` after major UI or logic changes.

## 🎨 Styling Guidelines

- Use CSS Variables defined in `src/app/globals.css`.
- Maintain the green primary color (`#16A34A`) for main actions and the blue color (`#337ab7`) for navigational/informational elements.
- Ensure all interactive elements have hover states and transitions.
