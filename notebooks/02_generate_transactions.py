# Databricks notebook source
from pyspark.sql import functions as F
import uuid, random
from datetime import datetime, timedelta

random.seed(42)
customers = [f"C{i:03d}" for i in range(1, 6)]
merchants = ["M001", "M002", "M003"]
currencies = ["EUR", "CHF"]
methods = ["CARD", "BANK_TRANSFER", "WALLET"]
statuses = ["APPROVED", "DECLINED", "PENDING"]
countries = ["LU", "DE", "FR", "BE"]

rows = []
base = datetime(2026, 1, 1)
for _ in range(50000):
    billing = random.choice(countries)
    merchant_country = random.choice(countries)
    rows.append((
        str(uuid.uuid4()), random.choice(customers), random.choice(merchants),
        base + timedelta(minutes=random.randint(0, 300000)),
        round(random.uniform(5, 500), 2), random.choice(currencies),
        random.choice(methods), random.choice(statuses), billing,
        merchant_country, f"D{random.randint(1,500):04d}"
    ))

cols = ["transaction_id","customer_id","merchant_id","transaction_ts","amount",
        "currency","payment_method","status","billing_country","merchant_country","device_id"]
df = spark.createDataFrame(rows, cols)

sample_bad = df.limit(25)
raw_df = (df
    .unionByName(sample_bad.withColumn("transaction_id", F.lit(None).cast("string")))
    .unionByName(sample_bad.withColumn("amount", -F.abs(F.col("amount"))))
    .unionByName(sample_bad.withColumn("currency", F.lit("XXX")))
    .unionByName(df.limit(100)))

(raw_df.write.format("delta").mode("overwrite")
 .saveAsTable("financial_analytics.bronze.transactions_raw"))
