# Connecting Power BI Desktop to this pipeline

If you have Power BI Desktop, that's the natural place for a "real" dashboard
(instead of the local preview from `dashboard.py`).

## Option A — connect directly to Azure SQL (recommended)
1. Power BI Desktop → **Get Data** → **Azure** → **Azure SQL Database**.
2. Enter the server: the `sql_server_fqdn` value from the Terraform output.
3. Enter the database: the `sql_database_name` value from the Terraform output.
4. Sign in with the SQL admin login/password.
5. Select the `dbo.sales_daily` view (and optionally `dbo.stores`, `dbo.products`) — Power BI will suggest relationships based on the foreign keys automatically.

## Option B — through the HTTP endpoint (Web connector)
1. **Get Data** → **Web**.
2. Enter the address: `https://<function-app-name>.azurewebsites.net/api/sales-summary?code=<function-key>`.
3. Power BI will import the already-aggregated JSON.

## Sample DAX measures (paste after importing the data)

```
Sales Value = SUMX(sales_daily, sales_daily[units_sold] * sales_daily[unit_price])

Sales Last 7 Days = 
CALCULATE(
    [Sales Value],
    DATESINPERIOD(sales_daily[sale_date], MAX(sales_daily[sale_date]), -7, DAY)
)
```

## Suggested visuals
- Bar chart: sales value by store
- Line chart: daily sales value trend
- KPI card: total sales for the current month
- Table: top 5 products by units sold
