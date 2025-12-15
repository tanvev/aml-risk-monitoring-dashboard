import pandas as pd

def build_features(transactions, customers):
    # Incoming transactions
    incoming = (
        transactions.groupby("to_customer")["amount"]
        .agg(total_in="sum", count_in="count")
        .reset_index()
        .rename(columns={"to_customer": "customer_id"})
    )

    # Outgoing transactions
    outgoing = (
        transactions.groupby("from_customer")["amount"]
        .agg(total_out="sum", count_out="count")
        .reset_index()
        .rename(columns={"from_customer": "customer_id"})
    )

    # FULL OUTER JOIN between incoming and outgoing
    features = pd.merge(incoming, outgoing, on="customer_id", how="outer")

    # Attach ALL customers (very important)
    features = customers[["customer_id", "kyc_risk_score"]].merge(
        features, on="customer_id", how="left"
    )

    # Fill missing numeric values
    for col in ["total_in", "count_in", "total_out", "count_out"]:
        if col not in features:
            features[col] = 0
        features[col] = features[col].fillna(0)

    # Derived features
    features["txn_count"] = features["count_in"] + features["count_out"]
    features["in_out_ratio"] = features["total_in"] / (features["total_out"] + 1)

    return features
