# Databricks notebook source
from pyspark.sql import functions as F
s = spark.table("financial_analytics.silver.transactions_clean")
checks = {
    "row_count_positive": s.count() > 0,
    "no_null_transaction_ids": s.filter(F.col("transaction_id").isNull()).count() == 0,
    "unique_transaction_ids": s.count() == s.select("transaction_id").distinct().count(),
    "valid_amounts": s.filter(F.col("amount") <= 0).count() == 0,
    "valid_currencies": s.filter(~F.col("currency").isin("EUR","CHF")).count() == 0,
    "valid_statuses": s.filter(~F.col("status").isin("APPROVED","DECLINED","PENDING")).count() == 0,
}
failed = [k for k,v in checks.items() if not v]
if failed:
    raise AssertionError(f"DQ FAILED: {failed}")
print("DQ PASSED", checks)
