# HR Analytics – Cloud Deployment (Group 9)

## About the Project
This project implements a **modern data stack** to analyze labor market data from the Jobtech API for a recruitment agency.  
The goal is to build, automate, and deploy a **cloud-based data pipeline** using **Azure** and modern open-source tools.

---

## Architecture Overview
The solution consists of the following components:

| Layer | Technology / Tools | Purpose |
|-------|-------------------|---------|
| **Ingestion (EL)** | `dlt`, `Dagster` | Fetches data from the Jobtech API |
| **Transformation (T)** | `dbt` | Cleans, models, and creates data marts |
| **Storage (DW)** | `DuckDB` (Azure File Share) | Stores data in a lightweight data warehouse |
| **Orchestration** | `Dagster` | Automates and monitors pipelines |
| **Visualization** | `Streamlit` | Interactive dashboard for HR analytics |
| **Infrastructure** | `Terraform` | Infrastructure-as-Code for Azure resources |

---

## Azure Resources
Terraform creates the following resources in Azure:

- **Resource Group** – logical container for all resources  
- **Storage Account + File Share** – stores the DuckDB file (`job_ads.duckdb`)  
- **Container Registry (ACR)** – stores Docker images  
- **Container Instance (Dagster)** – runs the pipeline once per day  
- **App Service (P0v3)** – hosts the Streamlit dashboard 24/7  

---

## Data Flow
1. Dagster triggers a **daily run** via the DLT pipeline.  
2. Data is fetched from the **Jobtech API** → loaded into **DuckDB**.  
3. `dbt` models staging tables into data marts.  
4. The Streamlit dashboard fetches data and visualizes KPIs.  

---

## Dashboard Features
- Number of job vacancies per **profession, region, and employer**  
- Filters for **municipality**, **occupational group**, and **employer**  
- KPIs for total jobs and top 5 professions  
- Daily updates via the Dagster pipeline  

---

## Deployment Steps
```Code
# 1. Create your own env_variable.sh
In the iac folder, create env_variable.sh and add: export ARM_SUBSCRIPTION_ID="<SUBSCRIPTION_ID>"
```bash
# 2. Initialize Terraform
terraform init

# 3. Create resources
terraform apply -auto-approve

```
### Additional Manual Steps

1. **Materialize Assets in Dagster:**

   - Open the Dagster UI in your browser.  
   - Navigate to the **Assets** tab.  
   - Click the **Materialize All** button to trigger materialization of all assets manually.  
   - This ensures that the latest data is processed and available before the first dashboard use.

2. **First-Time Deployment in Azure Web App:**

   - Go to the Azure Portal and navigate to your **App Service** instance.  
   - Open the **Deployment Center**.  
   - Set the container image to `hr-project-dashboard` and the tag to `latest`.  
   - Save the settings to ensure the web app runs the correct Docker image for the Streamlit dashboard.
  

---

## Cost Comparison Against Cloud Data Warehouse

| Component | DuckDB (Azure) | Snowflake (Cloud DW) | Comment |
|------------|----------------|----------------------|---------|
| **App Service (P0v3)** | ≈ 1,380 SEK | ≈ 1,380 SEK | 1 vCPU, 3.5 GB RAM, 24/7 active |
| **Container Registry (Basic)** | ≈ 55 SEK | ≈ 55 SEK | Image storage |
| **Storage (10 GB)** | ≈ 10 SEK (Azure File) | ≈ 4 SEK (Snowflake) | Proportional billing |
| **Compute (pipeline)** | ≈ 15 SEK (ACI 15 min/day) | ≈ 165 SEK (X-Small warehouse 15 min/day) | Runtime |
| **Total / month** | **≈ 1,460 SEK** | **≈ 1,550 SEK** | Difference ≈ +90 SEK for Snowflake |

**Conclusion:**  
App Service (P0v3) is the largest cost.  
DuckDB is most cost-effective for small volumes and daily runs.  
Snowflake is more scalable but justified only for larger data volumes or concurrent users.

---

