# Power BI Model

Recommended report pages:
1. Executive Overview
2. Transaction & Anomaly Analysis
3. Customer Analytics

Relationships:
- dim_date[transaction_date] 1:* fact_transactions[transaction_date]
- dim_customer[customer_id] 1:* fact_transactions[customer_id]
- dim_payment_method[payment_method] 1:* fact_transactions[payment_method]
- dim_currency[currency] 1:* fact_transactions[currency]

Use single-direction filtering from dimensions to fact. Use a currency slicer; do not aggregate EUR and CHF into one monetary KPI without FX conversion.

Suggested measures: Transaction Count, Transaction Value, Approved Transactions, Approval Rate, Average Ticket, Anomaly Count, Anomaly Rate.
