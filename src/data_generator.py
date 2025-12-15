# src/data_generator.py
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

random.seed(42)
np.random.seed(42)

N_CUSTOMERS = 5000
N_TRANSACTIONS = 500_000

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def random_date(start, end):
    delta = end - start
    return start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))

# ---------------- Customers ----------------
occupations = ['Salaried', 'Business', 'Student', 'Professional', 'Farmer']
branches = ['Nagpur', 'Pune', 'Bhopal', 'Indore', 'Mumbai']

customers = []
for i in range(N_CUSTOMERS):
    customers.append({
        "customer_id": f"CUST{i:06d}",
        "age": random.randint(18, 75),
        "occupation": random.choice(occupations),
        "income": int(np.random.lognormal(10, 0.7)),
        "pep": np.random.choice([0, 1], p=[0.98, 0.02]),
        "kyc_risk_score": random.randint(10, 80),
        "branch": random.choice(branches)
    })

customers_df = pd.DataFrame(customers)
customers_df.to_csv(f"{DATA_DIR}/customers.csv", index=False)

# ---------------- Transactions ----------------
channels = ['Branch', 'ATM', 'Mobile', 'Internet']
start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 1, 1)

customer_ids = customers_df["customer_id"].tolist()

transactions = []
for i in range(N_TRANSACTIONS):
    frm = random.choice(customer_ids)
    to = random.choice(customer_ids)
    while frm == to:
        to = random.choice(customer_ids)

    amount = round(np.random.exponential(20000) + 100, 2)

    transactions.append({
        "tx_id": f"TX{i:09d}",
        "from_customer": frm,
        "to_customer": to,
        "amount": amount,
        "timestamp": random_date(start_date, end_date),
        "channel": random.choice(channels),
        "is_cash": 1 if random.random() < 0.3 else 0
    })

transactions_df = pd.DataFrame(transactions)
transactions_df.to_csv(f"{DATA_DIR}/transactions.csv", index=False)

print("✅ 500k transaction dataset generated")
