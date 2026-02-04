# Frontend Test Plan

**Date:** February 4, 2026 | **Status:** Active

---

## 1. What to Test

### 1.1 UI Tests (6 Total)

**Health Check** (`tests/test_health_check.py`) - 2 tests:

| Test | Expected |
|------|----------|
| `test_backend_health` | Backend API returns 200 (local only) |
| `test_frontend_accessible` | Page loads, "Create Financial Incident" visible |

**Smoke Tests** (`tests/smoke/test_smoke_critical_path.py`) - 1 test:

| Test | Expected |
|------|----------|
| `test_create_incident_smoke` | Create incident → status=OPEN |

**Feature Tests** (`tests/features/test_refresh_functionality.py`) - 2 tests:

| Test | Expected |
|------|----------|
| `test_page_reload_preserves_open_status` | Create → Reload → status=OPEN persists |
| `test_page_reload_preserves_resolved_status` | Create → Analyze → Reload → status=RESOLVED persists |

**E2E Tests** (`tests/e2e/test_incident_full_flow.py`) - 1 test:

| Test | Expected |
|------|----------|
| `test_incident_full_flow` | Create → Analyze → View in list → Navigate back → status=RESOLVED |

---

## 2. How to Test

### 2.1 Framework: Playwright + Pytest

**Commands:**
- All tests: `pytest tests/ -v`
- Smoke only: `pytest tests/ -m smoke -v`
- Feature only: `pytest tests/ -m feature -v`
- E2E only: `pytest tests/ -m e2e -v`
- Visible browser: `HEADLESS=false pytest tests/ -v`

### 2.2 Page Object Model

| Page Object | Location |
|-------------|----------|
| `CreateIncidentPage` | `tests/pages/create_incident_page.py` |
| `IncidentPage` | `tests/pages/incident_page.py` |
| `IncidentsListPage` | `tests/pages/incidents_list_page.py` |

### 2.3 Prerequisites

**Local:**
- Backend running: `cd backend && uvicorn app.main:app --reload`
- Frontend running: `cd ui && npm run dev`
- Playwright installed: `playwright install chromium`

**CI:**
- `APP_URL` env variable set
- `HEADLESS=true`

---

## 3. Exit Criteria

| Criterion | Target |
|-----------|--------|
| Smoke tests pass rate | 100% |
| Feature tests pass rate | 95%+ |
| E2E tests | Pass or skip (if AI unavailable) |
| Critical defects | 0 open |

**Testing Complete When:**
- [ ] All 2 health check tests pass
- [ ] All 1 smoke test passes
- [ ] All 2 feature tests pass
- [ ] E2E test passes (or skipped in CI)
- [ ] CI pipeline green
