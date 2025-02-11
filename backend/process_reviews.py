import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Initialize Spark Session
spark = SparkSession.builder.appName("OlistDataset").getOrCreate()

# HDFS Path from Environment
hdfs_path = os.getenv("HDFS_PATH", "default_path")

try:
    print("📖 Reading Reviews Data from HDFS...")
    raw_reviews_df = spark.read.option("inferSchema", "true").json(hdfs_path)
    print("✅ Successfully loaded reviews data!")
except Exception as e:
    print(f"❌ Error loading JSON: {e}")
