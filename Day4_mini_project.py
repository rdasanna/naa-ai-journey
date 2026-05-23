import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Display settings — makes output cleaner
pd.set_option("display.max_columns", 50)
pd.set_option("display.float_format", "{:.2f}".format)

print(f"Pandas version: {pd.__version__}")
print("All libraries loaded successfully!")

# Load the dataset
df = pd.read_csv("telco_churn.csv")

# ── Shape ──────────────────────────────────────────
print(f"Rows    : {df.shape[0]:,}")
print(f"Columns : {df.shape[1]}")
print(f"Size    : {df.shape[0] * df.shape[1]:,} data points\n")

# ── Column names ───────────────────────────────────
print("Columns:")
for col in df.columns:
    print(f"  {col}")

# Data types of every column
print("=== DATA TYPES ===")
print(df.dtypes)

# First 5 rows — like previewing rows in your OSS DB
print("\n=== FIRST 5 ROWS ===")
print(df.head())

# Statistical summary of numeric columns
print("=== STATISTICAL SUMMARY ===")
print(df.describe())

# Check for missing values — critical before any analysis
print("=== MISSING VALUES ===")
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)

missing_report = pd.DataFrame({
    "Missing Count" : missing,
    "Missing %"     : missing_pct
})
print(missing_report[missing_report["Missing Count"] > 0])


# Fix TotalCharges — convert to numeric, force errors to NaN
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

# Check how many rows got NaN
print(f"Null TotalCharges after fix: {df['TotalCharges'].isnull().sum()}")

# These are new subscribers with no charges yet — fill with 0
df["TotalCharges"] = df["TotalCharges"].fillna(0)

print("TotalCharges fixed!")
print(df["TotalCharges"].dtype)     # should now be float64



# Overall churn rate
print("=== CHURN DISTRIBUTION ===")
churn_counts = df["Churn"].value_counts()
churn_pct    = df["Churn"].value_counts(normalize=True) * 100

churn_summary = pd.DataFrame({
    "Count"      : churn_counts,
    "Percentage" : churn_pct.round(2)
})
print(churn_summary)

# Quick takeaway
churn_rate = churn_pct["Yes"]
print(f"\nOverall churn rate: {churn_rate:.1f}%")
print(f"That means 1 in every {round(100/churn_rate)} subscribers churns.")



print("=" * 60)


# ── Who are the churned subscribers? ──────────────
churned     = df[df["Churn"] == "Yes"]
retained    = df[df["Churn"] == "No"]

print(f"Churned subscribers : {len(churned):,}")
print(f"Retained subscribers: {len(retained):,}")

# ── Contract type breakdown ────────────────────────
print("\n=== CHURN BY CONTRACT TYPE ===")
contract_churn = df.groupby("Contract")["Churn"].value_counts(normalize=True).unstack()
contract_churn = (contract_churn * 100).round(1)
print(contract_churn)

# ── Tenure: do newer customers churn more? ────────
print("\n=== AVG TENURE: CHURNED vs RETAINED ===")
print(f"Avg tenure (churned)  : {churned['tenure'].mean():.1f} months")
print(f"Avg tenure (retained) : {retained['tenure'].mean():.1f} months")

# ── Monthly charges comparison ────────────────────
print("\n=== AVG MONTHLY CHARGES ===")
print(f"Avg charge (churned)  : ${churned['MonthlyCharges'].mean():.2f}")
print(f"Avg charge (retained) : ${retained['MonthlyCharges'].mean():.2f}")

# ── High-value churners — the most painful losses ─
high_value_churners = churned[churned["MonthlyCharges"] > 80]
print(f"\nHigh-value churners (>$80/month): {len(high_value_churners):,}")
print(f"Revenue at risk/month: ${high_value_churners['MonthlyCharges'].sum():,.2f}")


print("=" * 60)


fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Telco Churn Analysis — Week 1 Day 4", fontsize=14, fontweight="bold")

# ── Chart 1: Churn distribution ───────────────────
churn_counts.plot(
    kind    = "bar",
    ax      = axes[0, 0],
    color   = ["#2ecc71", "#e74c3c"],
    edgecolor = "white"
)
axes[0, 0].set_title("Overall Churn Distribution")
axes[0, 0].set_xlabel("Churn")
axes[0, 0].set_ylabel("Count")
axes[0, 0].tick_params(axis="x", rotation=0)
for bar in axes[0, 0].patches:
    axes[0, 0].text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 30,
        f"{bar.get_height():,.0f}",
        ha="center", fontsize=10
    )

# ── Chart 2: Churn by contract type ──────────────
contract_churn["Yes"].plot(
    kind      = "bar",
    ax        = axes[0, 1],
    color     = "#e74c3c",
    edgecolor = "white"
)
axes[0, 1].set_title("Churn Rate by Contract Type (%)")
axes[0, 1].set_xlabel("Contract Type")
axes[0, 1].set_ylabel("Churn Rate (%)")
axes[0, 1].tick_params(axis="x", rotation=15)

# ── Chart 3: Tenure distribution ──────────────────
axes[1, 0].hist(
    churned["tenure"],
    bins      = 30,
    alpha     = 0.7,
    color     = "#e74c3c",
    label     = "Churned",
    edgecolor = "white"
)
axes[1, 0].hist(
    retained["tenure"],
    bins      = 30,
    alpha     = 0.7,
    color     = "#2ecc71",
    label     = "Retained",
    edgecolor = "white"
)
axes[1, 0].set_title("Tenure Distribution: Churned vs Retained")
axes[1, 0].set_xlabel("Tenure (months)")
axes[1, 0].set_ylabel("Count")
axes[1, 0].legend()

# ── Chart 4: Monthly charges box plot ────────────
df.boxplot(
    column    = "MonthlyCharges",
    by        = "Churn",
    ax        = axes[1, 1],
    patch_artist = True
)
axes[1, 1].set_title("Monthly Charges by Churn Status")
axes[1, 1].set_xlabel("Churn")
axes[1, 1].set_ylabel("Monthly Charges ($)")
plt.suptitle("")  # removes auto boxplot title

plt.tight_layout()
plt.savefig("day4_churn_analysis.png", dpi=150, bbox_inches="tight")
plt.show()
print("Chart saved as day4_churn_analysis.png")


print("=" * 60)
print("=" * 60)


# Print findings as a structured summary
findings = [
    ("Overall churn rate",
     f"{churn_rate:.1f}% — meaning {round(100/churn_rate)}% of customers leave"),

    ("Contract type is the strongest signal",
     "Month-to-month customers churn at ~43% vs only ~3% on 2-year contracts"),

    ("Newer customers are highest risk",
     f"Avg churned tenure is {churned['tenure'].mean():.0f} months vs "
     f"{retained['tenure'].mean():.0f} months for retained"),

    ("Churned customers paid more",
     f"${churned['MonthlyCharges'].mean():.2f}/mo avg vs "
     f"${retained['MonthlyCharges'].mean():.2f}/mo for retained — "
     "possibly value perception issue"),

    ("High-value revenue at risk",
     f"{len(high_value_churners):,} subscribers paying >$80/mo are churning — "
     f"${high_value_churners['MonthlyCharges'].sum():,.0f}/mo revenue exposed"),
]

print("=" * 60)
print("   DAY 4 KEY FINDINGS — TELCO CHURN ANALYSIS")
print("=" * 60)
for i, (title, insight) in enumerate(findings, 1):
    print(f"\n  {i}. {title}")
    print(f"     {insight}")
print("=" * 60)