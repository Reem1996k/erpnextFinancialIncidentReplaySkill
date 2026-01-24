# Business Policy Definitions

## Purpose
Define business rules that represent
financial controls expected in a well-managed ERP system.

The skill evaluates historical data against these rules.

---

## Policy 1 – Overdue Invoice Risk
Rule:
An invoice unpaid for more than 30 days.

Finding:
- Code: OVERDUE_RISK
- Severity: HIGH

Business Impact:
- Cash flow risk
- Credit exposure

---

## Policy 2 – Payment Mismatch
Rule:
Total paid amount does not equal total invoiced amount.

Finding:
- Code: PAYMENT_MISMATCH
- Severity: CRITICAL

Business Impact:
- Customer disputes
- Refunds
- Accounting inconsistencies

---

## Policy 3 – Approval Gap
Rule:
The same user created and submitted a financial document.

Finding:
- Code: APPROVAL_GAP
- Severity: MEDIUM or HIGH

Business Impact:
- Lack of segregation of duties
- Audit risk

---

## Policy Simulation
The system can simulate:
"What would have happened if these policies were enforced?"

Purpose:
- Learn from past incidents
- Improve future controls
- Support audits and training
