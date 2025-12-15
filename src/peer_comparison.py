import pandas as pd
import numpy as np

def peer_group_analysis(customer_id, customers, features):
    cust = customers[customers["customer_id"] == customer_id].iloc[0]

    income_low = cust["income"] * 0.7
    income_high = cust["income"] * 1.3

    peers = customers[
        (customers["branch"] == cust["branch"]) &
        (customers["income"] >= income_low) &
        (customers["income"] <= income_high)
    ]

    peer_features = features[features["customer_id"].isin(peers["customer_id"])]

    customer_row = features[features["customer_id"] == customer_id].iloc[0]

    metrics = ["txn_count", "total_out", "total_in"]

    results = {}
    for m in metrics:
        peer_values = peer_features[m]
        percentile = (peer_values < customer_row[m]).mean() * 100
        results[m] = {
            "customer": customer_row[m],
            "peer_avg": peer_values.mean(),
            "percentile": percentile
        }

    return results
