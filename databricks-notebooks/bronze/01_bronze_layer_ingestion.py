# Databricks notebook source
from pyspark.sql.functions import current_timestamp, lit, monotonically_increasing_id
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

data = [
    (1, "running", 30, 300, 140, "2025-01-15", "Morning run"),
    (2, "cycling", 45, 400, 130, "2025-01-15", "Interval training"),
    (3, "swimming", 60, 500, 120, "2025-01-16", "Pool session"),
    (1, "strength_training", 40, 250, 110, "2025-01-16", "Upper body"),
    (2, "yoga", 30, 150, 100, "2025-01-17", "Relaxation"),
    (3, "running", 25, 280, 145, "2025-01-17", "Sprint intervals"),
    (1, "cycling", 50, 450, 135, "2025-01-18", "Hill climb"),
    (2, "swimming", 55, 480, 125, "2025-01-18", "Endurance"),
    (3, "strength_training", 35, 220, 115, "2025-01-19", "Lower body"),
    (1, "yoga", 40, 180, 95, "2025-01-19", "Flexibility")
]

fitness_schema = StructType([
    StructField("user_id", IntegerType(), True),
    StructField("workout_type", StringType(), True),
    StructField("duration_minutes", IntegerType(), True),
    StructField("calories_burned", IntegerType(), True),
    StructField("heart_rate", IntegerType(), True),
    StructField("date", StringType(), True),
    StructField("notes", StringType(), True)
])

df_raw = spark.createDataFrame(data, fitness_schema)

print(f"Raw data loaded: {df_raw.count()} records")
display(df_raw)

# COMMAND ----------

df_bronze = df_raw.withColumn("ingestion_timestamp", current_timestamp()).withColumn("source_file", lit("fitness_data.csv")).withColumn("bronze_record_id", monotonically_increasing_id())

print(f"Bronze layer prepared: {df_bronze.count()} records")
display(df_bronze)

# COMMAND ----------

spark.sql("DROP TABLE IF EXISTS bronze_fitness_workouts")

df_bronze.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("bronze_fitness_workouts")

print("Bronze layer written as managed table: bronze_fitness_workouts")

# COMMAND ----------

display(spark.sql("SELECT * FROM bronze_fitness_workouts"))
print(f"Bronze table created with {spark.table('bronze_fitness_workouts').count()} records")