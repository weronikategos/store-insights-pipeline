# Store Insights Pipeline — a sales data pipeline in Azure

A cloud data pipeline: daily sales data lands in Azure SQL through an Azure
Function (timer trigger), and a second function (HTTP trigger) exposes
aggregated data that can be connected directly to Power BI. The whole
infrastructure is defined as code (Terraform), so the environment can be
reproduced with a single command.

## Tech stack and the role of each piece

| Layer | Technology | Role |
|---|---|---|
| Infrastructure | **Terraform** | Declarative description of the whole Azure environment — resource group, storage, function plan, Function App, SQL Server/Database |
| Data processing | **Azure Functions (Python, timer trigger)** | Runs daily to generate/ingest sales data and write it to the database |
| Data API | **Azure Functions (Python, HTTP trigger)** | Exposes aggregated sales data as JSON — a source for Power BI or any other frontend |
| Database | **Azure SQL Database** | Stores sales data, stores, and products in a normalized schema |
| Visualization | **Power BI** (or a local preview in Python/Plotly) | Sales trends, top products, KPI dashboard |
| CI | **GitHub Actions** | Automated Terraform validation (`fmt`, `validate`) and Python linting on every push |

## Repository structure

```
store-insights-pipeline/
├── infra/                      # Terraform — the whole Azure infrastructure
│   ├── providers.tf
│   ├── variables.tf
│   ├── main.tf
│   ├── outputs.tf
│   └── terraform.tfvars.example
├── function_app/
│   ├── GenerateDailySales/     # timer trigger — data generation/ingestion
│   ├── GetSalesSummary/        # HTTP trigger — aggregation API
│   ├── host.json
│   └── requirements.txt
├── sql/
│   └── schema.sql              # table schema + lookup data
├── dashboard/
│   ├── generate_sample_data.py # demo data for local preview
│   ├── dashboard.py            # local HTML dashboard (Plotly)
│   └── power_bi_notes.md       # how to connect Power BI to this pipeline
└── .github/workflows/ci.yml
```

## Running it

### 1. Infrastructure (Terraform)

```bash
cd infra
export TF_VAR_sql_admin_password="YourStrongPassword123!"
terraform init
terraform plan
terraform apply
```

Once `terraform apply` finishes, save the values from `terraform output` —
you'll need them in the next steps (SQL Server address, Function App name).

### 2. Database schema

Connect to the database (e.g. Azure Data Studio, `sqlcmd`, or the Azure
portal's Query Editor) and run `sql/schema.sql`.

### 3. Deploying the functions

```bash
cd function_app
func azure functionapp publish <function-app-name-from-output>
```

(requires [Azure Functions Core Tools](https://learn.microsoft.com/azure/azure-functions/functions-run-local))

### 4. Previewing the data without Power BI

```bash
cd dashboard
pip install pandas plotly
python generate_sample_data.py
python dashboard.py
# open dashboard_preview.html in a browser
```

See `dashboard/power_bi_notes.md` for connecting a real Power BI dashboard.

## A note on cost

All resources are sized for the free/cheapest tiers (Function App —
Consumption plan, SQL Database — Basic tier), so they fit within the limits
of an Azure for Students subscription. Remember to run `terraform destroy`
after testing to avoid leaving resources running.

## Possible next steps

- Data Factory instead of a Function App for more elaborate transformations
- A `staging` → `curated` layering (a simple medallion model) instead of one flat table
- Alerts (Azure Monitor) for unusual sales drops
- Unit tests for the aggregation logic in `GetSalesSummary`
