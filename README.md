# SWYNEX Data Cleaning & Preparation

Task 1 of my SWYNEX Technologies internship: clean a raw dataset and document every change.

## Dataset
`raw_orders.csv` is a **synthetic e-commerce orders dataset** (535 rows, 13 columns) created with `generate_raw_data.py` (seeded, so it is reproducible). It deliberately contains the data-quality issues found in real exports.

## Issues found and how they were fixed

| Issue | Example in raw data | Fix |
|---|---|---|
| Duplicate records | 35 exact/near-duplicate rows (same order, name in different case) | Normalised text, dropped duplicates, kept first `order_id` |
| Missing values | email (28), phone (46), city (25), date (9), quantity (27), unit_price (22), payment (17), rating (52) | Price → median of same product; quantity/rating → median; city/payment → `Unknown`; email/phone → `not_provided`; rows with no valid date dropped |
| Incorrect data types | `unit_price` as `Rs. 1,299` / `₹799`; quantity as `two`; dates stored as text | Converted to numeric / datetime |
| Inconsistent values | `bangalore`, `BENGALURU`, `Hyd`, `COD`, `cc`, `upi`, `delivered` | Mapped to one standard label per category |
| Mixed date formats | `2025-12-06`, `17/12/2025`, `17-Dec-2025`, `12-17-25` | Parsed each format, output ISO `YYYY-MM-DD` |
| Invalid values | quantity `-1`/`0`, rating `9`/`0`, email without `@`, impossible date `31/02/2025`, phone with `+91-` | Set invalid to missing, then handled as above; phone prefix stripped |
| Whitespace / casing | `"  ARJUN RAO "` | Trimmed, Title Case |

Result: **535 rows → 479 rows, 0 missing values**, correct data types, and a new `total_amount` column (`quantity × unit_price`).

## Files
- `raw_orders.csv` – messy input
- `clean_data.py` – cleaning script (Python + pandas)
- `cleaned_orders.csv` – final cleaned dataset
- `generate_raw_data.py` – script used to create the raw data

## How to run
```bash
pip install pandas numpy
python generate_raw_data.py   # optional: regenerates raw_orders.csv
python clean_data.py          # produces cleaned_orders.csv
```
