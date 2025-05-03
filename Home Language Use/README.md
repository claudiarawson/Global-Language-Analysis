# Global Home Language Network Analysis (Q272)

---

## Project Goals

**Goal**: Build and analyze a country-language bipartite network using World Values Survey Wave 7 Q272 data, which asks:  
> "What language do you normally speak at home?"

This project explores:
- Which languages are most widely spoken across countries?
- Which languages form clusters based on shared countries?
- What is the distribution of language usage (weights) across the network?

---

## Data Preparation

**Dataset Used:** `WVS_Cross-National_Wave_7_csv_v6_0.csv`  
I focused only on the columns: `B_COUNTRY` and `Q272` (the home language).

### Detailed Process:
1. Removed rows where Q272 ≤ 0 (invalid or missing responses).
2. Mapped numeric country and language codes to readable names.
3. Counted how many people in each country speak each language.
4. Calculated the percent for each country-language pair.
5. Saved the results to `spoken_languages_by_country.csv`.

### Supporting Datasets Obtained:
- `country_language_percentages.csv`: All country-language percentages.
- `language_global_percent_totals.csv`: Total language usage summed across all countries.
- `languages_by_degree.csv`: Network centrality of each language based on country connections.

---

##  Analysis Pipeline

### 1. Bipartite Graph Construction
- **Nodes:** 66 countries + 211 language labels (includes "Other").
- **Edges:** One for each country-language pair, weighted by percent of speakers.
- Visualized using `networkx.bipartite_layout`.  
 Saved as: `bipartite_graph.png`

---

### 2. Edge Weight Distribution
- At first, I used a **log-log histogram**, but small values were hard to see.
- I switched to a **linear-scale histogram** to better highlight how many links are small (<5%).
- This revealed a **long tail** — lots of small-percentage connections still count.
 Saved as: `weight_distribution.png`

---

### 3. Language–Language Projection + Clustering
- I built a new graph connecting **languages that appear together in countries**.
- Then I used **Louvain clustering** to group similar languages.
 Saved as: `network_visualization.png`

---

##  Languages Ranked by Network Degree (Excluding "Other")

| Language                         | Weighted Degree |
|----------------------------------|------------------|
| English                          | 154.5            |
| Spanish; Castilian              | 137.9            |
| French                           | 58.9             |
| Russian                          | 50.7             |
| Arabic                           | 44.3             |
| Filipino; Pilipino              | 40.5             |
| Hindi                            | 36.5             |
| Standard Chinese; Mandarin      | 35.5             |
| German                           | 32.9             |
| Portuguese                       | 31.3             |

 _Note: I excluded "Other" (which had degree 235) since it lumps many unnamed or local languages together and would inflate the ranking unfairly._

---

##  Top Country–Language Percentages

| Country     | Language                | Percent |
|-------------|--------------------------|---------|
| Bangladesh  | Bengali; Bangla         | 100.0   |
| Egypt       | Arabic                  | 100.0   |
| South Korea | Korean                  | 100.0   |
| Armenia     | Armenian; Hayeren       | 98.4    |
| Myanmar     | Burmese                 | 89.9    |
| Mexico      | Spanish; Castilian      | 99.8    |
| Uruguay     | Spanish; Castilian      | 99.7    |
| Czechia     | Czech                   | 98.7    |
| Indonesia   | Javanese                | 33.6    |
| India       | Hindi                   | 54.9    |

---

##  Key Observations

- **Long Tail**: Most country-language links are below 5%, but still represent real people and communities.
- **Language Hubs**: English, Spanish, Arabic, French, and Russian appear in many countries and are highly connected.
- **Clusters Formed**: Language families and historical regions tend to form groups (like Romance, Slavic, or Afro-Asiatic clusters).
- **Small Languages Matter**: Even low-percentage languages are part of the network and contribute to diversity.
- **“Other” Inflates Degree**: “Other” appears in many countries, but combines too many unnamed languages to be treated fairly in rankings.

---

##  Files Produced

### Graph Visualizations
- `bipartite_graph.png`
- `weight_distribution.png`
- `network_visualization.png`

### Data Tables
- `spoken_languages_by_country.csv`
- `country_language_percentages.csv`
- `language_global_percent_totals.csv`
- `languages_by_degree.csv`

---

## Tools Used
- Python (Pandas, NetworkX, Matplotlib)
- Louvain clustering (`python-louvain`)

---

