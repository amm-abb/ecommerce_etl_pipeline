import sys
from pathlib import Path
import logging

from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from paths import RAW_DATA_PATH, BRONZE_CUSTOMER_PATH, BRONZE_ORDER_PATH

# initialise
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logging.info("Generating bronze layer for customers and orders ...")

builder = SparkSession.builder.appName("BronzeLayer")
builder = (builder
                   .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
                   .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog"))
spark = configure_spark_with_delta_pip(builder).getOrCreate()

customers_df = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(str(RAW_DATA_PATH / "customers.csv"))
orders_df = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(str(RAW_DATA_PATH / "orders.csv"))

customers_df.write.format("delta").mode("overwrite").save(str(BRONZE_CUSTOMER_PATH))
orders_df.write.format("delta").mode("overwrite").save(str(BRONZE_ORDER_PATH))

logging.info("✅ Bronze layer created for customers and orders")