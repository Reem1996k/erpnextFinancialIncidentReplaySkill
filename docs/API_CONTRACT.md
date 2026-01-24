# API Contract – ERPNext Financial Incident Replay Skill

## Purpose
Provide a clear and explainable replay of financial activity
for a given business scope (Customer or Invoice).

The API does NOT modify ERP data.
It only analyzes and explains it.

---

## Base URL
http://localhost:8000

---

## Endpoints

### 1. Replay by Customer (Primary Endpoint)
GET /replay/customer/{customer_id}

#### Query Parameters
| Name | Type | Description |
|----|----|----|
| from_date | YYYY-MM-DD | Start date (default: 30 days ago) |
| to_date | YYYY-MM-DD | End date (default: today) |
| limit | integer | Max number of timeline events |

---

### 2. Replay by Invoice (Optional)
GET /replay/invoice/{invoice_id}

---

### 3. Create Incident Case
POST /cases

```json
{
  "title": "Customer dispute – unexpected charge",
  "scope_type": "customer",
  "scope_id": "CUST-0001",
  "notes": "Customer claims they were charged twice"
}

---

### 4. List Incident Cases
GET /cases

---

### 5. Get Incident Case by ID
GET /cases/{case_id}

---

### Replay Response Structure

{
  "scope": {
    "type": "customer",
    "customer_id": "CUST-0001",
    "invoice_id": null,
    "from_date": "2026-01-01",
    "to_date": "2026-01-22"
  },
  "summary": {
    "customer_name": "ABC Ltd",
    "currency": "USD",
    "open_invoices_count": 2,
    "total_outstanding": 900,
    "incident_types": ["PAYMENT_MISMATCH", "OVERDUE_RISK"]
  },
  "timeline": [
    {
      "timestamp": "2026-01-20T10:00:00Z",
      "event": "INVOICE_SUBMITTED",
      "reference": "INV-0003",
      "amount": 900
    }
  ],
  "findings": [
    {
      "code": "PAYMENT_MISMATCH",
      "severity": "CRITICAL",
      "message": "Total paid amount does not match invoiced amount.",
      "evidence": {
        "total_invoiced": 900,
        "total_paid": 1200
      }
    }
  ],
  "control_gaps": [
    {
      "gap": "NO_PAYMENT_VALIDATION",
      "why_it_matters": "Can cause disputes and financial losses.",
      "suggested_control": "Block payments exceeding invoice total."
    }
  ],
  "conclusion": "High financial risk detected due to payment inconsistencies."
}

---

### Severity Levels

LOW – informational
MEDIUM – review required
HIGH – business risk
CRITICAL – financial/compliance risk

