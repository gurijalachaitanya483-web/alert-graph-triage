"""Group alerts by topology and rank plausible upstream causes."""


def groups(edges, alerts):
    parent = {node: node for node in alerts}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    # Topology may connect alerts through healthy intermediate services.
    all_nodes = set(alerts) | {node for edge in edges for node in edge}
    parent = {node: node for node in all_nodes}
    for dependent, dependency in edges:
        union(dependent, dependency)
    incidents = {}
    for alert in alerts:
        incidents.setdefault(find(alert), set()).add(alert)
    return sorted(incidents.values(), key=lambda group: sorted(group)[0])


def rank_causes(edges, alerted):
    """Edges are (dependent, dependency); more affected dependents rank higher."""
    graph = {}
    for dependent, dependency in edges:
        graph.setdefault(dependency, set()).add(dependent)
    ranks = []
    for candidate in alerted:
        seen, pending = set(), list(graph.get(candidate, ()))
        while pending:
            node = pending.pop()
            if node in seen or node == candidate:
                continue
            seen.add(node)
            pending.extend(graph.get(node, ()))
        ranks.append((candidate, len(seen & alerted)))
    return sorted(ranks, key=lambda item: (-item[1], item[0]))


def main():
    edges = [
        ("checkout-api", "payment-db"), ("checkout-worker", "payment-db"),
        ("web", "checkout-api"), ("reporting", "analytics-db"),
    ]
    alerts = {"payment-db", "checkout-api", "checkout-worker", "web", "reporting"}
    for number, incident in enumerate(groups(edges, alerts), 1):
        print(f"Incident {number}: {', '.join(sorted(incident))}")
        print(f"  Ranked candidates: {rank_causes(edges, incident)}")


if __name__ == "__main__":
    main()
