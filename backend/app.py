from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pyspark.sql import SparkSession
import openai  # Ensure you have `pip install openai`
from fastapi.middleware.cors import CORSMiddleware
import os
import re
from datetime import datetime, timedelta
import pandas as pd
import time
from dotenv import load_dotenv

# Initialize FastAPI app
app = FastAPI()

# Allow React frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["Localhost"],  # Allow frontend here either its for Dashboard.py Or React 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Spark session
spark = SparkSession.builder \
    .appName("EcommerceQueryProcessor") \
    .getOrCreate()

# Define dataset paths
file_paths = {
    "customers": "hdfs://localhost:9000/bigdata/ecommerce/olist_customers_dataset.csv",
    "order_items": "hdfs://localhost:9000/bigdata/ecommerce/olist_order_items_dataset.csv",
    "order_payments": "hdfs://localhost:9000/bigdata/ecommerce/olist_order_payments_dataset.csv",
    "order_reviews": "hdfs://localhost:9000/bigdata/ecommerce/olist_order_reviews_dataset.csv",
    "orders": "hdfs://localhost:9000/bigdata/ecommerce/olist_orders_dataset.csv",
    "products": "hdfs://localhost:9000/bigdata/ecommerce/olist_products_dataset.csv",
    "sellers": "hdfs://localhost:9000/bigdata/ecommerce/olist_sellers_dataset.csv",
}

# Load tables dynamically into Spark
table_columns = {}
for table, path in file_paths.items():
    try:
        df = spark.read.csv(path, header=True, inferSchema=True)
        df.createOrReplaceTempView(table)
        table_columns[table] = df.columns
    except Exception as e:
        table_columns[table] = [f"Error loading table: {e}"]

print("✅ Loaded tables with extracted columns:", table_columns)

# Initialize OpenAI API
load_dotenv()
API_KEY = os.getenv("API_KEY")  # Set your OpenAI API key as an environment variable

# Input Model
class QueryRequest(BaseModel):
    question: str

# Function to generate SQL dynamically using OpenAI API
def generate_sql_query(user_question):
    """
    Converts user question into a valid SQL query using only available tables & columns.
    """
    tables_info = "\n".join([f"- `{t}`: {', '.join(cols)}" for t, cols in table_columns.items()])
    
    prompt = f"""
    Convert the following user question into a valid SQL query using only the available tables and columns:

    **Available Tables and Columns:**
    {tables_info}

    **Rules:**
    - Use only these columns.
    - Ensure valid SQL syntax (JOINs, WHERE, GROUP BY, etc.).
    - Use correct table names and avoid incorrect column references.
    - If calculating sales, use `SUM(order_items.price) AS total_sales`.
    - To filter by last month, use `orders.order_purchase_timestamp BETWEEN (SELECT MAX(order_purchase_timestamp) - INTERVAL 1 MONTH FROM orders) AND (SELECT MAX(order_purchase_timestamp) FROM orders)`.
    - Do NOT include unnecessary joins (e.g., geolocation data if not required).
    - Do NOT include explanations; return only valid SQL syntax.
    
    **User Question:** {user_question}
    
    **SQL Query:**
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": "You are an AI assistant that generates SQL queries."},
                      {"role": "user", "content": prompt}],
            temperature=0
        )
        generated_sql = response.choices[0].message.content.strip()
        match = re.search(r"SELECT .*?;", generated_sql, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(0)
        else:
            raise ValueError("❌ AI Failed to generate a valid SQL query.")
    except Exception as e:
        raise ValueError(f"❌ AI Failed to generate a correct query: {e}")

@app.post("/process_query/")
def process_query(request: QueryRequest):
    """
    Processes the natural language query and returns SQL results with latency measurements.
    """
    try:
        # Track SQL generation time
        start_generation = time.time()
        sql_query = generate_sql_query(request.question)
        end_generation = time.time()
        sql_generation_time = end_generation - start_generation  # Time in seconds

        print(f"✅ Generated SQL: {sql_query} (Time Taken: {sql_generation_time:.4f} sec)")

        # Track SQL execution time
        start_execution = time.time()
        result_df = spark.sql(sql_query)
        end_execution = time.time()
        sql_execution_time = end_execution - start_execution  # Time in seconds

        # Convert results to JSON
        result_json = result_df.toPandas().to_dict(orient="records")

        return {
            "sql_query": sql_query,
            "results": result_json,
            "latency": {
                "sql_generation_time": round(sql_generation_time, 4),  # Query Generation Time
                "sql_execution_time": round(sql_execution_time, 4),  # SQL Execution Time
                "total_time": round(sql_generation_time + sql_execution_time, 4)  # Total Latency
            }
        }

    except Exception as e:
        return HTTPException(status_code=500, detail=f"Error processing query: {e}")
