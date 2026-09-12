# Databricks notebook source
from pyspark.sql import functions as F
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.clustering import KMeans

s = spark.table("financial_analytics.silver.transactions_clean")
stats = s.groupBy("customer_id").agg(
    F.avg("amount").alias("customer_avg_amount"),
    F.stddev("amount").alias("customer_std_amount"),
    F.count("*").alias("customer_tx_count"))
f = (s.join(stats,"customer_id","left")
     .withColumn("hour_of_day", F.hour("transaction_ts"))
     .withColumn("is_weekend", F.dayofweek("transaction_ts").isin(1,7).cast("int"))
     .withColumn("amount_to_customer_avg", F.col("amount")/F.col("customer_avg_amount"))
     .fillna({"customer_std_amount":0.0}))

features = ["amount","customer_avg_amount","customer_std_amount","customer_tx_count",
            "hour_of_day","is_weekend","amount_to_customer_avg"]
v = VectorAssembler(inputCols=features, outputCol="features").transform(f)
scaler = StandardScaler(inputCol="features", outputCol="scaled_features",
                        withStd=True, withMean=True).fit(v)
sv = scaler.transform(v)
model = KMeans(k=6, seed=42, maxIter=30, featuresCol="scaled_features").fit(sv)
pred = model.transform(sv)
centers = {i:c.tolist() for i,c in enumerate(model.clusterCenters())}

@F.udf("double")
def cluster_distance(cluster_id, vector):
    import math
    if cluster_id is None or vector is None: return None
    vals = vector.toArray().tolist()
    center = centers[int(cluster_id)]
    return float(math.sqrt(sum((a-b)**2 for a,b in zip(vals,center))))

scored = pred.withColumn("anomaly_score", cluster_distance("prediction","scaled_features"))
threshold = scored.approxQuantile("anomaly_score",[0.99],0.001)[0]
scored = scored.withColumn("is_anomaly",(F.col("anomaly_score") >= F.lit(threshold)).cast("int"))

out = scored.select(
    "transaction_id","customer_id","transaction_ts","amount","currency","payment_method","status",
    F.col("prediction").alias("cluster_id"),"anomaly_score","is_anomaly",
    "customer_avg_amount","customer_std_amount","customer_tx_count",
    "hour_of_day","is_weekend","amount_to_customer_avg")
out.write.format("delta").mode("overwrite").saveAsTable(
    "financial_analytics.gold.transaction_anomaly_scores")
