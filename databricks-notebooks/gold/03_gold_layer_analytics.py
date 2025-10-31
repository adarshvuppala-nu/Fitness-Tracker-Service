# Databricks notebook source
from pyspark.sql.functions import count, sum, avg, countDistinct, min, max, datediff, col
df_silver = spark.table("silver_fitness_workouts")
print(f"Silver records loaded: {df_silver.count()}")

# COMMAND ----------

df_user_summary = df_silver.groupBy("user_id").agg(count("*").alias("total_workouts"), sum("duration_minutes").alias("total_duration_minutes"), sum("calories_burned").alias("total_calories_burned"), avg("heart_rate").alias("avg_heart_rate"), avg("calories_per_minute").alias("avg_calories_per_minute"), countDistinct("workout_type").alias("workout_variety"), min("date").alias("first_workout_date"), max("date").alias("last_workout_date")).withColumn("days_active", datediff(col("last_workout_date"), col("first_workout_date")) + 1)

print("User Summary Analytics:")
display(df_user_summary)

# COMMAND ----------

df_workout_analytics = df_silver.groupBy("workout_type").agg(count("*").alias("total_sessions"), avg("duration_minutes").alias("avg_duration"), avg("calories_burned").alias("avg_calories"), avg("heart_rate").alias("avg_heart_rate"), sum("calories_burned").alias("total_calories")).orderBy("total_sessions", ascending=False)

print("Workout Type Analytics:")
display(df_workout_analytics)

# COMMAND ----------

df_daily_trends = df_silver.groupBy("date").agg(count("*").alias("workouts_count"), sum("duration_minutes").alias("total_duration"), sum("calories_burned").alias("total_calories"), avg("heart_rate").alias("avg_heart_rate"), countDistinct("user_id").alias("active_users")).orderBy("date")

print("Daily Workout Trends:")
display(df_daily_trends)

# COMMAND ----------

df_monthly_summary = df_silver.groupBy("year", "month").agg(count("*").alias("total_workouts"), countDistinct("user_id").alias("unique_users"), sum("duration_minutes").alias("total_duration_minutes"), sum("calories_burned").alias("total_calories_burned"), avg("heart_rate").alias("avg_heart_rate")).orderBy("year", "month")

print("Monthly Summary:")
display(df_monthly_summary)

# COMMAND ----------

df_intensity_dist = df_silver.groupBy("intensity_level").agg(count("*").alias("workout_count"), avg("duration_minutes").alias("avg_duration"), avg("calories_burned").alias("avg_calories")).orderBy("workout_count", ascending=False)

print("Intensity Distribution:")
display(df_intensity_dist)

# COMMAND ----------

spark.sql("DROP TABLE IF EXISTS gold_user_summary")
df_user_summary.write.format("delta").mode("overwrite").saveAsTable("gold_user_summary")
spark.sql("DROP TABLE IF EXISTS gold_workout_analytics")
df_workout_analytics.write.format("delta").mode("overwrite").saveAsTable("gold_workout_analytics")

spark.sql("DROP TABLE IF EXISTS gold_daily_trends")
df_daily_trends.write.format("delta").mode("overwrite").saveAsTable("gold_daily_trends")

spark.sql("DROP TABLE IF EXISTS gold_monthly_summary")
df_monthly_summary.write.format("delta").mode("overwrite").saveAsTable("gold_monthly_summary")

spark.sql("DROP TABLE IF EXISTS gold_intensity_distribution")
df_intensity_dist.write.format("delta").mode("overwrite").saveAsTable("gold_intensity_distribution")

print("All Gold layer tables written successfully")

# COMMAND ----------

print("All Gold tables registered")
print(f"User summaries: {spark.table('gold_user_summary').count()}")
print(f"Workout analytics: {spark.table('gold_workout_analytics').count()}")
print(f"Daily trends: {spark.table('gold_daily_trends').count()}")
print(f"Monthly summaries: {spark.table('gold_monthly_summary').count()}")
print(f"Intensity distribution: {spark.table('gold_intensity_distribution').count()}")
display(spark.sql("SHOW TABLES").filter("tableName LIKE 'gold_%' OR tableName LIKE 'silver_%' OR tableName LIKE 'bronze_%'"))