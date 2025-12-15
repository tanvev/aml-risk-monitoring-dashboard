import networkx as nx

def compute_network_risk(transactions, customer_id):
    G = nx.DiGraph()

    for _, r in transactions.iterrows():
        G.add_edge(r["from_customer"], r["to_customer"], amount=r["amount"])

    if customer_id not in G:
        return 0

    in_deg = G.in_degree(customer_id)
    out_deg = G.out_degree(customer_id)

    in_amt = sum(G[u][customer_id]["amount"] for u in G.predecessors(customer_id))
    out_amt = sum(G[customer_id][v]["amount"] for v in G.successors(customer_id))

    pass_through = abs(in_amt - out_amt) / (in_amt + 1) < 0.25
    hub = in_deg >= 3 and out_deg >= 3

    score = 0
    score += min((in_deg + out_deg) * 8, 40)
    score += 30 if pass_through else 0
    score += 30 if hub else 0

    return min(score, 100)
