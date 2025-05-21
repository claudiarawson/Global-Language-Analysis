import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community import louvain_communities

# Load data
df = pd.read_csv('opensubtitles_pair_counts.csv')

# Build graph
G = nx.Graph()
for _, row in df.iterrows():
    G.add_edge(row['source'], row['target'], weight=row['count'])

# Detect clusters
communities = list(louvain_communities(G, weight='weight'))

# Choose a cluster
cluster_id = 2
nodes = communities[cluster_id]
subG = G.subgraph(nodes)

# Layout and draw
plt.figure(figsize=(8, 6))
pos = nx.spring_layout(subG, weight='weight', k=0.1, scale=1)
nx.draw_networkx_nodes(subG, pos, node_size=300)
nx.draw_networkx_edges(subG, pos)
nx.draw_networkx_labels(subG, pos, font_size=8)  # <-- labels here
plt.title(f'Cluster {cluster_id} with Node Labels (n={len(nodes)})')
plt.axis('off')
plt.tight_layout()
plt.show()
