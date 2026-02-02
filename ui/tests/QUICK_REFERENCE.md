# Quick Test Reference

## Run Smoke Tests Only
```bash
cd ui
pytest -m smoke
```

## Run E2E Tests Only
```bash
pytest -m e2e
```

## Run Smoke + E2E
```bash
pytest -m "smoke or e2e"
```

## Run All Tests
```bash
pytest
```

## Run with Browser Visible (Debug)
```bash
pytest -m smoke --headed --slowmo 500
```

## Run Specific Test File
```bash
pytest tests/smoke/test_smoke_critical_path.py
```

## Test Categories

- `smoke` - Fast critical path validation (< 10s)
- `e2e` - Complete end-to-end flows (20-60s)
- `feature` - Feature-specific tests
- `slow` - Long-running tests

## CI/CD Recommended Flow

```bash
# Stage 1: Fast feedback (smoke)
pytest -m smoke --browser chromium

# Stage 2: Full validation (if smoke passes)
pytest -m e2e --browser chromium
```
