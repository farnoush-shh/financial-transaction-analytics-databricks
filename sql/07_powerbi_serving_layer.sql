-- Power BI serving layer
CREATE OR REPLACE VIEW financial_analytics.gold.powerbi_daily_kpis AS
SELECT * FROM financial_analytics.gold.daily_kpis;

CREATE OR REPLACE VIEW financial_analytics.gold.powerbi_transaction_detail AS
SELECT t.*, COALESCE(a.anomaly_score,0) AS anomaly_score,
       COALESCE(a.is_anomaly,0) AS is_anomaly
FROM financial_analytics.silver.transactions_clean t
LEFT JOIN financial_analytics.gold.transaction_anomaly_scores a
  ON t.transaction_id = a.transaction_id;

CREATE OR REPLACE VIEW financial_analytics.gold.powerbi_customer_risk AS
SELECT c.*, COUNT(CASE WHEN a.is_anomaly=1 THEN 1 END) AS anomaly_count,
       MAX(a.anomaly_score) AS max_anomaly_score
FROM financial_analytics.gold.customer_metrics c
LEFT JOIN financial_analytics.gold.transaction_anomaly_scores a
  ON c.customer_id = a.customer_id
GROUP BY ALL;
