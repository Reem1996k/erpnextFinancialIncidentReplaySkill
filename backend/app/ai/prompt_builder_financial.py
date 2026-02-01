"""
Generic AI Prompt Builder for ERP Financial Incident Analysis

Generates prompts for Claude to analyze ANY Sales Invoice vs Sales Order discrepancy.
Works for all currencies, tax schemes, charges, and pricing scenarios.
"""

from typing import Dict, Any


def build_financial_analysis_prompt(
    invoice: Dict[str, Any],
    sales_order: Dict[str, Any],
    incident_description: str
) -> str:
    """
    Build a generic prompt for Claude to analyze invoice vs sales order discrepancies.
    
    Args:
        invoice: Dictionary containing invoice data (id, items, taxes, charges, totals, currency, etc.)
        sales_order: Dictionary containing sales order data (id, items, totals, currency, etc.)
        incident_description: Human description of the incident/concern
    
    Returns:
        A formatted prompt string for Claude API
    
    The prompt ensures Claude:
    - Uses ONLY provided data (no assumptions)
    - Identifies exact sources of discrepancy
    - Provides numeric breakdown
    - Suggests ONE concrete ERP resolution
    - Outputs valid JSON only
    """
    
    # Format invoice data
    invoice_id = invoice.get("id") or invoice.get("name") or "UNKNOWN"
    invoice_total = invoice.get("grand_total") or invoice.get("total") or 0
    invoice_currency = invoice.get("currency") or "UNKNOWN"
    invoice_items = invoice.get("items") or []
    invoice_taxes = invoice.get("taxes") or []
    invoice_charges = invoice.get("charges") or []
    invoice_subtotal = invoice.get("subtotal") or invoice.get("net_total") or sum(
        item.get("amount", 0) for item in invoice_items
    )
    
    # Format sales order data
    so_id = sales_order.get("id") or sales_order.get("name") or "UNKNOWN"
    so_total = sales_order.get("grand_total") or sales_order.get("total") or 0
    so_currency = sales_order.get("currency") or "UNKNOWN"
    so_items = sales_order.get("items") or []
    so_subtotal = sales_order.get("subtotal") or sales_order.get("net_total") or sum(
        item.get("amount", 0) for item in so_items
    )
    
    # Calculate totals for analysis
    invoice_tax_total = sum(tax.get("tax_amount", 0) for tax in invoice_taxes)
    invoice_charge_total = sum(charge.get("amount", 0) for charge in invoice_charges)
    difference = invoice_total - so_total
    
    # Format items comparison
    items_comparison = _format_items_comparison(invoice_items, so_items)
    
    # Build the prompt
    prompt = f"""You are an expert ERP Financial Analyst. Your task is to analyze a financial discrepancy between a Sales Invoice and its linked Sales Order.

STRICT RULES:
1. Use ONLY the provided ERP data
2. Do NOT assume or guess missing values
3. Do NOT invent ERP records or transactions
4. Be specific and factual
5. Identify EXACT numeric sources of the difference
6. Output MUST be valid JSON only (no markdown, no free text)

INCIDENT DESCRIPTION:
{incident_description}

SALES ORDER DATA:
- ID: {so_id}
- Currency: {so_currency}
- Total: {so_total}
- Subtotal: {so_subtotal}
- Items Count: {len(so_items)}
- Items:
{_format_items_list(so_items, "  ")}

INVOICE DATA:
- ID: {invoice_id}
- Currency: {invoice_currency}
- Total: {invoice_total}
- Subtotal: {invoice_subtotal}
- Tax Total: {invoice_tax_total}
- Charges Total: {invoice_charge_total}
- Items Count: {len(invoice_items)}
- Items:
{_format_items_list(invoice_items, "  ")}
- Taxes:
{_format_taxes_list(invoice_taxes, "  ")}
- Charges:
{_format_charges_list(invoice_charges, "  ")}

NUMERIC ANALYSIS:
- Total Difference: {difference} ({invoice_currency})
- Invoice Total vs SO Total: {invoice_total} - {so_total} = {difference}
- As Percentage: {((difference / so_total * 100) if so_total != 0 else 0):.1f}%

ITEMS COMPARISON (Line-by-Line):
{items_comparison}

YOUR TASK:
1. Analyze line-by-line: Do quantities, rates, and amounts match between Invoice and SO?
2. Identify all sources of difference:
   - Item price changes
   - Quantity changes
   - Tax additions/removals
   - Charges additions/removals
   - Currency conversions
   - Discounts applied
   - Missing/unlinked Sales Order
3. Provide numeric breakdown showing exactly how the final total differs
4. Explain WHY this difference exists based on ERP data
5. Suggest ONE clear, concrete ERP action to resolve

OUTPUT FORMAT (JSON ONLY - no other text):
{{
  "root_cause": "factual ERP-level cause extracted from provided data",
  "difference_breakdown": "numeric explanation with line items: 'SO subtotal: X + taxes: Y + charges: Z = invoice total'",
  "recommended_resolution": "single concrete ERP action (e.g., 'Apply tax rule ABC', 'Remove charge XYZ', 'Verify customer pricing', etc.)",
  "confidence_score": 0.0
}}

CONFIDENCE SCORE GUIDANCE:
- 0.95+: Data is complete, discrepancy fully explained with all sources identified
- 0.85-0.94: Data complete but multiple possible causes
- 0.70-0.84: Data mostly complete but some values missing or ambiguous
- 0.50-0.69: Partial data, explanation is uncertain
- <0.50: Insufficient data to explain discrepancy

OUTPUT ONLY THE JSON OBJECT. NO ADDITIONAL TEXT."""

    return prompt


def _format_items_list(items: list, indent: str = "") -> str:
    """Format items list for prompt."""
    if not items:
        return f"{indent}(No items provided)"
    
    formatted = []
    for idx, item in enumerate(items, 1):
        item_code = item.get("item_code") or item.get("id") or f"Item{idx}"
        qty = item.get("qty") or item.get("quantity") or 0
        rate = item.get("rate") or item.get("price") or 0
        amount = item.get("amount") or (qty * rate) or 0
        discount = item.get("discount_amount") or 0
        
        line = f"{indent}{idx}. {item_code}: qty={qty}, rate={rate}, amount={amount}"
        if discount:
            line += f", discount={discount}"
        formatted.append(line)
    
    return "\n".join(formatted)


def _format_taxes_list(taxes: list, indent: str = "") -> str:
    """Format taxes list for prompt."""
    if not taxes:
        return f"{indent}(No taxes applied)"
    
    formatted = []
    for idx, tax in enumerate(taxes, 1):
        tax_type = tax.get("tax_type") or tax.get("account_head") or "Tax"
        rate = tax.get("rate") or 0
        amount = tax.get("tax_amount") or 0
        formatted.append(f"{indent}{idx}. {tax_type}: rate={rate}%, amount={amount}")
    
    return "\n".join(formatted)


def _format_charges_list(charges: list, indent: str = "") -> str:
    """Format charges list for prompt."""
    if not charges:
        return f"{indent}(No additional charges)"
    
    formatted = []
    for idx, charge in enumerate(charges, 1):
        charge_type = charge.get("charge_type") or charge.get("type") or "Charge"
        amount = charge.get("amount") or 0
        formatted.append(f"{indent}{idx}. {charge_type}: {amount}")
    
    return "\n".join(formatted)


def _format_items_comparison(invoice_items: list, so_items: list) -> str:
    """Format side-by-side comparison of items."""
    lines = []
    
    # Build lookup by item code
    so_lookup = {
        (item.get("item_code") or item.get("id") or f"Item{idx}"): item
        for idx, item in enumerate(so_items)
    }
    
    # Compare each invoice item
    for inv_item in invoice_items:
        inv_code = inv_item.get("item_code") or inv_item.get("id") or "Unknown"
        inv_qty = inv_item.get("qty") or inv_item.get("quantity") or 0
        inv_rate = inv_item.get("rate") or inv_item.get("price") or 0
        inv_amount = inv_item.get("amount") or 0
        
        so_item = so_lookup.get(inv_code)
        
        if so_item:
            so_qty = so_item.get("qty") or so_item.get("quantity") or 0
            so_rate = so_item.get("rate") or so_item.get("price") or 0
            so_amount = so_item.get("amount") or 0
            
            qty_match = "✓" if inv_qty == so_qty else "✗"
            rate_match = "✓" if inv_rate == so_rate else "✗"
            
            lines.append(
                f"  {inv_code}: Qty {qty_match} (Invoice: {inv_qty} vs SO: {so_qty}), "
                f"Rate {rate_match} (Invoice: {inv_rate} vs SO: {so_rate}), "
                f"Amount (Invoice: {inv_amount} vs SO: {so_amount})"
            )
        else:
            lines.append(
                f"  {inv_code}: NOT IN SALES ORDER (Invoice qty={inv_qty}, rate={inv_rate}, amount={inv_amount})"
            )
    
    # Check for items in SO but not in Invoice
    invoice_codes = {
        (item.get("item_code") or item.get("id") or f"Item{idx}")
        for idx, item in enumerate(invoice_items)
    }
    
    for so_code in so_lookup:
        if so_code not in invoice_codes:
            so_item = so_lookup[so_code]
            so_qty = so_item.get("qty") or so_item.get("quantity") or 0
            so_amount = so_item.get("amount") or 0
            lines.append(f"  {so_code}: IN SALES ORDER BUT NOT IN INVOICE (qty={so_qty}, amount={so_amount})")
    
    if not lines:
        return "  (No items to compare)"
    
    return "\n".join(lines)
