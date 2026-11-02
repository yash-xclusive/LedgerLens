import networkx as nx

def build_entity_graph(records, transactions):
    """Build a transparent graph from the supplied synthetic records."""
    graph=nx.Graph()
    for r in records:
        graph.add_node(r["record_id"], kind="business_record", label=r["name"])
    for t in transactions:
        tx=t["transaction_id"]
        graph.add_node(tx, kind="transaction", label=tx)
        if t.get("entity_record_id"):
            graph.add_edge(tx, t["entity_record_id"], relationship="paid_by_or_to")
    return graph
