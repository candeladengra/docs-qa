# Screenshots TODO

To complete the portfolio presentation, capture the following screenshots after running the application:

## Required Screenshots

### 1. Main Application View
- Full page showing:
  - Document upload section (left sidebar)
  - Document list with status indicators
  - Chat interface (main area)
  - Save as: `screenshot.png` (replace placeholder in docs/)

### 2. Document Upload Flow
- Before upload: empty state
- After upload: document in "processing" status
- After processing: document in "ready" status
- Save as: `docs/upload-flow.png`

### 3. Q&A with Citations
- Chat showing:
  - User question
  - AI answer with citations
  - Expanded source snippet showing document name and page number
- Save as: `docs/qa-with-citations.png`

### 4. Multiple Documents
- Several documents uploaded
- Different statuses (processing, ready, failed)
- Chat showing answer combining sources from multiple docs
- Save as: `docs/multi-document.png`

## How to Capture

1. Start the application:
   ```bash
   docker-compose up --build
   ```

2. Open http://localhost:5173 in browser

3. Upload 1-2 sample PDFs (use any technical docs or papers)

4. Wait for processing to complete

5. Ask several questions:
   - "What is this document about?"
   - "Summarize the key points"
   - "What does it say about [specific topic]?"

6. Take screenshots at key moments

7. Replace `docs/screenshot.png` with the main view

8. Add additional screenshots to `docs/` folder

9. Update README.md to reference the new screenshots:
   ```markdown
   ![Main Interface](./docs/screenshot.png)
   ![Q&A with Citations](./docs/qa-with-citations.png)
   ```

## Optional: Create a Demo GIF

Use a tool like [peek](https://github.com/phw/peek) or [LICEcap](https://www.cockos.com/licecap/) to record:
1. Uploading a document
2. Waiting for it to process
3. Asking a question
4. Getting an answer with citations
5. Clicking to expand source snippet

Save as: `docs/demo.gif`
