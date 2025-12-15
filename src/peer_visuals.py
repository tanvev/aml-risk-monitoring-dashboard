import matplotlib.pyplot as plt

def peer_boxplot(customers, features, customer_id, metric):
    cust = customers[customers["customer_id"] == customer_id].iloc[0]

    low = cust["income"] * 0.7
    high = cust["income"] * 1.3

    peers = customers[
        (customers["branch"] == cust["branch"]) &
        (customers["income"] >= low) &
        (customers["income"] <= high)
    ]

    peer_features = features[features["customer_id"].isin(peers["customer_id"])]
    cust_value = features[features["customer_id"] == customer_id][metric].iloc[0]

    fig, ax = plt.subplots()
    ax.boxplot(peer_features[metric], vert=False)
    ax.scatter(cust_value, 1, color="red", label="Customer")
    ax.set_title(f"Peer Comparison: {metric}")
    ax.legend()

    return fig
