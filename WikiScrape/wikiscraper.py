import argparse
import os
import networkx as nx
import matplotlib.pyplot as plt
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Spider
from scrapy.utils.project import get_project_settings
from urllib.parse import urlparse, urldefrag
from itertools import combinations


class WikipediaLanguageSpider(Spider):
    name = 'wikipedia_language_spider'

    def __init__(self, start_urls, domain, max_pages, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = start_urls
        self.allowed_domains = [urlparse(domain).netloc]
        self.max_pages = max_pages
        self.visited = set()
        self.graph = nx.Graph()

    def parse(self, response):
        url = urldefrag(response.url)[0]

        if url not in self.visited:
            if len(self.visited) >= self.max_pages:
                return
            self.visited.add(url)

        if len(self.visited) % 10 == 0:
            print(f"Progress: {len(self.visited)} pages processed...")

        print(f"Visited: {url}")

        # Extract language codes
        lang_codes = set()
        for a in response.css('a[hreflang]'):
            lang = a.attrib.get('hreflang')
            if lang:
                lang_codes.add(lang)

        lang_codes.add('en')  # Include English (base language)

        # Skip pages with too many languages to speed up testing
        #if len(lang_codes) < 2 or len(lang_codes) > 10:
            #return

        article_title = url.split('/wiki/')[-1]
        edge_count = 0

        for lang1, lang2 in combinations(lang_codes, 2):
            edge = tuple(sorted((lang1, lang2)))
            if not self.graph.has_edge(*edge):
                self.graph.add_edge(*edge, articles=[article_title])
            else:
                self.graph[edge[0]][edge[1]]['articles'].append(article_title)
            edge_count += 1

        print(f"Added {edge_count} edges for: {article_title}")

        # Continue crawling internal article links
        for link in response.css('a::attr(href)').getall():
            if link.startswith('/wiki/') and ':' not in link and '#' not in link:
                full_url = response.urljoin(link)
                full_url = urldefrag(full_url)[0]
                if full_url not in self.visited and len(self.visited) < self.max_pages:
                    yield response.follow(full_url, self.parse)


def plot_graph(graph):
    if graph.number_of_nodes() == 0:
        print("Graph is empty.")
        return

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(graph, seed=42)
    nx.draw(graph, pos, with_labels=True, node_size=500, font_size=10)
    plt.title("Language Connectivity via Shared Wikipedia Articles")
    plt.axis("off")
    plt.show()


def run_crawler(crawler_file):
    with open(crawler_file, 'r') as file:
        lines = [line.strip() for line in file.readlines() if line.strip()]
        max_nodes = int(lines[0])
        domain = lines[1]
        seeds = lines[2:]

    results = {}

    class WrapperSpider(WikipediaLanguageSpider):
        custom_settings = {
            'LOG_ENABLED': False,
            'DOWNLOAD_DELAY': 1.0,
            'CONCURRENT_REQUESTS': 1,
            'AUTOTHROTTLE_ENABLED': True,
            'AUTOTHROTTLE_START_DELAY': 1.0,
            'AUTOTHROTTLE_MAX_DELAY': 2.0,
            'USER_AGENT': 'LanguageGraphBot/1.0 (https://example.com/contact)'
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def closed(self, reason):
            print("Spider closed, finalizing graph...")
            results['graph'] = self.graph
            print(f"Graph has {self.graph.number_of_nodes()} nodes and {self.graph.number_of_edges()} edges")


    process = CrawlerProcess(get_project_settings())
    process.crawl(WrapperSpider, start_urls=seeds,
                  domain=domain, max_pages=max_nodes)
    process.start()

    return results['graph']


def compute_pagerank(graph):
    return nx.pagerank(graph)


def main():
    parser = argparse.ArgumentParser(
        description="Wikipedia Language Graph Builder")
    parser.add_argument("--crawler", help="Input crawler file")
    parser.add_argument("--input", help="Input graph GML file")
    parser.add_argument("--crawler_graph", help="Output GML graph from crawler")
    parser.add_argument("--pagerank_values", help="Output file for PageRank values")
    parser.add_argument("--plotgraph", action="store_true", help="Plot the graph")

    args = parser.parse_args()
    graph = None

    try:
        if args.crawler:
            print("Starting crawling...")
            graph = run_crawler(args.crawler)
            print(f"Crawling finished. Languages found: {len(graph.nodes())}")
            if args.crawler_graph:
                nx.write_gml(graph, args.crawler_graph)
                print(f"Graph saved to {args.crawler_graph}")

        elif args.input:
            if not os.path.exists(args.input):
                raise FileNotFoundError(f"Input file {args.input} not found.")
            graph = nx.read_gml(args.input)
            print(f"Graph loaded from {args.input}. Nodes: {len(graph.nodes())}")

        else:
            raise ValueError("Either --crawler or --input must be provided.")

        if args.plotgraph:
            plot_graph(graph)

        if args.pagerank_values:
            pagerank = compute_pagerank(graph)
            with open(args.pagerank_values, 'w') as f:
                for node, rank in sorted(pagerank.items(), key=lambda item: item[1], reverse=True):
                    f.write(f"{node} {rank:.6f}\n")
            print(f"PageRank values written to {args.pagerank_values}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
