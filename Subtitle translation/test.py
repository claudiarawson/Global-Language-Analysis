#!/usr/bin/env python3
"""
make_cluster_graph.py

Builds a weighted translation network from OpenSubtitles pair counts,
detects communities, outputs GML, and visualizes with colored clusters,
full node labels (language names), edge widths & weight labels.
"""
import sys
import pandas as pd
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities
import matplotlib.pyplot as plt
import collections

# Optional ISO-to-language mapping
try:
    import pycountry
    def iso_to_name(code):
        base = code.split('_')[0]
        lang = pycountry.languages.get(alpha_2=base)
        return lang.name if lang else code
except ImportError:
    iso_to_name = lambda code: code


def main(csv_path):
    # Load CSV (no header assumed)
    df = pd.read_csv(csv_path, names=['source','target','count'], header=None)
    # Ensure numeric counts
    df['count'] = pd.to_numeric(df['count'], errors='coerce').fillna(0).astype(int)
    print(f"Loaded {len(df)} rows from {csv_path}")

    # Build graph with only positive edges
    G = nx.Graph()
    for _, row in df.iterrows():
        if row['count'] > 0:
            G.add_edge(row['source'], row['target'], weight=row['count'])
    print(f"Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    # Community detection (greedy modularity fallback)
    comms = greedy_modularity_communities(G, weight='weight')
    partition = {n: cid for cid, c in enumerate(comms) for n in c}
    nx.set_node_attributes(G, partition, 'cluster')
    print(f"Detected {len(comms)} communities")

    # Save GML
    gml_path = 'translation_network.gml'
    nx.write_gml(G, gml_path)
    print(f"Saved GML to {gml_path}")

    # Cluster size bar chart
    counts = collections.Counter(partition.values())
    plt.figure(figsize=(8,5))
    plt.bar(counts.keys(), counts.values(), color='skyblue')
    plt.xlabel('Cluster ID')
    plt.ylabel('Number of languages')
    plt.title('Cluster Sizes in Translation Network')
    plt.tight_layout()
    plt.savefig('cluster_sizes.png')
    print("Saved cluster_sizes.png")
    plt.show()

    # First 20 cluster assignments
    membership = pd.DataFrame(sorted(partition.items()), columns=['language','cluster'])
    membership['name'] = membership['language'].map(iso_to_name)
    print("First 20 language → cluster assignments:")
    print(membership.head(20).to_string(index=False))

    # Visualize top-edges subgraph
    # Select top-N edges by weight
    N = 500
    edges = sorted(G.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)[:N]
    H = nx.Graph()
    H.add_nodes_from(G.nodes(data=True))  # preserve all nodes for labeling
    for u, v, d in edges:
        H.add_edge(u, v, weight=d['weight'])

    # Layout
    pos = nx.spring_layout(H, seed=42, k=0.2)
    # Node colors by cluster
    unique_cids = sorted(set(partition.values()))
    cmap = plt.get_cmap('tab20')
    node_colors = [cmap(unique_cids.index(partition.get(n, -1)) % 20) for n in H.nodes()]
    # Node sizes by total degree weight
    sizes = [G.degree(n, weight='weight')/1e7 + 100 for n in H.nodes()]

    # Edge widths and labels
    max_w = max((d['weight'] for _,_,d in H.edges(data=True)), default=1)
    widths = [d['weight']/max_w * 5 for _,_,d in H.edges(data=True)]
    edge_labels = {(u, v): str(d['weight']) for u, v, d in H.edges(data=True)}

    plt.figure(figsize=(14,14))
    nx.draw_networkx_edges(H, pos, width=widths, alpha=0.6)
    nx.draw_networkx_nodes(H, pos, node_size=sizes, node_color=node_colors, alpha=0.9)
    # Label all nodes with language name
    labels = {n: iso_to_name(n) for n in H.nodes()}
    nx.draw_networkx_labels(H, pos, labels, font_size=8)
    # Label edges with weights
    nx.draw_networkx_edge_labels(H, pos, edge_labels=edge_labels, font_size=6)

    plt.title(f"Top {N} Translation Corridors (colored by cluster, labeled by language)")
    # Cluster legend
    for idx, cid in enumerate(unique_cids):
        plt.scatter([], [], c=[cmap(idx % 20)], label=f"Cluster {cid}")
    plt.legend(scatterpoints=1, fontsize=8, loc='upper right')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('network_by_cluster.png', dpi=300)
    print("Saved network_by_cluster.png")
    plt.show()

    # Print cluster size summary
    print("\nCluster size summary:")
    for cid, size in sorted(counts.items()):
        print(f" Cluster {cid:2d}: {size:3d} languages")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1])
