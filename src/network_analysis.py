import networkx as nx
import matplotlib.pyplot as plt

def build_customer_network(transactions, customer_id, max_nodes=15):
    G = nx.DiGraph()

    cust_tx = transactions[
        (transactions["from_customer"] == customer_id) |
        (transactions["to_customer"] == customer_id)
    ]

    for _, r in cust_tx.iterrows():
        G.add_edge(r["from_customer"], r["to_customer"], weight=r["amount"])

    nodes = list(G.nodes())[:max_nodes]
    subG = G.subgraph(nodes)

    return subG


def plot_network(subG, highlight):
    plt.figure(figsize=(6, 6))
    pos = nx.spring_layout(subG, seed=42)

    node_colors = ["red" if n == highlight else "lightblue" for n in subG.nodes()]

    nx.draw(
        subG,
        pos,
        with_labels=True,
        node_color=node_colors,
        node_size=800,
        font_size=8
    )

    plt.title("Transaction Network (Potential Mule Pattern)")
    return plt
