# src/graph_analysis.py
import networkx as nx
import matplotlib.pyplot as plt

def build_graph(transactions, top_customers, output_path):
    G = nx.DiGraph()

    for _, r in transactions.iterrows():
        G.add_edge(r['from_customer'], r['to_customer'])

    subG = G.subgraph(top_customers)

    plt.figure(figsize=(10,8))
    pos = nx.spring_layout(subG, seed=42)
    nx.draw(subG, pos, node_size=300, with_labels=True)
    plt.title("Suspicious Transaction Network")
    plt.savefig(output_path)
    plt.close()

    return output_path
