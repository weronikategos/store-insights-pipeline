-- Database schema for the Store Insights pipeline.
-- Run this once after creating the database (e.g. via Azure Data Studio / sqlcmd / the Azure portal).

CREATE TABLE dbo.stores (
    store_id    INT PRIMARY KEY,
    store_name  NVARCHAR(100) NOT NULL,
    city        NVARCHAR(100) NOT NULL
);

CREATE TABLE dbo.products (
    product_id  INT PRIMARY KEY,
    product_name NVARCHAR(100) NOT NULL,
    unit_price  DECIMAL(10, 2) NOT NULL
);

CREATE TABLE dbo.sales_daily (
    id          INT IDENTITY(1,1) PRIMARY KEY,
    sale_date   DATE NOT NULL,
    store_id    INT NOT NULL FOREIGN KEY REFERENCES dbo.stores(store_id),
    product_id  INT NOT NULL FOREIGN KEY REFERENCES dbo.products(product_id),
    units_sold  INT NOT NULL,
    unit_price  DECIMAL(10, 2) NOT NULL
);

CREATE INDEX idx_sales_daily_date ON dbo.sales_daily(sale_date);
CREATE INDEX idx_sales_daily_store ON dbo.sales_daily(store_id);

-- Lookup data (stores and products) — must exist before the
-- GenerateDailySales function starts inserting sales rows.
INSERT INTO dbo.stores (store_id, store_name, city) VALUES
    (1, 'Downtown Store', 'Poznan'),
    (2, 'West Store', 'Poznan'),
    (3, 'East Store', 'Wroclaw'),
    (4, 'South Store', 'Krakow');

INSERT INTO dbo.products (product_id, product_name, unit_price) VALUES
    (1, 'Product A', 10.0),
    (2, 'Product B', 5.0),
    (3, 'Product C', 20.0),
    (4, 'Product D', 3.0);
