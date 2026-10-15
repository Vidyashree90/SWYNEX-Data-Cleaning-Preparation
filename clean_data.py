"""SWYNEX Task 1 - Data Cleaning & Preparation
import re
import pandas as pd
import numpy as np

raw = pd.read_csv("raw_orders.csv", dtype=str, keep_default_na=False)
df = raw.copy()
log = {}

# 0. Profile: blanks -> NaN, strip whitespace
df = df.apply(lambda c: c.str.strip()).replace({"": np.nan, "N/A": np.nan})
log["missing_before"] = df.isna().sum().to_dict()

# 1. Duplicates (case-insensitive on text, then drop)
df["customer_name"] = df["customer_name"].str.title()
before = len(df)
df = df.drop_duplicates().drop_duplicates(subset=["order_id"], keep="first")
log["duplicates_removed"] = before - len(df)

# 2. Inconsistent values
city_map = {"bangalore": "Bengaluru", "bengaluru": "Bengaluru", "chennai": "Chennai", "madras": "Chennai",
            "hyderabad": "Hyderabad", "hyd": "Hyderabad", "mumbai": "Mumbai", "bombay": "Mumbai",
            "delhi": "Delhi", "new delhi": "Delhi"}
df["city"] = df["city"].str.lower().map(city_map)

pay_map = {"upi": "UPI", "u.p.i": "UPI", "credit card": "Credit Card", "credit_card": "Credit Card",
           "cc": "Credit Card", "cod": "Cash on Delivery", "cash on delivery": "Cash on Delivery",
           "net banking": "Net Banking", "netbanking": "Net Banking"}
df["payment_method"] = df["payment_method"].str.lower().map(pay_map)
df["order_status"] = df["order_status"].str.title()

# 3. Incorrect data types
def to_number(s):
    if pd.isna(s): return np.nan
    words = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
    s = s.lower()
    if s in words: return words[s]
    s = re.sub(r"[^\d.\-]", "", s)          # strip Rs., ₹, commas
    return float(s) if s not in ("", "-", ".") else np.nan

for col in ["quantity", "unit_price", "rating"]:
    df[col] = df[col].apply(to_number)

def parse_date(s):
    if pd.isna(s): return pd.NaT
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%b-%Y", "%m-%d-%y"):
        try: return pd.to_datetime(s, format=fmt)
        except ValueError: continue
    return pd.NaT                           # impossible dates e.g. 31/02/2025
df["order_date"] = df["order_date"].apply(parse_date)

# 4. Invalid values -> NaN
df.loc[~df["quantity"].between(1, 100), "quantity"] = np.nan
df.loc[~df["rating"].between(1, 5), "rating"] = np.nan
df.loc[df["unit_price"] <= 0, "unit_price"] = np.nan
df["phone"] = df["phone"].str.replace(r"^\+91-?", "", regex=True)
df.loc[~df["phone"].fillna("").str.fullmatch(r"[6-9]\d{9}"), "phone"] = np.nan
df.loc[~df["email"].fillna("").str.contains(r"^[^@\s]+@[^@\s]+\.[^@\s]+$"), "email"] = np.nan

# 5. Handle missing values
price_by_product = df.groupby("product")["unit_price"].transform("median")
df["unit_price"] = df["unit_price"].fillna(price_by_product)          # impute from product median
df["quantity"] = df["quantity"].fillna(df["quantity"].median())       # median
df["quantity"] = df["quantity"].astype(int)
df["rating"] = df["rating"].fillna(df["rating"].median()).astype(int)
df["city"] = df["city"].fillna("Unknown")
df["payment_method"] = df["payment_method"].fillna("Unknown")
df["email"] = df["email"].fillna("not_provided")
df["phone"] = df["phone"].fillna("not_provided")
df = df.dropna(subset=["order_date"])                                 # date is essential -> drop row

# 6. Derived column + final format
df["total_amount"] = df["quantity"] * df["unit_price"]
df["order_date"] = df["order_date"].dt.strftime("%Y-%m-%d")
df = df.sort_values("order_id").reset_index(drop=True)
df.to_csv("cleaned_orders.csv", index=False)

log["rows_before"], log["rows_after"] = len(raw), len(df)
log["missing_after"] = df.isna().sum().to_dict()
print("=== CLEANING REPORT ===")
for k, v in log.items(): print(k, ":", v)
print(df.dtypes)
