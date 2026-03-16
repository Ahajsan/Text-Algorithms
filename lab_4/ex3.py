import time
import tracemalloc
from typing import Dict
from collections import defaultdict


# Tablica sufiksów
def build_suffix_array(text: str):
    return sorted(range(len(text)), key=lambda i: text[i:])


# Drzewo sufiksów – uproszczona wersja
class SuffixTreeNode:
    def __init__(self):
        self.children = defaultdict(SuffixTreeNode)
        self.size = 0  # Liczba potomków


def build_suffix_tree(text: str) -> SuffixTreeNode:
    root = SuffixTreeNode()
    for i in range(len(text)):
        node = root
        for c in text[i:]:
            node = node.children[c]
    return root


def count_suffix_tree_nodes(node: SuffixTreeNode) -> int:
    count = 1  # Liczymy ten węzeł
    for child in node.children.values():
        count += count_suffix_tree_nodes(child)
    return count


# Pomiar zużycia pamięci i czasu
def measure_memory_and_time(func, *args):
    tracemalloc.start()
    start_time = time.perf_counter()
    result = func(*args)
    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        "result": result,
        "construction_time_ms": (end_time - start_time) * 1000,
        "memory_usage_kb": peak / 1024
    }


# Główna funkcja porównawcza
def compare_suffix_structures(text: str) -> Dict:
    suffix_array_data = measure_memory_and_time(build_suffix_array, text)
    suffix_tree_data = measure_memory_and_time(build_suffix_tree, text)

    suffix_array_size = len(suffix_array_data["result"])
    suffix_tree_size = count_suffix_tree_nodes(suffix_tree_data["result"])

    return {
        "suffix_array": {
            "construction_time_ms": suffix_array_data["construction_time_ms"],
            "memory_usage_kb": suffix_array_data["memory_usage_kb"],
            "size": suffix_array_size
        },
        "suffix_tree": {
            "construction_time_ms": suffix_tree_data["construction_time_ms"],
            "memory_usage_kb": suffix_tree_data["memory_usage_kb"],
            "size": suffix_tree_size
        }
    }
import matplotlib.pyplot as plt

def run_experiments():
    import random
    import string

    sizes = [100, 1000, 10000, 100000]
    results = []

    for size in sizes:
        text = ''.join(random.choices(string.ascii_lowercase, k=size))
        print(f"Testing size: {size}")
        stats = compare_suffix_structures(text)
        results.append({
            "size": size,
            "suffix_array": stats["suffix_array"],
            "suffix_tree": stats["suffix_tree"]
        })

    return results


def plot_results(results):
    sizes = [r["size"] for r in results]

    def extract(metric, structure):
        return [r[structure][metric] for r in results]

    # Construction time
    plt.figure(figsize=(10, 5))
    plt.plot(sizes, extract("construction_time_ms", "suffix_array"), label="Suffix Array")
    plt.plot(sizes, extract("construction_time_ms", "suffix_tree"), label="Suffix Tree")
    plt.xlabel("Text Length")
    plt.ylabel("Construction Time (ms)")
    plt.title("Construction Time vs Text Size")
    plt.legend()
    plt.grid(True)
    plt.xscale("log")
    plt.yscale("log")
    plt.show()

    # Memory usage
    plt.figure(figsize=(10, 5))
    plt.plot(sizes, extract("memory_usage_kb", "suffix_array"), label="Suffix Array")
    plt.plot(sizes, extract("memory_usage_kb", "suffix_tree"), label="Suffix Tree")
    plt.xlabel("Text Length")
    plt.ylabel("Memory Usage (KB)")
    plt.title("Memory Usage vs Text Size")
    plt.legend()
    plt.grid(True)
    plt.xscale("log")
    plt.yscale("log")
    plt.show()

    # Structure size
    plt.figure(figsize=(10, 5))
    plt.plot(sizes, extract("size", "suffix_array"), label="Suffix Array")
    plt.plot(sizes, extract("size", "suffix_tree"), label="Suffix Tree")
    plt.xlabel("Text Length")
    plt.ylabel("Structure Size")
    plt.title("Structure Size vs Text Size")
    plt.legend()
    plt.grid(True)
    plt.xscale("log")
    plt.yscale("log")
    plt.show()

