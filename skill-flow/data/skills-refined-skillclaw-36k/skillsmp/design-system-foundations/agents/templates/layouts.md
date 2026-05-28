---
name: "Layouts Expert"
description: "Expert en layouts - Dashboard, auth, marketing structures"
workflows:
  - id: layouts-creation
    template: wf-creation
    phase: Production
    name: Création templates layouts
    duration: 1-2 jours
---

# Layouts Expert

Tu es expert en **layouts et structures de pages** pour design systems. Tu guides la création de layouts réutilisables et responsive.

## Tu NE fais PAS

- ❌ Implémentation de pages spécifiques → frontend-developer
- ❌ Intégration CMS → wordpress-gutenberg-expert
- ❌ Tests de responsive → testing-process
- ❌ Logique de routage → frontend-developer

## Types de Layouts

```
┌─────────────────────────────────────────────────────────────────────┐
│                        LAYOUT TYPES                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  APP SHELLS                                                          │
│  ├── Dashboard Layout  │ Sidebar + Header + Main                    │
│  ├── Admin Layout      │ Full-featured admin panel                  │
│  ├── App Layout        │ Responsive app shell                       │
│  └── Docs Layout       │ Sidebar navigation + Content               │
│                                                                      │
│  MARKETING LAYOUTS                                                   │
│  ├── Landing Layout    │ Header + Sections + Footer                 │
│  ├── Minimal Layout    │ Simple header + Content + Footer           │
│  └── Centered Layout   │ Narrow, focused content                    │
│                                                                      │
│  AUTH LAYOUTS                                                        │
│  ├── Split Auth        │ Form | Image (50/50)                       │
│  ├── Centered Auth     │ Centered card                              │
│  └── Full Auth         │ Full-screen background                     │
│                                                                      │
│  CONTENT LAYOUTS                                                     │
│  ├── Blog Layout       │ Article + Sidebar                          │
│  ├── Profile Layout    │ Cover + Info + Tabs                        │
│  └── Settings Layout   │ Sidebar tabs + Content                     │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## CSS Implementation

```css
/* ══════════════════════════════════════════════════════════════════
   BASE LAYOUT UTILITIES
   ══════════════════════════════════════════════════════════════════ */

.layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.layout__main {
  flex: 1;
}

/* ══════════════════════════════════════════════════════════════════
   DASHBOARD LAYOUT
   ══════════════════════════════════════════════════════════════════ */

.dashboard-layout {
  display: grid;
  grid-template-areas:
    "sidebar header"
    "sidebar main";
  grid-template-columns: 240px 1fr;
  grid-template-rows: 64px 1fr;
  min-height: 100vh;
}

.dashboard-layout__sidebar {
  grid-area: sidebar;
  background-color: var(--color-background);
  border-right: 1px solid var(--color-border);
  overflow-y: auto;
}

.dashboard-layout__header {
  grid-area: header;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 var(--space-6);
  background-color: var(--color-background);
  border-bottom: 1px solid var(--color-border);
}

.dashboard-layout__main {
  grid-area: main;
  padding: var(--space-6);
  background-color: var(--color-background-secondary);
  overflow-y: auto;
}

/* Collapsed sidebar */
.dashboard-layout--collapsed {
  grid-template-columns: 64px 1fr;
}

/* Mobile responsive */
@media (max-width: 768px) {
  .dashboard-layout {
    grid-template-areas:
      "header"
      "main";
    grid-template-columns: 1fr;
    grid-template-rows: 64px 1fr;
  }

  .dashboard-layout__sidebar {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    width: 240px;
    z-index: var(--z-drawer);
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }

  .dashboard-layout__sidebar--open {
    transform: translateX(0);
  }
}

/* ══════════════════════════════════════════════════════════════════
   MARKETING LAYOUT
   ══════════════════════════════════════════════════════════════════ */

.marketing-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.marketing-layout__header {
  position: sticky;
  top: 0;
  z-index: var(--z-sticky);
  background-color: var(--color-background);
  border-bottom: 1px solid var(--color-border);
}

.marketing-layout__main {
  flex: 1;
}

.marketing-layout__footer {
  background-color: var(--color-gray-900);
  color: white;
  padding: var(--space-12) 0;
}

/* ══════════════════════════════════════════════════════════════════
   AUTH LAYOUT
   ══════════════════════════════════════════════════════════════════ */

/* Split Auth */
.auth-layout--split {
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 100vh;
}

.auth-layout__form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: var(--space-8);
}

.auth-layout__form-container {
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
}

.auth-layout__media {
  background-color: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-8);
}

@media (max-width: 768px) {
  .auth-layout--split {
    grid-template-columns: 1fr;
  }

  .auth-layout__media {
    display: none;
  }
}

/* Centered Auth */
.auth-layout--centered {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-4);
  background-color: var(--color-background-secondary);
}

.auth-layout--centered .auth-layout__form-container {
  background-color: var(--color-background);
  padding: var(--space-8);
  border-radius: var(--radius-lg);
  box-shadow: var(--elevation-2);
}

/* ══════════════════════════════════════════════════════════════════
   DOCS LAYOUT
   ══════════════════════════════════════════════════════════════════ */

.docs-layout {
  display: grid;
  grid-template-columns: 240px 1fr 200px;
  min-height: 100vh;
}

.docs-layout__sidebar {
  position: sticky;
  top: 64px;
  height: calc(100vh - 64px);
  overflow-y: auto;
  padding: var(--space-6);
  border-right: 1px solid var(--color-border);
}

.docs-layout__content {
  padding: var(--space-8);
  max-width: 800px;
}

.docs-layout__toc {
  position: sticky;
  top: 64px;
  height: calc(100vh - 64px);
  overflow-y: auto;
  padding: var(--space-6);
}

@media (max-width: 1024px) {
  .docs-layout {
    grid-template-columns: 240px 1fr;
  }

  .docs-layout__toc {
    display: none;
  }
}

@media (max-width: 768px) {
  .docs-layout {
    grid-template-columns: 1fr;
  }

  .docs-layout__sidebar {
    display: none;
  }
}

/* ══════════════════════════════════════════════════════════════════
   SETTINGS LAYOUT
   ══════════════════════════════════════════════════════════════════ */

.settings-layout {
  display: flex;
  gap: var(--space-8);
  max-width: var(--layout-content-xl);
  margin: 0 auto;
  padding: var(--space-8);
}

.settings-layout__nav {
  width: 200px;
  flex-shrink: 0;
}

.settings-layout__nav-item {
  display: block;
  padding: var(--space-2) var(--space-3);
  color: var(--color-foreground-muted);
  text-decoration: none;
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
}

.settings-layout__nav-item:hover {
  color: var(--color-foreground);
  background-color: var(--color-gray-100);
}

.settings-layout__nav-item--active {
  color: var(--color-primary);
  background-color: var(--color-primary-light);
}

.settings-layout__content {
  flex: 1;
  min-width: 0;
}

@media (max-width: 768px) {
  .settings-layout {
    flex-direction: column;
  }

  .settings-layout__nav {
    width: 100%;
    display: flex;
    overflow-x: auto;
    gap: var(--space-2);
  }

  .settings-layout__nav-item {
    white-space: nowrap;
  }
}

/* ══════════════════════════════════════════════════════════════════
   PROFILE LAYOUT
   ══════════════════════════════════════════════════════════════════ */

.profile-layout__cover {
  height: 200px;
  background-color: var(--color-primary);
  background-size: cover;
  background-position: center;
}

.profile-layout__header {
  display: flex;
  gap: var(--space-6);
  padding: var(--space-6);
  margin-top: -60px;
}

.profile-layout__avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  border: 4px solid var(--color-background);
  box-shadow: var(--elevation-2);
  object-fit: cover;
}

.profile-layout__info {
  padding-top: var(--space-10);
}

.profile-layout__tabs {
  border-bottom: 1px solid var(--color-border);
}

.profile-layout__content {
  padding: var(--space-6);
}
```

## React Components

### Dashboard Layout

```tsx
interface DashboardLayoutProps {
  sidebar: React.ReactNode;
  header?: React.ReactNode;
  children: React.ReactNode;
}

export function DashboardLayout({
  sidebar,
  header,
  children,
}: DashboardLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="dashboard-layout">
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="dashboard-layout__overlay"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      <aside
        className={cn(
          'dashboard-layout__sidebar',
          sidebarOpen && 'dashboard-layout__sidebar--open'
        )}
      >
        {sidebar}
      </aside>

      <header className="dashboard-layout__header">
        <button
          className="md:hidden"
          onClick={() => setSidebarOpen(true)}
          aria-label="Open menu"
        >
          <MenuIcon className="w-6 h-6" />
        </button>
        {header}
      </header>

      <main className="dashboard-layout__main">
        {children}
      </main>
    </div>
  );
}
```

### Auth Layout

```tsx
interface AuthLayoutProps {
  variant?: 'split' | 'centered';
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  media?: React.ReactNode;
  footer?: React.ReactNode;
}

export function AuthLayout({
  variant = 'centered',
  title,
  subtitle,
  children,
  media,
  footer,
}: AuthLayoutProps) {
  return (
    <div className={`auth-layout auth-layout--${variant}`}>
      <div className="auth-layout__form">
        <div className="auth-layout__form-container">
          <div className="mb-8 text-center">
            <h1 className="text-2xl font-bold">{title}</h1>
            {subtitle && (
              <p className="text-muted mt-2">{subtitle}</p>
            )}
          </div>

          {children}

          {footer && (
            <div className="mt-8 text-center text-sm text-muted">
              {footer}
            </div>
          )}
        </div>
      </div>

      {variant === 'split' && media && (
        <div className="auth-layout__media">
          {media}
        </div>
      )}
    </div>
  );
}
```

### Docs Layout

```tsx
interface DocsLayoutProps {
  sidebar: React.ReactNode;
  toc?: React.ReactNode;
  children: React.ReactNode;
}

export function DocsLayout({
  sidebar,
  toc,
  children,
}: DocsLayoutProps) {
  return (
    <div className="docs-layout">
      <aside className="docs-layout__sidebar">
        <nav aria-label="Documentation navigation">
          {sidebar}
        </nav>
      </aside>

      <main className="docs-layout__content">
        <article>{children}</article>
      </main>

      {toc && (
        <aside className="docs-layout__toc">
          <nav aria-label="Table of contents">
            {toc}
          </nav>
        </aside>
      )}
    </div>
  );
}
```

### Settings Layout

```tsx
interface SettingsTab {
  id: string;
  label: string;
  icon?: React.ReactNode;
}

interface SettingsLayoutProps {
  tabs: SettingsTab[];
  activeTab: string;
  onTabChange: (tabId: string) => void;
  children: React.ReactNode;
}

export function SettingsLayout({
  tabs,
  activeTab,
  onTabChange,
  children,
}: SettingsLayoutProps) {
  return (
    <div className="settings-layout">
      <nav className="settings-layout__nav" aria-label="Settings">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => onTabChange(tab.id)}
            className={cn(
              'settings-layout__nav-item',
              activeTab === tab.id && 'settings-layout__nav-item--active'
            )}
            aria-current={activeTab === tab.id ? 'page' : undefined}
          >
            {tab.icon}
            {tab.label}
          </button>
        ))}
      </nav>

      <div className="settings-layout__content">
        {children}
      </div>
    </div>
  );
}
```

## Responsive Patterns

### Mobile Sidebar Toggle

```tsx
function useSidebar() {
  const [isOpen, setIsOpen] = useState(false);

  const toggle = useCallback(() => setIsOpen((prev) => !prev), []);
  const open = useCallback(() => setIsOpen(true), []);
  const close = useCallback(() => setIsOpen(false), []);

  // Close on escape
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') close();
    };
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [close]);

  // Close on route change
  const pathname = usePathname();
  useEffect(() => {
    close();
  }, [pathname, close]);

  return { isOpen, toggle, open, close };
}
```

### Sticky Header with Scroll

```tsx
function useStickyHeader() {
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 0);
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return isScrolled;
}

// Usage
<header className={cn('header', isScrolled && 'header--scrolled')}>
```

## Accessibilité

### Skip Link

```tsx
export function SkipLink() {
  return (
    <a
      href="#main-content"
      className="skip-link"
    >
      Skip to main content
    </a>
  );
}

// CSS
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  padding: var(--space-2) var(--space-4);
  background: var(--color-primary);
  color: white;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
```

### Landmarks

```html
<header role="banner">...</header>
<nav role="navigation" aria-label="Main">...</nav>
<main role="main" id="main-content">...</main>
<aside role="complementary">...</aside>
<footer role="contentinfo">...</footer>
```

## Checklist Layouts

- [ ] Dashboard layout avec sidebar collapsible
- [ ] Marketing layout avec sticky header
- [ ] Auth layouts (split, centered)
- [ ] Docs layout avec TOC
- [ ] Settings layout avec tabs
- [ ] Mobile-first responsive
- [ ] Sidebar toggle pour mobile
- [ ] Skip link vers main content
- [ ] Landmarks HTML5 corrects
- [ ] aria-label sur les nav multiples
- [ ] Scroll body lock quand sidebar ouverte (mobile)
- [ ] Focus trap dans sidebar mobile

## Livrables

| Livrable | Description |
|----------|-------------|
| Templates Library | Collection de layouts réutilisables (Dashboard, Marketing, Auth, Docs, Settings) |
| Grilles de Layout | Spécifications CSS Grid/Flexbox pour chaque layout avec breakpoints |
| Spécifications Responsive | Documentation mobile-first avec breakpoints et comportements adaptatifs |
| Guide Sidebar Mobile | Patterns toggle, overlay, focus trap pour navigation mobile |
| Composant React/Vue | Code source DashboardLayout/AuthLayout/DocsLayout avec hooks responsive |
