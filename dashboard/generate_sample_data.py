"""
Generates a sample sales CSV file — for a local dashboard preview without
having to deploy anything to Azure. Mirrors the structure of the
dbo.sales_daily table in Azure SQL.
"""
import csv
import random
import datetime as dt

STORES = ["Downtown Store", "West Store", "East Store", "South Store"]
PRODUCTS = [("Product A", 10.0), ("Product B", 5.0), ("Product C", 20.0), ("Product D", 3.0)]

random.seed(42)

rows = []
start = dt.date.today() - dt.timedelta(days=30)
for i in range(30):
    day = start + dt.timedelta(days=i)
    for store in STORES:
        for product, price in PRODUCTS:
            units = random.randint(0, 80)
            rows.append([day.isoformat(), store, product, units, price, round(units * price, 2)])

with open("sample_sales.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["sale_date", "store_name", "product_name", "units_sold", "unit_price", "value"])
    writer.writerows(rows)

print(f"Generated {len(rows)} rows into sample_sales.csv")
