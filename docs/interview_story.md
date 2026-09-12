# Interview Story

## Problem
Demonstrate how a financial-transaction analytics product can move from raw events to trusted business reporting and anomaly investigation.

## Design
I used a Medallion architecture in Databricks. Bronze preserves raw data, Silver validates and quarantines quality issues, and Gold creates business-ready analytical outputs. A DQ gate stops downstream scoring when trusted data violates core rules.

## ML
I engineered customer-behaviour and temporal features and used KMeans as a simple unsupervised anomaly detector. I describe the output as anomalies requiring investigation, not confirmed fraud, because the dataset has no fraud labels.

## BI
I created Power BI serving views and a star schema with a transaction fact and date/customer/payment-method/currency dimensions. Currency is filtered rather than summing EUR and CHF together without FX conversion.

## Operationalisation
The notebooks are orchestrated as a Databricks Job and communicate through persisted Delta tables. Final grain validation checks that 50,000 fact rows correspond to 50,000 unique transaction IDs.
