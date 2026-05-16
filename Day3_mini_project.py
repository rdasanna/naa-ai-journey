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



# Challenges .... 

# Challenge 1: Regional drill-down

def filter_by_region(nodes, region):
    """Returns only nodes from the specified region (case-insensitive)."""
    return [node for node in nodes if node["region"].lower() == region.lower()]


west_nodes = filter_by_region(network_inventory, "West")
print(f"West region nodes ({len(west_nodes)} found):")
for node in west_nodes:
    print(f"  {node['id']} — {get_status(node)}")

print(len(filter_by_region(network_inventory, "west")))    # 2
print(len(filter_by_region(network_inventory, "WEST")))    # 2
print(len(filter_by_region(network_inventory, "West")))    # 2

# Challenge 2: Most critical node

# Approach 1: manual loop (easier to read when learning)
def most_critical_node_loop(nodes):
    """Returns the node with the lowest uptime percentage."""
    worst_node   = nodes[0]          # start by assuming first is worst
    worst_uptime = nodes[0]["uptime_pct"]

    for node in nodes:
        if node["uptime_pct"] < worst_uptime:
            worst_uptime = node["uptime_pct"]
            worst_node   = node

    return worst_node

# Approach 2: Pythonic one-liner (how experienced engineers write it)
def most_critical_node(nodes):
    """Returns the node with the lowest uptime percentage."""
    return min(nodes, key=lambda node: node["uptime_pct"])

# Test both — they should return identical results
result_loop = most_critical_node_loop(network_inventory)
result_fast = most_critical_node(network_inventory)

print(f"Loop result : {result_loop['id']}")
print(f"Fast result : {result_fast['id']}")

# Full report on the worst node
worst = most_critical_node(network_inventory)
alarm = worst["last_alarm"] or "No alarm recorded"
print(f"\n!! Most critical node !!")
print(f"  ID       : {worst['id']}")
print(f"  Region   : {worst['region']}")
print(f"  Uptime   : {worst['uptime_pct']}%")
print(f"  Errors   : {worst['error_rate']}")
print(f"  Status   : {get_status(worst)}")
print(f"  Alarm    : {alarm}")


def top_n_critical(nodes, n=3):
    """Returns the N nodes with the lowest uptime."""
    sorted_nodes = sorted(nodes, key=lambda node: node["uptime_pct"])
    return sorted_nodes[:n]

print("\nTop 3 most critical nodes:")
for i, node in enumerate(top_n_critical(network_inventory, 3), start=1):
    print(f"  #{i}: {node['id']} — {node['uptime_pct']}% uptime")


# Challenge 3: Export to CSV


    # Level 1: Basic CSV print (good starting point)
def export_summary_basic(nodes):
    """Prints nodes as CSV to the console."""
    print("id,region,type,uptime_pct,error_rate,status,last_alarm")
    for node in nodes:
        status    = get_status(node)
        alarm     = node["last_alarm"] or "None"
        print(f"{node['id']},{node['region']},{node['type']},"
              f"{node['uptime_pct']},{node['error_rate']},{status},{alarm}")

export_summary_basic(network_inventory)


# Level 2: Write to an actual .csv file (this is what pipelines do)
import csv

def export_summary_to_file(nodes, filename="network_health.csv"):
    """Writes nodes to a real CSV file."""
    fieldnames = ["id", "region", "type", "uptime_pct",
                  "error_rate", "status", "last_alarm"]

    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for node in nodes:
            writer.writerow({
                "id"         : node["id"],
                "region"     : node["region"],
                "type"       : node["type"],
                "uptime_pct" : node["uptime_pct"],
                "error_rate" : node["error_rate"],
                "status"     : get_status(node),
                "last_alarm" : node["last_alarm"] or "None"
            })

    print(f"Exported {len(nodes)} nodes to '{filename}'")

export_summary_to_file(network_inventory)
# Check your folder — network_health.csv now exists!

# Level 3: Read it back and verify (close the loop)
import csv

def read_exported_csv(filename="network_health.csv"):
    """Reads and prints the exported CSV back."""
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        rows   = list(reader)

    print(f"Read {len(rows)} rows from '{filename}'")
    print(f"Columns: {list(rows[0].keys())}")
    print(f"\nFirst row: {rows[0]}")
    return rows

data = read_exported_csv()




def print_report_v2(nodes):
    """Enhanced report using all 3 challenge functions."""
    print("=" * 60)
    print("      NETWORK HEALTH REPORT v2 — OSS DAILY SUMMARY")
    print("=" * 60)

    healthy  = [n for n in nodes if get_status(n) == "Healthy"]
    degraded = [n for n in nodes if get_status(n) == "Degraded"]
    critical = [n for n in nodes if get_status(n) == "Critical"]

    print(f"\n  Total nodes : {len(nodes)}")
    print(f"  Healthy     : {len(healthy)}")
    print(f"  Degraded    : {len(degraded)}")
    print(f"  Critical    : {len(critical)}")

    # Challenge 2: most critical node
    worst = most_critical_node(nodes)
    print(f"\n  Most critical node: {worst['id']} "
          f"({worst['uptime_pct']}% uptime)")

    # Challenge 1: regional drill-down
    print(f"\n  Regional drill-down:")
    for region in ["East", "West", "South"]:
        region_nodes = filter_by_region(nodes, region)
        region_crit  = [n for n in region_nodes if get_status(n) == "Critical"]
        print(f"    {region:<8}: {len(region_nodes)} nodes, "
              f"{len(region_crit)} critical")

    # Challenge 3: export
    export_summary_to_file(nodes)
    print(f"\n  CSV report saved.")
    print("=" * 60)

print_report_v2(network_inventory)