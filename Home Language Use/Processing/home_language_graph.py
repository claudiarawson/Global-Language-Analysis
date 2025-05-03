import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite
import community as community_louvain  # pip install python-louvain

# Load the processed CSV with country-language-percentage
df = pd.read_csv("../Datas/spoken_languages_by_country.csv")

# Initialize bipartite graph
B = nx.Graph()

# Add nodes: countries and languages
countries = df['country'].unique()
languages = df['language'].unique()
B.add_nodes_from(countries, bipartite=0, type='country')
B.add_nodes_from(languages, bipartite=1, type='language')

# Add edges with weights (percent of population)
for _, row in df.iterrows():
    B.add_edge(row['country'], row['language'], weight=row['percent'])

# 1. Bipartite Graph Plot (Country–Language network)
pos = nx.bipartite_layout(B, countries)
plt.figure(figsize=(18, 12))
nx.draw(
    B, pos,
    with_labels=True,
    node_size=50,
    font_size=5,
    edge_color='gray'
)
plt.title("Country–Language Bipartite Graph (Q272)")
plt.tight_layout()
plt.savefig("bipartite_graph.png")
plt.show()

# 2. Edge-Weight Histogram (log scale)
weights = [d['weight'] for _, _, d in B.edges(data=True)]
plt.figure(figsize=(10, 6))
plt.hist(weights, bins=50)
plt.title("Edge weight distribution (log scale)")
plt.xlabel("Percentage of population speaking a language")
plt.ylabel("Frequency (log scale)")
plt.tight_layout()
plt.savefig("weight_distribution.png")
plt.show()

# 3. Language–Language Network Projection + Louvain Clustering
language_graph = bipartite.weighted_projected_graph(B, languages)
partition = community_louvain.best_partition(language_graph, weight='weight')

# Visualize with colors for communities and sizes for importance
plt.figure(figsize=(15, 12))
pos = nx.spring_layout(language_graph, k=0.15, seed=42)
node_colors = [partition.get(n) for n in language_graph.nodes()]
node_sizes = [language_graph.degree(n, weight='weight') * 5 for n in language_graph.nodes()]
edge_weights = [d['weight'] * 0.03 for _, _, d in language_graph.edges(data=True)]

nx.draw_networkx(
    language_graph,
    pos,
    node_color=node_colors,
    node_size=node_sizes,
    edge_color=edge_weights,
    edge_cmap=plt.cm.Blues,
    with_labels=True,
    font_size=5
)
plt.title("Language–Language Network with Louvain Clustering")
plt.tight_layout()
plt.savefig("network_visualization.png")
plt.show()

# 4. Export all languages ranked by weighted degree
lang_degrees = language_graph.degree(weight='weight')
all_lang_degrees = sorted(lang_degrees, key=lambda x: x[1], reverse=True)
pd.DataFrame(all_lang_degrees, columns=['Language', 'Weighted Degree']).to_csv("../Datas/languages_by_degree.csv", index=False)
print("Languages by weighted degree saved to 'languages_by_degree.csv'.")

# 5. Export full list of country–language usage percentages
df.sort_values(by='percent', ascending=False)[['country', 'language', 'percent']].to_csv("country_language_percentages.csv", index=False)
print("Full list of country-language percentages saved to 'country_language_percentages.csv'.")

# 6. Export total global language share across all countries
df.groupby('language')['percent'].sum().sort_values(ascending=False).to_csv("language_global_percent_totals.csv", header=['TotalPercent'])
print("Total percent use of each language globally saved to 'language_global_percent_totals.csv'.")
