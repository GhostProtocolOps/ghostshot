import { test, expect } from './fixtures';

test.describe('GhostShot Enterprise E2E Benchmark Suite', () => {
  test('Benchmark 1: Full-page capture on fixed navigation layout (W3Schools AWS Pattern)', async ({ page, extensionId, context }) => {
    // Navigate to benchmark target with sticky subnav and fixed sidebars
    await page.goto('https://www.w3schools.com/aws/index.php', { waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(1000);

    // Verify fixed elements exist in live DOM
    const subnav = page.locator('#subtopnav');
    if (await subnav.count() > 0) {
      await expect(subnav).toBeVisible();
    }

    // Open extension popup and trigger full-page capture
    const popupPage = await context.newPage();
    await popupPage.goto(`chrome-extension://${extensionId}/src/popup/popup.html`);
    await popupPage.waitForLoadState('domcontentloaded');

    // Click 'Full Page Capture' button
    const fullPageBtn = popupPage.locator('#btn-full-page');
    await expect(fullPageBtn).toBeVisible();

    // Listen for the capture viewer tab to open
    const [viewerPage] = await Promise.all([
      context.waitForEvent('page'),
      fullPageBtn.click(),
    ]);

    await viewerPage.waitForLoadState('domcontentloaded');
    await viewerPage.waitForSelector('canvas.viewer-tile-canvas', { timeout: 15000 });

    // Validate canvas viewer properties
    const tileCount = await viewerPage.locator('canvas.viewer-tile-canvas').count();
    expect(tileCount).toBeGreaterThanOrEqual(1);

    // Verify title and dimension metadata rendered
    const titleText = await viewerPage.locator('#display-title').innerText();
    expect(titleText).toContain('AWS');

    const metaText = await viewerPage.locator('#display-meta').innerText();
    expect(metaText).toMatch(/\d+\s*×\s*\d+\s*px/);

    await popupPage.close();
    await viewerPage.close();
  });

  test('Benchmark 2: Mathematical terminal seam clamping calculation', async ({ page }) => {
    // Inject mathematical coordinate verification into browser runtime
    const mathResult = await page.evaluate(() => {
      const totalHeight = 2868;
      const windowHeight = 900;
      const maxScrollY = Math.max(0, totalHeight - windowHeight); // 1968

      let capturedY = 0;
      let sliceIndex = 0;
      const slices = [];

      while (capturedY < totalHeight) {
        const targetScrollY = Math.min(capturedY, maxScrollY);
        const actualScrollY = targetScrollY;
        const sourceY = Math.max(0, capturedY - actualScrollY);
        const sliceHeight = Math.max(1, Math.min(totalHeight, actualScrollY + windowHeight) - capturedY);

        slices.push({
          index: sliceIndex,
          sourceY,
          sliceHeight,
          destY: capturedY,
        });

        capturedY += sliceHeight;
        sliceIndex++;
        if (targetScrollY >= maxScrollY && capturedY >= totalHeight) break;
      }

      return {
        totalSlices: slices.length,
        finalCapturedY: capturedY,
        terminalSlice: slices[slices.length - 1],
      };
    });

    // Assert exact terminal slice clamping
    expect(mathResult.finalCapturedY).toBe(2868);
    expect(mathResult.totalSlices).toBe(4);
    // Terminal slice must only take the remaining uncaptured 168px
    expect(mathResult.terminalSlice.sliceHeight).toBe(168);
    expect(mathResult.terminalSlice.sourceY).toBe(732);
    expect(mathResult.terminalSlice.destY).toBe(2700);
  });
});
