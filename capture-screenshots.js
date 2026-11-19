const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
  });
  const page = await context.newPage();

  try {
    console.log('1. Navigating to the app...');
    await page.goto('http://localhost:5173/', { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForTimeout(3000);

    console.log('2. Waiting for file input to be visible...');
    await page.waitForSelector('#file-input', { timeout: 30000 });

    console.log('3. Uploading PDF document...');
    const fileInput = await page.locator('#file-input');
    await fileInput.setInputFiles(path.join(__dirname, 'samples', 'ai-basics.pdf'));
    await page.waitForTimeout(2000);

    console.log('4. Waiting for document to be processed (Ready status)...');
    let attempts = 0;
    const maxAttempts = 30;
    while (attempts < maxAttempts) {
      const statusReady = await page.locator('text=/Ready/i').count();
      if (statusReady > 0) {
        console.log('   Document is Ready!');
        break;
      }
      await page.waitForTimeout(2000);
      attempts++;
      if (attempts % 5 === 0) {
        console.log(`   Still waiting... (${attempts}/${maxAttempts})`);
        // Refresh the document list to check status
        await page.reload({ waitUntil: 'networkidle' });
        await page.waitForTimeout(1000);
      }
    }

    if (attempts >= maxAttempts) {
      console.log('   Warning: Document did not reach Ready status in time');
    }

    await page.waitForTimeout(1000);

    console.log('5. Taking screenshot of document list...');
    await page.screenshot({
      path: path.join(__dirname, 'docs', 'screenshot.png'),
      fullPage: false,
    });
    console.log('   Saved: docs/screenshot.png');

    console.log('6. Finding and clicking on the chat/question input...');
    // Look for the message input that becomes enabled when docs are ready
    const messageInput = await page.locator('.message-input, input.message-input, input[type="text"]').last();
    await page.waitForTimeout(1000);
    
    console.log('7. Asking a question...');
    await messageInput.fill('What is artificial intelligence?');
    await messageInput.press('Enter');

    console.log('8. Waiting for answer...');
    await page.waitForTimeout(8000);

    console.log('9. Looking for expandable citations...');
    // Look for any expandable elements (details/summary, buttons with expand text, etc.)
    const expandables = await page.locator('details summary, button:has-text("Show"), button:has-text("Expand"), [class*="citation"]').all();
    if (expandables.length > 0) {
      console.log(`   Found ${expandables.length} potential expandable elements, clicking first one`);
      await expandables[0].click();
      await page.waitForTimeout(1000);
    } else {
      console.log('   No obvious expandable element found, taking screenshot anyway...');
    }

    console.log('10. Taking screenshot of Q&A with citations...');
    await page.screenshot({
      path: path.join(__dirname, 'docs', 'qa-citations.png'),
      fullPage: true,
    });
    console.log('    Saved: docs/qa-citations.png');

    console.log('\n✓ Screenshots captured successfully!');
    
  } catch (error) {
    console.error('Error during screenshot capture:', error.message);
    console.error('Taking error screenshot...');
    await page.screenshot({
      path: path.join(__dirname, 'docs', 'error-screenshot.png'),
      fullPage: true,
    });
    console.log('Error screenshot saved: docs/error-screenshot.png');
    
    // Also save the page HTML for debugging
    const html = await page.content();
    const fs = require('fs');
    fs.writeFileSync(path.join(__dirname, 'docs', 'error-page.html'), html);
    console.log('Page HTML saved: docs/error-page.html');
    
    process.exit(1);
  } finally {
    await browser.close();
  }
})();
