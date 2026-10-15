"""Generates a deliberately messy synthetic customer-orders dataset (raw_orders.csv)."""
import random, csv
from datetime import date, timedelta
random.seed(42)

cities = {"Bengaluru": ["Bengaluru","bangalore","BENGALURU","Bangalore "],
          "Chennai": ["Chennai","chennai","MADRAS","Chennai "],
          "Hyderabad": ["Hyderabad","hyderabad","HYDERABAD","Hyd"],
          "Mumbai": ["Mumbai","bombay","MUMBAI","Mumbai "],
          "Delhi": ["Delhi","New Delhi","DELHI","delhi"]}
products = {"Wireless Mouse":799,"Mechanical Keyboard":2499,"USB-C Hub":1299,"Laptop Stand":999,
            "Webcam HD":1899,"Bluetooth Speaker":1599,"Phone Case":299,"Power Bank":1499}
pay_variants = {"UPI":["UPI","upi","Upi","U.P.I"],"Credit Card":["Credit Card","credit card","CC","credit_card"],
                "Cash on Delivery":["Cash on Delivery","COD","cod","Cash On Delivery"],
                "Net Banking":["Net Banking","netbanking","NET BANKING"]}
status_variants = ["Delivered","delivered","DELIVERED","Shipped","shipped","Cancelled","cancelled","Returned","Pending"]
first = ["Aarav","Vivaan","Ananya","Diya","Rohan","Priya","Karthik","Sneha","Arjun","Meera","Ishaan","Kavya","Rahul","Pooja","Vikram","Nisha"]
last = ["Sharma","Reddy","Iyer","Nair","Patel","Gupta","Kumar","Singh","Rao","Menon"]

def fmt_date(d):
    return random.choice([d.strftime("%Y-%m-%d"), d.strftime("%d/%m/%Y"), d.strftime("%d-%b-%Y"), d.strftime("%m-%d-%y")])

rows = []
start = date(2025, 1, 1)
for i in range(1, 501):
    name = f"{random.choice(first)} {random.choice(last)}"
    cid = f"C{random.randint(1000,1150)}"
    city_key = random.choice(list(cities))
    prod = random.choice(list(products))
    qty = random.choice([1,1,1,2,2,3,4,5])
    price = products[prod]
    d = start + timedelta(days=random.randint(0, 420))
    pay = random.choice(random.choice(list(pay_variants.values())))
    email = f"{name.lower().replace(' ','.')}@example.com"
    phone = "".join(random.choice("6789") if k==0 else random.choice("0123456789") for k in range(10))
    row = {"order_id": f"ORD{10000+i}", "customer_id": cid, "customer_name": name,
           "email": email, "phone": phone, "city": random.choice(cities[city_key]),
           "order_date": fmt_date(d), "product": prod, "quantity": qty,
           "unit_price": price, "payment_method": pay,
           "order_status": random.choice(status_variants),
           "rating": random.choice([1,2,3,4,5,5,4,4,3])}
    # --- inject problems ---
    r = random.random()
    if r < 0.06: row["email"] = ""                            # missing
    elif r < 0.09: row["email"] = row["email"].replace("@","")  # invalid
    if random.random() < 0.07: row["phone"] = ""
    elif random.random() < 0.04: row["phone"] = "+91-" + row["phone"]
    if random.random() < 0.05: row["quantity"] = ""
    if random.random() < 0.03: row["quantity"] = random.choice(["two","three","-1","0"])
    if random.random() < 0.05: row["unit_price"] = ""
    if random.random() < 0.04: row["unit_price"] = f"Rs. {price:,}"
    if random.random() < 0.03: row["unit_price"] = f"₹{price}"
    if random.random() < 0.08: row["rating"] = ""
    if random.random() < 0.02: row["rating"] = random.choice(["9","0","N/A"])
    if random.random() < 0.04: row["city"] = ""
    if random.random() < 0.03: row["payment_method"] = ""
    if random.random() < 0.03: row["order_date"] = ""
    if random.random() < 0.03: row["order_date"] = "31/02/2025"   # impossible date
    if random.random() < 0.05: row["customer_name"] = "  " + row["customer_name"].upper() + " "
    rows.append(row)

# duplicates (exact + near)
for r in random.sample(rows, 25): rows.append(dict(r))
for r in random.sample(rows, 10):
    c = dict(r); c["customer_name"] = c["customer_name"].lower(); rows.append(c)
random.shuffle(rows)
with open("raw_orders.csv","w",newline="",encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print("raw_orders.csv rows:", len(rows))
