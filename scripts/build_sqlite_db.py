from __future__ import annotations

import random
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd


DB = Path("data/case.db")
SCHEMA_PATH = Path("sql/schema.sql")


def build_database(db_path: Path = DB, schema_path: Path = SCHEMA_PATH) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    schema = schema_path.read_text(encoding="utf-8")

    random.seed(7)
    np.random.seed(7)

    customers = pd.DataFrame(
        {
            "customer_id": range(1, 401),
            "customer_name": [f"Customer {i:03d}" for i in range(1, 401)],
            "country": np.random.choice(
                ["AR", "ES", "UY", "CL"],
                size=400,
                p=[0.55, 0.30, 0.08, 0.07],
            ),
            "segment": np.random.choice(
                ["Retail", "Online", "Wholesale"],
                size=400,
                p=[0.55, 0.35, 0.10],
            ),
            "created_at": pd.to_datetime("2024-01-01")
            + pd.to_timedelta(np.random.randint(0, 365, size=400), unit="D"),
        }
    )
    customers["created_at"] = customers["created_at"].dt.strftime("%Y-%m-%d")

    products = pd.DataFrame(
        {
            "product_id": range(1, 41),
            "product_name": [f"Product {i:02d}" for i in range(1, 41)],
            "category": np.random.choice(
                ["Cremas", "Higiene", "Perfumería", "Dermocosmética"],
                size=40,
                p=[0.35, 0.30, 0.20, 0.15],
            ),
        }
    )

    start = datetime(2025, 1, 1)
    orders: list[list[object]] = []
    order_items: list[list[object]] = []

    for order_id in range(1, 4201):
        customer_id = random.randint(1, 400)
        order_date = start + timedelta(days=random.randint(0, 360))
        channel = random.choices(
            ["web", "store", "marketplace"],
            weights=[0.45, 0.40, 0.15],
        )[0]
        orders.append([order_id, customer_id, order_date.strftime("%Y-%m-%d"), channel])

        for product_id in random.sample(range(1, 41), random.randint(1, 4)):
            quantity = random.randint(1, 5)
            price = random.choice([800, 950, 1200, 1500, 1800, 2200, 2600])
            cost = round(price * random.uniform(0.45, 0.80), 2)
            order_items.append(
                [order_id, product_id, quantity, float(price), float(cost)]
            )

    orders_df = pd.DataFrame(
        orders,
        columns=["order_id", "customer_id", "order_date", "channel"],
    )
    items_df = pd.DataFrame(
        order_items,
        columns=["order_id", "product_id", "qty", "unit_price", "unit_cost"],
    )

    with sqlite3.connect(db_path) as connection:
        connection.executescript(schema)
        customers.to_sql("customers", connection, if_exists="append", index=False)
        products.to_sql("products", connection, if_exists="append", index=False)
        orders_df.to_sql("orders", connection, if_exists="append", index=False)
        items_df.to_sql("order_items", connection, if_exists="append", index=False)

    print(f"OK - Built SQLite DB at {db_path}")


def main() -> None:
    build_database()


if __name__ == "__main__":
    main()
