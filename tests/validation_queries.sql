SELECT COUNT(*) rows, COUNT(DISTINCT transaction_id) unique_transactions
FROM financial_analytics.gold.fact_transactions;

SELECT COUNT(*) invalid_amounts
FROM financial_analytics.silver.transactions_clean WHERE amount <= 0;

SELECT currency, COUNT(*) transaction_count
FROM financial_analytics.silver.transactions_clean GROUP BY currency;
