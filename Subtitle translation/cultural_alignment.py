#!/usr/bin/env python3
"""
cultural_alignment.py

Loads translation_network_louvain.gml, maps each language to a
Huntington civilization, and visualizes/measures how well
the Louvain clusters align with cultural spheres.
"""
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import normalized_mutual_info_score, adjusted_rand_score

# 1) Load graph and extract clusters
G = nx.read_gml('translation_network_louvain.gml')
partition = nx.get_node_attributes(G, 'cluster')
df = pd.DataFrame(partition.items(), columns=['language','cluster'])

# 2) Define your ISO→civilization mapping (expand as needed)
iso_to_civ = {
    # Western
    **dict.fromkeys(['en','fr','de','nl','sv','da','no','fi','pt','pt_BR'], 'Western'),
    # Latin American
    **dict.fromkeys(['es','es_ES','es_419'], 'Latin American'),
    # Orthodox
    **dict.fromkeys(['ru','ro','bg','sr','uk','el','be','mk'], 'Orthodox'),
    # Sinic
    **dict.fromkeys(['zh_CN','zh_TW','yue','ja','ko','vi'], 'Sinic'),
    # Islamic
    **dict.fromkeys(['ar','fa','tr','ur','he','hy'], 'Islamic'),
    # Hindu (Indic)
    **dict.fromkeys(['hi','bn','pa','ta','te','kn','ml','mr','or'], 'Hindu'),
    # African (sub-Saharan)
    **dict.fromkeys(['sw','am','yo','ig','af','so','zu'], 'African'),
    # Southeast Asian
    **dict.fromkeys(['id','ms','tl'], 'Southeast Asian'),
}
df['civilization'] = df['language'].map(iso_to_civ).fillna('Other')

# 3) Confusion matrix
cm = pd.crosstab(df['cluster'], df['civilization'])
print("\n--- Confusion matrix (clusters × civilizations) ---")
print(cm)

# 4) Heatmap of the confusion matrix
plt.figure(figsize=(10,6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Cluster vs. Civilization Heatmap')
plt.xlabel('Civilization')
plt.ylabel('Louvain Cluster ID')
plt.tight_layout()
plt.savefig('cluster_civ_confusion_heatmap.png')
print("Saved cluster_civ_confusion_heatmap.png")
plt.show()

# 5) Stacked‐bar breakdown per cluster
cm_norm = cm.div(cm.sum(axis=1), axis=0)  # row‐normalize
cm_norm.plot(kind='bar', stacked=True, figsize=(10,6), colormap='tab20')
plt.legend(bbox_to_anchor=(1.0,1.0))
plt.title('Cluster Composition by Civilization (normalized)')
plt.xlabel('Cluster ID')
plt.ylabel('Proportion of Languages')
plt.tight_layout()
plt.savefig('cluster_civ_composition.png')
print("Saved cluster_civ_composition.png")
plt.show()

# 6) Alignment scores
nmi = normalized_mutual_info_score(df['cluster'], df['civilization'])
ari = adjusted_rand_score(df['cluster'], df['civilization'])
print(f"\nNormalized Mutual Information (NMI): {nmi:.3f}")
print(f"Adjusted Rand Index (ARI): {ari:.3f}")
