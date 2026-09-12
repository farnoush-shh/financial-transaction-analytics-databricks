# Databricks notebook source
from pyspark.sql import functions as F
s = spark.table("financial_analytics.silver.transactions_clean")

daily = s.groupBy("transaction_date","currency").agg(
    F.count("*").alias("transaction_count"),
    F.sum("amount").alias("gross_transaction_value"),
    F.avg("amount").alias("average_ticket"),
    F.sum(F.when(F.col("status")=="APPROVED",1).otherwise(0)).alias("approved_count"),
    F.sum(F.when(F.col("status")=="DECLINED",1).otherwise(0)).alias("declined_count"),
    F.sum("is_cross_border").alias("cross_border_count")
).withColumn("approval_rate", F.col("approved_count")/F.col("transaction_count"))
daily.write.format("delta").mode("overwrite").saveAsTable("financial_analytics.gold.daily_kpis")

customer = s.groupBy("customer_id").agg(
    F.count("*").alias("transaction_count"),
    F.sum("amount").alias("total_transaction_value"),
    F.avg("amount").alias("average_transaction_value"),
    F.max("amount").alias("maximum_transaction_value"),
    F.sum(F.when(F.col("status")=="DECLINED",1).otherwise(0)).alias("declined_count"),
    F.sum("is_cross_border").alias("cross_border_count"),
    F.countDistinct("device_id").alias("distinct_devices"),
    F.min("transaction_ts").alias("first_transaction"),
    F.max("transaction_ts").alias("last_transaction")
).withColumn("decline_rate", F.col("declined_count")/F.col("transaction_count"))
customer.write.format("delta").mode("overwrite").saveAsTable("financial_analytics.gold.customer_metrics")

pm = s.groupBy("transaction_date","currency","payment_method","status").agg(
    F.count("*").alias("transaction_count"),
    F.sum("amount").alias("transaction_value"))
pm.write.format("delta").mode("overwrite").saveAsTable("financial_analytics.gold.payment_method_daily")
