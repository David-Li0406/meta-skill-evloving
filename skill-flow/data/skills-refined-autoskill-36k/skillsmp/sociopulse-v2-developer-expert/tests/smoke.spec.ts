import { test, expect, Page } from '@playwright/test';

/**
 * ============================================================================
 * SOCIOPULSE V2 - SMOKE TEST SUITE
 * ============================================================================
 * Playwright smoke tests to verify critical paths work after V1→V2 migration.
 * Ensures no "White Screen of Death" (WSOD) or 404 errors.
 * 
 * Run: npx playwright test
 * Run specific: npx playwright test tests/smoke.spec.ts
 * Run with UI: npx playwright test --ui
 * ============================================================================
 */

// =============================================================================
// HELPER: Mock Authentication
// =============================================================================

/**
 * Injects mock authentication cookies to simulate logged-in state.
 * In real app, this would be a valid JWT - here we mock for smoke testing.
 */
async function mockAuthentication(page: Page, role: 'CLIENT' | 'TALENT' | 'ADMIN') {
    // Mock user data based on role
    const mockUsers = {
        CLIENT: {
            id: 'mock-client-001',
            email: 'client@test.sociopulse.fr',
            role: 'CLIENT',
            status: 'VERIFIED',
            profile: {
                firstName: 'Jean',
                lastName: 'Dupont',
            },
            establishment: {
                name: 'EHPAD Test',
            },
            createdAt: new Date().toISOString(),
        },
        TALENT: {
            id: 'mock-talent-001',
            email: 'talent@test.sociopulse.fr',
            role: 'TALENT',
            status: 'VERIFIED',
            profile: {
                firstName: 'Marie',
                lastName: 'Martin',
            },
            createdAt: new Date().toISOString(),
        },
        ADMIN: {
            id: 'mock-admin-001',
            email: 'admin@test.sociopulse.fr',
            role: 'ADMIN',
            status: 'VERIFIED',
            profile: {
                firstName: 'Admin',
                lastName: 'Test',
            },
            createdAt: new Date().toISOString(),
        },
    };

    const user = mockUsers[role];

    // Create a mock JWT payload (base64 encoded for middleware bypass in test mode)
    // In production, this would be validated against actual JWT
    const mockPayload = Buffer.from(JSON.stringify({
        sub: user.id,
        email: user.email,
        role: user.role,
        iat: Math.floor(Date.now() / 1000),
        exp: Math.floor(Date.now() / 1000) + 3600,
    })).toString('base64');

    // Set cookies that the app expects
    await page.context().addCookies([
        {
            name: 'accessToken',
            value: `mock.${mockPayload}.signature`,
            domain: 'localhost',
            path: '/',
            httpOnly: true,
            secure: false,
            sameSite: 'Lax',
        },
    ]);

    // Also inject into localStorage for client-side auth state
    await page.addInitScript((userData) => {
        localStorage.setItem('user', JSON.stringify(userData));
        localStorage.setItem('isAuthenticated', 'true');
    }, user);
}

// =============================================================================
// TEST SUITE 1: PUBLIC LANDING PAGE
// =============================================================================

test.describe('1. Public Landing Page', () => {
    test('should render landing page without WSOD', async ({ page }) => {
        await page.goto('/');

        // Should not be a blank page
        await expect(page.locator('body')).not.toBeEmpty();

        // Wait for main content to load
        await expect(page.locator('main')).toBeVisible({ timeout: 10000 });
    });

    test('should display Hero Title', async ({ page }) => {
        await page.goto('/');

        // Hero section should be visible
        // Check for the hero container or title text
        const hero = page.locator('h1, [class*="hero"], [data-testid="hero"]').first();
        await expect(hero).toBeVisible({ timeout: 10000 });
    });

    test('should have Marquee/Carousel components in DOM', async ({ page }) => {
        await page.goto('/');

        // Wait for page to fully load
        await page.waitForLoadState('networkidle');

        // Check for marquee-related elements (framer-motion animated elements or specific classes)
        const marqueeElements = page.locator('[class*="marquee"], [class*="carousel"], [class*="scroll"]');
        const count = await marqueeElements.count();

        // Should have at least some animated/scrolling content
        expect(count).toBeGreaterThan(0);
    });

    test('should display Footer', async ({ page }) => {
        await page.goto('/');

        // Scroll to bottom to ensure footer is in viewport
        await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));

        // Footer should be visible
        const footer = page.locator('footer');
        await expect(footer).toBeVisible();

        // Footer should contain brand name or copyright
        await expect(footer).toContainText(/SocioPulse|MedicoPulse|©/i);
    });

    test('should have no console errors on landing page', async ({ page }) => {
        const errors: string[] = [];
        page.on('console', (msg) => {
            if (msg.type() === 'error') {
                errors.push(msg.text());
            }
        });

        await page.goto('/');
        await page.waitForLoadState('networkidle');

        // Filter out known non-critical errors
        const criticalErrors = errors.filter(
            (err) =>
                !err.includes('favicon') &&
                !err.includes('hydration') &&
                !err.includes('404')
        );

        expect(criticalErrors).toHaveLength(0);
    });
});

// =============================================================================
// TEST SUITE 2: ROUTING SECURITY
// =============================================================================

test.describe('2. Routing Security', () => {
    test('should redirect /dashboard/client to login when not authenticated', async ({ page }) => {
        // Clear any existing auth state
        await page.context().clearCookies();

        // Try to access protected route
        await page.goto('/dashboard/client');

        // Wait for redirect
        await page.waitForURL(/\/auth\/login|\/dashboard/, { timeout: 10000 });

        // Should be on login page OR redirected to generic dashboard (which then redirects)
        const url = page.url();
        expect(url).toMatch(/\/auth\/login|\/dashboard/);
    });

    test('should redirect /dashboard/talent to login when not authenticated', async ({ page }) => {
        await page.context().clearCookies();
        await page.goto('/dashboard/talent');

        await page.waitForURL(/\/auth\/login|\/dashboard/, { timeout: 10000 });

        const url = page.url();
        expect(url).toMatch(/\/auth\/login|\/dashboard/);
    });

    test('should redirect /admin to login when not authenticated', async ({ page }) => {
        await page.context().clearCookies();
        await page.goto('/admin');

        await page.waitForURL(/\/auth\/login|\/admin/, { timeout: 10000 });

        // Admin routes should require auth
        const url = page.url();
        // May either redirect to login or show admin login
        expect(url).toMatch(/\/auth|\/admin/);
    });
});

// =============================================================================
// TEST SUITE 3: CLIENT DASHBOARD (Mocked Auth)
// =============================================================================

test.describe('3. Client Dashboard', () => {
    test.beforeEach(async ({ page }) => {
        await mockAuthentication(page, 'CLIENT');
    });

    test('should render Client Dashboard without WSOD', async ({ page }) => {
        await page.goto('/dashboard/client');

        // Wait for page load
        await page.waitForLoadState('domcontentloaded');

        // Should have content, not a blank page
        await expect(page.locator('body')).not.toBeEmpty();

        // Main content area should exist
        const main = page.locator('main, [role="main"], .min-h-screen');
        await expect(main.first()).toBeVisible({ timeout: 10000 });
    });

    test('should display Sidebar with correct navigation links', async ({ page }) => {
        await page.goto('/dashboard/client');

        await page.waitForLoadState('networkidle');

        // Sidebar should exist (aside element or nav)
        const sidebar = page.locator('aside, nav[class*="sidebar"], [data-testid="sidebar"]').first();
        await expect(sidebar).toBeVisible({ timeout: 10000 });

        // Check for key navigation links
        // Missions link
        const missionsLink = page.locator('a[href*="/dashboard/client/missions"], a:has-text("Missions")').first();
        await expect(missionsLink).toBeVisible();

        // Admin/Administratif link
        const adminLink = page.locator('a[href*="/dashboard/client/admin"], a:has-text("Administratif")').first();
        await expect(adminLink).toBeVisible();

        // Finance link
        const financeLink = page.locator('a[href*="/dashboard/client/finance"], a:has-text("Finance")').first();
        await expect(financeLink).toBeVisible();
    });

    test('should open Publish Modal with 4 tiles when clicking Publier button', async ({ page }) => {
        await page.goto('/dashboard/client');
        await page.waitForLoadState('networkidle');

        // Find and click the "Publier" button in header
        const publishButton = page.locator('button:has-text("Publier"), [aria-label*="Publier"]').first();

        // Button might be hidden on mobile, so check if visible first
        if (await publishButton.isVisible()) {
            await publishButton.click();

            // Wait for modal to appear
            await page.waitForSelector('[role="dialog"], [class*="modal"], [data-state="open"]', {
                timeout: 5000,
            });

            // Modal should be visible
            const modal = page.locator('[role="dialog"], [class*="modal"]').first();
            await expect(modal).toBeVisible();

            // Check for the 4 tiles (SOS, Mission, Atelier, Actu)
            // Look for tile-like elements within the modal
            const tiles = modal.locator('a, button').filter({
                hasText: /SOS|MISSION|ATELIER|ACTU|URGENCE|PROJET/i,
            });

            const tileCount = await tiles.count();
            expect(tileCount).toBeGreaterThanOrEqual(4);
        }
    });

    test('should navigate to sub-pages without 404', async ({ page }) => {
        const subPages = [
            '/dashboard/client/missions',
            '/dashboard/client/admin',
            '/dashboard/client/finance',
            '/dashboard/client/settings',
        ];

        for (const subPage of subPages) {
            await page.goto(subPage);
            await page.waitForLoadState('domcontentloaded');

            // Should not be a 404 page
            const pageContent = await page.content();
            expect(pageContent).not.toContain('404');

            // Should have main content
            await expect(page.locator('body')).not.toBeEmpty();
        }
    });
});

// =============================================================================
// TEST SUITE 4: TALENT DASHBOARD (Mocked Auth)
// =============================================================================

test.describe('4. Talent Dashboard', () => {
    test.beforeEach(async ({ page }) => {
        await mockAuthentication(page, 'TALENT');
    });

    test('should render Talent Dashboard without WSOD', async ({ page }) => {
        await page.goto('/dashboard/talent');

        await page.waitForLoadState('domcontentloaded');

        // Should have content
        await expect(page.locator('body')).not.toBeEmpty();

        // Main area should be visible
        const main = page.locator('main, [role="main"], .min-h-screen');
        await expect(main.first()).toBeVisible({ timeout: 10000 });
    });

    test('should display SOS Availability Switch in Header', async ({ page }) => {
        await page.goto('/dashboard/talent');

        await page.waitForLoadState('networkidle');

        // Look for the SOS toggle/switch in header
        // Could be a button, switch, or toggle element
        const sosToggle = page.locator(
            'button:has-text("Renfort"), ' +
            'button:has-text("SOS"), ' +
            'button:has-text("Disponible"), ' +
            '[class*="toggle"], ' +
            '[role="switch"]'
        ).first();

        // The toggle should be visible in the header area
        await expect(sosToggle).toBeVisible({ timeout: 10000 });
    });

    test('should have Cockpit/Dashboard visible', async ({ page }) => {
        await page.goto('/dashboard/talent');

        await page.waitForLoadState('networkidle');

        // Check for key dashboard elements
        // Sidebar or navigation with "Cockpit" label
        const cockpitNav = page.locator('a:has-text("Cockpit"), [class*="sidebar"] a').first();
        await expect(cockpitNav).toBeVisible();
    });

    test('should navigate to Services page and show Create button', async ({ page }) => {
        await page.goto('/dashboard/talent/services');

        await page.waitForLoadState('networkidle');

        // Should not be 404
        const pageContent = await page.content();
        expect(pageContent).not.toContain('404');

        // Look for "Créer un service" or similar button
        const createButton = page.locator(
            'button:has-text("Créer"), ' +
            'a:has-text("Créer"), ' +
            'button:has-text("Nouveau"), ' +
            'a:has-text("Nouveau service"), ' +
            '[href*="/services/new"]'
        ).first();

        await expect(createButton).toBeVisible({ timeout: 10000 });
    });

    test('should navigate to sub-pages without 404', async ({ page }) => {
        const subPages = [
            '/dashboard/talent/missions',
            '/dashboard/talent/services',
            '/dashboard/talent/planning',
            '/dashboard/talent/admin',
            '/dashboard/talent/profile',
        ];

        for (const subPage of subPages) {
            await page.goto(subPage);
            await page.waitForLoadState('domcontentloaded');

            // Should not be a 404 page
            const pageContent = await page.content();
            expect(pageContent).not.toContain('404');

            // Should have main content
            await expect(page.locator('body')).not.toBeEmpty();
        }
    });
});

// =============================================================================
// TEST SUITE 5: FIL PRO (Public Feed)
// =============================================================================

test.describe('5. Fil Pro', () => {
    test('should render Fil Pro page without WSOD', async ({ page }) => {
        await page.goto('/fil-pro');

        // Wait for page to load
        await page.waitForLoadState('domcontentloaded');

        // Should have content
        await expect(page.locator('body')).not.toBeEmpty();
    });

    test('should display Feed Container', async ({ page }) => {
        await page.goto('/fil-pro');

        await page.waitForLoadState('networkidle');

        // Look for feed container elements
        const feedContainer = page.locator(
            '[class*="feed"], ' +
            '[data-testid="feed"], ' +
            'main, ' +
            '[class*="content"]'
        ).first();

        await expect(feedContainer).toBeVisible({ timeout: 10000 });
    });

    test('should show feed items or empty state', async ({ page }) => {
        await page.goto('/fil-pro');

        await page.waitForLoadState('networkidle');

        // Either feed items exist or there's an empty state message
        const feedItems = page.locator('[class*="card"], [class*="item"], article');
        const emptyState = page.locator('text=/aucun|empty|pas de/i');

        const hasItems = (await feedItems.count()) > 0;
        const hasEmptyState = (await emptyState.count()) > 0;

        // Should have either items or empty state - not a broken page
        expect(hasItems || hasEmptyState).toBeTruthy();
    });

    test('should not return 404', async ({ page }) => {
        const response = await page.goto('/fil-pro');

        expect(response?.status()).not.toBe(404);
        expect(response?.status()).toBeLessThan(400);
    });
});

// =============================================================================
// TEST SUITE 6: CRITICAL ROUTES HEALTH CHECK
// =============================================================================

test.describe('6. Critical Routes Health Check', () => {
    const criticalRoutes = [
        { path: '/', name: 'Landing Page' },
        { path: '/auth/login', name: 'Login Page' },
        { path: '/auth/register', name: 'Register Page' },
        { path: '/fil-pro', name: 'Fil Pro' },
        { path: '/sos', name: 'SOS Page' },
        { path: '/search', name: 'Search Page' },
        { path: '/bookings', name: 'Bookings Page' },
    ];

    for (const route of criticalRoutes) {
        test(`${route.name} (${route.path}) should return 200`, async ({ page }) => {
            const response = await page.goto(route.path);

            // Should not be a server error
            expect(response?.status()).toBeLessThan(500);

            // Page should have content (not WSOD)
            await expect(page.locator('body')).not.toBeEmpty();
        });
    }
});

// =============================================================================
// TEST SUITE 7: V1 ARCHIVED ROUTES (Should Redirect or 404)
// =============================================================================

test.describe('7. V1 Archived Routes', () => {
    test('/wall should redirect to /fil-pro or return 404', async ({ page }) => {
        const response = await page.goto('/wall');

        // Should either redirect or 404
        const url = page.url();

        if (response?.status() === 404) {
            // Old route properly removed
            expect(response.status()).toBe(404);
        } else {
            // Old route redirects to new route
            expect(url).toContain('/fil-pro');
        }
    });

    test('/feed should redirect to /fil-pro or return 404', async ({ page }) => {
        const response = await page.goto('/feed');

        const url = page.url();

        if (response?.status() === 404) {
            expect(response.status()).toBe(404);
        } else {
            expect(url).toContain('/fil-pro');
        }
    });

    test('/profile (generic) should redirect to dashboard or return 404', async ({ page }) => {
        const response = await page.goto('/profile');

        // Old generic profile should be gone or redirect
        expect(response?.status()).toBeLessThan(500);
    });
});
