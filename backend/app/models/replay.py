from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel


class ReplayScope(BaseModel):
    type: Literal["customer", "invoice"]
    customer_id: Optional[str] = None
    invoice_id: Optional[str] = None
    from_date: str
    to_date: str


class ReplaySummary(BaseModel):
    customer_name: str
    currency: str
    open_invoices_count: int
    total_outstanding: float
    incident_types: List[str]


class TimelineEvent(BaseModel):
    timestamp: str
    event: str
    reference: str
    amount: Optional[float] = None


class Finding(BaseModel):
    code: str
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    message: str
    evidence: Dict[str, Any] = {}


class ControlGap(BaseModel):
    gap: str
    why_it_matters: str
    suggested_control: str


class ReplayResponse(BaseModel):
    scope: ReplayScope
    summary: ReplaySummary
    timeline: List[TimelineEvent]
    findings: List[Finding]
    control_gaps: List[ControlGap]
    conclusion: str
