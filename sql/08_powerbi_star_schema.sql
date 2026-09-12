-- Star-schema serving views
CREATE OR REPLACE VIEW financial_analytics.gold.dim_date AS
SELECT DISTINCT transaction_date,
  YEAR(transaction_date) AS year,
  MONTH(transaction_date) AS month_number,
  DATE_FORMAT(transaction_date,'MMMM') AS month_name,
  QUARTER(transaction_date) AS quarter,
  DAYOFWEEK(transaction_date) AS day_of_week_number,
  DATE_FORMAT(transaction_date,'EEEE') AS day_of_week
FROM financial_analytics.silver.transactions_clean;

CREATE OR REPLACE VIEW financial_analytics.gold.dim_customer AS
SELECT customer_id, COUNT(*) AS lifetime_transactions,
       ROUND(AVG(amount),2) AS average_transaction_value,
       ROUND(MAX(amount),2) AS maximum_transaction_value,
       COUNT(DISTINCT device_id) AS distinct_devices
FROM financial_analytics.silver.transactions_clean
GROUP BY customer_id;

CREATE OR REPLACE VIEW financial_analytics.gold.dim_payment_method AS
SELECT DISTINCT payment_method FROM financial_analytics.silver.transactions_clean;

CREATE OR REPLACE VIEW financial_analytics.gold.dim_currency AS
SELECT DISTINCT currency FROM financial_analytics.silver.transactions_clean;

CREATE OR REPLACE VIEW financial_analytics.gold.fact_transactions AS
SELECT t.transaction_id,t.customer_id,t.merchant_id,t.transaction_ts,t.transaction_date,
       t.amount,t.currency,t.payment_method,t.status,t.billing_country,t.merchant_country,
       t.device_id,t.is_cross_border,
       COALESCE(a.anomaly_score,0) AS anomaly_score,
       COALESCE(a.is_anomaly,0) AS is_anomaly
FROM financial_analytics.silver.transactions_clean t
LEFT JOIN financial_analytics.gold.transaction_anomaly_scores a
  ON t.transaction_id=a.transaction_id;
