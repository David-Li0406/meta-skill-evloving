import { defineConfig, devices } from '@playwright/test';

const demoPort = process.env.DEMO_PORT || '4173';
const baseURL = process.env.DEMO_BASE_URL || `http://127.0.0.1:${demoPort}`;

export default defineConfig({
  testDir: './tests',
  testMatch: '**/*.spec.ts',
  timeout: 20_000,
  retries: 0,
  use: {
    baseURL,
    headless: true,
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium-desktop',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'chromium-touch',
      use: {
        ...devices['Pixel 5'],
        viewport: { width: 1080, height: 2340 },
        hasTouch: true,
      },
    },
  ],
  reporter: [
    ['list'],
    ['html', { outputFolder: 'playwright-report' }],
    ['junit', { outputFile: 'junit-report.xml' }]
  ]
});
