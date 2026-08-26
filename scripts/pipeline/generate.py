# import
import sys
from pathlib import Path
import logging

from faker import Faker
import random
import pandas as pd
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from paths import RAW_DATA_PATH

customers_file_path = RAW_DATA_PATH / "customers.csv"
orders_file_path = RAW_DATA_PATH / "orders.csv"

# initialise
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
fake = Faker()

customers = []
orders = []

product_names = ['Laptop', 'Phone', 'Tablet', 'Headphones']
statuses = ['completed', 'pending', 'cancelled']

start_date = datetime(2000, 1, 1)
end_date = datetime.today()

logging.info("generating e-commerce data ...")

# generate random customers
for customer_id in range(1, 11):
    customers.append({
        "customer_id": customer_id,
        "name": fake.name(),
        "email": fake.email()
    })

customers_df = pd.DataFrame(customers)
if customers_file_path.exists():
    customers_file_path.unlink(missing_ok=True)

if customers_df.to_csv(customers_file_path.resolve(), index=False) is not None:
    logging.error("error writing customers dataframe into csv file")

# generate random orders and order_items
for order_id in range(1, 101):
    days = (end_date - start_date).days
    order_date = start_date + timedelta(days=random.randint(0, days))
    orders.append({
        "order_id": order_id,
        "customer_id": random.choice(customers_df['customer_id']),
        "product": random.choice(product_names),
        "quantity": random.randint(1, 5),
        "price": round(random.uniform(5, 1000), 2),
        "order_date": order_date.date(),
        "status": random.choice(statuses)
    })

orders_df = pd.DataFrame(orders)
if orders_file_path.exists():
    orders_file_path.unlink(missing_ok=True)

if orders_df.to_csv(orders_file_path.resolve(), index=False) is not None:
    logging.error("error writing orders dataframe into csv file")

logging.info("generating e-commerce data ended")