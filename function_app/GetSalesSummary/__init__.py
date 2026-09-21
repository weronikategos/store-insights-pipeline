"""
HTTP endpoint: GET /api/sales-summary?days=7

Returns aggregated sales (value and unit count) broken down by store for
the last N days. Can be used as a data source for Power BI (Web connector)
or for any frontend/dashboard.
"""
import os
import json
import logging

import azure.functions as func
import pyodbc


def get_connection():
    conn_str = os.environ["SQL_CONNECTION_STRING"]
    return pyodbc.connect(conn_str)


def main(req: func.HttpRequest) -> func.HttpResponse:
    days = int(req.params.get("days", 7))
    logging.info("Fetching sales summary for the last %d days", days)

    query = """
        SELECT
            s.store_id,
            st.store_name,
            SUM(s.units_sold) AS total_units,
            SUM(s.units_sold * s.unit_price) AS total_value
        FROM dbo.sales_daily s
        JOIN dbo.stores st ON st.store_id = s.store_id
        WHERE s.sale_date >= DATEADD(day, -?, CAST(GETDATE() AS date))
        GROUP BY s.store_id, st.store_name
        ORDER BY total_value DESC
    """

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, days)
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
    finally:
        conn.close()

    return func.HttpResponse(
        json.dumps(results, default=str, ensure_ascii=False),
        mimetype="application/json",
        status_code=200,
    )
