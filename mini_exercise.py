# === Telecom Data: Manual CDR Analysis ===
# CDR = Call Detail Record — you already know this!

subscribers = [
    {"id": "SUB001", "name": "Alice",   "plan": "Postpaid", "monthly_gb": 12.5, "tenure_months": 36},
    {"id": "SUB002", "name": "Bob",     "plan": "Prepaid",  "monthly_gb": 2.1,  "tenure_months": 8},
    {"id": "SUB003", "name": "Carol",   "plan": "Postpaid", "monthly_gb": 18.9, "tenure_months": 60},
    {"id": "SUB004", "name": "David",   "plan": "Prepaid",  "monthly_gb": 0.5,  "tenure_months": 3},
    {"id": "SUB005", "name": "Eve",     "plan": "Postpaid", "monthly_gb": 9.2,  "tenure_months": 24},
]

# Calculate average data usage
total_gb = sum(s["monthly_gb"] for s in subscribers)
avg_gb = total_gb / len(subscribers)
print(f"Average monthly data usage: {avg_gb:.1f} GB")

# Find high-usage subscribers (>10 GB)
high_usage = [s for s in subscribers if s["monthly_gb"] > 10]
print(f"\nHigh-usage subscribers ({len(high_usage)} found):")
for s in high_usage:
    print(f"  {s['name']} ({s['plan']}) — {s['monthly_gb']} GB")

# Flag possible churn risk: Prepaid + tenure < 6 months
churn_risk = [s for s in subscribers if s["plan"] == "Prepaid" and s["tenure_months"] < 6]
print(f"\nChurn risk flags ({len(churn_risk)} found):")
for s in churn_risk:
    print(f"  {s['name']} — only {s['tenure_months']} months tenure")