from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

date_str = datetime.today().strftime("%Y%m%d")

# In Spark container: Windows ./data is mounted to /opt/data
input_path = f"/opt/data/sales_{date_str}.csv"
output_path = f"/opt/data/curated_sales_{date_str}.parquet"

spark = SparkSession.builder \
    .appName("Sales Transformation") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

df = spark.read.csv(input_path, header=True, inferSchema=True)
df2 = df.withColumn("revenue", col("quantity") * col("price"))

df2.write.mode("overwrite").parquet(output_path)

print(f"✅ Wrote parquet to: {output_path}")

spark.stop()
