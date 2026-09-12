# Financial Transaction Analytics Data Product

End-to-end portfolio data product built with **Databricks, PySpark, SQL, Delta Lake and Power BI**.

> **Data note:** the project uses 50,000 simulated financial transactions. It is a portfolio project, not production banking data.

## What this project demonstrates

- Medallion architecture: Bronze → Silver → Gold
- Delta Lake persistence
- PySpark transformations and feature engineering
- Data-quality validation, deduplication and quarantine
- Business-ready KPI datasets
- Unsupervised KMeans-based anomaly scoring
- Power BI serving views and star-schema modelling
- Databricks Jobs orchestration and quality gates

## Architecture

```text
Synthetic Transactions
        |
        v
Bronze: transactions_raw
        |
        v
Silver: transactions_clean + transactions_quarantine
        |
        v
Gold: daily_kpis / customer_metrics / payment_method_daily
        |
        +--> DQ validation gate
        |
        +--> PySpark anomaly detection --> transaction_anomaly_scores
        |
        v
Power BI serving views + fact/dimension model
        |
        v
Executive / Transaction & Anomaly / Customer Analytics dashboards
```

## Dataset

The generator creates 50,000 synthetic transactions and injects controlled quality issues:
- missing transaction IDs
- negative amounts
- unsupported currencies
- duplicate transactions

The Silver layer validates, quarantines and deduplicates the raw data. The trusted output is validated to contain **50,000 rows and 50,000 unique transaction IDs**.

## Repository structure

```text
notebooks/
  02_generate_transactions.py
  03_silver_data_quality.py
  04_gold_analytics.py
  05_data_quality_validation.py
  06_anomaly_detection.py
sql/
  07_powerbi_serving_layer.sql
  08_powerbi_star_schema.sql
docs/
  architecture.md
  data_dictionary.md
  interview_story.md
powerbi/
  README.md
tests/
  validation_queries.sql
```

## Key design decisions

1. **Persist between workflow tasks.** Tasks exchange data through Delta tables rather than notebook variables.
2. **Fail on bad trusted data.** DQ validation acts as a pipeline gate before anomaly scoring.
3. **Do not call anomalies fraud.** The ML use case is unsupervised and has no confirmed fraud labels.
4. **Do not mix currencies.** EUR and CHF values are kept separate unless an FX conversion layer is introduced.
5. **Preserve fact grain.** `fact_transactions` is validated at one row per transaction.

## Power BI pages

- Executive Overview
- Transaction & Anomaly Analysis
- Customer Analytics

Use dimension columns for slicers and single-direction `1:*` relationships from dimensions to `fact_transactions`.

## Tech stack

Databricks · PySpark · Spark SQL · Delta Lake · Databricks Jobs · Power BI · DAX · KMeans

## Portfolio talking point

I designed an end-to-end financial transaction analytics product rather than a standalone notebook: raw simulated transactions are validated through Bronze/Silver/Gold layers, quality gates prevent unreliable downstream processing, anomaly scores are generated in PySpark, and curated fact/dimension models are served to Power BI through an orchestrated Databricks workflow.
