# Global-Language-Analysis
## 


---

## Subtitle translation: Lesly and Fozhan

### Goal: Build and analyze a global translation-frequency network of 94 languages from the OpenSubtitles v2024 corpus, to answer questions like


- Which are the largest language clusters?
- Which language acts as the biggest “bridge” (high betweenness)?
- Is English truly the most central?
- Do East–West or colonial ties appear?
- How do smaller languages hook into the network?

**Extended vision:** Compare these patterns to other cross-lingual networks (Wikipedia inter-language links, Google Trends correlations) for deeper cultural insights.

---

### Data Acquisition
```bash
OPUS-API “?languages=true”
```

Retrieved the list of all 94 ISO language codes in OpenSubtitles v2024.

OPUS-API per-pair metadata

Loop over every ordered (source, target) pair to pull the field alignment_pairs (number of subtitle sentence alignments).

Saved as opensubtitles_pair_counts.csv (~6,752 nonzero rows).

Key decision:
**We never downloaded the raw subtitle files (3 TB!). For our network, only the counts matter. :>**

---

### Analysis Pipeline
All code lives in a single Python script, main.py under the folder Subtitle translation, whose major stages are:

**Summary Statistics**
```bash
count.describe() & log-scale histogram → shows a heavy-tailed edge-weight distribution (min = 8, 25 % ≈ 9.6 K, median ≈ 1.4 × 10⁵, max ≈ 1.15 × 10⁸).
```

**Top Translation Corridors**

Extract top 10 language-pairs by volume (e.g. en–pt_BR ~115 M, en–es ~105 M, ro–en ~100 M, etc.).

Weighted Degree

Sum of edge-weights per language → overall hubs (en, pt_BR, ro, es, ar, nl, pl, tr, el, fr).

**Quick Subgraph & Betweenness**

Threshold edges ≥ 10 million to preview “Component 1” (37 languages) and compute quick betweenness on that subgraph → English dominates.

Full Graph Construction

Keep edges ≥ 1,000 to retain connectivity while dropping the tiniest noise.

Louvain Community Detection

Partition 90-node graph into clusters (e.g. Indo-European, Afro-Asiatic, Sino-Tibetan blocks).

**Full Betweenness Centrality**

Transform weights → distances (1/weight) and compute normalized betweenness for all 90 nodes.

Node-Level Metrics

Merged degree, betweenness, and cluster assignments into nodes_metrics.csv (now includes all nodes, filling missing values with zeros).

Small-Language Connectivity

For the bottom 25 % by volume, report both

num_neighbors_all (any link)


num_neighbors_strong (links ≥ 10 K)


Exported in small_language_connectivity.csv.


Colonial-Tie Extraction


Filtered French→former-colonies (e.g. cm, sn, ml) into colonial_edges.csv.



### Visualizations
Edge-Weight Histogram


Saved as weight_distribution.png: log-scale bins showing the long tail.


Network Plot (network_visualization.png)


Subgraph of top 500 edges by weight.


Nodes colored by Louvain cluster (legend included).


Node sizes ∝ weighted degree.


Edges drawn with width ∝ weight, and each edge labelled with its raw count.


All nodes labeled, with font sizes balanced for readability.


### Immediate Findings
Heavy-tail: A handful of language-pairs (en–pt_BR, en–es, en–ro) dominate, but millions of lower-volume links knit smaller languages in.


Language hubs: English is by far the busiest and has the highest betweenness; Portuguese, Romanian, Spanish, Arabic also rank very high.


Clusters: Clear groupings by family/region (e.g. Romance, Slavic, Afro-Asiatic, Sino-Tibetan).


Small languages: Many in the bottom quartile have dozens of connections (even if not “strong”), often via English or the regional lingua franca.


Colonial signals: French→Cameroon, French→Senegal edges appear but are far lower volume than European intra-cluster corridors.




