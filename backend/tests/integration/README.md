# Integration Tests

## Overview

These tests validate the **complete system** with **REAL external dependencies**:
- ✅ Real ERPNext API (via ngrok)
- ✅ Real Anthropic Claude AI
- ✅ Real database operations
- ✅ Real error handling

**NO MOCKS** - this tests actual production behavior.

## Setup Instructions

### 1. Create Environment File

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your real credentials
nano .env  # or use your favorite editor
```

### 2. Required Credentials

Your `.env` file must contain:

```env
# ERPNext Configuration
ERPNEXT_BASE_URL=https://your-ngrok-url.ngrok-free.dev
ERPNEXT_API_KEY=your_actual_api_key
ERPNEXT_API_SECRET=your_actual_api_secret

# AI Configuration
ANTHROPIC_API_KEY=sk-ant-your-actual-key
AI_ENABLED=true
```

### 3. Update Test Data

Edit `tests/integration/test_analysis_integration.py`:

```python
# Line ~46 - Update with a REAL invoice ID from your ERPNext
VALID_INVOICE_ID = "ACC-SINV-2026-00009"  # Change this!
```

## Running Tests

```bash
# Run all integration tests
pytest tests/integration/ -v

# Run specific test file
pytest tests/integration/test_analysis_integration.py -v

# Run with output (see API calls)
pytest tests/integration/test_analysis_integration.py -v -s

# Run single test
pytest tests/integration/test_analysis_integration.py::TestAnalysisIntegration::test_analyze_incident_real_erp_success -v
```

## What Gets Tested

### 1. Happy Path - Real ERP + AI Success
- Creates incident with real invoice ID
- Fetches real data from ERPNext
- Calls real Claude API
- ✅ Status: RESOLVED
- ✅ Analysis source: AI
- ✅ Confidence score: 0.0-1.0

### 2. ERP Error Handling
- Uses invalid invoice ID
- AI fails due to missing data
- ✅ Status: UNDER_REVIEW (graceful failure)
- ✅ Analysis source: AI_FAILED
- ✅ API returns 200 (not 500)

### 3. Incident Not Found
- Non-existent incident ID
- ✅ Returns HTTP 404

## Cost Considerations

⚠️ **These tests consume API credits:**
- Anthropic Claude API calls (~$0.03 per test with Claude 3.5 Sonnet)
- Run strategically - not on every commit

## CI/CD Integration

For GitHub Actions / GitLab CI:

```yaml
env:
  ERPNEXT_BASE_URL: ${{ secrets.ERPNEXT_BASE_URL }}
  ERPNEXT_API_KEY: ${{ secrets.ERPNEXT_API_KEY }}
  ERPNEXT_API_SECRET: ${{ secrets.ERPNEXT_API_SECRET }}
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
  AI_ENABLED: true

jobs:
  integration-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Integration Tests
        run: pytest tests/integration/ -v
```

## Troubleshooting

### Tests are skipped

**Symptom:**
```
SKIPPED [1] - Missing required environment variables
```

**Solution:**
1. Ensure `.env` file exists in `backend/` directory
2. Verify all required variables are set (not empty)
3. Check for typos in variable names

### ERPNext connection fails

**Symptom:**
```
Connection refused / Timeout
```

**Solution:**
1. Verify ngrok tunnel is running
2. Check ERPNEXT_BASE_URL is correct (no trailing slash)
3. Test manually: `curl https://your-url.ngrok-free.dev/api/method/ping`

### AI analysis fails

**Symptom:**
```
Status: UNDER_REVIEW, analysis_source: AI_FAILED
```

**Solution:**
1. Verify ANTHROPIC_API_KEY is valid
2. Check API credit balance
3. Verify invoice ID exists in ERPNext
4. Review logs for specific AI error

## vs Unit Tests

| Aspect | Unit Tests | Integration Tests |
|--------|-----------|------------------|
| **Location** | `tests/api/` | `tests/integration/` |
| **Mocks** | Yes (AI, ERP) | No - Real services |
| **Speed** | Fast (<1s) | Slow (5-10s per test) |
| **Cost** | Free | Consumes API credits |
| **Purpose** | Validate logic | Validate integration |
| **When to run** | Every commit | Before deploy / PR |
| **Credentials** | Not required | Required |

Run unit tests frequently, integration tests strategically.

## Production Risks Covered

✅ **Network failures** - ERPNext unreachable  
✅ **Data quality** - Invalid invoice IDs  
✅ **AI availability** - Claude API down  
✅ **Graceful degradation** - UNDER_REVIEW fallback  
✅ **End-to-end flow** - Complete data pipeline  
✅ **Business logic** - Status transitions  

These tests give confidence that the system works in production!
