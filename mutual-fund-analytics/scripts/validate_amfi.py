import pandas as pd

fund_master = pd.read_csv("Data/raw/01_fund_master.csv")
nav_history = pd.read_csv("Data/raw/02_nav_history.csv")

print("FUND MASTER COLUMNS")
print(fund_master.columns.tolist())

print("\nNAV HISTORY COLUMNS")
print(nav_history.columns.tolist())
import pandas as pd

print("="*50)
print("AMFI VALIDATION STARTED")
print("="*50)

fund_master = pd.read_csv("Data/raw/01_fund_master.csv")

live_nav = pd.read_csv("Data/raw/live_nav_hdfc_top100.csv")

print("Fund Master Records :", len(fund_master))
print("Live NAV Records :", len(live_nav))

matched = fund_master[
    fund_master["scheme_name"]
    .str.contains("Top 100", case=False, na=False)
]

print("\nMatching Schemes Found:")
print(matched[["amfi_code", "scheme_name"]])

print("\nLive NAV Sample:")
print(live_nav.head())

print("\nAMFI VALIDATION COMPLETED")
print("="*50)