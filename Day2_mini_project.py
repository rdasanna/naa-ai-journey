# ============================================
# Day 2 Mini Project: Subscriber Batch Analyzer
# Telecom AI Journey — Week 1
# ============================================

subscribers = [
    {"id": "S001", "name": "Alice Morgan",   "plan": "Postpaid", "gb_used": 18.2, "tenure": 48, "spend": 145.00, "roaming": True},
    {"id": "S002", "name": "Bob Tran",       "plan": "Prepaid",  "gb_used": 0.8,  "tenure": 4,  "spend": 25.00,  "roaming": False},
    {"id": "S003", "name": "Carol Singh",    "plan": "Postpaid", "gb_used": 9.5,  "tenure": 24, "spend": 89.00,  "roaming": False},
    {"id": "S004", "name": "David Okafor",   "plan": "Postpaid", "gb_used": 31.0, "tenure": 72, "spend": 210.00, "roaming": True},
    {"id": "S005", "name": "Elena Vasquez",  "plan": "Prepaid",  "gb_used": 2.1,  "tenure": 2,  "spend": 15.00,  "roaming": False},
    {"id": "S006", "name": "Frank Liu",      "plan": "Postpaid", "gb_used": 5.5,  "tenure": 13, "spend": 75.00,  "roaming": False},
]

# --- Analysis ---
total_revenue  = 0
churn_risks    = []
high_value     = []
upsell_targets = []

for sub in subscribers:
    total_revenue += sub["spend"]

    # Churn risk: low tenure + low spend
    if sub["tenure"] < 6 and sub["spend"] < 30:
        churn_risks.append(sub["name"])

    # High value: spend > $100
    if sub["spend"] >= 100:
        high_value.append(sub["name"])

    # Upsell: heavy data user on Prepaid
    if sub["gb_used"] > 5 and sub["plan"] == "Prepaid":
        upsell_targets.append(sub["name"])

avg_revenue = total_revenue / len(subscribers)

# --- Report ---
print("=" * 45)
print("   SUBSCRIBER BATCH ANALYSIS REPORT")
print("=" * 45)
print(f"Total subscribers  : {len(subscribers)}")
print(f"Total revenue      : ${total_revenue:.2f}")
print(f"Avg revenue/sub    : ${avg_revenue:.2f}")
print()
print(f"Churn risks ({len(churn_risks)})   : {', '.join(churn_risks) or 'None'}")
print(f"High value ({len(high_value)})     : {', '.join(high_value) or 'None'}")
print(f"Upsell targets ({len(upsell_targets)}) : {', '.join(upsell_targets) or 'None'}")
print("=" * 45)