import sys
from pathlib import Path
import logging

from pyspark.sql import SparkSession
from pyspark.sql.functions import to_timestamp, col

from delta import configure_spark_with_delta_pip

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from paths import BRONZE_CUSTOMER_PATH, BRONZE_ORDER_PATH, SILVER_ORDER_PATH

# initialise
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logging.info("Generating silver layer ...")

builder = SparkSession.builder.appName("SilverLayer")
builder = (builder
                   .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
                   .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog"))
spark = configure_spark_with_delta_pip(builder).getOrCreate()

# Load Bronze Data
bronze_customers_df = spark.read.format("delta").load(str(BRONZE_CUSTOMER_PATH))
bronze_orders_df = spark.read.format("delta").load(str(BRONZE_ORDER_PATH))

# Clean orders (convert date, calculate total price)
silver_orders_df = (
    bronze_orders_df
    .dropDuplicates(["order_id"])
    .filter(col("status") != "cancelled")
    .withColumn("price", col("price").cast("double"))
    .withColumn("quantity", col("quantity").cast("int"))
)

# Save Silver layer
silver_orders_df.write.format("delta").mode("overwrite").save(str(SILVER_ORDER_PATH))

logging.info("✅ Silver layer created with enriched orders")
