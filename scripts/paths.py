from pathlib import Path

# Project root: directory containing paths.py
PROJECT_ROOT = Path(__file__).resolve().parent.parent

PIPELINE_ROOT = PROJECT_ROOT / "scripts" / "pipeline"

# raw data paths
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw"
RAW_DELTA_PATH = PROJECT_ROOT / "data" / "delta"

# delta data paths
BRONZE_CUSTOMER_PATH = RAW_DELTA_PATH / "customers_bronze"
BRONZE_ORDER_PATH = RAW_DELTA_PATH / "orders_bronze"

SILVER_ORDER_PATH = RAW_DELTA_PATH / "orders_silver"

GOLD_ORDER_PATH = RAW_DELTA_PATH / "orders_gold/daily_sales"
