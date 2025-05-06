#!/usr/bin/env python3
"""
evaluate_clusters.py

Given translation_network_louvain.gml, 
print full membership, compute confusion matrix vs Huntington civilizations,
and report Normalized Mutual Information.
"""
import networkx as nx
import pandas as pd
from sklearn.metrics import normalized_mutual_info_score

def main(gml_path):
    # 1) Load GML
    G = nx.read_gml(gml_path)
    partition = nx.get_node_attributes(G, 'cluster')
    clusters_df = pd.DataFrame(list(partition.items()), columns=['language','cluster'])

    # 2) Full membership table
    clusters_df_sorted = clusters_df.sort_values(['cluster','language'])
    print("\nFull cluster membership:")
    print(clusters_df_sorted.to_string(index=False))

    # 3) Reference ISO → Huntington civilization
    iso_to_civ = {
        # Western
        'en':'Western','fr':'Western','de':'Western','nl':'Western',
        'sv':'Western','da':'Western','no':'Western','fi':'Western',
        # Latin American
        'es':'Latin American','pt_BR':'Latin American',
        # Orthodox
        'ru':'Orthodox','ro':'Orthodox','bg':'Orthodox','sr':'Orthodox',
        'uk':'Orthodox','el':'Orthodox',
        # Sinic
        'zh_CN':'Sinic','zh_TW':'Sinic','ja':'Sinic','ko':'Sinic',
        # Islamic
        'ar':'Islamic','fa':'Islamic','tr':'Islamic','ur':'Islamic',
        # Hindu
        'hi':'Hindu','bn':'Hindu','pa':'Hindu','ta':'Hindu',
        # African
        'sw':'African','am':'African','yo':'African','ig':'African',
        # Fallback → 'Other'
    }

    # 4) Map languages to civilizations
    clusters_df['civilization'] = clusters_df['language'].map(iso_to_civ).fillna('Other')

    # 5) Confusion matrix
    cm = pd.crosstab(clusters_df['cluster'], clusters_df['civilization'])
    print("\nConfusion matrix (Cluster vs Civilization):")
    print(cm.to_string())

    # 6) Compute and report NMI
    nmi = normalized_mutual_info_score(clusters_df['cluster'], clusters_df['civilization'])
    print(f"\nNormalized Mutual Information: {nmi:.3f}")

if __name__ == "__main__":
    import sys
    if len(sys.argv)!=2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1])
