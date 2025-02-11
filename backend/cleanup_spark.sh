#!/bin/bash

# Clear Spark temp files
echo "Cleaning Spark temporary files..."
rm -rf /tmp/*
rm -rf /usr/local/spark/work/*
rm -rf ~/spark-events/*

# Clear Spark logs
echo "Cleaning Spark logs..."
rm -rf /usr/local/spark/logs/*

# Expunge HDFS temporary files
echo "Expunging HDFS old files..."
hdfs dfs -expunge

# Clear Spark cache (requires PySpark)
echo "Clearing Spark catalog cache..."
python3 -c "from pyspark.sql import SparkSession; spark = SparkSession.builder.getOrCreate(); spark.catalog.clearCache(); print('✅ Spark cache cleared')"

echo "✅ Spark cleanup completed!"
