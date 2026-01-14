import os, sqlite3, random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

random.seed(7)
np.random.seed(7)

DB = "data/case.db"
os.makedirs("data", exist_ok=True)

schema = open("sql/schema.sql", "r", encoding="utf-8").read()

customers = pd.DataFrame({
    "customer_id": range(1, 401),
    "customer_name": [f"Customer {i:03d}" for i in range(1, 401)],
    "country": np.random.choice(["AR","ES","UY","CL"], size=400, p=[0.55,0.30,0.08,0.07]),
    "segment": np.random.choice(["Retail","Online","Wholesale"], size=400, p=[0.55,0.35,0.10]),
    "created_at": pd.to_datetime("2024-01-01") + pd.to_timedelta(np.random.randint(0, 365, size=400), unit="D")
})
customers["created_at"] = customers["created_at"].dt.strftime("%Y-%m-%d")

products = pd.DataFrame({
    "product_id": range(1, 41),
    "product_name": [f"Product {i:02d}" for i in range(1, 41)],
    "category": np.random.choice(["Cremas","Higiene","Perfumería","Dermocosmética"], size=40, p=[0.35,0.30,0.20,0.15])
})

start = datetime(2025,1,1)
orders = []
order_items = []
order_id = 1

for _ in range(4200):
    cid = random.randint(1, 400)
    d = start + timedelta(days=random.randint(0, 360))
    channel = random.choices(["web","store","marketplace"], weights=[0.45,0.40,0.15])[0]
    orders.append([order_id, cid, d.strftime("%Y-%m-%d"), channel])

    n_items = random.randint(1, 4)
    chosen = random.sample(range(1, 41), n_items)
    for pid in chosen:
        qty = random.randint(1, 5)
        price = random.choice([800,950,1200,1500,1800,2200,2600])
        cost = round(price * random.uniform(0.45,0.80), 2)
        order_items.append([order_id, pid, qty, float(price), float(cost)])

    order_id += 1

orders = pd.DataFrame(orders, columns=["order_id","customer_id","order_date","channel"])
order_items = pd.DataFrame(order_items, columns=["order_id","product_id","qty","unit_price","unit_cost"])

with sqlite3.connect(DB) as con:
    con.executescript(schema)
    customers.to_sql("customers", con, if_exists="append", index=False)
    products.to_sql("products", con, if_exists="append", index=False)
    orders.to_sql("orders", con, if_exists="append", index=False)
    order_items.to_sql("order_items", con, if_exists="append", index=False)

print("OK - Built SQLite DB at", DB)
