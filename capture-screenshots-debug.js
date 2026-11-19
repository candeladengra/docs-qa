const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ 
    headless: false,  // Run headed to see what's happening
    slowMo: 500 
  });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
  });
  const page = await context.newPage();

  // Listen to console messages
  page.on('console', msg => console.log('BROWSER:', msg.text()));
  page.on('pageerror', err => console.error('PAGE ERROR:', err.message));

  try {
    console.log('1. Navigating to the app...');
    await page.goto('http://localhost:5173/', { waitUntil: 'networkidle', timeout: 60000 });
    
    console.log('2. Waiting for React to render...');
    await page.waitForTimeout(5000);
    
    console.log('3. Checking what\'s in the root div...');
    const rootContent = await page.locator('#root').innerHTML();
    console.log('Root content length:', rootContent.length);
    
    if (rootContent.length < 100) {
      console.error('React app did not render!');
      console.log('Full HTML:');
      console.log(await page.content());
    } else {
      console.log('React app rendered successfully!');
    }
    
    console.log('\nWaiting 30 seconds so you can inspect the browser...');
    await page.waitForTimeout(30000);
    
  } catch (error) {
    console.error('Error:', error.message);
  } finally {
    await browser.close();
  }
})();
