# Backend Function Inventory Report
**Generated:** January 29, 2026  
**Project:** ERPNext Financial Incident Replay Skill  
**Total Functions Analyzed:** 101

---

## 📊 Executive Summary

| **Metric** | **Count** | **Percentage** |
|------------|-----------|----------------|
| ✅ **Functions In Use** | 59 | 58% |
| ⚠️ **Available (Test/Mock)** | 9 | 9% |
| ❌ **Not Used (Dead Code)** | 33 | 33% |
| **Total Functions** | **101** | **100%** |

### Status by Folder

| **Folder** | **Total** | **✅ In Use** | **⚠️ Available** | **❌ Not Used** | **% Active** |
|------------|-----------|---------------|------------------|-----------------|--------------|
| `app/` | 1 | 1 | 0 | 0 | 100% |
| `api/` | 7 | 7 | 0 | 0 | 100% |
| `controllers/` | 9 | 9 | 0 | 0 | 100% |
| `ai/` | 21 | 15 | 3 | 3 | 71% |
| `integrations/` | 17 | 11 | 6 | 0 | 65% |
| `services/` | 34 | 10 | 0 | 24 | 29% ⚠️ |
| `models/` | 9 | 3 | 0 | 6 | 33% |
| `db/` | 3 | 3 | 0 | 0 | 100% |

---

## 📁 Detailed Inventory by Folder

---

## 1️⃣ FOLDER: `app/` (Root)

### **File: `main.py`**

| # | Function | Status | Used By | Description |
|---|----------|--------|---------|-------------|
| 1 | `health()` | ✅ **IN USE** | GET /health endpoint | Health check endpoint |

**Folder Summary:** 1/1 functions active (100%)

---

## 2️⃣ FOLDER: `app/api/` (API Routes)

### **File: `incidents.py`**

| # | Function | Status | Used By | Description |
|---|----------|--------|---------|-------------|
| 1 | `get_db()` | ✅ **IN USE** | Dependency for all routes | Database session dependency |
| 2 | `create_new_incident()` | ✅ **IN USE** | POST /incidents/ | Create new incident endpoint |
| 3 | `list_incidents()` | ✅ **IN USE** | GET /incidents/ | List all incidents endpoint |
| 4 | `get_incident()` | ✅ **IN USE** | GET /incidents/{id} | Get single incident endpoint |
| 5 | `replay_incident()` | ✅ **IN USE** | POST /incidents/{id}/replay | Run replay analysis endpoint |

### **File: `analysis.py`**

| # | Function | Status | Used By | Description |
|---|----------|--------|---------|-------------|
| 1 | `get_db()` | ✅ **IN USE** | Dependency | Database session dependency |
| 2 | `analyze_incident()` | ✅ **IN USE** | POST /incidents/{id}/analyze | Trigger analysis endpoint |

**Folder Summary:** 7/7 functions active (100%)

**API Endpoints Active:**
- ✅ POST `/incidents/` - Create incident
- ✅ GET `/incidents/` - List incidents
- ✅ GET `/incidents/{id}` - Get incident
- ✅ POST `/incidents/{id}/replay` - Run replay
- ✅ POST `/incidents/{id}/analyze` - Analyze incident
- ✅ GET `/health` - Health check

---

## 3️⃣ FOLDER: `app/controllers/` (Business Logic Controllers)

### **File: `incident_controller.py`**

| # | Function | Status | Used By | Description |
|---|----------|--------|---------|-------------|
| 1 | `create_incident()` | ✅ **IN USE** | API: create_new_incident() | Creates new incident in database |
| 2 | `get_incident_by_id()` | ✅ **IN USE** | API routes, internal calls | Retrieves incident by ID |
| 3 | `get_all_incidents()` | ✅ **IN USE** | API: list_incidents() | Returns all incidents |
| 4 | `run_replay_for_incident()` | ✅ **IN USE** | API: replay_incident() | Runs replay analysis |
| 5 | `resolve_incident()` | ✅ **IN USE** | API: analyze_incident() | Main orchestrator for AI/Rule analysis |
| 6 | `_resolve_with_ai()` | ✅ **IN USE** | Called by: resolve_incident() | AI-only analysis path |
| 7 | `_resolve_with_rules()` | ✅ **IN USE** | Called by: resolve_incident() | Rule-only analysis path |
| 8 | `_run_ai_analysis_for_incident()` | ✅ **IN USE** | Called by: _resolve_with_ai() | Orchestrates AI analysis |
| 9 | `_gather_erp_data_for_incident()` | ✅ **IN USE** ⚠️ | Called by: _run_ai_analysis_for_incident() | Fetches ERP data (HAS BUGS) |

**Folder Summary:** 9/9 functions active (100%)

**Note:** Function #9 `_gather_erp_data_for_incident()` is active but contains bugs:
- ❌ NameError: Variable scoping issues
- ❌ Dead code: Unused items list
- ❌ Inefficient logic: Wrong lookup order
- ✅ Fix ready but tool disabled

---

## 4️⃣ FOLDER: `app/ai/` (AI Integration Layer)

### **File: `ai_factory.py`**

| # | Function | Status | Used By | Description |
|---|----------|--------|---------|-------------|
| 1 | `get_ai_client()` | ✅ **IN USE** | Controller: _resolve_with_ai() | Factory function returning AIClientAnthropic |

### **File: `ai_client_base.py`** (Abstract Base Class)

| # | Method | Status | Used By | Description |
|---|----------|--------|---------|-------------|
| 1 | `analyze()` | ✅ **IN USE** | Implemented by AIClientAnthropic | Abstract method for AI analysis |
| 2 | `is_available()` | ✅ **IN USE** | Implemented by AIClientAnthropic | Check if AI client is configured |

### **File: `ai_client_anthropic.py`** ⭐ (Active Claude Client)

| # | Method | Status | Used By | Description |
|---|----------|--------|---------|-------------|
| 1 | `__init__()` | ✅ **IN USE** | Factory: get_ai_client() | Initialize Claude client with API key |
| 2 | `is_available()` | ✅ **IN USE** | Internal validation | Check if API key configured |
| 3 | `analyze()` | ✅ **IN USE** | AIResolver: resolve_incident() | Main analysis method - calls Claude API |
| 4 | `_parse_claude_response()` | ✅ **IN USE** | Called by: analyze() | Parse Claude JSON response |
| 5 | `_normalize_response()` | ✅ **IN USE** | Called by: analyze() | Normalize response to standard format |

### **File: `ai_client_mock.py`** (Test Client)

| # | Method | Status | Used By | Description |
|---|----------|--------|---------|-------------|
| 1 | `__init__()` | ⚠️ **AVAILABLE** | Available for testing | Mock AI client constructor |
| 2 | `is_available()` | ⚠️ **AVAILABLE** | Available for testing | Always returns True for testing |
| 3 | `analyze()` | ⚠️ **AVAILABLE** | Available for testing | Returns mock AI response |

### **File: `ai_resolver.py`**

| # | Method | Status | Used By | Description |
|---|----------|--------|---------|-------------|
| 1 | `__init__()` | ✅ **IN USE** | Controller: _run_ai_analysis_for_incident() | Initialize with AI client |
| 2 | `resolve_incident()` | ✅ **IN USE** | Controller: _run_ai_analysis_for_incident() | Main entry point for AI analysis |
| 3 | `_run_rule_analysis()` | ❌ **NOT USED** | DEAD CODE | Unused method (lines 112-142) |
| 4 | `_run_ai_analysis()` | ❌ **NOT USED** | DEAD CODE | Unused method (lines 145-194) |
| 5 | `_merge_analyses()` | ❌ **NOT USED** | DEAD CODE | Unused method (lines 197-258) |

### **File: `ai_result_mapper.py`**

| # | Method | Status | Used By | Description |
|---|----------|--------|---------|-------------|
| 1 | `map_ai_response()` | ✅ **IN USE** | AIResolver: resolve_incident() | Maps Claude response to standard format |
| 2 | `map_ai_result()` | ❌ **NOT USED** | Alternative mapper (unused) | Redundant mapping function |

### **File: `prompt_builder_financial.py`**

| # | Function | Status | Used By | Description |
|---|----------|--------|---------|-------------|
| 1 | `build_financial_analysis_prompt()` | ✅ **IN USE** | AIResolver: resolve_incident() | Builds comprehensive AI prompt with ERP data |
| 2 | `_format_items_list()` | ✅ **IN USE** | Called by: build_financial_analysis_prompt() | Formats invoice items for prompt |
| 3 | `_format_taxes_list()` | ✅ **IN USE** | Called by: build_financial_analysis_prompt() | Formats tax information for prompt |
| 4 | `_format_charges_list()` | ✅ **IN USE** | Called by: build_financial_analysis_prompt() | Formats charges for prompt |
| 5 | `_format_items_comparison()` | ✅ **IN USE** | Called by: build_financial_analysis_prompt() | Compares invoice vs SO items |

**Folder Summary:** 15/21 functions active (71%)
- ✅ Active: 15
- ⚠️ Available (Test): 3
- ❌ Dead Code: 3 (in ai_resolver.py)

---

## 5️⃣ FOLDER: `app/integrations/` (ERP Integration)

### **File: `client_factory.py`**

| # | Function | Status | Used By | Description |
|---|----------|--------|---------|-------------|
| 1 | `get_erp_client()` | ✅ **IN USE** | Controller, ReplayEngine, Analyzers | Returns Real or Mock ERP client |

### **File: `erpnext_client_base.py`** (Abstract Base Class)

| # | Method | Status | Used By | Description |
|---|----------|--------|---------|-------------|
| 1 | `get_invoice()` | ✅ **IN USE** | Implemented by Real + Mock | Abstract method for invoice retrieval |
| 2 | `get_sales_order()` | ✅ **IN USE** | Implemented by Real + Mock | Abstract method for SO retrieval |
| 3 | `get_customer()` | ✅ **IN USE** | Implemented by Real + Mock | Abstract method for customer retrieval |
| 4 | `get_item()` | ✅ **IN USE** | Implemented by Real + Mock | Abstract method for item retrieval |

### **File: `erpnext_real_client.py`** ⭐ (ACTIVE CLIENT - ERP_CLIENT_MODE=real)

| # | Method | Status | Used By | Description |
|---|----------|--------|---------|-------------|
| 1 | `__init__()` | ✅ **IN USE** | Factory: get_erp_client() | Initialize with ERPNext URL and token |
| 2 | `_get_headers()` | ✅ **IN USE** | Called by: _make_request() | Generates HTTP headers with auth token |
| 3 | `_make_request()` | ✅ **IN USE** | Called by: all get_* methods | Makes HTTP GET to ERPNext API |
| 4 | `get_invoice()` | ✅ **IN USE** | Controller: _gather_erp_data_for_incident() | Fetches invoice via REST API |
| 5 | `get_sales_order()` | ✅ **IN USE** | Controller: _gather_erp_data_for_incident() | Fetches sales order via REST API |
| 6 | `get_customer()` | ✅ **IN USE** | Controller: _gather_erp_data_for_incident() | Fetches customer via REST API |
| 7 | `get_item()` | ✅ **IN USE** | Available (not currently called) | Fetches item data via REST API |

**API Endpoint Pattern:**
- Base URL: `http://localhost:8080`
- Invoice: `/api/resource/Sales Invoice/{invoice_id}`
- Sales Order: `/api/resource/Sales Order/{order_id}`
- Customer: `/api/resource/Customer/{customer_id}`
- Item: `/api/resource/Item/{item_code}`

### **File: `erpnext_mock_client.py`** (Test Client - ERP_CLIENT_MODE=mock)

| # | Method | Status | Used By | Description |
|---|----------|--------|---------|-------------|
| 1 | `get_invoice()` | ⚠️ **AVAILABLE** | Used when ERP_CLIENT_MODE=mock | Returns hardcoded test invoice data |
| 2 | `get_sales_order()` | ⚠️ **AVAILABLE** | Used when ERP_CLIENT_MODE=mock | Returns hardcoded test SO data |
| 3 | `get_customer()` | ⚠️ **AVAILABLE** | Used when ERP_CLIENT_MODE=mock | Returns hardcoded test customer data |
| 4 | `get_item()` | ⚠️ **AVAILABLE** | Used when ERP_CLIENT_MODE=mock | Returns hardcoded test item data |

**Test Data Available:**
- Invoices: INV-001, INV-002, INV-003, ACC-SINV-2026-00009
- Sales Orders: SO-001, SO-002, SO-2026-00005
- Customers: CUST-001, CUST-002

**Folder Summary:** 11/17 functions active (65%)
- ✅ Active: 11 (Real client)
- ⚠️ Available: 6 (Mock client - dormant)
- ❌ Dead Code: 0

---

## 6️⃣ FOLDER: `app/services/` (Business Services)

### **File: `replay_engine.py`** ✅ (ACTIVE - Rule-Based Analysis)

| # | Method | Status | Used By | Description |
|---|----------|--------|---------|-------------|
| 1 | `__init__()` | ✅ **IN USE** | Controller: run_replay_for_incident(), _resolve_with_rules() | Initialize with ERP client |
| 2 | `analyze_incident()` | ✅ **IN USE** | Controller: run_replay_for_incident(), _resolve_with_rules() | Main rule-based analysis entry point |
| 3 | `_run_rule_based_analysis()` | ✅ **IN USE** | Called by: analyze_incident() | Executes rule-based analysis logic |

### **File: `incident_analyzers.py`** ✅ (ACTIVE - Specific Rule Analyzers)

#### **Class: AnalysisResult** (Data Class)

| # | Method | Status | Used By | Description |
|---|----------|--------|---------|-------------|
| 1 | `__init__()` | ✅ **IN USE** | All analyzer classes | Creates analysis result object |
| 2 | `to_dict()` | ✅ **IN USE** | ReplayEngine: analyze_incident() | Converts result to dictionary |
| 3 | `is_undetermined()` | ✅ **IN USE** | Internal checks | Checks if analysis is undetermined |

#### **Class: PricingIssueAnalyzer**

| # | Method | Status | Used By | Description |
|---|----------|--------|---------|-------------|
| 1 | `__init__()` | ✅ **IN USE** | Factory: get_analyzer() | Initialize pricing analyzer |
| 2 | `analyze()` | ✅ **IN USE** | ReplayEngine: _run_rule_based_analysis() | Checks for pricing variance between invoice and SO |

#### **Class: DuplicateInvoiceAnalyzer**

| # | Method | Status | Used By | Description |
|---|----------|--------|---------|-------------|
| 1 | `__init__()` | ✅ **IN USE** | Factory: get_analyzer() | Initialize duplicate detector |
| 2 | `analyze()` | ✅ **IN USE** | ReplayEngine: _run_rule_based_analysis() | Detects duplicate invoices |

#### **Class: DeliveryBillingMismatchAnalyzer**

| # | Method | Status | Used By | Description |
|---|----------|--------|---------|-------------|
| 1 | `__init__()` | ✅ **IN USE** | Factory: get_analyzer() | Initialize delivery/billing checker |
| 2 | `analyze()` | ✅ **IN USE** | ReplayEngine: _run_rule_based_analysis() | Checks delivery vs billing mismatches |

#### **Class: IncidentAnalyzerFactory**

| # | Method | Status | Used By | Description |
|---|----------|--------|---------|-------------|
| 1 | `get_analyzer()` | ✅ **IN USE** | ReplayEngine: _run_rule_based_analysis() | Factory method returning correct analyzer |

**Supported Incident Types:**
- ✅ `PRICING_ISSUE` → PricingIssueAnalyzer
- ✅ `DUPLICATE_INVOICE` → DuplicateInvoiceAnalyzer
- ✅ `DELIVERY_BILLING_MISMATCH` → DeliveryBillingMismatchAnalyzer

### **File: `erp_data_extractor.py`** ❌ (NOT USED - Alternative Implementation)

| # | Method | Status | Used By | Description |
|---|----------|--------|---------|-------------|
| 1 | `__init__()` | ❌ **NOT USED** | Class never imported | Constructor |
| 2 | `extract_incident_data()` | ❌ **NOT USED** | Class never imported | Main extraction method |
| 3 | `_extract_invoice()` | ❌ **NOT USED** | Class never imported | Extract invoice data |
| 4 | `_extract_sales_order()` | ❌ **NOT USED** | Class never imported | Extract SO data |
| 5 | `_extract_customer()` | ❌ **NOT USED** | Class never imported | Extract customer data |
| 6 | `_validate_completeness()` | ❌ **NOT USED** | Class never imported | Validate data completeness |
| 7 | `_safe_float()` | ❌ **NOT USED** | Class never imported | Safe float conversion |
| 8 | `_error_response()` | ❌ **NOT USED** | Class never imported | Generate error response |
| 9 | `_resolve_sales_order_reference()` | ❌ **NOT USED** | Class never imported | Resolve SO reference |
| 10 | `get_sales_order_for_items()` | ❌ **NOT USED** | Class never imported | Get SO from items |

**Why Unused:** Replaced by `_gather_erp_data_for_incident()` in controller

### **File: `incident_analysis_service.py`** ❌ (NOT USED - Alternative Service)

| # | Method | Status | Used By | Description |
|---|----------|--------|---------|-------------|
| 1 | `__init__()` | ❌ **NOT USED** | Class never imported | Constructor |
| 2 | `analyze_incident()` | ❌ **NOT USED** | Class never imported | Alternative analysis orchestrator |
| 3 | `_perform_rule_based_analysis()` | ❌ **NOT USED** | Class never imported | Rule-based analysis method |
| 4 | `_perform_ai_analysis()` | ❌ **NOT USED** | Class never imported | AI analysis method |
| 5 | `_handle_incomplete_data()` | ❌ **NOT USED** | Class never imported | Handle incomplete data |
| 6 | `_handle_error()` | ❌ **NOT USED** | Class never imported | Error handler |
| 7 | `_build_analysis_prompt()` | ❌ **NOT USED** | Class never imported | Build AI prompt |
| 8 | `_structure_ai_response()` | ❌ **NOT USED** | Class never imported | Structure AI response |

**Why Unused:** Alternative implementation never integrated

### **File: `ai_analyzer.py`** ❌ (NOT USED - Alternative AI Service)

#### **Class: AIAnalyzerConfig**

| # | Method | Status | Used By | Description |
|---|----------|--------|---------|-------------|
| 1 | `__init__()` | ❌ **NOT USED** | Class never imported | Config constructor |
| 2 | `is_configured()` | ❌ **NOT USED** | Class never imported | Check if configured |

#### **Class: AIAnalyzer**

| # | Method | Status | Used By | Description |
|---|----------|--------|---------|-------------|
| 1 | `__init__()` | ❌ **NOT USED** | Class never imported | Constructor |
| 2 | `_validate_config()` | ❌ **NOT USED** | Class never imported | Validate configuration |
| 3 | `analyze()` | ❌ **NOT USED** | Class never imported | Main analysis method |
| 4 | `_build_prompt()` | ❌ **NOT USED** | Class never imported | Build AI prompt |
| 5 | `_call_llm()` | ❌ **NOT USED** | Class never imported | Call LLM |
| 6 | `_call_openai()` | ❌ **NOT USED** | Class never imported | Call OpenAI API |
| 7 | `_call_anthropic()` | ❌ **NOT USED** | Class never imported | Call Anthropic API |
| 8 | `_call_custom_api()` | ❌ **NOT USED** | Class never imported | Call custom API |
| 9 | `_parse_ai_response()` | ❌ **NOT USED** | Class never imported | Parse AI response |
| 10 | `_format_details()` | ❌ **NOT USED** | Class never imported | Format details |

**Why Unused:** Alternative AI implementation. System uses AIClientAnthropic + AIResolver instead.

**Folder Summary:** 10/34 functions active (29%)
- ✅ Active: 10 (ReplayEngine + Analyzers)
- ❌ Dead Code: 24 (3 entire unused files)

**Critical Issue:** 71% of services folder is dead code!

---

## 7️⃣ FOLDER: `app/models/` (Data Models)

### **File: `incident.py`** ✅ (Pydantic Models - ACTIVE)

| # | Class | Status | Used By | Description |
|---|----------|--------|---------|-------------|
| 1 | `IncidentCreate` | ✅ **IN USE** | API request validation | Validates POST /incidents/ request body |
| 2 | `IncidentResponse` | ✅ **IN USE** | API response serialization | Serializes Incident objects to JSON |

### **File: `replay.py`** ❌ (Unused Pydantic Models)

| # | Class | Status | Used By | Description |
|---|----------|--------|---------|-------------|
| 1 | `ReplayScope` | ❌ **NOT USED** | Never imported | Defines replay scope |
| 2 | `ReplaySummary` | ❌ **NOT USED** | Never imported | Replay summary structure |
| 3 | `TimelineEvent` | ❌ **NOT USED** | Never imported | Timeline event structure |
| 4 | `Finding` | ❌ **NOT USED** | Never imported | Finding structure |
| 5 | `ControlGap` | ❌ **NOT USED** | Never imported | Control gap structure |
| 6 | `ReplayResponse` | ❌ **NOT USED** | Never imported | Complete replay response |

**Why Unused:** Old schema design. Current implementation uses Incident model fields directly:
- `replay_summary`
- `replay_details`
- `replay_conclusion`
- `analysis_source`
- `confidence_score`

### **File: `health.py`** ✅ (Pydantic Model - ACTIVE)

| # | Class | Status | Used By | Description |
|---|----------|--------|---------|-------------|
| 1 | `HealthResponse` | ✅ **IN USE** | GET /health endpoint | Health check response model |

**Folder Summary:** 3/9 models active (33%)
- ✅ Active: 3
- ❌ Not Used: 6 (entire replay.py file)

---

## 8️⃣ FOLDER: `app/db/` (Database Layer)

### **File: `models.py`** ✅ (SQLAlchemy ORM)

| # | Class | Status | Used By | Description |
|---|----------|--------|---------|-------------|
| 1 | `Incident` | ✅ **IN USE** | All controllers, API endpoints | Main database table for incidents |

**Incident Model Fields:**
- `id` (Primary Key)
- `erp_reference` (Unique)
- `incident_type`
- `description`
- `status` (OPEN, ANALYZED, RESOLVED, UNDER_REVIEW)
- `replay_summary`
- `replay_details`
- `replay_conclusion`
- `analysis_source` (AI, RULE, AI_FAILED, RULE_FAILED)
- `confidence_score`
- `replayed_at`
- `ai_analysis_json`
- `created_at`
- `updated_at`

### **File: `database.py`** ✅ (Database Configuration)

| # | Component | Status | Used By | Description |
|---|----------|--------|---------|-------------|
| 1 | `engine` | ✅ **IN USE** | SQLAlchemy session creation | Database engine |
| 2 | `SessionLocal` | ✅ **IN USE** | API get_db() dependency | Session factory |
| 3 | `Base` | ✅ **IN USE** | ORM models inheritance | Declarative base |

**Database Configuration:**
- SQLite: `backend/incidents.db`
- Connection String: `sqlite:///./incidents.db`

**Folder Summary:** 3/3 components active (100%)

---

## 📈 Call Chain Analysis

### **Active Call Chain (AI Path):**

```
User Request
    ↓
POST /incidents/{id}/analyze (API)
    ↓
analyze_incident() [analysis.py]
    ↓
resolve_incident() [incident_controller.py]
    ↓ [IF AI_ENABLED=true]
    ↓
_resolve_with_ai() [incident_controller.py]
    ↓
get_ai_client() [ai_factory.py]
    │
    ├─→ AIClientAnthropic.__init__()
    │
    ↓
_run_ai_analysis_for_incident() [incident_controller.py]
    ↓
get_erp_client() [client_factory.py]
    │
    ├─→ ERPNextRealClient.__init__()
    │
    ↓
_gather_erp_data_for_incident() [incident_controller.py]
    ↓
    ├─→ erp_client.get_invoice()
    ├─→ erp_client.get_sales_order()
    └─→ erp_client.get_customer()
    │
    ↓ [Returns erp_data dict]
    ↓
AIResolver.resolve_incident() [ai_resolver.py]
    ↓
build_financial_analysis_prompt() [prompt_builder_financial.py]
    ↓
    ├─→ _format_items_list()
    ├─→ _format_taxes_list()
    ├─→ _format_charges_list()
    └─→ _format_items_comparison()
    │
    ↓ [Returns prompt string]
    ↓
ai_client.analyze(prompt) [AIClientAnthropic]
    ↓
    ├─→ Claude API Call (Anthropic)
    ↓
    ├─→ _parse_claude_response()
    └─→ _normalize_response()
    │
    ↓ [Returns AI response dict]
    ↓
AIResultMapper.map_ai_response() [ai_result_mapper.py]
    ↓ [Returns standardized result]
    ↓
Back to _resolve_with_ai()
    ↓
Persist to Database (SQLAlchemy)
    ↓
Return IncidentResponse to User
```

### **Active Call Chain (Rule Path):**

```
User Request
    ↓
resolve_incident() [incident_controller.py]
    ↓ [IF AI_ENABLED=false]
    ↓
_resolve_with_rules() [incident_controller.py]
    ↓
ReplayEngine.analyze_incident() [replay_engine.py]
    ↓
_run_rule_based_analysis() [replay_engine.py]
    ↓
IncidentAnalyzerFactory.get_analyzer() [incident_analyzers.py]
    ↓
    ├─→ PricingIssueAnalyzer.analyze()
    ├─→ DuplicateInvoiceAnalyzer.analyze()
    └─→ DeliveryBillingMismatchAnalyzer.analyze()
    │
    ↓ [Returns AnalysisResult]
    ↓
AnalysisResult.to_dict()
    ↓
Back to _resolve_with_rules()
    ↓
Persist to Database
    ↓
Return IncidentResponse to User
```

---

## ⚠️ Critical Issues Found

### **1. Buggy Function (Active but Broken)**

**Function:** `_gather_erp_data_for_incident()` in `incident_controller.py`  
**Status:** ✅ IN USE but ⚠️ HAS BUGS  
**Location:** Lines 312-367

**Issues:**
- ❌ **NameError:** `so_id` variable used outside loop scope
- ❌ **Dead Code:** Creates `items=[]` list but never uses it
- ❌ **Wrong Logic:** Tries to iterate items when SO should be at invoice header level
- ❌ **Debug Code:** Uses `print()` instead of logging

**Impact:** CRITICAL - Blocks Sales Order linking for ALL incidents

**Fix Status:** Corrected version provided, awaiting tool re-enable

---

### **2. Dead Code (3 Entire Files)**

#### **File: `services/erp_data_extractor.py`**
- **Lines:** 432 total
- **Functions:** 10
- **Status:** ❌ NEVER IMPORTED
- **Reason:** Replaced by `_gather_erp_data_for_incident()` in controller
- **Recommendation:** DELETE

#### **File: `services/incident_analysis_service.py`**
- **Lines:** ~300
- **Functions:** 8
- **Status:** ❌ NEVER IMPORTED
- **Reason:** Alternative implementation never integrated
- **Recommendation:** DELETE

#### **File: `services/ai_analyzer.py`**
- **Lines:** ~350
- **Functions:** 12
- **Status:** ❌ NEVER IMPORTED
- **Reason:** Alternative AI layer (uses AIClientAnthropic + AIResolver instead)
- **Recommendation:** DELETE

**Total Dead Code:** ~1,082 lines across 3 files (30 functions)

---

### **3. Dead Methods in Active Classes**

#### **File: `ai/ai_resolver.py`**

**Dead Methods (Never Called):**
1. `_run_rule_analysis()` - Lines 112-142 (30 lines)
2. `_run_ai_analysis()` - Lines 145-194 (49 lines)
3. `_merge_analyses()` - Lines 197-258 (61 lines)

**Total:** 140 lines of dead code

**Reason:** System now uses STRICT SEPARATION (AI-only OR Rule-only paths, no merging)

**Recommendation:** DELETE lines 112-258

---

### **4. Unused Models**

#### **File: `models/replay.py`**

**Unused Models:** 6 Pydantic classes
- `ReplayScope`
- `ReplaySummary`
- `TimelineEvent`
- `Finding`
- `ControlGap`
- `ReplayResponse`

**Reason:** Old schema design. Current implementation uses Incident model fields directly.

**Recommendation:** DELETE entire file

---

## 💡 Recommendations

### **Immediate Actions (High Priority)**

#### **1. Fix Buggy Function** 🔴 CRITICAL
- File: `incident_controller.py`
- Function: `_gather_erp_data_for_incident()`
- Action: Apply corrected version (lines 312-367)
- Impact: Fixes Sales Order linking bug

#### **2. Delete Dead Files** 🟡 MEDIUM
Delete 3 entire files (1,082 lines):
- `services/erp_data_extractor.py`
- `services/incident_analysis_service.py`
- `services/ai_analyzer.py`
- `models/replay.py`

#### **3. Remove Dead Methods** 🟡 MEDIUM
- File: `ai/ai_resolver.py`
- Action: Delete lines 112-258 (3 methods)
- Impact: Clean up 140 lines

---

### **Code Cleanup Summary**

| **Action** | **Files** | **Lines Removed** | **Functions Removed** |
|------------|-----------|-------------------|----------------------|
| Delete dead files | 4 | ~1,400 | 30 |
| Remove dead methods | 1 | 140 | 3 |
| Fix buggy function | 1 | 0 (rewrite) | 0 |
| **TOTAL** | **6** | **~1,540** | **33** |

**Result After Cleanup:**
- Functions: 101 → 68 (-33%)
- Active Code: 58% → 86% (+28%)
- Codebase Size: Reduced by ~1,540 lines
- Maintenance: Much easier (fewer files to track)

---

## 📋 Testing Checklist

### **Functions to Test After Cleanup:**

✅ **API Endpoints:**
- POST `/incidents/` - Create incident
- GET `/incidents/` - List incidents
- GET `/incidents/{id}` - Get incident
- POST `/incidents/{id}/replay` - Run replay
- POST `/incidents/{id}/analyze` - Analyze incident
- GET `/health` - Health check

✅ **AI Path (AI_ENABLED=true):**
- Get AI client
- Gather ERP data (after fix)
- Build AI prompt
- Call Claude API
- Map response
- Persist results

✅ **Rule Path (AI_ENABLED=false):**
- Get rule analyzer
- Run rule-based analysis
- Return analysis result
- Persist results

✅ **ERP Integration:**
- Get invoice from ERPNext
- Get sales order from ERPNext
- Get customer from ERPNext

---

## 📊 Statistics by Status

### **✅ Functions In Use: 59 (58%)**

**Distribution:**
- API Layer: 7 functions (12%)
- Controllers: 9 functions (15%)
- AI Layer: 15 functions (25%)
- Integrations: 11 functions (19%)
- Services: 10 functions (17%)
- Models/DB: 7 components (12%)

### **⚠️ Available (Test/Mock): 9 (9%)**

**Distribution:**
- AI Mock Client: 3 methods
- ERP Mock Client: 6 methods

### **❌ Not Used (Dead Code): 33 (33%)**

**Distribution:**
- services/erp_data_extractor.py: 10 functions
- services/incident_analysis_service.py: 8 functions
- services/ai_analyzer.py: 12 functions
- ai/ai_resolver.py: 3 methods
- models/replay.py: 6 classes

---

## 🎯 Conclusion

### **Current State:**
- Total Functions: 101
- Active Usage: 58%
- Dead Code: 33%
- Test Code: 9%

### **After Cleanup:**
- Total Functions: 68 (-33)
- Active Usage: 86% (+28%)
- Dead Code: 0% (-33%)
- Test Code: 13% (+4%)

### **Key Strengths:**
✅ Well-structured API layer (100% active)  
✅ Clean controller layer (100% active)  
✅ Solid database layer (100% active)  
✅ Working AI integration with Claude  
✅ Functional rule-based analyzers  

### **Key Weaknesses:**
❌ 33% dead code (1,540 lines)  
❌ Critical bug in ERP data gathering  
❌ 3 entire unused service files  
❌ Unused legacy models  

### **Priority:**
1. 🔴 **Fix `_gather_erp_data_for_incident()` bug** (CRITICAL)
2. 🟡 Delete 4 dead files (MEDIUM)
3. 🟢 Remove dead methods from ai_resolver.py (LOW)

---

## 📝 Appendix: Environment Configuration

### **Active Configuration (ERP_CLIENT_MODE=real, AI_ENABLED=true):**

```
# ERP Configuration
ERPNEXT_BASE_URL=http://localhost:8080
ERPNEXT_API_TOKEN=<api_key>:<api_secret>
ERP_CLIENT_MODE=real

# AI Configuration
AI_ENABLED=true
AI_PROVIDER=claude
CLAUDE_API_KEY=<your_key>
CLAUDE_MODEL=claude-3-sonnet-20240229

# Database
DATABASE_URL=sqlite:///./incidents.db
```

### **Mock Configuration (for testing):**

```
ERP_CLIENT_MODE=mock
AI_ENABLED=false
```

---

**Report Generated:** January 29, 2026  
**Total Analysis Time:** Complete codebase scan  
**Files Analyzed:** 23 Python files  
**Functions Catalogued:** 101  

---

**End of Report**
