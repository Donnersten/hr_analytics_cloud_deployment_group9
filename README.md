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

## How Terraform Works in This Project

Terraform is used to provision and manage all Azure infrastructure components required for this project. It automates the creation of resource groups, storage accounts, container registries, container instances, and app services, ensuring that the environment is consistent and reproducible.

In addition, Terraform integrates with Docker to automate the process of building Docker images and pushing them to the Azure Container Registry (ACR). Through Terraform resources or local-exec commands, it ensures that the latest Docker images are deployed seamlessly to the Azure Web App and Container Instances. This integration enables reproducible deployment of both infrastructure and application containers together, simplifying management and reducing the risk of configuration drift.

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

### Assumptions
- Pipeline runs **once per day** (~15 minutes).  
- **App Service (P0v3)** runs **24/7** to host the Streamlit dashboard.  
- Approximately **10 GB** of data stored per month.  
- **1 vCPU, 3.5 GB RAM** used for compute services.  
- Prices are based on **October 2025 Azure and Snowflake pricing** (≈ 11.2 SEK/USD).  

---

### Azure Deployment (DuckDB-based)
| Component | Estimated Monthly Cost | Notes |
|------------|------------------------|-------|
| **App Service (P0v3)** | ≈ 612 SEK | Premium v3 plan, 24/7 active |
| **Container Registry (Basic)** | ≈ 55 SEK | Stores Docker images for pipeline & dashboard |
| **Azure File Share (10 GB)** | ≈ 10 SEK | DuckDB file storage |
| **Container Instance (Dagster)** | ≈ 15 SEK | 15 minutes per day runtime |
| **Total / Month** | **≈ 692 SEK** | Dominated by App Service cost |

---

### Snowflake Deployment
| Component | Estimated Monthly Cost | Notes |
|------------|------------------------|-------|
| **App Service (P0v3)** | ≈ 612 SEK | Dashboard hosting (same as Azure) |
| **Container Registry (Basic)** | ≈ 55 SEK | Image storage |
| **Snowflake Storage (10 GB)** | ≈ 4 SEK | $40/TB → proportional billing |
| **Snowflake Compute (XS)** | ≈ 165 SEK | 1 credit/hour × 7.5 hours/month |
| **Total / Month** | **≈ 836 SEK** | Slightly higher due to compute credits |

---

### Local / Lightweight DuckDB Deployment
| Component | Estimated Monthly Cost | Notes |
|------------|------------------------|-------|
| **DuckDB Engine** | 0 SEK | Free and open-source (MIT license) |
| **Local Storage (10 GB)** | 0–10 SEK | Depends on file location (local or cloud) |
| **Compute** | 0 SEK | Uses existing system CPU during execution |
| **Total / Month** | **≈ 0–10 SEK** | Only storage costs apply if hosted remotely |

---

### Monthly Cost Distribution (Approximation)

```
Azure (DuckDB)
App Service: ██████████████████████████████████████████████████ (94%)
Others: ██ (6%)

Snowflake
App Service: ████████████████████████████████████████████ (89%)
Compute: ████ (10%)
Storage: █ (1%)
```

---

### Analysis
While DuckDB and Snowflake present similar total monthly costs at small scale, their **cost models differ fundamentally**:  
- DuckDB incurs **minimal compute cost** because it runs locally or inside a lightweight container.  
- Snowflake charges per **credit**, even for short workloads.  
- The **App Service** cost dominates both architectures, overshadowing differences in compute or storage.  

For a **daily pipeline with limited data**, DuckDB remains the **most cost-efficient**.  
Snowflake becomes beneficial for **large-scale data**, **parallel pipelines**, or **multi-user environments** that require concurrent access and auto-scaling.

---


