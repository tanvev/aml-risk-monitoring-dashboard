import pandas as pd

def behavioral_shift(transactions, customer_id):
    transactions["timestamp"] = pd.to_datetime(transactions["timestamp"])

    cust_tx = transactions[
        (transactions["from_customer"] == customer_id) |
        (transactions["to_customer"] == customer_id)
    ]

    recent = cust_tx[cust_tx["timestamp"] >= pd.Timestamp.now() - pd.Timedelta(days=30)]
    past = cust_tx[cust_tx["timestamp"] < pd.Timestamp.now() - pd.Timedelta(days=30)]

    def stats(df):
        return {
            "txn_count": len(df),
            "total_amount": df["amount"].sum(),
            "avg_amount": df["amount"].mean() if len(df) else 0
        }

    return stats(past), stats(recent)
