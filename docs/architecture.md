# Architecture

## Layers
**Bronze** preserves raw simulated transaction records including injected quality problems.  
**Silver** applies validity rules, deduplication, quarantine and derived fields.  
**Gold** provides business KPIs, customer metrics, payment-method aggregates and anomaly scores.  
**Serving** exposes Power BI views plus a fact/dimension star schema.

## Workflow
Databricks Jobs executes:
`generate_transactions → silver_data_quality → gold_analytics → data_quality_validation → anomaly_detection → powerbi_serving`.

Tasks exchange persisted Delta objects rather than notebook-local variables.
