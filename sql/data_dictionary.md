# Mutual Fund Analytics - Data Dictionary

## 01_fund_master.csv

| Column | Description |
|----------|------------|
| amfi_code | Unique AMFI scheme code |
| fund_house | Asset management company |
| scheme_name | Name of mutual fund scheme |
| category | Fund category |
| sub_category | Fund sub category |
| plan | Direct/Regular plan |
| launch_date | Launch date |
| benchmark | Benchmark index |
| expense_ratio_pct | Expense ratio (%) |
| exit_load_pct | Exit load (%) |
| min_sip_amount | Minimum SIP amount |
| min_lumpsum_amount | Minimum lumpsum amount |
| fund_manager | Fund manager name |
| risk_category | Risk category |
| sebi_category_code | SEBI category code |

---

## 02_nav_history.csv

| Column | Description |
|----------|------------|
| amfi_code | Scheme code |
| date | NAV date |
| nav | Net Asset Value |

---

## 08_investor_transactions.csv

Contains investor purchase, redemption and SIP transaction details.

---

## 07_scheme_performance.csv

Contains annual return and performance metrics of schemes.

---

## Live NAV Dataset

Generated using AMFI API.

File:

live_nav_hdfc_top100.csv

Columns:

- date
- nav
