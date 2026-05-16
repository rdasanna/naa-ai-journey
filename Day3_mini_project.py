# ================================================
# Day 3 Mini Project: Network Health Report
# Telecom AI Journey — Week 1, Day 3
# ================================================

# --- Data ---
network_inventory = [
    {"id": "RTR-NYC-01", "region": "East",  "type": "Router", "uptime_pct": 99.95, "error_rate": 0.002, "last_alarm": None},
    {"id": "SW-LAX-03",  "region": "West",  "type": "Switch", "uptime_pct": 97.80, "error_rate": 0.080, "last_alarm": "Port flap"},
    {"id": "OLT-CHI-07", "region": "East",  "type": "OLT",    "uptime_pct": 99.50, "error_rate": 0.015, "last_alarm": "Rx power low"},
    {"id": "BTS-MIA-02", "region": "South", "type": "BTS",    "uptime_pct": 95.10, "error_rate": 0.120, "last_alarm": "Hardware fault"},
    {"id": "GPON-DAL-01","region": "South", "type": "GPON",   "uptime_pct": 99.99, "error_rate": 0.001, "last_alarm": None},
    {"id": "RTR-SEA-04", "region": "West",  "type": "Router", "uptime_pct": 98.50, "error_rate": 0.040, "last_alarm": "CPU high"},
]

# --- Functions ---
def get_status(node):
    if node["uptime_pct"] >= 99.9 and node["error_rate"] < 0.01:
        return "Healthy"
    elif node["uptime_pct"] >= 98.0 and node["error_rate"] < 0.05:
        return "Degraded"
    else:
        return "Critical"

def summarize_by_region(nodes):
    """Returns a dict of region -> status counts."""
    summary = {}
    for node in nodes:
        region = node["region"]
        status = get_status(node)
        if region not in summary:
            summary[region] = {"Healthy": 0, "Degraded": 0, "Critical": 0}
        summary[region][status] += 1
    return summary

def print_report(nodes):
    print("=" * 60)
    print("        NETWORK HEALTH REPORT — OSS DAILY SUMMARY")
    print("=" * 60)

    healthy  = [n for n in nodes if get_status(n) == "Healthy"]
    degraded = [n for n in nodes if get_status(n) == "Degraded"]
    critical = [n for n in nodes if get_status(n) == "Critical"]

    print(f"\n  Total nodes : {len(nodes)}")
    print(f"  Healthy     : {len(healthy)}")
    print(f"  Degraded    : {len(degraded)}")
    print(f"  Critical    : {len(critical)}")

    if critical:
        print(f"\n  !! CRITICAL ALERTS ({len(critical)}) !!")
        for node in critical:
            alarm = node['last_alarm'] or 'Unknown'
            print(f"     {node['id']} [{node['region']}] — {alarm}")

    print(f"\n  Regional breakdown:")
    for region, counts in summarize_by_region(nodes).items():
        print(f"     {region:<8}: {counts}")

    avg_uptime = sum(n["uptime_pct"] for n in nodes) / len(nodes)
    print(f"\n  Avg network uptime: {avg_uptime:.2f}%")
    print("=" * 60)

# --- Run it ---
print_report(network_inventory)