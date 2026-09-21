"""
Runs daily at 5:00 AM (timer trigger).

In a real system, this trigger would pull sales data from a source system
(e.g. SAP, an ERP, or point-of-sale APIs). Here — for portfolio purposes —
it generates realistic-looking synthetic data and writes it to Azure SQL,
so the whole pipeline can be run and tested without access to real
company systems.
"""
import os
import random
import logging
import datetime as dt

import azure.functions as func
import pyodbc

STORES = [
    (1, "Downtown Store"),
    (2, "West Store"),
    (3, "East Store"),
    (4, "South Store"),
]

PRODUCTS = [
    (1, "Product A", 10.0),
    (2, "Product B", 5.0),
    (3, "Product C", 20.0),
    (4, "Product D", 3.0),
]


def get_connection():
    conn_str = os.environ["SQL_CONNECTION_STRING"]
    return pyodbc.connect(conn_str)


def generate_rows(target_date: dt.date):
    rows = []
    for store_id, _ in STORES:
        for product_id, _, unit_price in PRODUCTS:
            units_sold = random.randint(0, 80)
            rows.append((target_date, store_id, product_id, units_sold, unit_price))
    return rows


def main(mytimer: func.TimerRequest) -> None:
    target_date = dt.date.today() - dt.timedelta(days=1)
    logging.info("Generating sales data for %s", target_date)

    rows = generate_rows(target_date)

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.executemany(
            """
            INSERT INTO dbo.sales_daily
                (sale_date, store_id, product_id, units_sold, unit_price)
            VALUES (?, ?, ?, ?, ?)
            """,
            rows,
        )
        conn.commit()
        logging.info("Wrote %d rows to sales_daily.", len(rows))
    finally:
        conn.close()
