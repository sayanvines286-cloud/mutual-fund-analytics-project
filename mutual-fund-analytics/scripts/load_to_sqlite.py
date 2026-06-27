import pandas as pd
import sqlite3

print("="*50)
print("SQLITE LOAD STARTED")
print("="*50)

conn = sqlite3.connect("bluestock_mf.db")

nav = pd.read_csv("Data/processed/clean_nav.csv")
tx = pd.read_csv("Data/processed/clean_transactions.csv")
perf = pd.read_csv("Data/processed/clean_performance.csv")

nav.to_sql(
    "nav_history",
    conn,
    if_exists="replace",
    index=False
)

tx.to_sql(
    "transactions",
    conn,
    if_exists="replace",
    index=False
)

perf.to_sql(
    "performance",
    conn,
    if_exists="replace",
    index=False
)

print("NAV rows:", len(nav))
print("Transaction rows:", len(tx))
print("Performance rows:", len(perf))

conn.close()

print("="*50)
print("DATABASE CREATED")
print("="*50)