
---

## 📄 `docs/UI_WIREFRAME.md`

```md
# UI Wireframe – Financial Incident Replay Skill

## Design Principle
One screen.
No ERP knowledge required.
Everything explained in business language.

---

## Replay Dashboard (Single Page)

### Input Section
- Scope selector: Customer / Invoice
- Text input: Customer ID or Invoice ID
- Date range (optional)
- Button: Replay

---

## Summary Section
- Customer name
- Total outstanding amount
- Open invoices count
- Incident severity badges

---

## Timeline Section
Chronological event list:
- Invoice created
- Invoice submitted
- Payment received
- Adjustments

Each event shows:
- Timestamp
- Event type
- Reference ID
- Amount

---

## Findings Section
Table with:
- Finding code
- Severity
- Plain-language explanation

This is the “what is wrong” area.

---

## Control Gaps Section
Cards explaining:
- Which control is missing
- Why it matters
- Suggested improvement

---

## Conclusion Section
Narrative summary:
- Overall risk level
- Business meaning
- Recommended action

---

## Incident Case Management
- Button: Create Incident Case
- Fields:
  - Case title
  - Notes
- Cases are saved locally and can be reviewed later

---

## Future Enhancement
Policy Simulation:
- As-Is (what happened)
- What-If (under stricter policy)
