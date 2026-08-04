# Medallion Data Engineering Pipeline
### End-to-End Data Engineering Architecture using Apache Airflow, Databricks & dbt

![Architecture Diagram](a_clean_technical_architecture_diagram_infograph.png)

---

# Overview

This project implements a modern ** Data Warehouse Data Engineering Platform** based on the **Medallion Architecture**.

The pipeline ingests transactional and file-based data from multiple sources into a Bronze layer before progressively refining the data into analytical models.

The architecture demonstrates industry best practices including:

- Apache Airflow orchestration
- Incremental ingestion
- Change Data Capture (CDC)
- Upserts (MERGE)
- Databricks Delta Lake
- dbt transformations
- Slowly Changing Dimensions (SCD)
- Star Schema modeling
- Incremental warehouse loading

The final Gold layer provides analytics-ready dimensional models for reporting and business intelligence.

---

# Architecture

The complete architecture is shown below.

![Architecture](a_clean_technical_architecture_diagram_infograph.png)

---

# Technology Stack

| Component | Technology |
|-----------|------------|
| Workflow Orchestration | Apache Airflow |
| Data Lake | Databricks Delta Lake |
| Transformation | dbt |
| Storage | AWS S3 |
| Operational Database | GhostDB |
| Processing | Databricks |
| Data Modeling | Star Schema |
| Warehouse Pattern | Medallion Architecture |

---

# Pipeline Flow

```
GhostDB
        \
         \
          ---> Bronze ---> Silver ---> Gold ---> Analytics
         /
AWS S3  /
```

---

# Data Flow

## 1. Data Sources

The pipeline consumes data from two primary systems.

### GhostDB

Transactional operational database containing:

- Customers
- Employees
- Orders
- Products
- Stores

Data is extracted using:

- CDC (Change Data Capture)
- Incremental Loads

---

### AWS S3

Raw files uploaded by business systems.

Supported formats include:

- CSV
- JSON
- Parquet
- Log Files

---

# Bronze Layer (Raw)

## Purpose

Landing zone for raw source data.

Characteristics

- Raw ingestion
- No transformations
- Schema preserved
- Append-only where possible
- Audit columns added

Processing

- CDC Incremental Loads
- MERGE (Upsert)
- Metadata Capture
- Source Tracking
- Ingestion Timestamp

Example Bronze Tables

```
bronze_customers
bronze_orders
bronze_products
bronze_employees
bronze_stores
```

---

# Silver Layer (Clean)

The Silver layer standardizes data for enterprise use.

Transformations include:

- Duplicate removal
- Data cleansing
- Null handling
- Standardized formats
- Business validation
- Data quality rules
- Column normalization

Output

A single integrated

**One Big Table (OBT)**

```
obt_sales
```

This table combines data from all operational entities.

---

# Gold Layer (Business)

The Gold layer transforms the OBT into a dimensional model.

Techniques

- Star Schema
- Incremental Loading
- SCD Type 2
- Business Calculations
- Surrogate Keys

---

# Gold Tables

## Dimensions

```
dim_customer
dim_employees
dim_orders
dim_products
dim_stores
```

## Facts

```
fact_orders
```

---

# Star Schema

```
                 dim_customer
                      |
                      |
dim_products ---- fact_orders ---- dim_stores
                      |
                      |
                dim_employees
                      |
                 dim_orders
```

---

# Airflow Orchestration

Apache Airflow controls the complete workflow.

Typical DAG

```
Extract GhostDB
        |

Extract S3 Files
        |

Bronze Ingestion
        |

Bronze Validation
        |

Silver dbt Models
        |

OBT Generation
        |

Gold dbt Models
        |

Data Quality Tests
        |

Publish Warehouse
```

---

# Incremental Loading Strategy

GhostDB

- CDC
- Watermark columns
- Updated timestamps

AWS S3

- New file detection
- Modified file detection

Bronze

- MERGE INTO
- Upserts

Silver

- Incremental dbt models

Gold

- Incremental dimensions
- Incremental facts
- SCD Type 2

---


# Data Quality Rules

The pipeline enforces:

- No duplicate primary keys
- Mandatory columns populated
- Valid foreign keys
- Positive quantities
- Positive prices
- Valid dates
- Accepted null thresholds
- Schema validation

---


# License

This project is intended as a reference implementation for modern data engineering pipelines following the Medallion Architecture using Apache Airflow, Databricks, and dbt.
