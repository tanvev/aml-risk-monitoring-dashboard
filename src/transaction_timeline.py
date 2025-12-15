import pandas as pd

def get_transaction_timeline(transactions, customer_id, days=90):
    transactions["timestamp"] = pd.to_datetime(transactions["timestamp"])

    recent_tx = transactions[
        (transactions["from_customer"] == customer_id) |
        (transactions["to_customer"] == customer_id)
    ]

    cutoff = pd.Timestamp.now() - pd.Timedelta(days=days)
    recent_tx = recent_tx[recent_tx["timestamp"] >= cutoff]

    return recent_tx.sort_values("timestamp")
