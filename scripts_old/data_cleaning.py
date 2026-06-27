import pandas as pd
import os

os.makedirs("Data/processed", exist_ok=True)

print("="*50)
print("DATA CLEANING STARTED")
print("="*50)

# NAV HISTORY
nav = pd.read_csv("Data/raw/02_nav_history.csv")

nav["date"] = pd.to_datetime(nav["date"])

nav = nav.sort_values(["amfi_code", "date"])

nav = nav.drop_duplicates()

nav = nav[nav["nav"] > 0]

nav.to_csv("Data/processed/clean_nav.csv", index=False)

print("NAV cleaned:", nav.shape)

# INVESTOR TRANSACTIONS
tx = pd.read_csv("Data/raw/08_investor_transactions.csv")

tx = tx.drop_duplicates()

tx.to_csv(
    "Data/processed/clean_transactions.csv",
    index=False
)

print("Transactions cleaned:", tx.shape)

# PERFORMANCE DATA
perf = pd.read_csv(
    "Data/raw/07_scheme_performance.csv"
)

perf = perf.drop_duplicates()

perf.to_csv(
    "Data/processed/clean_performance.csv",
    index=False
)

print("Performance cleaned:", perf.shape)

print("="*50)
print("DATA CLEANING COMPLETED")
print("="*50)