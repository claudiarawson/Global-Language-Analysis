import os
import re
import csv
from collections import defaultdict
from itertools import combinations

DUMPS_DIR = "datasets"
OUTPUT_DIRECTED_CSV = "language_network_directed.csv"
OUTPUT_UNDIRECTED_CSV = "language_network_cooccurrence.csv"

pattern = re.compile(r"\((\d+),'([^']+)','[^']+'\)")

directed_edges = defaultdict(int)
undirected_edges = defaultdict(int)

for filename in os.listdir(DUMPS_DIR):
    if not filename.endswith("langlinks.sql"):
        continue

    match = re.match(r"^(\w{2,})wiki-", filename)
    if not match:
        continue
    source_lang = match.group(1)

    print(f"Processing: {filename} (source={source_lang})")

    with open(os.path.join(DUMPS_DIR, filename), 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if line.startswith("INSERT INTO"):
                matches = pattern.findall(line)
                page_links = defaultdict(set)
                for page_id, target_lang in matches:
                    page_links[page_id].add(target_lang)

                for langs in page_links.values():
                    for target_lang in langs:
                        directed_edges[(source_lang, target_lang)] += 1

                    for lang1, lang2 in combinations(sorted(langs), 2):
                        undirected_edges[frozenset((lang1, lang2))] += 1

# Save directed edges
with open(OUTPUT_DIRECTED_CSV, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['source', 'target', 'weight'])
    for (src, tgt), weight in directed_edges.items():
        writer.writerow([src, tgt, weight])

# Save undirected co-occurrence edges
with open(OUTPUT_UNDIRECTED_CSV, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['lang1', 'lang2', 'weight'])
    for langs, weight in undirected_edges.items():
        lang1, lang2 = sorted(langs)
        writer.writerow([lang1, lang2, weight])
