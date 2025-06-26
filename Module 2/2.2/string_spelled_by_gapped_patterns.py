import random
import pyperclip

# Pair/organize patterns where pattern1-suffix = pattern2-prefix for both reads

def format_read_pairs(read_pairs: list) -> list:
    """
    Format read pairs into a list of tuples.

    Args:
      read_pairs (list of str): List of read pairs in the format "pattern1|pattern2".

    Returns:
      list of tuples: Each tuple contains two strings (pattern1, pattern2).
    """
    return [tuple(pair.split('|')) for pair in read_pairs]


def construct_read_pairs_de_bruijn_graph(read_pairs: list) -> dict:
    '''
    Constructs a De Bruijn graph from a list of read pairs by pairing suffixes and prefixes.

    Args:
      read_pairs (list of str): List of read pairs in the format "pattern1|pattern2".

    Returns:
      graph (dict): A De Bruijn graph where suffix of read_pair1 = prefix of read_pair2.
    '''
    graph = {}
    read_pairs = format_read_pairs(read_pairs)
    for a_read1, a_read2 in read_pairs:
        read_pair_a = f"{a_read1}|{a_read2}"
        suffix = [a_read1[1:], a_read2[1:]]

        for b_read1, b_read2 in read_pairs:
            if a_read1 == b_read1 and a_read2 == b_read2:
                continue
            
            read_pair_b = f"{b_read1}|{b_read2}"
            prefix = [b_read1[:-1], b_read2[:-1]]
            if suffix == prefix:
                if read_pair_a not in graph:
                    graph[read_pair_a] = []
                graph[read_pair_a].append(read_pair_b)

    return graph


def connect_boundary_nodes(graph: dict[int, list[int]]) -> tuple[dict[int, list[int]], int, int]:
  '''
  Find the starting and ending nodes for an Eulerian path in a directed graph.
  
  Parameters:
    graph (dict[int, list[int]]): a directed graph represented as an adjacency list

  Returns:
    graph (dict[int, list[int]]): the modified graph with the end node connected to the start node
  '''

  # Initialize start and end nodes
  start_node = end_node = None
  nodes = set(graph.keys()).union(set(node for edges in graph.values() for node in edges))
  
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


def construct_genome_from_read_pairs(path: list[str], k: int, d: int) -> str:
    n = len(path)
    genome = "a" * (2*k+(n-1)+d)
    read_num = 0
    
    for read_pair in path:
      read_1, read_2 = read_pair.split('|')

      if read_num == 0:
        genome = read_1 + genome[k:k+d] + read_2 + genome[k+d+k:]

      else:
        genome = genome[0:read_num] + read_1 + genome[read_num+k:read_num+k+d] + read_2 + genome[read_num+k+d+k:]
      read_num += 1

    return genome


### Test Cases ###
# k = 4 
# d = 2
# read_pairs = ["GACC|GCGC", "ACCG|CGCC", "CCGA|GCCG", "CGAG|CCGG", "GAGC|CGGA"]


# file = open("string_spelled_by_gapped_patterns.txt", "r").readlines()
file = open("string_reconstruction_from_read_pairs.txt", "r").readlines()
k, d = map(int, file[0].strip().split())
read_pairs = file[1].strip().split()

graph = construct_read_pairs_de_bruijn_graph(read_pairs)
new_graph, start_node, end_node = connect_boundary_nodes(graph)
path = eulerian_path(new_graph, start_node)
genome = construct_genome_from_read_pairs(path, k, d)

print(genome)
pyperclip.copy(genome)