"""
translator_network_analysis.py

Comprehensive analysis of the OpenSubtitles translation network.
Generates summary stats, top corridors, degree, betweenness,
communities, colonial ties, small-language connectivity, and visualization.
"""
import pandas as pd
import networkx as nx
import community as community_louvain
import matplotlib.pyplot as plt
import argparse


def load_data(path):
    df = pd.read_csv(path)
    df = df.dropna(subset=['source', 'target', 'count'])
    df['count'] = df['count'].astype(int)
    return df


def summary_statistics(df):
    print("Weight distribution summary:")
    print(df['count'].describe())
    plt.figure()
    df['count'].hist(log=True, bins=50)
    plt.title("Edge weight distribution (log scale)")
    plt.savefig("weight_distribution.png")
    print("Saved weight distribution histogram to weight_distribution.png")
    plt.show()


def top_translation_corridors(df, top_n=10):
    top = df.sort_values('count', ascending=False).head(top_n)
    print(f"Top {top_n} translation corridors:")
    print(top)
    top.to_csv("top_edges.csv", index=False)


def weighted_degree(df):
    deg_src = df.groupby('source')['count'].sum()
    deg_tgt = df.groupby('target')['count'].sum()
    wdeg = deg_src.add(deg_tgt, fill_value=0).sort_values(ascending=False)
    wdeg_df = wdeg.reset_index()
    wdeg_df.columns = ['language', 'weighted_degree']
    wdeg_df.to_csv("weighted_degree.csv", index=False)
    print("Saved weighted degree to weighted_degree.csv")
    print("Top 10 languages by weighted degree:")
    print(wdeg_df.head(10))
    return wdeg_df


def thresholded_subgraph(df, threshold):
    H = nx.Graph()
    for _, r in df[df['count'] >= threshold].iterrows():
        w = r['count']
        H.add_edge(r.source, r.target, weight=w)
    comps = sorted(nx.connected_components(H), key=len, reverse=True)
    for i, comp in enumerate(comps[:5]):
        print(f"Component {i+1} (size {len(comp)}): {comp}")
    return H


def quick_betweenness(H):
    dist = {(u, v): 1.0 / d['weight'] for u, v, d in H.edges(data=True)}
    dist.update({(v, u): w for (u, v), w in dist.items()})
    bc = nx.betweenness_centrality(H, weight=lambda u, v, d: dist[(u, v)], normalized=True)
    top5 = sorted(bc.items(), key=lambda x: x[1], reverse=True)[:5]
    print("Top 5 bridges in thresholded graph:")
    for lang, score in top5:
        print(f"{lang}: {score:.4f}")
    return bc


def build_full_graph(df, min_weight=1000):
    G = nx.Graph()
    for _, r in df.iterrows():
        count = r['count']
        if count >= min_weight:
            G.add_edge(r.source, r.target, weight=count)
    print(f"Full graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges (min_weight={min_weight})")
    return G


def compute_full_louvain(G):
    print("Running Louvain community detection on full graph...")
    partition = community_louvain.best_partition(G, weight='weight')
    clusters = pd.DataFrame.from_dict(partition, orient='index', columns=['cluster']).reset_index()
    clusters.columns = ['language', 'cluster']
    clusters.to_csv('clusters.csv', index=False)
    print("Saved clusters to clusters.csv")
    return partition


def full_betweenness(G):
    print("Computing full betweenness centrality...")
    dist = {(u, v): 1.0 / d['weight'] for u, v, d in G.edges(data=True)}
    dist.update({(v, u): w for (u, v), w in dist.items()})
    bc = nx.betweenness_centrality(G, weight=lambda u, v, d: dist[(u, v)], normalized=True)
    bc_df = pd.DataFrame(bc.items(), columns=['language', 'betweenness']).sort_values('betweenness', ascending=False)
    bc_df.to_csv('betweenness.csv', index=False)
    print("Saved betweenness centrality to betweenness.csv")
    return bc


def node_metrics_csv(G, wdeg_df, bc):
    # Ensure all graph nodes are included
    bc_series = pd.Series(bc, name='betweenness')
    wdeg_series = pd.Series(wdeg_df.set_index('language')['weighted_degree'], name='weighted_degree')
    nodes = pd.DataFrame({'language': list(G.nodes())})
    metrics = nodes.set_index('language').join(wdeg_series).join(bc_series).reset_index()
    # fill missing with zeros
    metrics[['weighted_degree','betweenness']] = metrics[['weighted_degree','betweenness']].fillna(0)
    partition = pd.read_csv('clusters.csv')
    metrics = metrics.merge(partition, on='language', how='left').fillna({'cluster': -1})
    metrics.to_csv('nodes_metrics.csv', index=False)
    print("Saved combined node metrics to nodes_metrics.csv")


def visualize_graph(G, partition, wdeg, top_edges=500):
    print("Visualizing full network with top edges and weights...")
    # Filter to top edges by weight
    edges = sorted(G.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)[:top_edges]
    H = nx.Graph()
    for u, v, d in edges:
        H.add_edge(u, v, weight=d['weight'])
    # layout
    plt.figure(figsize=(14, 14))
    pos = nx.spring_layout(H, seed=42, k=0.2)
    # color map for clusters
    uniq_clusters = sorted(set(partition.values()))
    cmap = plt.get_cmap('tab20')
    node_colors = [cmap(uniq_clusters.index(partition.get(node, -1)) % 20) for node in H.nodes()]
    # size by degree in full graph
    sizes = [max(wdeg.get(node,1),1)/1e7 for node in H.nodes()]
    # draw edges with widths proportional to weight
    max_w = max(d['weight'] for (_,_,d) in H.edges(data=True))
    widths = [d['weight']/max_w * 5 for (_,_,d) in H.edges(data=True)]
    nx.draw_networkx_edges(H, pos, width=widths, alpha=0.6)
    # draw nodes
    nx.draw_networkx_nodes(H, pos, node_size=sizes, node_color=node_colors, alpha=0.9)
    # label all nodes
    labels = {node: node for node in H.nodes()}
    nx.draw_networkx_labels(H, pos, labels, font_size=8)
    # edge weight labels
    edge_labels = {(u, v): f"{d['weight']}" for u, v, d in H.edges(data=True)}
    nx.draw_networkx_edge_labels(H, pos, edge_labels=edge_labels, font_size=6)
    plt.title("Top translation corridors network (nodes colored by cluster, sized by volume, edge widths & labels by count)")
    # legend for clusters
    for idx, c in enumerate(uniq_clusters):
        plt.scatter([], [], c=[cmap(idx % 20)], label=f"Cluster {c}")
    plt.legend(scatterpoints=1, fontsize=8, loc='upper right')
    plt.axis('off')
    plt.savefig("network_visualization.png", dpi=300)
    print("Saved network visualization to network_visualization.png")
    plt.show()


def small_language_connectivity(df, wdeg_df):
    cutoff = wdeg_df['weighted_degree'].quantile(0.25)
    small = wdeg_df[wdeg_df['weighted_degree'] <= cutoff]['language']
    result = []
    for lang in small:
        all_nbrs = set(df[(df.source == lang) | (df.target == lang)]['source'] + df[(df.source == lang) | (df.target == lang)]['target']) - {lang}
        strong_nbrs = set(df[((df.source == lang) | (df.target == lang)) & (df['count'] >= 10000)]['source'] + df[((df.source == lang) | (df.target == lang)) & (df['count'] >= 10000)]['target']) - {lang}
        result.append({'language': lang, 'num_neighbors_all': len(all_nbrs), 'num_strong_neighbors': len(strong_nbrs)})
    slc_df = pd.DataFrame(result).sort_values('num_neighbors_all')
    slc_df.to_csv('small_language_connectivity.csv', index=False)
    print("Saved small-language connectivity to small_language_connectivity.csv")
    print(slc_df.head(10))
    return slc_df


def extract_colonial_edges(df):
    patterns = ['af', 'sn', 'cm', 'ml', 'ht', 'cd']
    colonial = df[(df.source == 'fr') & df.target.str.startswith(tuple(patterns))]
    colonial.to_csv('colonial_edges.csv', index=False)
    print("Saved colonial French-Africa edges to colonial_edges.csv")


def main():
    parser = argparse.ArgumentParser(description="Analyze translation network from OpenSubtitles pair counts")
    parser.add_argument("csv_path", help="Path to opensubtitles_pair_counts.csv")
    args = parser.parse_args()

    df = load_data(args.csv_path)
    summary_statistics(df)
    top_translation_corridors(df, top_n=10)
    wdeg_df = weighted_degree(df)
    H = thresholded_subgraph(df, threshold=1e7)
    quick_betweenness(H)
    extract_colonial_edges(df)
    G = build_full_graph(df, min_weight=1000)
    partition = compute_full_louvain(G)
    bc = full_betweenness(G)
    node_metrics_csv(G, wdeg_df, bc)
    wdeg_map = dict(zip(wdeg_df['language'], wdeg_df['weighted_degree']))
    visualize_graph(G, partition, wdeg_map, top_edges=500)
    small_language_connectivity(df, wdeg_df)


if __name__ == "__main__":
    main()
