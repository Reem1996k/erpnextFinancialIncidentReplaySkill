# Playwright UI Automation Tests - Financial Incident Replay

Comprehensive UI automation test suite for the Financial Incident Replay application using Playwright Test with Page Object Model (POM) pattern.

## Project Structure

```
ui/tests/
├── pages/
│   └── IncidentPage.ts           # Page Object Model for Incident Replay page
├── specs/
│   └── incident-replay.spec.ts   # Test specifications and scenarios
├── playwright.config.ts          # Playwright configuration
├── package.json                  # Project dependencies and scripts
└── README.md                      # This file
```

## Setup & Installation

### Prerequisites
- Node.js 16+ (LTS recommended)
- npm or yarn package manager
- Backend server running on `http://127.0.0.1:8000`

### Installation Steps

1. Navigate to the tests directory:
```bash
cd ui/tests
```

2. Install dependencies:
```bash
npm install
```

3. Ensure the backend server is running:
```bash
cd ../../backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

## Running Tests

### Run all tests
```bash
npm test
```

### Run with UI Mode (Interactive)
```bash
npm run test:ui
```

### Run with Headed Mode (See Browser)
```bash
npm run test:headed
```

### Run in Debug Mode
```bash
npm run test:debug
```

### Run tests for specific browser
```bash
npm run test:chrome      # Chromium only
npm run test:firefox     # Firefox only
npm run test:webkit      # WebKit (Safari) only
npm run test:mobile      # Mobile Chrome
```

### View Test Report
```bash
npm run report
```

## Test Coverage

### Test Scenarios

1. **Page Navigation & Loading**
   - Navigate to incident page by ID
   - Verify page title and header
   - Verify URL structure

2. **Initial State Verification**
   - Verify incident status "OPEN"
   - Verify "no analysis" message
   - Verify incident metadata display

3. **Incident Metadata Display**
   - Verify incident ID
   - Verify ERP reference
   - Verify incident type
   - Verify description

4. **Analysis Results Display**
   - Create and analyze incident via API
   - Navigate to analyzed incident
   - Verify status changed to "ANALYZED"
   - Verify no analysis message removed
   - Verify summary section visible
   - Verify details section visible
   - Verify conclusion section visible
   - Verify decision badge visible

5. **Decision Badge Verification**
   - Verify badge is visible
   - Verify badge contains valid decision type
   - Verify badge has correct styling

6. **Page Structure & Styling**
   - Verify header section
   - Verify content area
   - Verify footer section
   - Verify proper styling applied

7. **Happy Path Workflow**
   - Complete end-to-end user flow
   - Create incident → View initial state → Analyze → Verify results

## Page Object Model (IncidentPage)

The `IncidentPage` class encapsulates all interactions with the incident replay page:

### Key Methods

**Navigation**
- `navigateToIncident(incidentId)` - Navigate to incident page

**Verification**
- `verifyPageTitleVisible()` - Verify page title
- `verifyPageTitleVisible()` - Verify page title
- `verifySummarySectionVisible()` - Verify summary section
- `verifyDetailsSectionVisible()` - Verify details section
- `verifyConclusionSectionVisible()` - Verify conclusion section
- `verifyDecisionBadgeVisible()` - Verify decision badge

**Getters**
- `getIncidentReference()` - Get ERP reference
- `getIncidentStatus()` - Get incident status
- `getIncidentType()` - Get incident type
- `getDescription()` - Get incident description
- `getSummaryContent()` - Get summary text
- `getDetailsContent()` - Get details text
- `getConclusionContent()` - Get conclusion text
- `getDecisionBadgeText()` - Get decision badge text

**Checks**
- `isAnalyzed()` - Check if incident is analyzed
- `hasNoAnalysisMessage()` - Check for "no analysis" message
- `hasDecisionType(decisionType)` - Check decision type

**Utilities**
- `getPageUrl()` - Get current page URL
- `takeScreenshot(filename)` - Take screenshot for debugging

## Configuration Details

### Browser Coverage
- **Chromium** - Desktop Chrome
- **Firefox** - Desktop Firefox
- **WebKit** - Desktop Safari
- **Mobile Chrome** - Mobile viewport (Pixel 5)

### Timeouts
- **Global timeout**: 30 seconds
- **Expect timeout**: 5 seconds
- **Page load**: Network idle

### Artifacts on Failure
- Screenshots on failure
- Videos on failure
- Traces on first retry

## Best Practices

1. **Locator Strategy**
   - Prefer `data-testid` attributes when available
   - Use semantic selectors (class, text content)
   - Avoid brittle XPath expressions

2. **Assertions**
   - Use clear, descriptive assertions
   - Group related assertions
   - Prefer waitFor over manual sleeps

3. **Test Isolation**
   - Each test creates its own incident data
   - No dependencies between tests
   - Uses `beforeEach` for setup

4. **Error Handling**
   - Graceful fallbacks for optional elements
   - Meaningful error messages
   - Timeout awareness

## Debugging

### Enable Debug Mode
```bash
npm run test:debug
```
This opens Playwright Inspector for step-by-step debugging.

### View Test Traces
Traces are automatically recorded on first retry. View with:
```bash
npx playwright show-trace <path-to-trace>
```

### Screenshots & Videos
Check `test-results/` directory for:
- Screenshots on failure
- Video recordings
- Test logs

## CI/CD Integration

### GitHub Actions Example
```yaml
- name: Install dependencies
  run: npm install
  working-directory: ui/tests

- name: Run Playwright tests
  run: npm test
  working-directory: ui/tests

- name: Upload report
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: playwright-report
    path: ui/tests/playwright-report/
```

## Troubleshooting

### Tests fail to connect to backend
- Verify backend is running on `http://127.0.0.1:8000`
- Check `playwright.config.ts` baseURL setting
- Ensure no firewall blocks localhost:8000

### Element not found errors
- Check if page structure matches selectors
- Use `--debug` flag to inspect live
- Verify data is present in backend

### Timeout errors
- Increase timeout in `playwright.config.ts`
- Check network conditions
- Verify backend response times

## Contributing

When adding new tests:
1. Add new methods to `IncidentPage` class
2. Create descriptive test names
3. Include detailed comments
4. Add corresponding documentation

## Resources

- [Playwright Documentation](https://playwright.dev)
- [Best Practices](https://playwright.dev/docs/best-practices)
- [Debugging Guide](https://playwright.dev/docs/debug)
- [Page Object Model Pattern](https://playwright.dev/docs/pom)
