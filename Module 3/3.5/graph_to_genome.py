import pyperclip
from chromosome_cycle_transformation import cycle_to_chromosome

def find_cycles(genome_graph) -> list:
  genome_graph = list(sorted(genome_graph))
  cycles = []

  while genome_graph:
    current_cycle = []

    start_node = min(node for edge in genome_graph for node in edge)
    final_edge_index = next(i for i, tup in enumerate(genome_graph) if start_node in tup)

    if final_edge_index == 0:
      start_node += 1
      final_edge_index = next(i for i, tup in enumerate(genome_graph) if start_node in tup)

    current_cycle = genome_graph[:final_edge_index + 1]
    genome_graph = genome_graph[final_edge_index + 1:]

    unordered_cycle = [int(item) for tup in current_cycle for item in tup]
    ordered_cycle = [unordered_cycle[-1]] + unordered_cycle[:-1]

    cycles.append(ordered_cycle)

  return cycles


def graph_to_genome(genome_graph) -> list:
  chromosomes = []

  for cycle in find_cycles(genome_graph):
    chromosome = cycle_to_chromosome(cycle)
    chromosomes.append(chromosome)

  return chromosomes


if __name__ == "__main__":
  file = open("graph_to_genome.txt", "r").read().strip()

  # Split into tuple strings and convert to tuple of ints
  tuple_strings = file.split("),")
  input = {
      tuple(map(int, pair.strip("() ").split(",")))
      for pair in tuple_strings
  }

  result = graph_to_genome(input)
  formatted = "".join(f"({' '.join(sublist)})" for sublist in result)
  print(f"Chromosomes: {formatted}")
  pyperclip.copy(formatted)


# Sample Input:
# (2, 4), (3, 6), (5, 1), (7, 9), (10, 12), (11, 8)

# Sample Output:
# (+1 -2 -3)(-4 +5 -6)


# GraphToGenome(GenomeGraph)
#      P ← an empty set of chromosomes
#      for each cycle Nodes in GenomeGraph
#           Nodes ← sequence of nodes in this cycle (starting from node 1)
#           Chromosome ← CycleToChromosome(Nodes)
#           add Chromosome to P
#      return P