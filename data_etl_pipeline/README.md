# Airflow ETL Pipeline — NASA APOD + PostgreSQL

An end-to-end ETL pipeline built with Apache Airflow that extracts daily astronomy data from NASA's Astronomy Picture of the Day (APOD) API, transforms it, and loads it into a PostgreSQL database. The entire stack runs in Docker via Astronomer.

---

## Table of Contents

- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Airflow Connections](#airflow-connections)
- [DAG Overview](#dag-overview)
- [Database Schema](#database-schema)

---

## Architecture

```
NASA APOD API
     │
     │  HTTP GET /planetary/apod
     ▼
┌─────────────┐     ┌─────────────────┐     ┌──────────────┐
│   Extract   │────▶│    Transform    │────▶│     Load     │
│ HttpOperator│     │  @task (Python) │     │ PostgresHook │
└─────────────┘     └─────────────────┘     └──────────────┘
                                                    │
                                                    ▼
                                          ┌──────────────────┐
                                          │   PostgreSQL DB  │
                                          │   (Docker)       │
                                          └──────────────────┘
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Apache Airflow | Pipeline orchestration |
| Astronomer Runtime | Managed Airflow on Docker |
| PostgreSQL 13 | Data storage |
| Docker + Docker Compose | Containerised services |
| NASA APOD API | Data source |

---

## Project Structure

```
.
├── dags/
│   └── etl.py              # Main DAG definition
├── Dockerfile              # Custom Astro runtime image
├── docker-compose.yml      # PostgreSQL service
├── requirements.txt        # Python provider packages
├── packages.txt            # OS-level packages
├── airflow_settings.yaml   # Local connections / variables
└── README.md
```

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Astronomer CLI](https://www.astronomer.io/docs/astro/cli/install-cli)
- [NASA API Key](https://api.nasa.gov/) (free)

---

## Getting Started

**1. Clone the repository**
```bash
git clone <your-repo-url>
cd data_etl_pipeline
```

**2. Start the PostgreSQL container**
```bash
docker-compose up -d
```

**3. Start Airflow**
```bash
astro dev start --no-cache
```

**4. Open the Airflow UI**
```
http://localhost:8080
```
Default credentials: `admin / admin`

**5. Add connections** (see [Airflow Connections](#airflow-connections) below)

**6. Trigger the DAG** — enable `nasa_apod_postgres` and trigger manually or wait for the daily schedule.

---

## Airflow Connections

Go to **Admin → Connections → +** in the Airflow UI and add the following:

### NASA API
| Field | Value |
|---|---|
| Connection ID | `nasa_api` |
| Connection Type | `HTTP` |
| Host | `https://api.nasa.gov` |
| Extra | `{"api_key": "<your_nasa_api_key>"}` |

### PostgreSQL
| Field | Value |
|---|---|
| Connection ID | `my_postgres_connection` |
| Connection Type | `Postgres` |
| Host | `postgres` ⚠️ not `localhost` |
| Schema | `postgres` |
| Login | `postgres` |
| Password | `postgres` |
| Port | `5432` |

> ⚠️ Use `postgres` as the host — inside Docker, containers communicate via service names, not `localhost`.

---

## DAG Overview

**DAG ID:** `nasa_apod_postgres`  
**Schedule:** `@daily`  
**Catchup:** `False`

```
create_table ──▶ extract_apod ──▶ transform_apod_data ──▶ load_data_to_postgres
```

| Task | Type | Description |
|---|---|---|
| `create_table` | `@task` | Creates `apod_data` table in Postgres if it doesn't exist |
| `extract_apod` | `HttpOperator` | GET request to NASA APOD API, returns JSON response |
| `transform_apod_data` | `@task` | Picks required fields from the API response |
| `load_data_to_postgres` | `@task` | Inserts transformed record into the database |

---

## Database Schema

```sql
CREATE TABLE IF NOT EXISTS apod_data (
    id          SERIAL PRIMARY KEY,
    title       VARCHAR(255),
    explanation TEXT,
    url         TEXT,
    date        DATE,
    media_type  VARCHAR(50)
);
```
