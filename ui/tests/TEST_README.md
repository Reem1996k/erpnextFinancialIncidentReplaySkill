# UI Test Suite

Complete E2E test suite for the Financial Incident Replay System using Playwright (Python) and pytest.

## Project Structure

```
ui/tests/
├── conftest.py                 # Pytest configuration and fixtures
├── requirements.txt            # Python dependencies
├── e2e/                        # End-to-end tests
│   └── test_incident_full_flow.py
├── features/                   # Feature-level tests
│   └── test_analysis_view.py
└── pages/                      # Page Object Model (POM)
    ├── create_incident_page.py
    ├── incident_page.py
    └── incidents_list_page.py
```

## Setup

### Install Dependencies

```bash
cd ui
pip install -r tests/requirements.txt
playwright install chromium
```

### Start the Application

Ensure both backend and frontend are running:

```bash
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd ui
npm run dev
```

The application should be available at http://localhost:3000

## Running Tests

### Run All Tests

```bash
cd ui
pytest
```

### Run Only E2E Tests

```bash
pytest -m e2e
```

### Run with Headed Browser (watch tests execute)

```bash
pytest --headed
```

### Run Specific Test File

```bash
pytest tests/e2e/test_incident_full_flow.py
```

### Run with Verbose Output

```bash
pytest -v
```

### Run with Playwright Debug Mode

```bash
PWDEBUG=1 pytest tests/e2e/test_incident_full_flow.py
```

## Test Flow

### Complete E2E Test (`test_incident_full_flow`)

1. **Create Incident Page**
   - Navigate to "/"
   - Fill ERP reference
   - Select incident type
   - Enter description
   - Click "Create & Analyze"
   - Wait for "Analyzing..." indicator
   - Wait for automatic redirect to incident page

2. **Incident Analysis Page**
   - Verify initial status is "OPEN"
   - Click "Run Analysis" button
   - Verify "Analyzing..." appears
   - Verify button becomes disabled
   - Wait for status to change to "RESOLVED" (up to 60s)
   - Verify confidence score is visible
   - Verify analysis summary is visible

3. **Incidents List Navigation**
   - Click "Incidents" in header navigation
   - Click "View" for first incident
   - Verify status remains "RESOLVED"

## Page Object Model

### CreateIncidentPage

Handles the incident creation form.

**Methods:**
- `open()` - Navigate to create page
- `fill_erp_reference(value)` - Fill ERP reference field
- `select_incident_type(value)` - Select incident type from dropdown
- `fill_description(text)` - Fill description textarea
- `submit()` - Submit form and handle analyzing state

### IncidentPage

Handles the incident details and analysis page.

**Methods:**
- `expect_status(status, timeout)` - Verify status badge
- `run_analysis()` - Click Run Analysis button
- `expect_analyzing()` - Verify analyzing state
- `wait_for_resolved()` - Wait for analysis completion
- `expect_confidence()` - Verify confidence score visible
- `expect_summary()` - Verify analysis summary visible

### IncidentsListPage

Handles the incidents list page.

**Methods:**
- `open()` - Navigate directly to list
- `navigate_via_header()` - Click Incidents link in header
- `click_view_for_first_incident()` - Click View button

## Best Practices

### ✅ DO

- Use role-based locators: `get_by_role("button", name="...")`
- Use placeholder locators: `get_by_placeholder("...")`
- Use proper waiting: `expect().to_be_visible(timeout=...)`
- Use Page Object Model for maintainability
- Handle async state transitions properly
- Add meaningful timeouts for long operations

### ❌ DON'T

- Use `sleep()` - always use proper waiting strategies
- Hardcode URLs - use pytest base_url configuration
- Use fragile locators (CSS classes, complex XPath)
- Mix test logic with page actions
- Ignore async state changes

## Configuration

### pytest.ini

```ini
[pytest]
base_url = http://localhost:3000
testpaths = tests
addopts = -v --tb=short
```

### playwright.config.py

Contains Playwright-specific configuration and base URL setup.

## Troubleshooting

### Tests Timeout

- Ensure backend is running and responsive
- Check if ERPNext mock is configured correctly
- Increase timeout values for slow AI responses

### Navigation Issues

- Verify base_url is set correctly
- Check if frontend is running on port 3000
- Ensure no other services are blocking the port

### Element Not Found

- Check if UI text/labels have changed
- Verify locators match the current UI
- Use `pytest --headed` to watch what's happening

## CI/CD Integration

Tests are designed to run in CI environments:

```bash
# Install dependencies
pip install -r tests/requirements.txt
playwright install --with-deps chromium

# Run tests
pytest --browser chromium --screenshot on-failure-only
```

## Additional Resources

- [Playwright Python Docs](https://playwright.dev/python/)
- [pytest Documentation](https://docs.pytest.org/)
- [Page Object Model Pattern](https://playwright.dev/python/docs/pom)
