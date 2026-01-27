import os
from dotenv import load_dotenv

load_dotenv()

print("ERPNEXT_BASE_URL =", os.getenv("ERPNEXT_BASE_URL"))
print("ERPNEXT_API_TOKEN =", os.getenv("ERPNEXT_API_TOKEN"))

from app.integrations.erpnext_real_client import ERPNextRealClient

client = ERPNextRealClient()

invoice = client.get_invoice("ACC-SINV-2026-00004")
print("Invoice:", invoice)

order = client.get_sales_order("SO-0001")
print("Order:", order)
