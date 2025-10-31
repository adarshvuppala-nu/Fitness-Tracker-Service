# Databricks notebook source
from pyspark.sql.functions import col, year, month, dayofmonth, dayofweek, to_date, round, current_timestamp, when
df_bronze = spark.table("bronze_fitness_workouts")
print(f"Bronze records loaded: {df_bronze.count()}")
display(df_bronze.limit(5))


# COMMAND ----------

df_silver = df_bronze.filter(col("user_id").isNotNull()).filter(col("workout_type").isNotNull()).filter(col("duration_minutes") > 0).filter(col("calories_burned") > 0).filter(col("heart_rate").between(60, 200)).dropDuplicates(["user_id", "date", "workout_type"])

print(f"Records after validation: {df_silver.count()}")
print(f"Records filtered out: {df_bronze.count() - df_silver.count()}")

# COMMAND ----------

df_silver = df_silver.withColumn("date", to_date(col("date"), "yyyy-MM-dd")).withColumn("year", year(col("date"))).withColumn("month", month(col("date"))).withColumn("day", dayofmonth(col("date"))).withColumn("day_of_week", dayofweek(col("date"))).withColumn("calories_per_minute", round(col("calories_burned") / col("duration_minutes"), 2)).withColumn("intensity_level", when(col("heart_rate") >= 150, "High").when(col("heart_rate") >= 120, "Medium").otherwise("Low")).withColumn("processed_timestamp", current_timestamp())

display(df_silver.limit(10))

# COMMAND ----------

spark.sql("DROP TABLE IF EXISTS silver_fitness_workouts")

df_silver.write.format("delta").mode("overwrite").option("overwriteSchema", "true").partitionBy("year", "month").saveAsTable("silver_fitness_workouts")
print("Silver layer written as managed table: silver_fitness_workouts")

# COMMAND ----------

display(spark.sql("SELECT * FROM silver_fitness_workouts"))
print(f"Silver table created with {spark.table('silver_fitness_workouts').count()} records")

# COMMAND ----------

print("Data Quality Checks:")
print(f"Total records: {df_silver.count()}")
print(f"Null check - user_id: {df_silver.filter(col('user_id').isNull()).count()}")
print(f"Null check - workout_type: {df_silver.filter(col('workout_type').isNull()).count()}")
print(f"Duration range: {df_silver.agg({'duration_minutes': 'min'}).collect()[0][0]} to {df_silver.agg({'duration_minutes': 'max'}).collect()[0][0]} minutes")
print(f"Calories range: {df_silver.agg({'calories_burned': 'min'}).collect()[0][0]} to {df_silver.agg({'calories_burned': 'max'}).collect()[0][0]} kcal")
print(f"Heart rate range: {df_silver.agg({'heart_rate': 'min'}).collect()[0][0]} to {df_silver.agg({'heart_rate': 'max'}).collect()[0][0]} bpm")

display(df_silver.groupBy("workout_type").count().orderBy("count", ascending=False))