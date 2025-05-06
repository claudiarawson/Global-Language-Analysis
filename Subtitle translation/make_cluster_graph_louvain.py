# Hypothesis 1: Language Clusters via Louvain Clustering
# File: make_cluster_graph_louvain.py
#!/usr/bin/env python3
"""
make_cluster_graph_louvain.py

Builds a weighted translation network from OpenSubtitles pair counts,
uses Louvain at resolution=1.0 to detect ~5–8 clusters,
outputs GML, cluster-size bar chart, and network visualization.
"""
import sys
import pandas as pd
import networkx as nx
from networkx.algorithms.community import louvain_communities
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


def main(csv_path, resolution=1.0, top_n=500):
    # 1) Load pair counts
    df = pd.read_csv(csv_path, names=['source','target','count'], header=None)
    df['count'] = pd.to_numeric(df['count'], errors='coerce').fillna(0).astype(int)
    print(f"Loaded {len(df)} rows from {csv_path}")

    # 2) Build full graph
    G = nx.Graph()
    for _, r in df.iterrows():
        if r['count'] > 0:
            G.add_edge(r.source, r.target, weight=r['count'])
    print(f"Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    # 3) Louvain community detection
    comms = louvain_communities(G, weight='weight', resolution=resolution)
    partition = {n: cid for cid, comm in enumerate(comms) for n in comm}
    nx.set_node_attributes(G, partition, 'cluster')
    print(f"Louvain: resolution={resolution}, detected {len(comms)} clusters")

    # 4) Save GML
    nx.write_gml(G, 'translation_network_louvain.gml')
    print("Saved GML to translation_network_louvain.gml")

    # 5) Cluster-size bar chart
    counts = collections.Counter(partition.values())
    plt.figure(figsize=(8,5))
    plt.bar(counts.keys(), counts.values(), color='tab:blue')
    plt.xlabel('Cluster ID')
    plt.ylabel('Number of languages')
    plt.title('Cluster Sizes (Louvain)')
    plt.tight_layout()
    plt.savefig('cluster_sizes_louvain.png')
    print("Saved cluster_sizes_louvain.png")
    plt.show()

    # 6) Print cluster memberships
    membership = pd.DataFrame(sorted(partition.items()), columns=['language','cluster'])
    membership['name'] = membership['language'].map(iso_to_name)
    print("First 20 language → cluster assignments:")
    print(membership.head(20).to_string(index=False))

    # 7) Subgraph of top-N edges
    edge_list = sorted(G.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)[:top_n]
    H = nx.Graph()
    H.add_nodes_from(G.nodes(data=True))
    for u,v,d in edge_list:
        H.add_edge(u, v, weight=d['weight'])

    # 8) Visualize network
    pos = nx.spring_layout(H, seed=42, k=0.2)
    cmap = plt.get_cmap('tab20')
    colors = [cmap(partition.get(n, -1) % 20) for n in H.nodes()]
    sizes = [G.degree(n, weight='weight')/1e7 + 50 for n in H.nodes()]
    max_w = max(d['weight'] for _,_,d in H.edges(data=True))
    widths = [d['weight']/max_w*5 for _,_,d in H.edges(data=True)]
    edge_labels = {(u,v):str(d['weight']) for u,v,d in H.edges(data=True)}

    plt.figure(figsize=(14,14))
    nx.draw_networkx_edges(H, pos, width=widths, alpha=0.6)
    nx.draw_networkx_nodes(H, pos, node_size=sizes, node_color=colors, alpha=0.9)
    labels = {n: iso_to_name(n) for n in H.nodes()}
    nx.draw_networkx_labels(H, pos, labels, font_size=8)
    nx.draw_networkx_edge_labels(H, pos, edge_labels=edge_labels, font_size=6)
    plt.title(f"Top {top_n} Corridors – Louvain Clusters")
    for cid in sorted(counts):
        plt.scatter([], [], c=[cmap(cid%20)], label=f"Cluster {cid}")
    plt.legend(scatterpoints=1, fontsize=8, loc='upper right')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('network_louvain_clusters.png', dpi=300)
    print("Saved network_louvain_clusters.png")
    plt.show()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    path = sys.argv[1]
    res = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
    main(path, resolution=res)