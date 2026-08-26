import sys
from pathlib import Path

from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from paths import SILVER_ORDER_PATH, GOLD_ORDER_PATH

builder = SparkSession.builder.appName("ETL_Pipeline")
builder = (builder
                   .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
                   .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog"))
spark = configure_spark_with_delta_pip(builder).getOrCreate()

spark.sql(f"""SELECT *
FROM delta.`{GOLD_ORDER_PATH}`
ORDER BY order_date;""").show()

spark.sql(f"""SELECT customer_id, SUM(price * quantity) AS total_spent
FROM delta.`{SILVER_ORDER_PATH}`
GROUP BY customer_id
ORDER BY total_spent DESC;""").show()

# revenue
spark.sql(f"""SELECT product, SUM(price * quantity) AS revenue
FROM delta.`{SILVER_ORDER_PATH}`
GROUP BY product;""").show()

