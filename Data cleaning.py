import pandas as pd

# -----------------------------
# File Path
# -----------------------------
base_path = r"C:\Users\explo\Desktop\lpg_dashboard_project\data\\"

# -----------------------------
# Load datasets
# -----------------------------
production = pd.read_csv(base_path + "lpg_production.csv")
consumption = pd.read_csv(base_path + "lpg_consumption.csv")
imports = pd.read_csv(base_path + "lpg_imports.csv")
prices = pd.read_csv(base_path + "lpg_prices.csv")
crude = pd.read_csv(base_path + "crude_oil_prices.csv")
inflation = pd.read_csv(base_path + "inflation.csv")
subsidy = pd.read_csv(base_path + "lpg_subsidy.csv")
ujjwala = pd.read_csv(base_path + "pm_ujjwala.csv")

# -----------------------------
# Clean function (IMPORTANT)
# -----------------------------
def clean(df):
    # Clean column names
    df.columns = df.columns.str.strip().str.replace(" ", "_")

    # Fix Year column (handles strings, spaces, fiscal years)
    df["Year"] = df["Year"].astype(str).str.strip()
    df["Year"] = df["Year"].str[:4]  # handles '2010-11'
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

    # Drop invalid years
    df = df.dropna(subset=["Year"])
    df["Year"] = df["Year"].astype(int)

    return df

# -----------------------------
# Apply cleaning (FIXED)
# -----------------------------
production = clean(production)
consumption = clean(consumption)
imports = clean(imports)
prices = clean(prices)
crude = clean(crude)
inflation = clean(inflation)
subsidy = clean(subsidy)
ujjwala = clean(ujjwala)

# -----------------------------
# DEBUG (optional - remove later)
# -----------------------------
print("Inflation Preview:")
print(inflation.head())
print(inflation.dtypes)

# -----------------------------
# Merge datasets (LEFT JOIN)
# -----------------------------
df = production.merge(consumption, on="Year", how="left") \
    .merge(imports, on="Year", how="left") \
    .merge(prices, on="Year", how="left") \
    .merge(crude, on="Year", how="left") \
    .merge(inflation, on="Year", how="left") \
    .merge(subsidy, on="Year", how="left") \
    .merge(ujjwala, on="Year", how="left")

# -----------------------------
# Convert numeric columns
# -----------------------------
numeric_cols = [
    "Production_MMT",
    "Consumption_MMT",
    "Imports_MMT",
    "Price_INR",
    "Crude_Price_USD",
    "Inflation_Rate",
    "Subsidy_Crore",
    "Beneficiaries_Million"
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# -----------------------------
# Feature Engineering (KPIs)
# -----------------------------

# Import Dependency %
df["Import_Dependency_%"] = (df["Imports_MMT"] / df["Consumption_MMT"]) * 100

# Consumption Growth %
df["Consumption_Growth_%"] = df["Consumption_MMT"].pct_change() * 100

# Price vs Crude Ratio
df["Price_to_Crude_Ratio"] = df["Price_INR"] / df["Crude_Price_USD"]

# Subsidy per Consumption
df["Subsidy_per_MMT"] = df["Subsidy_Crore"] / df["Consumption_MMT"]

# -----------------------------
# Handle missing values (optional)
# -----------------------------
df["Consumption_Growth_%"].fillna(0, inplace=True)

# -----------------------------
# Sort data
# -----------------------------
df = df.sort_values("Year")

# -----------------------------
# Keep only required columns
# -----------------------------
final_cols = [
    "Year",
    "Production_MMT",
    "Consumption_MMT",
    "Imports_MMT",
    "Price_INR",
    "Crude_Price_USD",
    "Inflation_Rate",
    "Subsidy_Crore",
    "Beneficiaries_Million",
    "Import_Dependency_%",
    "Consumption_Growth_%",
    "Price_to_Crude_Ratio",
    "Subsidy_per_MMT"
]

df = df[final_cols]

# -----------------------------
# Final validation
# -----------------------------
print("\nMissing Values:\n", df.isnull().sum())
print("\nData Types:\n", df.dtypes)

# -----------------------------
# Save final dataset
# -----------------------------
output_path = base_path + "final_lpg_dataset.csv"
df.to_csv(output_path, index=False)

print("\n✅ FINAL CLEAN DATASET CREATED SUCCESSFULLY!")
print(f"📁 Saved at: {output_path}")