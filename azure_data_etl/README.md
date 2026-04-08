# Azure Data ETL Pipeline — Brazilian E-Commerce

An end-to-end data engineering pipeline built on Microsoft Azure, processing the [Olist Brazilian E-Commerce dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) using a **Medallion Architecture (Bronze → Silver → Gold)**.

---

## Architecture

```
┌─────────────────────────────┐
│         Data Sources        │
│   HTTP (via GitHub)         │
│   SQL Table                 │
└──────────────┬──────────────┘
               │ Data Ingestion
               ▼
     ┌─────────────────────┐
     │  Azure Data Factory │   ← Orchestrates ingestion
     └──────────┬──────────┘
                │ Raw Data
                ▼
     ┌─────────────────────┐
     │  ADLS Gen2          │   ← Bronze Layer (raw data)
     └──────────┬──────────┘
                │
                ▼
     ┌─────────────────────┐
     │  Azure Databricks   │ ◄── MongoDB (table enrichment)
     │  Bronze → Silver    │
     └──────────┬──────────┘
                │ Transformed Data
                ▼
     ┌─────────────────────┐
     │  ADLS Gen2          │   ← Silver Layer (cleaned & enriched)
     └──────────┬──────────┘
                │
                ▼
     ┌─────────────────────┐
     │  Azure Synapse      │   ← Gold Layer (analytics-ready)
     └─────────────────────┘
```

---

## Tech Stack

| Service | Role |
|---|---|
| **Azure Data Factory (ADF)** | Pipeline orchestration and data ingestion |
| **ADLS Gen2 — Bronze** | Raw, unprocessed data storage |
| **Azure Databricks** | PySpark-based cleaning and transformation (Bronze → Silver) |
| **MongoDB** | Reference/lookup tables for data enrichment in Databricks |
| **ADLS Gen2 — Silver** | Cleaned and enriched data storage |
| **Azure Synapse Analytics** | Final aggregations and Gold layer serving |

---

## Dataset

**[Olist Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)**  
A real-world e-commerce dataset from the Brazilian marketplace Olist, containing ~100k orders across multiple tables: orders, customers, products, sellers, payments, reviews, and geolocation.

---

## Repository Structure

```
azure_data_etl/
├── dataFactory/            # ADF pipeline definitions (JSON)
├── databricks_notebooks/   # PySpark transformation notebooks (Bronze → Silver)
└── Synapse/                # Synapse scripts and config (Silver → Gold)
```

---

## Pipeline Flow

| Layer | Service | Description |
|---|---|---|
| **Bronze** | ADLS Gen2 | Raw data ingested as-is from sources via ADF |
| **Silver** | ADLS Gen2 | Cleaned, typed, and MongoDB-enriched data via Databricks |
| **Gold** | Azure Synapse | Aggregated, analytics-ready tables |

---

## Getting Started

### Prerequisites

- Active Azure subscription
- Azure CLI installed and authenticated
- Access to ADF, Databricks, ADLS Gen2, Synapse, and MongoDB instances
- Kaggle account to download the dataset

### Setup Steps

1. **Download the dataset**  
   Download the Olist dataset from [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) and upload the CSV files to your ADLS Gen2 Bronze container.

2. **Configure Azure Data Factory**  
   Import the pipeline definitions from `dataFactory/` into your ADF instance. Update linked service credentials to point to your ADLS Gen2 storage account and data sources.

3. **Set up Azure Databricks**  
   Upload notebooks from `databricks_notebooks/` to your Databricks workspace. Mount your ADLS Gen2 storage and configure the MongoDB connection string for enrichment lookups. Run notebooks to produce the Silver layer.

4. **Deploy Synapse**  
   Apply configurations from the `Synapse/` folder to your Synapse workspace. Create external tables or views over the Silver layer in ADLS Gen2 and run aggregation scripts to produce the Gold layer.

---

## Author

[ako305](https://github.com/ako305)
