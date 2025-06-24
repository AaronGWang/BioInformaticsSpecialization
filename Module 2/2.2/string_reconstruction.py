import random
import pyperclip


def construct_de_bruijn_graph(k: int, patterns: list[str]) -> dict[str, set[str]]:
  '''
  Construct a De Bruijn graph from a list of k-mers.

  Parameters:
    k (int): the length of the k-mers
    patterns (list[str]): a list of k-mers

  Returns:
    edges (dict[str, set[str]]): a directed graph represented as an adjacency list
  '''
  edges = {}

  for pattern in patterns:
    pattern_suffix = pattern[1:]

    for other_pattern in patterns:

      if other_pattern == pattern:
        continue

      other_pattern_prefix = other_pattern[:-1]

      if pattern_suffix == other_pattern_prefix:
        if pattern in edges:
          edges[pattern].append(other_pattern)
        else:
          edges[pattern] = [other_pattern]

  return edges


def connect_boundary_nodes(graph: dict[str, list[str]]):
  '''
  Find the starting and ending nodes for an Eulerian path in a directed graph.
  
  Parameters:
    graph (dict[str, list[str]]): a directed graph represented as an adjacency list

  Returns:
    graph (dict[str, list[str]]): the modified graph with the end node connected to the start node
  '''

  # Initialize start and end nodes
  start_node = end_node = None
  nodes = list(set(graph.keys()).union(set(node for edges in graph.values() for node in edges)))
  
  # Initialize dictionaries to track in-degrees and out-degrees for each node
  in_degrees = {node: 0 for node in nodes}
  out_degrees = {node: 0 for node in nodes}

  # Calculate in-degrees and out-degrees for each node
  for node, edges in graph.items():
    out_degrees[node] = len(edges)
    for neighbor in edges:
      in_degrees[neighbor] += 1

  # Identify the start and end nodes based on the degree conditions
  for node in nodes:
    out_deg = out_degrees.get(node, 0)
    in_deg = in_degrees.get(node, 0)

    if out_deg - in_deg == 1:
      start_node = node
    elif in_deg - out_deg == 1:
      end_node = node

  graph[end_node] = graph.get(end_node, []) + [start_node]
  return graph, start_node, end_node


def eulerian_path(graph: dict[int, list[int]], start_node: int) -> list[int]:
  '''
  Find an Eulerian cycle in a directed graph using a random walk approach.

  Parameters:
    graph (dict[int, list[int]]): a directed graph represented as an adjacency list


  Returns:
    cycle (list[int]): an Eulerian cycle in the graph
  '''
  # Initialize the cycle and starting node
  path = []
  current_node = start_node
  path.append(current_node)

  while True:
    # Walk through the graph
    next_node = random.choice(graph[current_node])
    path.append(next_node)
    graph[current_node].remove(next_node)
    current_node = next_node

    # If we have no unexplored edges left, we can break the loop
    if not any(graph.values()):
      break

    # If we get stuck back at the starting node
    if not graph[current_node]:

      path.pop()
      # Run through the cycle to find a node with unexplored edges
      for i in range(len(path)):
        if graph[path[i]]:
          # Reorder the cycle to start and end from the node with unexplored edges
          new_ending_node = path[i]
          path = path[i:] + path[:i]
          path.append(new_ending_node)

          # Begin walking from the end of the cycle by breaking the for loop
          current_node = path[-1]
          break

  return path[:-1]


def construct_genome(kmers: list[str]) -> str:
  '''
  Construct a genome from a list of k-mers (assuming the first kmer is the beginning of the genome).

  Parameters:
    kmers (list[str]): a list of k-mers

  Returns:
    genome (str): a genome
  '''
  k = len(kmers[0])
  genome = kmers[0]

  for kmer in kmers[1:]:
    genome_suffix = genome[-(k-1):]
    kmer_prefix = kmer[:k-1]

    if genome_suffix == kmer_prefix:
      genome += kmer[-1:]

  return genome


### Test Cases ###
# k = 4
# patterns = ['CTTA', 'ACCA', 'TACC', 'GGCT', 'GCTT', 'TTAC']


file = open("string_reconstruction.txt").read().strip().splitlines()
k = int(file[0])
patterns = list(file[1].split())


while True:
  de_bruijn_graph = construct_de_bruijn_graph(k, patterns)
  new_graph, start_node, end_node = connect_boundary_node(de_bruijn_graph)
  path = eulerian_path(new_graph, start_node)

  if path[0] == start_node and path[-1] == end_node:
    break

genome = construct_genome(path)
print(genome)
pyperclip.copy(genome)