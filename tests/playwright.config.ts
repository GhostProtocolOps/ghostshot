import { defineConfig } from '@playwright/test';
import path from 'path';

export default defineConfig({
  testDir: './e2e',
  timeout: 30000,
  retries: 0,
  workers: 1, // Run sequentially for browser extension testing
  use: {
    headless: false, // Chrome extensions are only supported in headed mode
    viewport: { width: 1440, height: 900 },
    ignoreHTTPSErrors: true,
  },
  projects: [
    {
      name: 'chromium-extension',
      use: {
        channel: 'chromium',
      },
    },
  ],
});
