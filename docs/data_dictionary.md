# Data Dictionary

| Field | Meaning |
|---|---|
| transaction_id | Unique synthetic transaction identifier |
| customer_id | Synthetic customer identifier |
| merchant_id | Synthetic merchant identifier |
| transaction_ts | Transaction timestamp |
| transaction_date | Derived transaction date |
| amount | Transaction amount in its stated currency |
| currency | EUR or CHF after Silver validation |
| payment_method | CARD, BANK_TRANSFER or WALLET |
| status | APPROVED, DECLINED or PENDING |
| billing_country | Synthetic customer billing country |
| merchant_country | Synthetic merchant country |
| device_id | Synthetic device identifier |
| is_cross_border | 1 when billing and merchant countries differ |
| anomaly_score | Distance from assigned KMeans cluster centre |
| is_anomaly | 1 when score is at/above the approximate 99th percentile |
