import sys
from pathlib import Path
import logging

from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, col, count

from delta import configure_spark_with_delta_pip

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from paths import SILVER_ORDER_PATH, GOLD_ORDER_PATH

# initialise
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logging.info("Generating gold layer for daily sales ...")

builder = SparkSession.builder.appName("GoldLayer")
builder = (builder
                   .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
                   .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog"))
spark = configure_spark_with_delta_pip(builder).getOrCreate()

# Load Silver Data
silver_orders_df = spark.read.format("delta").load(str(SILVER_ORDER_PATH))

df_gold = (
    silver_orders_df
    .groupBy("order_date")
    .agg(
        sum(col("price") * col("quantity")).alias("daily_sales"),
        count("order_id").alias("total_orders")
    )
)

# Save Gold layer
df_gold.write.format("delta").mode("overwrite").save(str(GOLD_ORDER_PATH))

logging.info("✅ Gold layer created with daily sales")
