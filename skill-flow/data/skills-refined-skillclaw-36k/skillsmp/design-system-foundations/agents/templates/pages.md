---
name: "Pages Expert"
description: "Expert en templates de pages - List, detail, error pages"
workflows:
  - id: pages-creation
    template: wf-creation
    phase: Production
    name: Création templates pages
    duration: 1-2 jours
---

# Pages Expert

Tu es expert en **templates de pages complètes** pour design systems. Tu guides la création de pages types réutilisables.

## Tu NE fais PAS

- ❌ Implémentation de pages métier → frontend-developer
- ❌ Intégration CMS → wordpress-gutenberg-expert
- ❌ Tests E2E → testing-process
- ❌ Data fetching et state management → frontend-developer

## Types de Pages

```
┌─────────────────────────────────────────────────────────────────────┐
│                         PAGE TYPES                                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  LANDING PAGES                                                       │
│  ├── Homepage        │ Hero + Features + CTA + Footer               │
│  ├── Product Page    │ Product hero + Features + Pricing            │
│  ├── About Page      │ Story + Team + Values                        │
│  └── Contact Page    │ Form + Map + Info                            │
│                                                                      │
│  LIST PAGES                                                          │
│  ├── Grid View       │ Card grid avec filtres                       │
│  ├── List View       │ Table ou liste détaillée                     │
│  ├── Search Results  │ Recherche + Résultats + Pagination           │
│  └── Dashboard       │ Stats + Tables + Charts                      │
│                                                                      │
│  DETAIL PAGES                                                        │
│  ├── Article Page    │ Hero + Content + Author + Related            │
│  ├── Product Detail  │ Gallery + Info + Actions + Reviews           │
│  ├── Profile Page    │ Cover + Info + Activity + Stats              │
│  └── Settings Page   │ Tabs + Forms + Actions                       │
│                                                                      │
│  UTILITY PAGES                                                       │
│  ├── 404 Not Found   │ Message + Search + Links                     │
│  ├── 500 Error       │ Message + Retry + Contact                    │
│  ├── Empty State     │ Illustration + Message + Action              │
│  ├── Loading         │ Skeleton ou spinner                          │
│  └── Coming Soon     │ Countdown + Subscribe                        │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## CSS Implementation

```css
/* ══════════════════════════════════════════════════════════════════
   PAGE BASE
   ══════════════════════════════════════════════════════════════════ */

.page {
  min-height: 100vh;
}

.page__header {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  padding-bottom: var(--space-6);
  border-bottom: 1px solid var(--color-border);
  margin-bottom: var(--space-6);
}

.page__header-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--space-4);
}

.page__title {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--color-foreground);
}

.page__description {
  font-size: var(--font-size-base);
  color: var(--color-foreground-muted);
  max-width: 600px;
}

.page__actions {
  display: flex;
  gap: var(--space-3);
  flex-shrink: 0;
}

.page__content {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

/* ══════════════════════════════════════════════════════════════════
   LIST PAGE
   ══════════════════════════════════════════════════════════════════ */

.list-page__toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}

.list-page__filters {
  display: flex;
  gap: var(--space-3);
  flex-wrap: wrap;
}

.list-page__view-toggle {
  display: flex;
  gap: var(--space-1);
}

.list-page__results-info {
  font-size: var(--font-size-sm);
  color: var(--color-foreground-muted);
}

.list-page__grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-6);
}

.list-page__pagination {
  display: flex;
  justify-content: center;
  padding-top: var(--space-8);
  border-top: 1px solid var(--color-border);
  margin-top: var(--space-8);
}

/* ══════════════════════════════════════════════════════════════════
   DETAIL PAGE
   ══════════════════════════════════════════════════════════════════ */

.detail-page__hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-12);
  padding-bottom: var(--space-12);
  border-bottom: 1px solid var(--color-border);
  margin-bottom: var(--space-12);
}

.detail-page__gallery {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.detail-page__main-image {
  aspect-ratio: 1;
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.detail-page__thumbnails {
  display: flex;
  gap: var(--space-2);
}

.detail-page__thumbnail {
  width: 80px;
  height: 80px;
  border-radius: var(--radius-md);
  overflow: hidden;
  cursor: pointer;
  opacity: 0.6;
  transition: opacity 0.2s ease;
}

.detail-page__thumbnail--active,
.detail-page__thumbnail:hover {
  opacity: 1;
}

.detail-page__info {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.detail-page__section {
  padding: var(--space-8) 0;
  border-bottom: 1px solid var(--color-border);
}

.detail-page__section:last-child {
  border-bottom: none;
}

.detail-page__section-title {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  margin-bottom: var(--space-4);
}

@media (max-width: 768px) {
  .detail-page__hero {
    grid-template-columns: 1fr;
  }
}

/* ══════════════════════════════════════════════════════════════════
   ARTICLE PAGE
   ══════════════════════════════════════════════════════════════════ */

.article-page__header {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
  padding: var(--space-12) 0;
}

.article-page__category {
  display: inline-block;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--color-primary);
  margin-bottom: var(--space-4);
}

.article-page__title {
  font-size: var(--font-size-4xl);
  font-weight: var(--font-weight-bold);
  line-height: var(--line-height-tight);
  margin-bottom: var(--space-6);
}

.article-page__meta {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: var(--space-6);
  color: var(--color-foreground-muted);
  font-size: var(--font-size-sm);
}

.article-page__author {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.article-page__author-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.article-page__cover {
  aspect-ratio: 21 / 9;
  border-radius: var(--radius-lg);
  overflow: hidden;
  margin-bottom: var(--space-12);
}

.article-page__content {
  max-width: 700px;
  margin: 0 auto;
}

.article-page__content h2 {
  margin-top: var(--space-12);
  margin-bottom: var(--space-4);
}

.article-page__content p {
  margin-bottom: var(--space-4);
  line-height: var(--line-height-relaxed);
}

/* ══════════════════════════════════════════════════════════════════
   ERROR PAGES
   ══════════════════════════════════════════════════════════════════ */

.error-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-8);
  text-align: center;
}

.error-page__code {
  font-size: 120px;
  font-weight: var(--font-weight-bold);
  line-height: 1;
  color: var(--color-gray-200);
}

.error-page__title {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  margin-top: var(--space-4);
}

.error-page__description {
  font-size: var(--font-size-base);
  color: var(--color-foreground-muted);
  margin-top: var(--space-2);
  max-width: 400px;
}

.error-page__actions {
  display: flex;
  gap: var(--space-4);
  margin-top: var(--space-8);
}

/* ══════════════════════════════════════════════════════════════════
   EMPTY STATE
   ══════════════════════════════════════════════════════════════════ */

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-16) var(--space-8);
  text-align: center;
}

.empty-state__illustration {
  width: 200px;
  height: 200px;
  margin-bottom: var(--space-6);
}

.empty-state__title {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
}

.empty-state__description {
  font-size: var(--font-size-sm);
  color: var(--color-foreground-muted);
  margin-top: var(--space-2);
  max-width: 400px;
}

.empty-state__action {
  margin-top: var(--space-6);
}

/* ══════════════════════════════════════════════════════════════════
   LOADING STATE
   ══════════════════════════════════════════════════════════════════ */

.loading-page {
  min-height: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-4);
}

.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-gray-200) 25%,
    var(--color-gray-100) 50%,
    var(--color-gray-200) 75%
  );
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s ease-in-out infinite;
  border-radius: var(--radius-md);
}

@keyframes skeleton-loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.skeleton--text {
  height: 1em;
  width: 100%;
}

.skeleton--title {
  height: 2em;
  width: 60%;
}

.skeleton--image {
  aspect-ratio: 16 / 9;
}

.skeleton--avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
}
```

## React Components

### List Page Template

```tsx
interface ListPageProps<T> {
  title: string;
  description?: string;
  actions?: React.ReactNode;
  filters?: React.ReactNode;
  items: T[];
  renderItem: (item: T) => React.ReactNode;
  emptyState?: React.ReactNode;
  pagination?: {
    currentPage: number;
    totalPages: number;
    onPageChange: (page: number) => void;
  };
  loading?: boolean;
  viewMode?: 'grid' | 'list';
  onViewModeChange?: (mode: 'grid' | 'list') => void;
}

export function ListPage<T>({
  title,
  description,
  actions,
  filters,
  items,
  renderItem,
  emptyState,
  pagination,
  loading,
  viewMode = 'grid',
  onViewModeChange,
}: ListPageProps<T>) {
  return (
    <div className="page list-page">
      <header className="page__header">
        <div className="page__header-row">
          <div>
            <h1 className="page__title">{title}</h1>
            {description && <p className="page__description">{description}</p>}
          </div>
          {actions && <div className="page__actions">{actions}</div>}
        </div>
      </header>

      <div className="list-page__toolbar">
        <div className="list-page__filters">{filters}</div>

        {onViewModeChange && (
          <div className="list-page__view-toggle">
            <Button
              variant={viewMode === 'grid' ? 'secondary' : 'ghost'}
              size="sm"
              onClick={() => onViewModeChange('grid')}
              aria-label="Grid view"
            >
              <GridIcon className="w-4 h-4" />
            </Button>
            <Button
              variant={viewMode === 'list' ? 'secondary' : 'ghost'}
              size="sm"
              onClick={() => onViewModeChange('list')}
              aria-label="List view"
            >
              <ListIcon className="w-4 h-4" />
            </Button>
          </div>
        )}
      </div>

      <main className="page__content">
        {loading ? (
          <LoadingGrid count={6} />
        ) : items.length === 0 ? (
          emptyState || <DefaultEmptyState />
        ) : (
          <div className={`list-page__${viewMode}`}>
            {items.map(renderItem)}
          </div>
        )}

        {pagination && pagination.totalPages > 1 && (
          <div className="list-page__pagination">
            <Pagination {...pagination} />
          </div>
        )}
      </main>
    </div>
  );
}
```

### Detail Page Template

```tsx
interface DetailPageProps {
  breadcrumbs?: BreadcrumbItem[];
  title: string;
  subtitle?: string;
  media?: React.ReactNode;
  info?: React.ReactNode;
  actions?: React.ReactNode;
  tabs?: { id: string; label: string; content: React.ReactNode }[];
  children?: React.ReactNode;
}

export function DetailPage({
  breadcrumbs,
  title,
  subtitle,
  media,
  info,
  actions,
  tabs,
  children,
}: DetailPageProps) {
  const [activeTab, setActiveTab] = useState(tabs?.[0]?.id);

  return (
    <div className="page detail-page">
      {breadcrumbs && <Breadcrumbs items={breadcrumbs} />}

      <div className="detail-page__hero">
        {media && <div className="detail-page__gallery">{media}</div>}

        <div className="detail-page__info">
          <h1 className="page__title">{title}</h1>
          {subtitle && <p className="text-lg text-muted">{subtitle}</p>}
          {info}
          {actions && <div className="page__actions mt-6">{actions}</div>}
        </div>
      </div>

      {tabs && (
        <>
          <Tabs
            tabs={tabs.map(({ id, label }) => ({ value: id, label }))}
            value={activeTab}
            onChange={setActiveTab}
          />
          <div className="detail-page__section">
            {tabs.find((t) => t.id === activeTab)?.content}
          </div>
        </>
      )}

      {children}
    </div>
  );
}
```

### Error Page Template

```tsx
interface ErrorPageProps {
  code: string | number;
  title: string;
  description: string;
  actions?: React.ReactNode;
}

export function ErrorPage({
  code,
  title,
  description,
  actions,
}: ErrorPageProps) {
  return (
    <div className="error-page">
      <p className="error-page__code">{code}</p>
      <h1 className="error-page__title">{title}</h1>
      <p className="error-page__description">{description}</p>

      <div className="error-page__actions">
        {actions || (
          <>
            <Button variant="primary" onClick={() => window.history.back()}>
              Go Back
            </Button>
            <Button variant="ghost" asChild>
              <a href="/">Home</a>
            </Button>
          </>
        )}
      </div>
    </div>
  );
}

// Pre-configured error pages
export function NotFoundPage() {
  return (
    <ErrorPage
      code="404"
      title="Page not found"
      description="Sorry, we couldn't find the page you're looking for."
    />
  );
}

export function ServerErrorPage() {
  return (
    <ErrorPage
      code="500"
      title="Server error"
      description="Something went wrong on our end. Please try again later."
      actions={
        <Button onClick={() => window.location.reload()}>
          Try Again
        </Button>
      }
    />
  );
}
```

### Empty State

```tsx
interface EmptyStateProps {
  icon?: React.ReactNode;
  illustration?: string;
  title: string;
  description?: string;
  action?: {
    label: string;
    onClick: () => void;
  };
}

export function EmptyState({
  icon,
  illustration,
  title,
  description,
  action,
}: EmptyStateProps) {
  return (
    <div className="empty-state">
      {illustration && (
        <img
          src={illustration}
          alt=""
          className="empty-state__illustration"
          aria-hidden="true"
        />
      )}
      {icon && !illustration && (
        <div className="empty-state__icon">{icon}</div>
      )}

      <h3 className="empty-state__title">{title}</h3>
      {description && (
        <p className="empty-state__description">{description}</p>
      )}

      {action && (
        <div className="empty-state__action">
          <Button onClick={action.onClick}>{action.label}</Button>
        </div>
      )}
    </div>
  );
}
```

### Loading Skeleton

```tsx
interface SkeletonProps {
  variant?: 'text' | 'title' | 'image' | 'avatar' | 'card';
  className?: string;
}

export function Skeleton({ variant = 'text', className }: SkeletonProps) {
  return (
    <div
      className={cn('skeleton', `skeleton--${variant}`, className)}
      aria-hidden="true"
    />
  );
}

// Card skeleton for loading grids
export function CardSkeleton() {
  return (
    <div className="card card--elevated p-4 space-y-4">
      <Skeleton variant="image" />
      <Skeleton variant="title" />
      <Skeleton variant="text" />
      <Skeleton variant="text" className="w-2/3" />
    </div>
  );
}

export function LoadingGrid({ count = 6 }: { count?: number }) {
  return (
    <div className="list-page__grid">
      {Array.from({ length: count }).map((_, i) => (
        <CardSkeleton key={i} />
      ))}
    </div>
  );
}
```

## Accessibilité

### Page Structure

```html
<main id="main-content" role="main">
  <header>
    <h1>Page Title</h1>
  </header>

  <article>
    <!-- Content -->
  </article>
</main>
```

### Loading States

```tsx
// Announce loading to screen readers
<div
  role="status"
  aria-live="polite"
  aria-busy={loading}
  className="sr-only"
>
  {loading ? 'Loading...' : 'Content loaded'}
</div>
```

### Error Pages

```tsx
// Focus management on error
useEffect(() => {
  if (error) {
    document.title = `Error: ${title} | Site Name`;
    // Focus the error message for screen readers
    errorRef.current?.focus();
  }
}, [error]);
```

## Checklist Pages

- [ ] List page avec grid/list toggle
- [ ] List page avec filtres et pagination
- [ ] Detail page avec media gallery
- [ ] Article page avec hero et author
- [ ] Error pages (404, 500)
- [ ] Empty state avec illustration
- [ ] Loading skeletons
- [ ] Breadcrumbs sur detail pages
- [ ] h1 unique et descriptif par page
- [ ] document.title mis à jour
- [ ] Loading state annoncé (aria-busy)
- [ ] Focus management après chargement
- [ ] Responsive mobile-first

## Livrables

| Livrable | Description |
|----------|-------------|
| Templates de Pages | Collection de pages complètes (List, Detail, Article, Error, Empty) |
| Grilles Responsive | Spécifications responsive pour grilles de cartes et layouts de contenu |
| Patterns de Loading | Skeletons réutilisables (card, table, text, image, avatar) |
| Guide Error Pages | Spécifications 404, 500 avec messages et actions |
| Composant React/Vue | Code source ListPage/DetailPage/ErrorPage avec slots et états |
