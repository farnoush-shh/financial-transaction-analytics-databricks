# Databricks notebook source
from pyspark.sql import functions as F

raw = spark.table("financial_analytics.bronze.transactions_raw")
tagged = raw.withColumn(
    "dq_reason",
    F.when(F.col("transaction_id").isNull(), "MISSING_TRANSACTION_ID")
     .when(F.col("amount") <= 0, "INVALID_AMOUNT")
     .when(~F.col("currency").isin("EUR","CHF"), "UNSUPPORTED_CURRENCY")
)
invalid = tagged.filter(F.col("dq_reason").isNotNull())
candidate = tagged.filter(F.col("dq_reason").isNull()).drop("dq_reason")

dup_ids = (candidate.groupBy("transaction_id").count()
           .filter(F.col("count") > 1).select("transaction_id"))
dup_records = candidate.join(dup_ids, "transaction_id", "inner") \
    .withColumn("dq_reason", F.lit("DUPLICATE_TRANSACTION_ID"))

clean = (candidate.dropDuplicates(["transaction_id"])
         .withColumn("transaction_date", F.to_date("transaction_ts"))
         .withColumn("transaction_hour", F.hour("transaction_ts"))
         .withColumn("is_cross_border",
                     (F.col("billing_country") != F.col("merchant_country")).cast("int")))

quarantine = invalid.unionByName(dup_records, allowMissingColumns=True)

clean.write.format("delta").mode("overwrite").saveAsTable(
    "financial_analytics.silver.transactions_clean")
quarantine.write.format("delta").mode("overwrite").saveAsTable(
    "financial_analytics.silver.transactions_quarantine")
