"""
Build a FastAPI application skeleton.

Requirements:
- Create a FastAPI app instance
- Health check endpoint: GET /health
- No business logic
- Ready for future routers
- Clean, minimal, production-ready structure
"""
from fastapi import FastAPI
from app.models.health import HealthResponse
from app.models.replay import ReplayResponse, ReplayScope, ReplaySummary, Finding, ControlGap, TimelineEvent

app = FastAPI(title="ERPNext Financial Incident Replay Skill", version="0.1.0")


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.get("/replay/customer/{customer_id}", response_model=ReplayResponse)
def replay_customer(customer_id: str) -> ReplayResponse:
    # Dummy response for skeleton stage (no ERPNext integration yet)
    scope = ReplayScope(
        type="customer",
        customer_id=customer_id,
        invoice_id=None,
        from_date="2026-01-01",
        to_date="2026-01-22",
    )

    summary = ReplaySummary(
        customer_name="Demo Customer",
        currency="USD",
        open_invoices_count=2,
        total_outstanding=900.0,
        incident_types=["PAYMENT_MISMATCH", "OVERDUE_RISK"],
    )

    timeline = [
        TimelineEvent(
            timestamp="2026-01-20T10:00:00Z",
            event="INVOICE_SUBMITTED",
            reference="INV-0003",
            amount=900.0,
        )
    ]

    findings = [
        Finding(
            code="PAYMENT_MISMATCH",
            severity="CRITICAL",
            message="Total paid amount does not match invoiced amount.",
            evidence={"total_invoiced": 900.0, "total_paid": 1200.0},
        )
    ]

    control_gaps = [
        ControlGap(
            gap="NO_PAYMENT_VALIDATION",
            why_it_matters="Can cause disputes and financial losses.",
            suggested_control="Block payments exceeding invoice total.",
        )
    ]

    return ReplayResponse(
        scope=scope,
        summary=summary,
        timeline=timeline,
        findings=findings,
        control_gaps=control_gaps,
        conclusion="High financial risk detected due to payment inconsistencies.",
    )
