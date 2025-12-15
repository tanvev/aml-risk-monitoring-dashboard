import networkx as nx
import matplotlib.pyplot as plt

def plot_clean_network(transactions, customer_id):
    G = nx.DiGraph()

    cust_tx = transactions[
        (transactions["from_customer"] == customer_id) |
        (transactions["to_customer"] == customer_id)
    ]

    for _, r in cust_tx.iterrows():
        G.add_edge(r["from_customer"], r["to_customer"])

    sub_nodes = list(G.nodes())[:12]
    subG = G.subgraph(sub_nodes)

    plt.figure(figsize=(7, 7))
    pos = nx.spring_layout(subG, k=1.8, seed=42)

    nx.draw(
        subG,
        pos,
        node_size=900,
        node_color=[
            "red" if n == customer_id else "#8ecae6"
            for n in subG.nodes()
        ],
        with_labels=False
    )

    for node, (x, y) in pos.items():
        plt.text(x, y + 0.06, node, fontsize=8, ha="center")

    plt.title("Transaction Network (Clean View)")
    return plt
