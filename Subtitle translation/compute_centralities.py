
# Hypothesis 2: Centrality Metrics (Hubs & Bridges)
# File: compute_centralities.py
#!/usr/bin/env python3
"""
compute_centralities.py

Builds the translation network and computes three centrality metrics:
- weighted degree
- betweenness centrality
- PageRank
Outputs CSV + bar charts + degree vs betweenness scatter.
"""
import sys
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def main(csv_path):
    df = pd.read_csv(csv_path, names=['source','target','count'], header=None)
    df['count'] = pd.to_numeric(df['count'], errors='coerce').fillna(0).astype(int)

    # Build graph
    G = nx.Graph()
    for _, r in df.iterrows():
        if r['count'] > 0:
            G.add_edge(r['source'], r['target'], weight=r['count'])
    print(f"Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    # Weighted degree
    deg = dict(G.degree(weight='weight'))
    # Betweenness (distance=1/weight)
    dist = {(u,v):1/d['weight'] for u,v,d in G.edges(data=True)}
    dist.update({(v,u):w for (u,v),w in dist.items()})
    bc = nx.betweenness_centrality(G, weight=lambda u,v,d: dist[(u,v)], normalized=True)
    # PageRank
    pr = nx.pagerank(G, weight='weight')

    # Collate
    dfm = pd.DataFrame({'language': list(G.nodes())})
    dfm['weighted_degree'] = dfm['language'].map(deg).fillna(0).astype(int)
    dfm['betweenness'] = dfm['language'].map(bc).fillna(0.0)
    dfm['pagerank'] = dfm['language'].map(pr).fillna(0.0)
    dfm.to_csv('nodes_centrality.csv', index=False)
    print("Saved nodes_centrality.csv")

    # Top-10 tables
    for col in ['weighted_degree','betweenness','pagerank']:
        print(f"\nTop 10 by {col}:")
        print(dfm.nlargest(10,col)[['language',col]].to_string(index=False))

    # Bar charts
    plt.figure(figsize=(8,4))
    for (title, col, fname) in [
        ('Weighted Degree','weighted_degree','top_degree.png'),
        ('Betweenness','betweenness','top_betweenness.png'),
        ('PageRank','pagerank','top_pagerank.png'),
    ]:
        top10 = dfm.nlargest(10, col)
        plt.clf()
        plt.bar(top10['language'], top10[col])
        plt.xticks(rotation=45)
        plt.title(f"Top 10 by {title}")
        plt.tight_layout()
        plt.savefig(fname)
        print(f"Saved {fname}")

    # Degree vs Betweenness scatter
    plt.clf()
    plt.scatter(dfm['weighted_degree'], dfm['betweenness'])
    plt.xscale('log'); plt.yscale('log')
    plt.xlabel('Weighted Degree'); plt.ylabel('Betweenness')
    plt.title('Degree vs Betweenness (log-log)')
    plt.tight_layout(); plt.savefig('degree_vs_betweenness.png')
    print("Saved degree_vs_betweenness.png")

if __name__=='__main__':
    if len(sys.argv)!=2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1])
