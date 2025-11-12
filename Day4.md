# Day 4: DevOps & Data Engineering - Implementation Guide

## Current Status
- AWS S3 bucket created: fitness-tracker-data-pipeline
- Sample data uploaded to S3 raw folder
- IAM user created for S3 access
- Databricks Community Edition account created
- EC2 instance running at 54.146.186.49

## Architecture Overview
Data Flow: Raw CSV → Bronze Layer (Raw Ingestion) → Silver Layer (Cleaned & Validated) → Gold Layer (Analytics Aggregations)
Storage: DBFS (Databricks File System) for Medallion architecture
CI/CD: Jenkins pipeline for automated notebook deployment
Orchestration: Databricks Jobs for automated ETL execution

## Assignment Requirements (15 Marks)
1. Databricks ETL Pipeline (4 marks)
2. Medallion Architecture (2 marks)
3. CI/CD Pipeline (4 marks)
4. Data Processing (3 marks)
5. Documentation (2 marks)

## PHASE 1: Data Preparation

### 1.1 Upload Data to DBFS

In Databricks workspace, click Data icon in left sidebar.

Click Create Table button.

Select Upload File.

Click browse and select fitness_data.csv from your local machine.

After upload completes, note the DBFS path shown: /FileStore/tables/fitness_data.csv

Take screenshot of uploaded file.

## PHASE 2: Bronze Layer Implementation

### 2.1 Create Bronze Layer Notebook

In Databricks workspace, click Workspace in left sidebar.

Click Create → Notebook.

Name: 01_bronze_layer_ingestion

Language: Python

Click Create.

In top-right corner, click Connect and select Serverless Starter Warehouse.

### 2.2 Bronze Layer Code

Copy and paste this code into cells:

Cell 1:

```python
from pyspark.sql.functions import current_timestamp, lit, monotonically_increasing_id
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

fitness_schema = StructType([
    StructField("user_id", IntegerType(), True),
    StructField("workout_type", StringType(), True),
    StructField("duration_minutes", IntegerType(), True),
    StructField("calories_burned", IntegerType(), True),
    StructField("heart_rate", IntegerType(), True),
    StructField("date", StringType(), True),
    StructField("notes", StringType(), True)
])

raw_data_path = "dbfs:/FileStore/tables/fitness_data.csv"

df_raw = spark.read.format("csv").option("header", "true").schema(fitness_schema).load(raw_data_path)

print(f"Raw data loaded: {df_raw.count()} records")
display(df_raw)
```

Cell 2:

```python
df_bronze = df_raw.withColumn("ingestion_timestamp", current_timestamp()).withColumn("source_file", lit("fitness_data.csv")).withColumn("bronze_record_id", monotonically_increasing_id())

print(f"Bronze layer prepared: {df_bronze.count()} records")
display(df_bronze)
```

Cell 3:

```python
bronze_path = "dbfs:/bronze/fitness_workouts"

df_bronze.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(bronze_path)

print(f"Bronze layer written to {bronze_path}")
```

Cell 4:

```python
spark.sql(f"CREATE TABLE IF NOT EXISTS bronze_fitness_workouts USING DELTA LOCATION '{bronze_path}'")

display(spark.sql("SELECT * FROM bronze_fitness_workouts"))
print(f"Bronze table created with {spark.table('bronze_fitness_workouts').count()} records")
```

Run all cells by clicking Run All at top.

Take screenshot of successful execution showing output and record counts.

## PHASE 3: Silver Layer Implementation

### 3.1 Create Silver Layer Notebook

Click Workspace → Create → Notebook.

Name: 02_silver_layer_transformation

Language: Python

Click Create and connect to Serverless Starter Warehouse.

### 3.2 Silver Layer Code

Cell 1:

```python
from pyspark.sql.functions import col, year, month, dayofmonth, dayofweek, to_date, round, current_timestamp, when

bronze_path = "dbfs:/bronze/fitness_workouts"

df_bronze = spark.read.format("delta").load(bronze_path)

print(f"Bronze records loaded: {df_bronze.count()}")
display(df_bronze.limit(5))
```

Cell 2:

```python
df_silver = df_bronze.filter(col("user_id").isNotNull()).filter(col("workout_type").isNotNull()).filter(col("duration_minutes") > 0).filter(col("calories_burned") > 0).filter(col("heart_rate").between(60, 200)).dropDuplicates(["user_id", "date", "workout_type"])

print(f"Records after validation: {df_silver.count()}")
print(f"Records filtered out: {df_bronze.count() - df_silver.count()}")
```

Cell 3:

```python
df_silver = df_silver.withColumn("date", to_date(col("date"), "yyyy-MM-dd")).withColumn("year", year(col("date"))).withColumn("month", month(col("date"))).withColumn("day", dayofmonth(col("date"))).withColumn("day_of_week", dayofweek(col("date"))).withColumn("calories_per_minute", round(col("calories_burned") / col("duration_minutes"), 2)).withColumn("intensity_level", when(col("heart_rate") >= 150, "High").when(col("heart_rate") >= 120, "Medium").otherwise("Low")).withColumn("processed_timestamp", current_timestamp())

display(df_silver.limit(10))
```

Cell 4:

```python
silver_path = "dbfs:/silver/fitness_workouts"

df_silver.write.format("delta").mode("overwrite").option("overwriteSchema", "true").partitionBy("year", "month").save(silver_path)

print(f"Silver layer written to {silver_path}")
```

Cell 5:

```python
spark.sql(f"CREATE TABLE IF NOT EXISTS silver_fitness_workouts USING DELTA LOCATION '{silver_path}'")

display(spark.sql("SELECT * FROM silver_fitness_workouts"))
print(f"Silver table created with {spark.table('silver_fitness_workouts').count()} records")
```

Cell 6:

```python
print("Data Quality Checks:")
print(f"Total records: {df_silver.count()}")
print(f"Null check - user_id: {df_silver.filter(col('user_id').isNull()).count()}")
print(f"Null check - workout_type: {df_silver.filter(col('workout_type').isNull()).count()}")
print(f"Duration range: {df_silver.agg({'duration_minutes': 'min'}).collect()[0][0]} to {df_silver.agg({'duration_minutes': 'max'}).collect()[0][0]} minutes")
print(f"Calories range: {df_silver.agg({'calories_burned': 'min'}).collect()[0][0]} to {df_silver.agg({'calories_burned': 'max'}).collect()[0][0]} kcal")
print(f"Heart rate range: {df_silver.agg({'heart_rate': 'min'}).collect()[0][0]} to {df_silver.agg({'heart_rate': 'max'}).collect()[0][0]} bpm")

display(df_silver.groupBy("workout_type").count().orderBy("count", ascending=False))
```

Run all cells and take screenshot of output.

## PHASE 4: Gold Layer Implementation

### 4.1 Create Gold Layer Notebook

Click Workspace → Create → Notebook.

Name: 03_gold_layer_analytics

Language: Python

Click Create and connect to Serverless Starter Warehouse.

### 4.2 Gold Layer Code

Cell 1:

```python
from pyspark.sql.functions import count, sum, avg, countDistinct, min, max, datediff, col

silver_path = "dbfs:/silver/fitness_workouts"

df_silver = spark.read.format("delta").load(silver_path)

print(f"Silver records loaded: {df_silver.count()}")
```

Cell 2:

```python
df_user_summary = df_silver.groupBy("user_id").agg(count("*").alias("total_workouts"), sum("duration_minutes").alias("total_duration_minutes"), sum("calories_burned").alias("total_calories_burned"), avg("heart_rate").alias("avg_heart_rate"), avg("calories_per_minute").alias("avg_calories_per_minute"), countDistinct("workout_type").alias("workout_variety"), min("date").alias("first_workout_date"), max("date").alias("last_workout_date")).withColumn("days_active", datediff(col("last_workout_date"), col("first_workout_date")) + 1)

print("User Summary Analytics:")
display(df_user_summary)
```

Cell 3:

```python
df_workout_analytics = df_silver.groupBy("workout_type").agg(count("*").alias("total_sessions"), avg("duration_minutes").alias("avg_duration"), avg("calories_burned").alias("avg_calories"), avg("heart_rate").alias("avg_heart_rate"), sum("calories_burned").alias("total_calories")).orderBy("total_sessions", ascending=False)

print("Workout Type Analytics:")
display(df_workout_analytics)
```

Cell 4:

```python
df_daily_trends = df_silver.groupBy("date").agg(count("*").alias("workouts_count"), sum("duration_minutes").alias("total_duration"), sum("calories_burned").alias("total_calories"), avg("heart_rate").alias("avg_heart_rate"), countDistinct("user_id").alias("active_users")).orderBy("date")

print("Daily Workout Trends:")
display(df_daily_trends)
```

Cell 5:

```python
df_monthly_summary = df_silver.groupBy("year", "month").agg(count("*").alias("total_workouts"), countDistinct("user_id").alias("unique_users"), sum("duration_minutes").alias("total_duration_minutes"), sum("calories_burned").alias("total_calories_burned"), avg("heart_rate").alias("avg_heart_rate")).orderBy("year", "month")

print("Monthly Summary:")
display(df_monthly_summary)
```

Cell 6:

```python
df_intensity_dist = df_silver.groupBy("intensity_level").agg(count("*").alias("workout_count"), avg("duration_minutes").alias("avg_duration"), avg("calories_burned").alias("avg_calories")).orderBy("workout_count", ascending=False)

print("Intensity Distribution:")
display(df_intensity_dist)
```

Cell 7:

```python
gold_path = "dbfs:/gold"

df_user_summary.write.format("delta").mode("overwrite").save(f"{gold_path}/user_summary")

df_workout_analytics.write.format("delta").mode("overwrite").save(f"{gold_path}/workout_analytics")

df_daily_trends.write.format("delta").mode("overwrite").save(f"{gold_path}/daily_trends")

df_monthly_summary.write.format("delta").mode("overwrite").save(f"{gold_path}/monthly_summary")

df_intensity_dist.write.format("delta").mode("overwrite").save(f"{gold_path}/intensity_distribution")

print("All Gold layer tables written successfully")
```

Cell 8:

```python
spark.sql(f"CREATE TABLE IF NOT EXISTS gold_user_summary USING DELTA LOCATION '{gold_path}/user_summary'")
spark.sql(f"CREATE TABLE IF NOT EXISTS gold_workout_analytics USING DELTA LOCATION '{gold_path}/workout_analytics'")
spark.sql(f"CREATE TABLE IF NOT EXISTS gold_daily_trends USING DELTA LOCATION '{gold_path}/daily_trends'")
spark.sql(f"CREATE TABLE IF NOT EXISTS gold_monthly_summary USING DELTA LOCATION '{gold_path}/monthly_summary'")
spark.sql(f"CREATE TABLE IF NOT EXISTS gold_intensity_distribution USING DELTA LOCATION '{gold_path}/intensity_distribution'")

print("All Gold tables registered")
print(f"User summaries: {spark.table('gold_user_summary').count()}")
print(f"Workout analytics: {spark.table('gold_workout_analytics').count()}")
print(f"Daily trends: {spark.table('gold_daily_trends').count()}")
print(f"Monthly summaries: {spark.table('gold_monthly_summary').count()}")
print(f"Intensity distribution: {spark.table('gold_intensity_distribution').count()}")
```

Run all cells and take screenshot of output showing all analytics tables.

## PHASE 5: Databricks Job Creation

### 5.1 Create Workflow Job

Click Workflows in left sidebar.

Click Create Job button.

Job name: fitness_etl_pipeline

### 5.2 Add Bronze Task

Click Add task.

Task name: bronze_ingestion

Type: Notebook

Notebook path: /Users/your-email@gmail.com/01_bronze_layer_ingestion

Cluster: Serverless

Click Create task.

### 5.3 Add Silver Task

Click + below bronze_ingestion task.

Task name: silver_transformation

Type: Notebook

Notebook path: /Users/your-email@gmail.com/02_silver_layer_transformation

Cluster: Serverless

Depends on: bronze_ingestion

Click Create task.

### 5.4 Add Gold Task

Click + below silver_transformation task.

Task name: gold_analytics

Type: Notebook

Notebook path: /Users/your-email@gmail.com/03_gold_layer_analytics

Cluster: Serverless

Depends on: silver_transformation

Click Create task.

Click Save.

### 5.5 Run Workflow

Click Run now button.

Monitor execution in the run details page.

Take screenshot of successful workflow execution showing all tasks completed.

## PHASE 6: Jenkins Setup

### 6.1 Install Jenkins Using Docker

SSH into EC2 instance:

```bash
ssh -i ~/Downloads/fitness-tracker-key.pem ec2-user@54.146.186.49
```

Run Jenkins container:

```bash
docker run -d -p 8080:8080 -p 50000:50000 --name jenkins --restart=always -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
```

Wait 30 seconds for Jenkins to start:

```bash
sleep 30
```

Get initial admin password:

```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Copy the password output (long alphanumeric string).

### 6.2 Configure Security Group

In AWS Console, go to EC2 → Security Groups.

Select your instance security group.

Add inbound rule:
- Type: Custom TCP
- Port: 8080
- Source: 0.0.0.0/0

Save rules.

### 6.3 Access Jenkins Web Interface

Open browser: http://54.146.186.49:8080

Wait for Jenkins unlock page to load.

Paste the initial admin password from step 6.1.

Click Continue.

Click Install suggested plugins.

Wait for plugin installation to complete.

Create First Admin User:
- Username: admin
- Password: your choice
- Full name: Admin
- Email: your email

Click Save and Continue.

Click Save and Finish.

Click Start using Jenkins.

Take screenshot of Jenkins dashboard.

## PHASE 7: Databricks Token Generation

### 7.1 Generate Token

In Databricks, click username in top-right → User Settings.

Go to Developer → Access tokens.

Click Generate new token.

Comment: Jenkins CI/CD

Lifetime: 90 days

Click Generate.

Copy token and save securely.

Take screenshot of token generation page.

## PHASE 8: Jenkins Pipeline Configuration

### 8.1 Add Databricks Credentials

In Jenkins, click Manage Jenkins → Credentials.

Click (global) → Add Credentials.

Kind: Secret text

Secret: paste Databricks token

ID: databricks-token

Description: Databricks Access Token

Click Create.

### 8.2 Install Jenkins Plugins

Click Manage Jenkins → Plugins.

Go to Available plugins.

Search and install:
- Git plugin
- Pipeline plugin
- Credentials Binding Plugin

Click Install.

### 8.3 Export Notebooks

In Databricks, for each notebook:

Click File → Export → Source file.

Download as .py file.

Save to local directory: databricks-notebooks/

## PHASE 9: Repository Setup

### 9.1 Create Directory Structure

On local machine:

```bash
cd "/Users/adarshvuppala/Downloads/Modern Data & AI Software Foundations/fitness-tracker-api"
mkdir -p databricks-notebooks/bronze databricks-notebooks/silver databricks-notebooks/gold
```

### 9.2 Save Notebook Files

Move downloaded .py files:
- 01_bronze_layer_ingestion.py → databricks-notebooks/bronze/
- 02_silver_layer_transformation.py → databricks-notebooks/silver/
- 03_gold_layer_analytics.py → databricks-notebooks/gold/

### 9.3 Create Jenkinsfile

Create file: databricks-notebooks/Jenkinsfile

```groovy
pipeline {
    agent any

    environment {
        DATABRICKS_HOST = 'https://community.cloud.databricks.com'
        DATABRICKS_TOKEN = credentials('databricks-token')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo 'Repository checked out'
            }
        }

        stage('Install Databricks CLI') {
            steps {
                sh '''
                    pip3 install databricks-cli --user
                    export PATH=$PATH:~/.local/bin
                    databricks --version
                '''
            }
        }

        stage('Configure Databricks') {
            steps {
                sh '''
                    export PATH=$PATH:~/.local/bin
                    cat > ~/.databrickscfg <<EOF
[DEFAULT]
host = ${DATABRICKS_HOST}
token = ${DATABRICKS_TOKEN}
EOF
                '''
            }
        }

        stage('Deploy Bronze Notebook') {
            steps {
                sh '''
                    export PATH=$PATH:~/.local/bin
                    databricks workspace import databricks-notebooks/bronze/01_bronze_layer_ingestion.py /Users/vuppalaadarsh28@gmail.com/01_bronze_layer_ingestion --language PYTHON --format SOURCE --overwrite
                '''
            }
        }

        stage('Deploy Silver Notebook') {
            steps {
                sh '''
                    export PATH=$PATH:~/.local/bin
                    databricks workspace import databricks-notebooks/silver/02_silver_layer_transformation.py /Users/vuppalaadarsh28@gmail.com/02_silver_layer_transformation --language PYTHON --format SOURCE --overwrite
                '''
            }
        }

        stage('Deploy Gold Notebook') {
            steps {
                sh '''
                    export PATH=$PATH:~/.local/bin
                    databricks workspace import databricks-notebooks/gold/03_gold_layer_analytics.py /Users/vuppalaadarsh28@gmail.com/03_gold_layer_analytics --language PYTHON --format SOURCE --overwrite
                '''
            }
        }

        stage('Validation') {
            steps {
                echo 'Bronze layer deployment: SUCCESS'
                echo 'Silver layer deployment: SUCCESS'
                echo 'Gold layer deployment: SUCCESS'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully'
        }
        failure {
            echo 'Pipeline failed'
        }
    }
}
```

## PHASE 10: Jenkins Job Creation

### 10.1 Create Pipeline Job

In Jenkins dashboard, click New Item.

Item name: databricks-etl-pipeline

Select Pipeline.

Click OK.

### 10.2 Configure Pipeline

Description: Automated Databricks notebook deployment

Pipeline section:
- Definition: Pipeline script from SCM
- SCM: Git
- Repository URL: your GitHub repository URL
- Branch: main
- Script Path: databricks-notebooks/Jenkinsfile

Click Save.

### 10.3 Test Pipeline

Click Build Now.

Monitor Console Output.

Verify all stages complete successfully.

Take screenshots of:
- Build in progress
- Console output
- Stage view showing all stages passed

## PHASE 11: Verification

### 11.1 Verify DBFS Data

In Databricks, create new notebook: 04_verification

Cell 1:

```python
display(dbutils.fs.ls("dbfs:/bronze"))
display(dbutils.fs.ls("dbfs:/silver"))
display(dbutils.fs.ls("dbfs:/gold"))
```

Cell 2:

```python
print(f"Bronze records: {spark.table('bronze_fitness_workouts').count()}")
print(f"Silver records: {spark.table('silver_fitness_workouts').count()}")
print(f"Gold user summary: {spark.table('gold_user_summary').count()}")
print(f"Gold workout analytics: {spark.table('gold_workout_analytics').count()}")
print(f"Gold daily trends: {spark.table('gold_daily_trends').count()}")
print(f"Gold monthly summary: {spark.table('gold_monthly_summary').count()}")
print(f"Gold intensity distribution: {spark.table('gold_intensity_distribution').count()}")
```

Run and take screenshot.

### 11.2 Data Validation Notebook

Create notebook: 05_data_validation

Cell 1:

```python
from pyspark.sql.functions import col
from pyspark.sql import Row

validation_results = []

bronze_count = spark.table("bronze_fitness_workouts").count()
validation_results.append(("Bronze Layer Records", bronze_count, "PASS" if bronze_count > 0 else "FAIL"))

silver_count = spark.table("silver_fitness_workouts").count()
validation_results.append(("Silver Layer Records", silver_count, "PASS" if silver_count > 0 else "FAIL"))

null_check = spark.table("silver_fitness_workouts").filter(col("user_id").isNull()).count()
validation_results.append(("Silver Null Check", null_check, "PASS" if null_check == 0 else "FAIL"))

user_summary_count = spark.table("gold_user_summary").count()
validation_results.append(("Gold User Summary", user_summary_count, "PASS" if user_summary_count > 0 else "FAIL"))

workout_analytics_count = spark.table("gold_workout_analytics").count()
validation_results.append(("Gold Workout Analytics", workout_analytics_count, "PASS" if workout_analytics_count > 0 else "FAIL"))

daily_trends_count = spark.table("gold_daily_trends").count()
validation_results.append(("Gold Daily Trends", daily_trends_count, "PASS" if daily_trends_count > 0 else "FAIL"))

monthly_summary_count = spark.table("gold_monthly_summary").count()
validation_results.append(("Gold Monthly Summary", monthly_summary_count, "PASS" if monthly_summary_count > 0 else "FAIL"))

intensity_dist_count = spark.table("gold_intensity_distribution").count()
validation_results.append(("Gold Intensity Distribution", intensity_dist_count, "PASS" if intensity_dist_count > 0 else "FAIL"))

validation_df = spark.createDataFrame([Row(check=r[0], result=r[1], status=r[2]) for r in validation_results])
display(validation_df)

failed_checks = validation_df.filter(col("status") == "FAIL").count()
if failed_checks > 0:
    print(f"VALIDATION FAILED: {failed_checks} checks failed")
else:
    print("VALIDATION PASSED: All checks successful")
```

Run and take screenshot showing all PASS.

## PHASE 12: Documentation

### 12.1 Required Screenshots

Databricks:
1. Workspace showing all notebooks
2. Uploaded data file in Data section
3. Bronze notebook execution with output
4. Silver notebook execution with data quality checks
5. Gold notebook execution with all analytics tables
6. Workflow job showing all 3 tasks
7. Workflow run showing successful execution
8. Verification notebook showing DBFS structure
9. Validation notebook showing all checks passed

Jenkins:
10. Jenkins dashboard
11. Pipeline job configuration
12. Build history
13. Console output of successful build
14. Stage view showing all stages green

Integration:
15. Databricks tables list showing bronze, silver, gold tables
16. Query results from gold tables showing analytics data

### 12.2 Documentation Structure

Create PDF document with sections:

1. Architecture Overview
   - Medallion architecture diagram
   - Data flow explanation
   - Technology stack

2. Implementation Details
   - DBFS data storage setup
   - Bronze layer ingestion logic
   - Silver layer transformation and validation
   - Gold layer analytics aggregations
   - Delta Lake usage

3. CI/CD Pipeline
   - Jenkins installation steps
   - Pipeline configuration
   - Automated deployment process
   - Build execution evidence

4. Data Validation
   - Quality checks implemented
   - Validation results
   - Record counts at each layer

5. Analytics Results
   - User summary metrics
   - Workout analytics
   - Daily and monthly trends
   - Intensity distribution

6. Screenshots Evidence
   - All required screenshots numbered and labeled

## Submission Checklist

- [ ] Databricks Community Edition account active
- [ ] Data uploaded to DBFS
- [ ] Bronze layer notebook created and executed
- [ ] Silver layer notebook created and executed
- [ ] Gold layer notebook created and executed
- [ ] All Delta tables created
- [ ] Databricks workflow job created with 3 tasks
- [ ] Workflow executed successfully
- [ ] Jenkins installed on EC2
- [ ] Databricks token generated
- [ ] Jenkins credentials configured
- [ ] Jenkinsfile created
- [ ] Jenkins pipeline job created
- [ ] Pipeline executed successfully
- [ ] Validation notebook shows all checks passed
- [ ] All screenshots captured
- [ ] Documentation PDF created
- [ ] Code ready to commit to GitHub

## Expected Marks

Databricks ETL Pipeline (4 marks):
- Bronze layer with metadata tracking: 1.5 marks
- Silver layer with validation and transformation: 1.5 marks
- Gold layer with 5 analytics tables: 1 mark

Medallion Architecture (2 marks):
- Delta Lake implementation: 1 mark
- Proper layering with partitioning: 1 mark

CI/CD Pipeline (4 marks):
- Jenkins setup and configuration: 1 mark
- Complete Jenkinsfile with all stages: 1.5 marks
- Successful automated deployment: 1.5 marks

Data Processing (3 marks):
- Real fitness data processing: 1 mark
- Meaningful analytics with aggregations: 1 mark
- Data validation checks: 1 mark

Documentation (2 marks):
- Complete screenshots: 1 mark
- Clear documentation: 1 mark

Total: 15 marks
